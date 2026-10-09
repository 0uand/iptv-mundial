#!/usr/bin/env bash
# Baixa o EPG em blocos (resiliente): cada bloco de canais vira um guide_N.xml;
# no fim tudo é mesclado em epg/guide.xml.gz.
# Uso: EPG_DIR=/tmp/epg scripts/epg_grab.sh
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EPG_DIR="${EPG_DIR:-/tmp/epg}"
CHUNK="${EPG_CHUNK:-500}"
DAYS="${EPG_DAYS:-3}"
WORK="$EPG_DIR/chunks"; rm -rf "$WORK"; mkdir -p "$WORK"

python3 - "$ROOT/epg/channels.xml" "$WORK" "$CHUNK" <<'EOF'
import sys, re
src, work, chunk = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = [l for l in open(src, encoding="utf-8").read().splitlines() if l.strip().startswith("<channel ")]
for i in range(0, len(lines), chunk):
    with open(f"{work}/c{i//chunk:03d}.channels.xml", "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<channels>\n' + "\n".join(lines[i:i+chunk]) + "\n</channels>\n")
print(f"{(len(lines)+chunk-1)//chunk} blocos de até {chunk} canais")
EOF

cd "$EPG_DIR"
for f in "$WORK"/c*.channels.xml; do
  n=$(basename "$f" .channels.xml)
  echo "== bloco $n"
  timeout 40m npm run grab --- --channels="$f" --days="$DAYS" --maxConnections=40 --timeout=15000 --output="$WORK/$n.xml" >"$WORK/$n.log" 2>&1 || echo "   (bloco $n incompleto)"
  tail -1 "$WORK/$n.log"
done

python3 - "$WORK" "$ROOT/epg" <<'EOF'
import sys, glob, re, gzip, json, datetime
work, out = sys.argv[1], sys.argv[2]
chans, progs, seen = [], [], set()
for f in sorted(glob.glob(f"{work}/c*.xml")):
    x = open(f, encoding="utf-8").read()
    for m in re.finditer(r"<channel id=\"([^\"]+)\">.*?</channel>", x, re.S):
        if m.group(1) not in seen:
            seen.add(m.group(1)); chans.append(m.group(0))
    progs += re.findall(r"<programme .*?</programme>", x, re.S)
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv generator-info-name="iptv-mundial">\n' + "\n".join(chans) + "\n" + "\n".join(progs) + "\n</tv>\n"
with gzip.open(f"{out}/guide.xml.gz", "wt", encoding="utf-8", compresslevel=9) as g: g.write(xml)
info = {"updated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "channels": len({re.search(r'channel="([^"]+)"', p).group(1) for p in progs}), "programmes": len(progs)}
json.dump(info, open(f"{out}/info.json", "w"))
print("EPG:", info)
EOF
