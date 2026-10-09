#!/usr/bin/env python3
"""Catálogo VOD legal: filmes, séries e desenhos em domínio público do Internet Archive.

Gera vod/filmes.m3u, vod/series.m3u, vod/desenhos.m3u e vod/catalog.json (cache).
Só usa coleções públicas do archive.org; os arquivos ficam hospedados lá.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/vod"
CACHE = f"{OUT}/catalog.json"
os.makedirs(OUT, exist_ok=True)

# coleção -> (arquivo de saída, grupo, quantidade)
COLLECTIONS = [
    ("feature_films",        "filmes",   "🎬 Filmes | Clássicos",          1500),
    ("SciFi_Horror",         "filmes",   "🎬 Filmes | Ficção e Terror",     400),
    ("silent_films",         "filmes",   "🎬 Filmes | Cinema Mudo",         300),
    ("classic_tv",           "series",   "📺 Séries | TV Clássica",         800),
    ("animationandcartoons", "desenhos", "🧸 Desenhos | Animação Clássica", 500),
]
BLOCK = re.compile(r"\b(xxx|porn|adult|erotic|nudist|nudie|stag film)\b", re.I)
UA = {"User-Agent": "iptv-mundial/1.0 (+https://github.com/0uand/iptv-mundial)"}

def get(url, retries=3):
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == retries - 1: raise
            time.sleep(2 * (i + 1))

def search(collection, rows):
    q = urllib.parse.quote(f"collection:{collection} AND mediatype:movies")
    url = (f"https://archive.org/advancedsearch.php?q={q}&fl[]=identifier&fl[]=title&fl[]=year"
           f"&fl[]=description&fl[]=subject&fl[]=language&fl[]=downloads&fl[]=runtime"
           f"&sort[]=downloads+desc&rows={rows}&output=json")
    return get(url)["response"]["docs"]

def best_file(identifier):
    """Escolhe o melhor MP4 (h.264) do item. Retorna (url, tamanho_bytes) ou None."""
    meta = get(f"https://archive.org/metadata/{identifier}/files")
    files = meta.get("result", [])
    cands = [f for f in files if f.get("name", "").lower().endswith(".mp4")]
    if not cands:
        cands = [f for f in files if f.get("name", "").lower().endswith((".m4v", ".ogv", ".mkv"))]
    if not cands: return None
    # prefere derivados h.264 (compatíveis com iOS/Apple TV) e maiores
    def score(f):
        n = f["name"].lower()
        return (("h.264" in n or "512kb" in n or n.endswith(".mp4")), int(f.get("size", 0) or 0))
    f = max(cands, key=score)
    return f"https://archive.org/download/{identifier}/{urllib.parse.quote(f['name'])}", int(f.get("size", 0) or 0)

cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
items = []  # (coleção, saída, grupo, doc)
seen = set()
for coll, out, group, rows in COLLECTIONS:
    for d in search(coll, rows):
        ident = d["identifier"]
        if ident in seen: continue
        text = " ".join(str(d.get(k, "")) for k in ("title", "description", "subject"))
        if BLOCK.search(text): continue
        seen.add(ident)
        items.append((coll, out, group, d))

todo = [it for it in items if it[3]["identifier"] not in cache]
print(f"{len(items)} itens, {len(todo)} para resolver arquivo", flush=True)
with ThreadPoolExecutor(max_workers=16) as ex:
    futs = {ex.submit(best_file, it[3]["identifier"]): it for it in todo}
    for n, fut in enumerate(as_completed(futs), 1):
        it = futs[fut]
        try:
            res = fut.result()
        except Exception as e:
            res = None
        cache[it[3]["identifier"]] = {"url": res[0], "size": res[1]} if res else None
        if n % 200 == 0: print(f"  {n}/{len(todo)}", flush=True)
json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

def esc(s):
    if isinstance(s, list): s = s[0] if s else ""
    return re.sub(r"[\r\n,]+", " ", str(s)).strip()
def year(d):
    y = d.get("year") or ""
    if isinstance(y, list): y = y[0]
    m = re.search(r"\d{4}", str(y)); return m.group(0) if m else ""

by_out = {}
for coll, out, group, d in items:
    c = cache.get(d["identifier"])
    if not c or not c["url"] or c["size"] < 5_000_000: continue  # ignora trailers/arquivos quebrados
    by_out.setdefault(out, []).append((group, d, c))

counts = {}
for out, rows in by_out.items():
    rows.sort(key=lambda r: (r[0], esc(r[1].get("title") or "").lower()))
    with open(f"{OUT}/{out}.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for group, d, c in rows:
            ident = d["identifier"]; y = year(d)
            title = esc(d.get("title") or ident) + (f" ({y})" if y else "")
            f.write(f'#EXTINF:-1 tvg-id="ia.{ident}" tvg-logo="https://archive.org/services/img/{ident}" group-title="{group}",{title}\n')
            f.write(c["url"] + "\n")
    counts[out] = len(rows)
print("OK:", counts)
