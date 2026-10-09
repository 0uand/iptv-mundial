#!/usr/bin/env bash
# Roda na sua rede: resolve as lives do YouTube e publica youtube.m3u + index.m3u no GitHub.
set -e
DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$DIR"
git pull -q --rebase || true
YT_ATTEMPTS=2 YT_CLIENTS=android,web,ios YT_WORKERS=4 python3 scripts/youtube_resolve.py
python3 scripts/youtube_vod_resolve.py || true
python3 - <<'PY'
# reanexa YouTube TV (e shows) ao index.m3u sem reconstruir o resto
import os
idx = open("index.m3u", encoding="utf-8").read().splitlines()
out, skip = [], False
for ln in idx:
    if ln.startswith("#EXTINF"): skip = ("▶️ YouTube TV" in ln) or ("Movies | Shows" in ln) or ("Movies | Surf" in ln)
    if not skip: out.append(ln)
def tail(p): return [l for l in open(p, encoding="utf-8").read().splitlines()[1:] if l and not l.startswith("# ")] if os.path.exists(p) else []
yt = tail("youtube.m3u"); shows = tail("vod/shows.m3u")
pos = next((i for i, l in enumerate(out) if l.startswith("#EXTINF") and ("Movies |" in l or "Series |" in l)), len(out))
out[pos:pos] = yt
out += shows
open("index.m3u", "w", encoding="utf-8").write("\n".join(out) + "\n")
PY
git add -A
git diff --cached --quiet || git commit -qm "chore: YouTube TV renovado da rede de casa ($(date '+%Y-%m-%d %H:%M'))"
git push -q origin main
echo "✅ $(date '+%d/%m %H:%M') — YouTube TV publicado"
