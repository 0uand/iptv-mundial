#!/usr/bin/env python3
"""uandtv — resolve os vídeos de data/uandtv.txt em URLs diretas e gera uandtv.m3u
(grupo "📺 uandtv", um item por vídeo). As URLs do YouTube expiram em ~6 h; roda junto com youtube.yml
a cada 4 h. Se o YouTube bloquear o IP do runner, a lista anterior é mantida.
A versão "canal 24 h" (um vídeo atrás do outro, com logo) é a página web em tv/index.html.
"""
import json, os, re, subprocess, sys, datetime, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT, STATE = f"{ROOT}/data/uandtv.txt", f"{ROOT}/uandtv.m3u", f"{ROOT}/data/uandtv_state.json"
CLIENTS = ("android", "android_vr", "web_embedded", "tv_embedded", "ios")
GROUP = "📺 uandtv"

def run(cmd, t=120):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=t)
    except subprocess.TimeoutExpired: return None

def resolve(vid):
    for attempt in range(2):
        for c in CLIENTS:
            r = run(["yt-dlp", "-q", "--no-warnings", "--extractor-args", f"youtube:player_client={c}",
                     "-f", "best[ext=mp4][height<=1080]/best[protocol^=m3u8]/best", "-g",
                     "--print", "%(title)s\t%(duration)s\t%(thumbnail)s", f"https://www.youtube.com/watch?v={vid}"], 90)
            if r and r.returncode == 0:
                lines = r.stdout.strip().splitlines()
                if len(lines) >= 2 and lines[-1].startswith("http"):
                    title, dur, thumb = (lines[0].split("\t") + ["", "", ""])[:3]
                    try: dur = int(float(dur))
                    except: dur = -1
                    return title, dur, thumb, lines[-1]
            time.sleep(2 + 3 * attempt)
    return None

ids = [l.strip() for l in open(SRC, encoding="utf-8") if l.strip() and not l.startswith("#")]
items = [(vid, m) for vid in ids if (m := resolve(vid))]

prev = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
if not items and os.path.exists(OUT):
    print(f"ABORTADO: nenhum vídeo resolvido (antes: {prev.get('count')}); mantendo uandtv.m3u anterior"); sys.exit(0)

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
with open(OUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"# uandtv — programação resolvida em {now} (URLs expiram em ~6 h; atualizado a cada 4 h)\n")
    for n, (vid, (title, dur, thumb, url)) in enumerate(items, 1):
        title = re.sub(r"[\r\n,]+", " ", title).strip()
        f.write(f'#EXTINF:{dur} tvg-id="uandtv.{vid}" tvg-logo="{thumb}" group-title="{GROUP}",uandtv {n:02d} · {title}\n')
        f.write("#EXTVLCOPT:http-user-agent=Mozilla/5.0\n")
        f.write(url + "\n")
json.dump({"updated": now, "count": len(items), "total": len(ids)}, open(STATE, "w"))
print(f"OK: {len(items)}/{len(ids)} vídeos")
