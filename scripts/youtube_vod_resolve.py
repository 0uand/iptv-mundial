#!/usr/bin/env python3
"""Shows, festivais e surf sob demanda a partir de canais OFICIAIS do YouTube (data/youtube_vod.csv).
Lista os vídeos públicos do canal, filtra por palavras-chave e resolve o MP4/HLS. Gera vod/shows.m3u.
As URLs expiram em ~6 h; o resolvedor roda periodicamente e, se falhar, mantém a lista anterior.
"""
import csv, json, os, re, subprocess, sys, datetime, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC, OUT, STATE = f"{ROOT}/data/youtube_vod.csv", f"{ROOT}/vod/shows.m3u", f"{ROOT}/data/youtube_vod_state.json"
CLIENTS = ("android", "android_vr", "web_embedded", "tv_embedded")

def run(cmd, t=120):
    try: return subprocess.run(cmd, capture_output=True, text=True, timeout=t)
    except subprocess.TimeoutExpired: return None

def list_videos(handle, flt, mx):
    r = run(["yt-dlp", "-q", "--no-warnings", "--flat-playlist", "--playlist-end", str(mx * 6),
             "--print", "%(id)s\t%(title)s\t%(duration)s", f"https://www.youtube.com/@{handle}/videos"], 180)
    if not r: return []
    out = []
    pat = re.compile(flt, re.I)
    for ln in r.stdout.splitlines():
        parts = ln.split("\t")
        if len(parts) < 3: continue
        vid, title, dur = parts
        try: dur = float(dur)
        except: dur = 0
        if pat.search(title) and dur >= 150:   # ignora teasers curtos
            out.append((vid, title, dur))
        if len(out) >= mx: break
    return out

def resolve(vid):
    for attempt in range(2):
        for c in CLIENTS:
            r = run(["yt-dlp", "-q", "--no-warnings", "--extractor-args", f"youtube:player_client={c}",
                     "-f", "best[ext=mp4][height<=1080]/best[protocol^=m3u8]/best", "-g",
                     "--print", "%(thumbnail)s", f"https://www.youtube.com/watch?v={vid}"], 90)
            if r and r.returncode == 0:
                lines = r.stdout.strip().splitlines()
                if len(lines) >= 2 and lines[-1].startswith("http"): return lines[-1], lines[0]
            time.sleep(2 + 3 * attempt)
    return None, None

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
items, fails = [], 0
for row in rows:
    vids = list_videos(row["handle"], row["filter"], int(row["max"]))
    print(f"{row['handle']}: {len(vids)} vídeos candidatos", flush=True)
    for vid, title, dur in vids:
        url, thumb = resolve(vid)
        if url: items.append((row["group"], vid, title, dur, url, thumb))
        else: fails += 1

prev = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
if len(items) < max(1, prev.get("count", 0) // 2) and os.path.exists(OUT):
    print(f"ABORTADO: só {len(items)} resolvidos (antes: {prev.get('count')}); mantendo vod/shows.m3u anterior"); sys.exit(0)

now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
os.makedirs(f"{ROOT}/vod", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"# Shows, festivais e surf — vídeos públicos de canais oficiais do YouTube, resolvidos em {now}\n")
    for group, vid, title, dur, url, thumb in items:
        title = re.sub(r"[\r\n,]+", " ", title).strip()
        mins = int(dur // 60)
        f.write(f'#EXTINF:{int(dur)} tvg-id="ytv.{vid}" tvg-logo="{thumb}" tvg-type="movie" group-title="{group}",{title} ({mins} min)\n')
        f.write('#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
        f.write(url + "\n")
json.dump({"updated": now, "count": len(items), "failed": fails}, open(STATE, "w"))
print(f"OK: {len(items)} vídeos ({fails} falharam)")
