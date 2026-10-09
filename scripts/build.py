#!/usr/bin/env python3
"""Gera as playlists a partir da fonte pública iptv-org.
Saída: index.m3u (tudo), countries/<cc>.m3u, categories/<cat>.m3u, README.md
"""
import re, os, csv, glob, io, urllib.request, zipfile, tempfile, sys, datetime
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER_REPO = os.environ.get("GITHUB_REPOSITORY", "0uand/iptv-mundial")
RAW = f"https://raw.githubusercontent.com/{OWNER_REPO}/main"

def fetch(url):
    with urllib.request.urlopen(url, timeout=120) as r: return r.read()

# Fonte: clone local (IPTV_SRC / IPTV_DB) ou download direto
if os.environ.get("IPTV_SRC"):
    streams_dir = os.environ["IPTV_SRC"]
else:
    tmp = tempfile.mkdtemp()
    z = zipfile.ZipFile(io.BytesIO(fetch("https://github.com/iptv-org/iptv/archive/refs/heads/master.zip")))
    z.extractall(tmp)
    streams_dir = glob.glob(f"{tmp}/iptv-*/streams")[0]
db = {}
for f in ("countries", "channels", "logos", "categories"):
    if os.environ.get("IPTV_DB"):
        raw = open(f"{os.environ['IPTV_DB']}/{f}.csv", encoding="utf-8").read()
    else:
        raw = fetch(f"https://raw.githubusercontent.com/iptv-org/database/master/data/{f}.csv").decode("utf-8")
    db[f] = list(csv.DictReader(io.StringIO(raw)))

PT = {"Brazil":"Brasil","United States":"Estados Unidos","Germany":"Alemanha","Spain":"Espanha","France":"França","Italy":"Itália","United Kingdom":"Reino Unido","Argentina":"Argentina","Mexico":"México","Japan":"Japão","India":"Índia","Russia":"Rússia","Canada":"Canadá","Colombia":"Colômbia","Netherlands":"Holanda","Turkey":"Turquia","South Korea":"Coreia do Sul","Australia":"Austrália","Switzerland":"Suíça","Belgium":"Bélgica","Austria":"Áustria","Poland":"Polônia","Greece":"Grécia","Sweden":"Suécia","Norway":"Noruega","Denmark":"Dinamarca","Finland":"Finlândia","Ireland":"Irlanda","Uruguay":"Uruguai","Paraguay":"Paraguai","Bolivia":"Bolívia","Ecuador":"Equador","Dominican Republic":"República Dominicana","Mozambique":"Moçambique","Cape Verde":"Cabo Verde","South Africa":"África do Sul","Egypt":"Egito","Saudi Arabia":"Arábia Saudita","United Arab Emirates":"Emirados Árabes","Ukraine":"Ucrânia","Czech Republic":"República Tcheca","Hungary":"Hungria","Romania":"Romênia","Indonesia":"Indonésia","Philippines":"Filipinas","Thailand":"Tailândia","Vietnam":"Vietnã","Malaysia":"Malásia","Singapore":"Singapura","Pakistan":"Paquistão","Nigeria":"Nigéria","Kenya":"Quênia","Morocco":"Marrocos","Algeria":"Argélia","Tunisia":"Tunísia","Lebanon":"Líbano","Iran":"Irã","Iraq":"Iraque","New Zealand":"Nova Zelândia","Croatia":"Croácia","Serbia":"Sérvia","Slovakia":"Eslováquia","Slovenia":"Eslovênia","Bulgaria":"Bulgária","Lithuania":"Lituânia","Latvia":"Letônia","Estonia":"Estônia","Iceland":"Islândia","Luxembourg":"Luxemburgo","Albania":"Albânia","Georgia":"Geórgia","Armenia":"Armênia","Azerbaijan":"Azerbaijão","Kazakhstan":"Cazaquistão","Qatar":"Catar","Jordan":"Jordânia","Ethiopia":"Etiópia","Ghana":"Gana","Puerto Rico":"Porto Rico","Panama":"Panamá","Nicaragua":"Nicarágua","Trinidad and Tobago":"Trinidad e Tobago","Macao":"Macau","North Korea":"Coreia do Norte","Mongolia":"Mongólia","Myanmar (Burma)":"Mianmar","Cambodia":"Camboja","Moldova":"Moldávia","Cyprus":"Chipre","Bosnia and Herzegovina":"Bósnia","North Macedonia":"Macedônia do Norte","Uzbekistan":"Uzbequistão","Kyrgyzstan":"Quirguistão","Tajikistan":"Tajiquistão","Turkmenistan":"Turcomenistão","Afghanistan":"Afeganistão","Syria":"Síria","Yemen":"Iêmen","Oman":"Omã","Bahrain":"Bahrein","Libya":"Líbia","Sudan":"Sudão","Tanzania":"Tanzânia","Rwanda":"Ruanda","Cameroon":"Camarões","Ivory Coast":"Costa do Marfim","Democratic Republic of the Congo":"RD Congo","Zimbabwe":"Zimbábue","Zambia":"Zâmbia","Namibia":"Namíbia","Botswana":"Botsuana","Mauritius":"Maurício","Guinea-Bissau":"Guiné-Bissau","São Tomé and Príncipe":"São Tomé e Príncipe","East Timor":"Timor-Leste","Vatican City":"Vaticano","Monaco":"Mônaco","Greenland":"Groenlândia","Faroe Islands":"Ilhas Faroé"}
CATPT = {"news":"Notícias","sports":"Esportes","movies":"Filmes","music":"Música","kids":"Infantil","entertainment":"Entretenimento","general":"Geral","documentary":"Documentários","religious":"Religioso","education":"Educação","lifestyle":"Estilo de vida","series":"Séries","business":"Negócios","culture":"Cultura","comedy":"Comédia","animation":"Animação","auto":"Automotivo","cooking":"Culinária","family":"Família","legislative":"Legislativo","outdoor":"Outdoor","public":"Pública","relax":"Relax","science":"Ciência","shop":"Compras","travel":"Viagem","weather":"Clima","classic":"Clássicos"}

countries = {r["code"].lower(): (PT.get(r["name"], r["name"]), r["flag"]) for r in db["countries"]}
countries["int"] = ("Internacional", "🌐")
cat_of, nsfw = {}, set()
for r in db["channels"]:
    cat_of[r["id"]] = (r.get("categories") or "").split(";")[0]
    if r.get("is_nsfw") == "TRUE": nsfw.add(r["id"])
logos = {}
for r in db["logos"]:
    logos.setdefault(r["channel"], r["url"])

rows, seen = [], set()
for p in sorted(glob.glob(f"{streams_dir}/*.m3u")):
    code = os.path.basename(p)[:-4].split("_")[0]
    cur, hdrs = None, []
    for ln in open(p, encoding="utf-8", errors="ignore"):
        ln = ln.rstrip("\n")
        if ln.startswith("#EXTINF"): cur, hdrs = ln, []
        elif ln.startswith(("#EXTVLCOPT", "#KODIPROP")): hdrs.append(ln)
        elif ln.startswith("http") and cur:
            url = ln.strip()
            name = cur.split(",", 1)[1].strip()
            tid = (re.search(r'tvg-id="([^"]*)"', cur) or [None, ""])[1].split("@")[0]
            if url in seen or "[Geo-blocked]" in name or tid in nsfw or re.search(r"\b(xxx|porn|adult|erotic)\b", name, re.I):
                cur = None; continue
            seen.add(url)
            clean = re.sub(r"\s*\(\d+p\)|\s*\[Not 24/7\]", "", name).strip()
            logo = (re.search(r'tvg-logo="([^"]*)"', cur) or [None, ""])[1] or logos.get(tid, "")
            rows.append(dict(code=code, name=clean, url=url, hdrs=hdrs, tid=tid, logo=logo, cat=cat_of.get(tid, "") or "general"))
            cur = None

PRI = {"br":0,"pt":1,"us":2,"uk":3,"es":4,"ar":5,"int":6}
def ckey(code): return (PRI.get(code, 10), countries.get(code, (code.upper(),))[0])
rows.sort(key=lambda r: (ckey(r["code"]), CATPT.get(r["cat"], "Geral"), r["name"].lower()))

def write(path, items):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write('#EXTM3U x-tvg-url="https://iptv-org.github.io/epg/guides/pt.xml"\n')
        for r in items:
            cn, fl = countries.get(r["code"], (r["code"].upper(), ""))
            grp = f'{fl} {cn} | {CATPT.get(r["cat"], "Geral")}'.strip()
            f.write(f'#EXTINF:-1 tvg-id="{r["tid"]}" tvg-logo="{r["logo"]}" group-title="{grp}",{r["name"]}\n')
            for h in r["hdrs"]: f.write(h + "\n")
            f.write(r["url"] + "\n")

write(f"{ROOT}/index.m3u", rows)
bycountry, bycat = defaultdict(list), defaultdict(list)
for r in rows: bycountry[r["code"]].append(r); bycat[r["cat"]].append(r)
for c, items in bycountry.items(): write(f"{ROOT}/countries/{c}.m3u", items)
for c, items in bycat.items(): write(f"{ROOT}/categories/{c}.m3u", items)

today = datetime.date.today().strftime("%d/%m/%Y")
md = [f"# 📺 IPTV Mundial\n",
      f"Lista IPTV gratuita com **{len(rows):,}** canais de **{len(bycountry)}** países, organizada por país e categoria. Atualizada automaticamente toda semana a partir da base pública [iptv-org](https://github.com/iptv-org/iptv) — só canais que as próprias emissoras disponibilizam abertamente.\n".replace(f"{len(rows):,}", f"{len(rows):,}".replace(",", ".")),
      f"_Última atualização: {today}_\n",
      "## 🚀 Como usar\n",
      "Cole a URL abaixo no seu app de IPTV (IPTV Smarters, TiviMate, GSE Smart IPTV, iPlayTV, Flex IPTV, VLC, Kodi…):\n",
      f"```\n{RAW}/index.m3u\n```\n",
      "Ou use apenas um país / categoria com as URLs das tabelas abaixo. O guia de programação (EPG) já está configurado dentro da lista.\n",
      "## 🌎 Por país\n", "| País | Canais | Playlist |", "|---|---:|---|"]
for c in sorted(bycountry, key=ckey):
    cn, fl = countries.get(c, (c.upper(), ""))
    md.append(f"| {fl} {cn} | {len(bycountry[c])} | `{RAW}/countries/{c}.m3u` |")
md += ["\n## 🎬 Por categoria\n", "| Categoria | Canais | Playlist |", "|---|---:|---|"]
for c in sorted(bycat, key=lambda x: CATPT.get(x, "Geral")):
    md.append(f"| {CATPT.get(c, 'Geral')} | {len(bycat[c])} | `{RAW}/categories/{c}.m3u` |")
md += ["\n## ⚠️ Avisos\n",
       "- Em listas públicas, parte dos canais pode estar fora do ar em um dado momento — a lista é regenerada semanalmente para remover links mortos conhecidos.",
       "- Alguns canais só funcionam no país de origem (bloqueio de região imposto pela própria emissora, não pelo seu aparelho).",
       "- Nenhum stream é hospedado aqui; o repositório apenas reúne links públicos. Problemas com um canal específico devem ser reportados à emissora ou ao projeto iptv-org.\n",
       "## 📄 Licença\n", "Dados derivados do projeto [iptv-org/iptv](https://github.com/iptv-org/iptv) (Unlicense)."]
open(f"{ROOT}/README.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print(f"OK: {len(rows)} canais, {len(bycountry)} países, {len(bycat)} categorias")
