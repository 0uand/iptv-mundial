#!/usr/bin/env python3
"""Detecta canais com replay (catchup/timeshift) e grava data/catchup.json.

Como funciona: para cada stream HLS, pede o mesmo manifesto com `?utc=<1 h atrás>`
(convenção Flussonic / DVR). Se o servidor devolver uma playlist válida e diferente
da ao vivo, o canal tem arquivo e recebe as tags catchup-* no build.
Também mede o tamanho da janela DVR quando o servidor informa.
"""
import json, os, re, sys, time, urllib.parse, urllib.request, ssl
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/data/catchup.json"
PLAYLISTS = [f"{ROOT}/index.m3u"]
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TIMEOUT = 8
WORKERS = int(os.environ.get("PROBE_WORKERS", "48"))
BUDGET = int(os.environ.get("PROBE_BUDGET_SEC", "3600"))  # tempo máximo total

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as r:
        return r.read(200_000).decode("utf-8", "ignore"), dict(r.headers)

def with_param(url, **kw):
    u = urllib.parse.urlsplit(url); q = dict(urllib.parse.parse_qsl(u.query)); q.update(kw)
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, urllib.parse.urlencode(q), u.fragment))

def probe(url):
    if ".m3u8" not in url.split("?")[0].lower() and "m3u8" not in url.lower():
        return None
    try:
        live, hdr = fetch(url)
    except Exception:
        return None
    if "#EXTM3U" not in live: return None
    server = (hdr.get("Server") or hdr.get("server") or "").lower()
    utc = int(time.time()) - 3600
    try:
        arch, _ = fetch(with_param(url, utc=utc, lutc=utc + 600))
    except Exception:
        return None
    if "#EXTM3U" not in arch: return None
    # master? segue a primeira variante levando o parâmetro utc junto
    if "#EXT-X-STREAM-INF" in arch and "#EXTINF" not in arch:
        var = next((l.strip() for l in arch.splitlines() if l.strip() and not l.startswith("#")), None)
        if not var: return None
        var = urllib.parse.urljoin(url, var)
        try:
            arch, _ = fetch(with_param(var, utc=utc, lutc=utc + 600))
            live, _ = fetch(var)
        except Exception:
            return None
    if "#EXTINF" not in arch: return None
    ok = False
    m = re.search(r"#EXT-X-PROGRAM-DATE-TIME:(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", arch)
    if m:
        import datetime as _dt
        t = _dt.datetime.fromisoformat(m.group(1)).replace(tzinfo=_dt.timezone.utc).timestamp()
        ok = abs(t - utc) < 900          # segmentos datados de ~1 h atrás → arquivo de verdade
    elif "#EXT-X-ENDLIST" in arch and "#EXT-X-ENDLIST" not in live:
        ok = True                        # janela servida como VOD fechado
    if not ok:
        # 2ª convenção: Flussonic  .../archive-<utc>-<duração>.m3u8
        m2 = re.match(r"^(https?://[^?]+)/[^/?]+\.m3u8(\?.*)?$", url)
        if not m2: return None
        base, qs = m2.group(1), m2.group(2) or ""
        try:
            arch, _ = fetch(f"{base}/archive-{utc}-600.m3u8{qs}")
        except Exception:
            return None
        if "#EXTM3U" not in arch or "#EXTINF" not in arch: return None
        if "#EXT-X-PROGRAM-DATE-TIME" in arch:
            m = re.search(r"#EXT-X-PROGRAM-DATE-TIME:(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", arch)
            import datetime as _dt
            t = _dt.datetime.fromisoformat(m.group(1)).replace(tzinfo=_dt.timezone.utc).timestamp()
            if abs(t - utc) > 900: return None
        elif "#EXT-X-ENDLIST" not in arch:
            return None
        return {"type": "flussonic", "source": "", "days": 3, "server": server[:40]}
    days = 1
    if "flussonic" in server:
        days = 3
    m = re.search(r"#EXT-X-(?:DVR|PLAYLIST-DURATION|TIMESHIFT)[^\n]*?(\d+)", live)
    if m:
        days = max(1, min(7, int(m.group(1)) // 86400 or 1))
    return {"type": "default", "source": with_param(url, utc="{utc}", lutc="{lutc}").replace("%7B", "{").replace("%7D", "}"),
            "days": days, "server": server[:40]}

urls, seen = [], set()
for p in PLAYLISTS:
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if ln.startswith("http") and "googlevideo" not in ln and "archive.org" not in ln and ln not in seen:
            seen.add(ln); urls.append(ln)

old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
found, start, done = {}, time.time(), 0
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = {ex.submit(probe, u): u for u in urls}
    for fut in as_completed(futs):
        done += 1
        try:
            r = fut.result()
        except Exception:
            r = None
        if r: found[futs[fut]] = r
        if done % 1000 == 0:
            print(f"  {done}/{len(urls)} sondados, {len(found)} com replay", flush=True)
        if time.time() - start > BUDGET:
            print("  orçamento de tempo esgotado; mantendo resultados anteriores para o restante", flush=True)
            for f2, u2 in futs.items():
                if not f2.done() and u2 in old: found[u2] = old[u2]
            ex.shutdown(wait=False, cancel_futures=True)
            break

json.dump(found, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(f"OK: {len(found)} canais com replay de {done} sondados")
