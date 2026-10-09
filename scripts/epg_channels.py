#!/usr/bin/env python3
"""Monta epg/channels.xml: para cada canal das playlists, escolhe UMA fonte de guia
no projeto iptv-org/epg (pasta sites/) cujo xmltv_id case com o tvg-id do canal.

Uso: EPG_DIR=/caminho/do/clone/iptv-org/epg python3 scripts/epg_channels.py
Prioriza países e categorias de interesse e limita o total para caber no tempo do workflow.
"""
import glob, os, re, sys, html
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EPG_DIR = os.environ.get("EPG_DIR", "/tmp/epg")
MAX = int(os.environ.get("EPG_MAX_CHANNELS", "4000"))
COUNTRY_PRI = {"br": 0, "pt": 1, "us": 2, "uk": 3, "es": 4, "ar": 5, "mx": 6, "it": 7, "fr": 8, "de": 9}
CAT_PRI = {"Música": 0, "Entretenimento": 1, "Notícias": 2, "Esportes": 3, "Filmes": 4, "Séries": 5}
# sites preferidos por país (guias locais são mais completos)
SITE_PRI = {"br": ["mi.tv", "meuguia.tv"], "pt": ["tv.sapo.pt", "tvcabo.co.ao"], "us": ["tvtv.us", "tvpassport.com", "ontvtonight.com", "tvguide.com", "pluto.tv", "plex.tv", "xumo.tv"],
            "uk": ["sky.com", "freeview.co.uk", "virginmedia.com"], "es": ["programacion-tv.elpais.com", "movistarplus.es"], "ar": ["mi.tv"], "mx": ["mi.tv", "gatotv.com"]}

# 1) canais que temos nas playlists (tvg-id completo + país + categoria)
wanted = {}
for p in glob.glob(f"{ROOT}/countries/*.m3u"):
    code = os.path.basename(p)[:-4]
    for ln in open(p, encoding="utf-8"):
        m = re.match(r'#EXTINF:-1 tvg-id="([^"]+)".*group-title="[^|]*\| ([^"]+)"', ln)
        if m and m.group(1):
            tid = m.group(1)
            wanted.setdefault(tid, (code, m.group(2)))

# 2) índice de todas as entradas de canal dos sites do iptv-org/epg
index = {}  # xmltv_id -> [(site, site_id, lang, name)]
base_index = {}  # id sem @feed -> lista
for f in glob.glob(f"{EPG_DIR}/sites/*/*.channels.xml"):
    site = os.path.basename(os.path.dirname(f))
    for m in re.finditer(r'<channel\s+([^>]*)>([^<]*)</channel>', open(f, encoding="utf-8").read()):
        attrs = dict(re.findall(r'(\w+)="([^"]*)"', m.group(1)))
        xid = attrs.get("xmltv_id", "")
        if not xid: continue
        entry = (site, html.unescape(attrs.get("site_id", "")), attrs.get("lang", ""), html.unescape(m.group(2)))
        index.setdefault(xid, []).append(entry)
        base_index.setdefault(xid.split("@")[0], []).append((xid, entry))

def pick(tid, code):
    cands = index.get(tid) or [e for _, e in base_index.get(tid.split("@")[0], [])]
    if not cands: return None
    pri = SITE_PRI.get(code, [])
    cands.sort(key=lambda e: (pri.index(e[0]) if e[0] in pri else 99, e[0]))
    return cands[0]

def key(item):
    tid, (code, cat) = item
    return (COUNTRY_PRI.get(code, 50), CAT_PRI.get(cat, 50), tid)

chosen = []
for tid, (code, cat) in sorted(wanted.items(), key=key):
    e = pick(tid, code)
    if e: chosen.append((tid, e))
    if len(chosen) >= MAX: break

os.makedirs(f"{ROOT}/epg", exist_ok=True)
with open(f"{ROOT}/epg/channels.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<channels>\n')
    for tid, (site, site_id, lang, name) in chosen:
        f.write(f'  <channel site="{site}" lang="{escape(lang)}" xmltv_id="{escape(tid)}" site_id="{escape(site_id)}">{escape(name)}</channel>\n')
    f.write('</channels>\n')
from collections import Counter
print(f"OK: {len(chosen)} canais com fonte de EPG (de {len(wanted)} na lista)")
print("por site:", Counter(e[0] for _, e in chosen).most_common(12))
