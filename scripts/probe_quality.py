#!/usr/bin/env python3
"""Mede a resolução REAL de cada stream HLS lendo as variantes do manifesto (#EXT-X-STREAM-INF)
e grava data/quality.json {url: {"w":..,"h":..,"bw":..,"variants":n}}.
O build usa isso para colocar a melhor fonte de cada canal primeiro (ninguém é removido).
"""
import json, os, re, ssl, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/data/quality.json"
UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
CTX = ssl.create_default_context(); CTX.check_hostname = False; CTX.verify_mode = ssl.CERT_NONE
TIMEOUT = 10
WORKERS = int(os.environ.get("PROBE_WORKERS", "64"))
BUDGET = int(os.environ.get("PROBE_BUDGET_SEC", "2400"))

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=CTX) as r:
        return r.read(300_000).decode("utf-8", "ignore"), r.geturl()

def probe(url):
    try:
        body, final = fetch(url)
    except Exception:
        return None
    if "#EXTM3U" not in body: return None
    best = (0, 0, 0); n = 0
    for m in re.finditer(r"#EXT-X-STREAM-INF:([^\n]*)", body):
        attrs = m.group(1); n += 1
        r = re.search(r"RESOLUTION=(\d+)x(\d+)", attrs)
        b = re.search(r"(?:AVERAGE-)?BANDWIDTH=(\d+)", attrs)
        w, h = (int(r.group(1)), int(r.group(2))) if r else (0, 0)
        bw = int(b.group(1)) if b else 0
        if (h, bw) > (best[1], best[2]): best = (w, h, bw)
    if n == 0:
        # media playlist sem variantes: não dá para saber a resolução; marca como desconhecido mas vivo
        return {"w": 0, "h": 0, "bw": 0, "variants": 0, "alive": True}
    return {"w": best[0], "h": best[1], "bw": best[2], "variants": n, "alive": True}

urls, seen = [], set()
for p in (f"{ROOT}/tv.m3u",):
    for ln in open(p, encoding="utf-8"):
        ln = ln.strip()
        if ln.startswith("http") and ln not in seen and ("m3u8" in ln.lower() or ".m3u" in ln.lower() or "/live" in ln.lower() or "playlist" in ln.lower() or "jmp2.uk" in ln):
            seen.add(ln); urls.append(ln)

old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
res, start, done = {}, time.time(), 0
with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    futs = {ex.submit(probe, u): u for u in urls}
    for fut in as_completed(futs):
        done += 1
        try: r = fut.result()
        except Exception: r = None
        if r: res[futs[fut]] = r
        if done % 2000 == 0: print(f"  {done}/{len(urls)} sondados, {len(res)} vivos", flush=True)
        if time.time() - start > BUDGET:
            print("  orçamento esgotado; mantendo resultados antigos para o restante", flush=True)
            for f2, u2 in futs.items():
                if not f2.done() and u2 in old: res[u2] = old[u2]
            ex.shutdown(wait=False, cancel_futures=True); break
json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
from collections import Counter
c = Counter(("4K" if v["h"] >= 2160 else "FHD" if v["h"] >= 1080 else "HD" if v["h"] >= 720 else "SD" if v["h"] else "?") for v in res.values())
print(f"OK: {len(res)} vivos de {done} sondados — {dict(c)}")
