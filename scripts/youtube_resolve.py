#!/usr/bin/env python3
"""Resolve as transmissões ao vivo públicas do YouTube listadas em data/youtube.csv
e gera youtube.m3u com o manifesto HLS atual de cada canal.

IMPORTANTE: o YouTube amarra cada URL ao IP de quem a resolveu e ela expira em ~6 h.
Por isso este script precisa rodar NA MESMA REDE em que você assiste (casa), a cada 4 h —
veja scripts/home/README.md. Resolvido num servidor (GitHub, nuvem), não toca na sua TV.
"""
import csv, json, os, re, subprocess, sys, datetime
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/data/youtube.csv"
OUT = f"{ROOT}/youtube.m3u"
STATE = f"{ROOT}/data/youtube_state.json"

CATPT = {"news":"Notícias","sports":"Esportes","music":"Música","entertainment":"Entretenimento",
         "general":"Geral","science":"Ciência","business":"Negócios","culture":"Cultura","legislative":"Legislativo"}
FLAG = {"br":"🇧🇷","us":"🇺🇸","uk":"🇬🇧","pt":"🇵🇹","de":"🇩🇪","fr":"🇫🇷","qa":"🇶🇦","tr":"🇹🇷","sg":"🇸🇬",
        "jp":"🇯🇵","ar":"🇦🇷","mx":"🇲🇽","co":"🇨🇴","int":"🌐"}

def resolve(row):
    url = f"https://www.youtube.com/watch?v={row['video_id']}" if row.get("video_id") else f"https://www.youtube.com/@{row['handle']}/live"
    import time
    for attempt in range(int(os.environ.get("YT_ATTEMPTS", "4"))):
      for client in os.environ.get("YT_CLIENTS", "android,android_vr,web_embedded,tv_embedded,ios").split(","):
        cmd = ["yt-dlp", "-q", "--no-warnings", "--no-playlist",
               "--extractor-args", f"youtube:player_client={client}",
               "-f", "best[protocol^=m3u8]/best", "-g",
               "--print", "%(id)s|%(title)s|%(is_live)s|%(thumbnail)s", url]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
        except subprocess.TimeoutExpired:
            continue
        err = res.stderr
        if "not currently live" in err or "will begin in" in err or "Premieres in" in err:
            return dict(row, hls=None, reason="offline")
        out = res.stdout.strip().splitlines()
        if len(out) >= 2 and "|" in out[0] and out[-1].startswith("http"):
            vid, title, is_live, thumb = (out[0].split("|") + ["", "", "", ""])[:4]
            if is_live == "True" and "googlevideo.com" in out[-1]:
                return dict(row, video_id=vid, title=title, hls=out[-1], thumb=thumb)
        time.sleep(3 + 4 * attempt)
    return dict(row, hls=None, reason="bloqueado")

rows = list(csv.DictReader(open(SRC, encoding="utf-8")))
with ThreadPoolExecutor(max_workers=int(os.environ.get("YT_WORKERS", "3"))) as ex:
    results = list(ex.map(resolve, rows))

live = [r for r in results if r.get("hls")]
# proteção: se esta rodada resolveu menos da metade da anterior (ex.: bloqueio do YouTube no runner),
# mantém a lista anterior em vez de publicar uma pior
prev = json.load(open(STATE, encoding="utf-8")) if os.path.exists(STATE) else {}
if len(live) < max(1, len(prev.get("live", [])) // 2) and os.path.exists(OUT):
    print(f"ABORTADO: só {len(live)} lives resolvidas (antes: {len(prev.get('live', []))}); mantendo youtube.m3u anterior")
    sys.exit(0)
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
with open(OUT, "w", encoding="utf-8") as f:
    f.write('#EXTM3U x-tvg-url="https://raw.githubusercontent.com/0uand/iptv-mundial/main/epg/guide.xml.gz"\n')
    f.write(f"# YouTube TV — lives públicas resolvidas em {now} (URLs expiram em ~6 h; atualizado a cada 4 h)\n")
    for r in live:
        grp = f"▶️ YouTube TV | {CATPT.get(r['category'], 'Geral')}"
        logo = r["logo"] or r.get("thumb", "")
        name = f"{FLAG.get(r['country'], '')} {r['name']}".strip()
        f.write(f'#EXTINF:-1 tvg-id="yt.{r["handle"]}" tvg-logo="{logo}" group-title="{grp}",{name}\n')
        f.write('#EXTVLCOPT:http-user-agent=Mozilla/5.0\n')
        f.write(r["hls"] + "\n")

json.dump({"updated": now, "live": [r["handle"] for r in live],
           "offline": [r["handle"] for r in results if not r.get("hls")]},
          open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(live)} ao vivo / {len(results)}")
print("offline:", [r['handle'] for r in results if r.get('reason') == 'offline'])
print("bloqueado:", [r['handle'] for r in results if r.get('reason') == 'bloqueado'])
