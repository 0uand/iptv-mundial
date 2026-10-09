#!/usr/bin/env python3
"""Gera as playlists a partir da fonte pública iptv-org.
Saída: index.m3u (tudo), countries/<cc>.m3u, categories/<cat>.m3u, README.md
"""
import re, os, csv, glob, io, json, urllib.request, zipfile, tempfile, sys, datetime
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

MUSIC_RE = re.compile(r"\b(vevo|mtv|music|m[uú]sica|musik|musique|hits?|radio|r[aá]dio|fm|clubbing|dance|hip.?hop|rock|jazz|k-?pop|stingray|trace|qello|concert|karaoke|4ever|sertanejo|pagode|funk|samba|gospel music|mezzo|djing|edm|rap|reggae|salsa|cumbia|tango|schlager|deutsche musik|rtl hits|clubland|now 80s|now 90s|kerrang|magic|kiss|heart|capital|box hits|vh1|cmt|bet jams|revolt|xite|loop|flow|beat|soul|blues|classical|opera|symphony|hitlist|top 40|charts?)\b", re.I)
ENT_RE = re.compile(r"\b(entertainment|entretenimento|comedy|com[eé]dia|humor|reality|variety|show|lifestyle|celebrity|gossip|fun|divers[ãa]o|telenovela|novela)\b", re.I)
def guess_cat(name, cat):
    if cat and cat != "general": return cat
    if MUSIC_RE.search(name): return "music"
    if ENT_RE.search(name): return "entertainment"
    return cat or "general"

rows, seen = [], set()
EXCLUDE_CATS = {"religious"}
LOGO_OVERRIDES = {r"^SBT( Nacional| News| Interior| Cuiaba| Nova Mutum| Rondonopolis)?$": "https://sbt-news-assets-prod.s3.sa-east-1.amazonaws.com/sbt_black_1_b78d9ef3d9.png"}
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
            tid = (re.search(r'tvg-id="([^"]*)"', cur) or [None, ""])[1]
            base = tid.split("@")[0]
            if url in seen or "[Geo-blocked]" in name or base in nsfw or re.search(r"\b(xxx|porn|adult|erotic)\b", name, re.I):
                cur = None; continue
            seen.add(url)
            mres = re.search(r"\((\d{3,4})p\)", name)
            res = int(mres.group(1)) if mres else 0
            clean = re.sub(r"\s*\(\d+p\)|\s*\[Not 24/7\]", "", name).strip()
            logo = (re.search(r'tvg-logo="([^"]*)"', cur) or [None, ""])[1] or logos.get(base, "")
            cat = guess_cat(clean, cat_of.get(base, ""))
            if cat in EXCLUDE_CATS or re.search(r"\b(igreja|gospel|evang[eé]lic|cat[oó]lic|canção nova|rede vida|tv aparecida|novo tempo|3abn|church|christian|god tv|daystar|ewtn|islam|quran|al.?quran|hindu|sikh|jesus|bible|biblia|pastor|ministério|ministerio|padre|rede super|sat 7|tbn|hope channel|loveworld|iurd|igreja universal)\b", clean, re.I):
                cur = None; continue
            # logos oficiais
            for pat, lg in LOGO_OVERRIDES.items():
                if re.search(pat, clean, re.I): logo = lg
            rows.append(dict(code=code, name=clean, url=url, hdrs=hdrs, tid=tid, logo=logo, cat=cat, res=res))
            cur = None

# Ordem dos países: Brasil → EUA → Reino Unido → América Latina (por tamanho) → Portugal/Espanha →
# grandes mercados por tamanho e importância → demais por nº de canais
ORDER = ["br", "us", "uk",
         "mx", "ar", "co", "cl", "pe", "ve", "ec", "uy", "py", "bo", "do", "cr", "pa", "gt", "hn", "sv", "ni", "cu", "pr",
         "pt", "es",
         "ca", "de", "fr", "it", "jp", "kr", "au", "nl", "ch", "be", "se", "no", "dk", "fi", "ie", "at", "pl", "gr", "cz", "hu", "ro",
         "in", "cn", "ru", "tr", "sa", "ae", "qa", "il", "za", "ng", "eg", "id", "th", "vn", "ph", "my", "sg", "hk", "tw", "nz", "ua", "int"]
PRI = {c: i for i, c in enumerate(ORDER)}
def ckey(code):
    name = countries.get(code, (code.upper(),))[0]
    return (PRI.get(code, 1000), 0, name) if code in PRI else (1000, -len(bycode.get(code, [])), name)
CAT_PRI = {"music": 0, "entertainment": 1}
PINNED = [  # (grupo, regex de nome, países permitidos)
    ("⭐ TV Aberta Brasil", r"^(Red Bull TV BR|Rede Globo|TV Globo Sao Paulo|GloboNews|SBT Nacional|SBT News|Record|RecordTV|Record News|Band|BandNews|Band Sports|Rede TV!|Rede TV! SP|TV Cultura|TV Brasil|TV Gazeta|Arte 1|Canal Rural|Jovem Pan News|CNN Brasil|TVE RS|Cultura Fast)$", {"br"}),
    ("🏄 Surf & Ação", r"^(Red Bull TV BR|Surf Cinema|SURFER TV|Fuel TV|FUEL TV|Red Bull TV|Red Bull TV BR|Inside Outside|Extreme Sports Channel|Nautical Channel|Outside TV|Outside TV\+|Waves|Adventure Sports Network)$", None),
]
def catkey(cat): return (CAT_PRI.get(cat, 5), CATPT.get(cat, "Geral"))
bycode = {}
for r in rows: bycode.setdefault(r["code"], []).append(r)
rows.sort(key=lambda r: (ckey(r["code"]), catkey(r["cat"]), r["name"].lower(), -r["res"]))
def qlabel(res):
    if res >= 2160: return " [4K]"
    if res >= 1080: return " [FHD]"
    if res >= 720: return " [HD]"
    if res > 0: return " [SD]"
    return ""
# fontes alternativas do mesmo canal (mesmo nome/país) ficam depois da melhor e marcadas
_seen_alt = {}
for r in rows:
    k = (r["code"], r["name"].lower())
    n_ = _seen_alt.get(k, 0); _seen_alt[k] = n_ + 1
    r["label"] = r["name"] + qlabel(r["res"]) + (f" (fonte {n_ + 1})" if n_ else "")

CATCHUP = {}
_cp = f"{ROOT}/data/catchup.json"
if os.path.exists(_cp):
    CATCHUP = json.load(open(_cp, encoding="utf-8"))

def write(path, items, group=None, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode, encoding="utf-8") as f:
        if mode == "w": f.write(f'#EXTM3U x-tvg-url="{RAW}/epg/guide.xml.gz"\n')
        for r in items:
            cn, fl = countries.get(r["code"], (r["code"].upper(), ""))
            grp = group or f'{fl} {cn} | {CATPT.get(r["cat"], "Geral")}'.strip()
            cu = CATCHUP.get(r["url"])
            extra = ""
            if cu and cu.get("type") == "flussonic":
                extra = f' catchup="flussonic" catchup-days="{cu["days"]}"'
            elif cu:
                extra = f' catchup="default" catchup-source="{cu["source"]}" catchup-days="{cu["days"]}"'
            f.write(f'#EXTINF:-1 tvg-id="{r["tid"]}" tvg-logo="{r["logo"]}" tvg-type="live" group-title="{grp}"{extra},{r.get("label", r["name"])}\n')
            for h in r["hdrs"]: f.write(h + "\n")
            f.write(r["url"] + "\n")

def tail_of(path):
    """linhas de outra playlist (sem o cabeçalho), para anexar"""
    if not os.path.exists(path): return []
    return [ln for ln in open(path, encoding="utf-8").read().splitlines()[1:] if ln and not ln.startswith("# ")]
def append_lines(path, lines):
    with open(path, "a", encoding="utf-8") as f:
        for ln in lines: f.write(ln + "\n")

pinned_sets = []
for grp, rx, codes in PINNED:
    sel, names = [], set()
    for r in sorted(rows, key=lambda r: (0 if r["name"] == "Red Bull TV BR" else 1, r["name"].lower(), 0 if r["code"] == "br" else 1, -r["res"])):
        if re.match(rx, r["name"]) and (codes is None or r["code"] in codes) and r["name"].lower() not in names:
            sel.append(r); names.add(r["name"].lower())
    pinned_sets.append((grp, sel))

# 📡 TV (ao vivo): grupos fixos + todos os países
write(f"{ROOT}/tv.m3u", [])
for grp, sel in pinned_sets: write(f"{ROOT}/tv.m3u", sel, group=grp, mode="a")
append_lines(f"{ROOT}/tv.m3u", tail_of(f"{ROOT}/youtube.m3u"))
write(f"{ROOT}/tv.m3u", rows, mode="a")
# 🎬 Filmes e 📺 Séries (VOD)
write(f"{ROOT}/filmes.m3u", []); append_lines(f"{ROOT}/filmes.m3u", tail_of(f"{ROOT}/vod/filmes.m3u"))
write(f"{ROOT}/series.m3u", []); append_lines(f"{ROOT}/series.m3u", tail_of(f"{ROOT}/vod/series.m3u") + tail_of(f"{ROOT}/vod/desenhos.m3u"))
# index = tudo
write(f"{ROOT}/index.m3u", []); append_lines(f"{ROOT}/index.m3u", tail_of(f"{ROOT}/tv.m3u") + tail_of(f"{ROOT}/filmes.m3u") + tail_of(f"{ROOT}/series.m3u"))
for grp, sel in pinned_sets:
    slug = {"⭐ TV Aberta Brasil": "tv-aberta-brasil", "🏄 Surf & Ação": "surf"}[grp]
    write(f"{ROOT}/hubs/{slug}.m3u", sel, group=grp)
# hubs mundiais de Música e Entretenimento (todos os países)
write(f"{ROOT}/hubs/musica-mundial.m3u", [r for r in rows if r["cat"] == "music"])
write(f"{ROOT}/hubs/entretenimento-mundial.m3u", [r for r in rows if r["cat"] == "entertainment"])
write(f"{ROOT}/hubs/4k-uhd.m3u", sorted([r for r in rows if r["res"] >= 2160], key=lambda r: r["name"].lower()), group="📺 4K / UHD")
write(f"{ROOT}/hubs/full-hd.m3u", [r for r in rows if r["res"] >= 1080])
write(f"{ROOT}/hubs/vevo.m3u", [r for r in rows if r["name"].lower().startswith("vevo")])
write(f"{ROOT}/hubs/musica-e-entretenimento-brasil.m3u", [r for r in rows if r["code"] == "br" and r["cat"] in ("music", "entertainment")])
bycountry, bycat = defaultdict(list), defaultdict(list)
for r in rows: bycountry[r["code"]].append(r); bycat[r["cat"]].append(r)
for c, items in bycountry.items(): write(f"{ROOT}/countries/{c}.m3u", items)
for c, items in bycat.items(): write(f"{ROOT}/categories/{c}.m3u", items)

today = datetime.date.today().strftime("%d/%m/%Y")
def n(x): return f"{x:,}".replace(",", ".")
def cnt(path):
    return sum(1 for l in open(path, encoding="utf-8") if l.startswith("http")) if os.path.exists(path) else 0
n_yt = cnt(f"{ROOT}/youtube.m3u"); n_f = cnt(f"{ROOT}/vod/filmes.m3u"); n_s = cnt(f"{ROOT}/vod/series.m3u"); n_d = cnt(f"{ROOT}/vod/desenhos.m3u")
n_cu = sum(1 for r in rows if r["url"] in CATCHUP)
epg_info = json.load(open(f"{ROOT}/epg/info.json")) if os.path.exists(f"{ROOT}/epg/info.json") else {}
yt_state = json.load(open(f"{ROOT}/data/youtube_state.json")) if os.path.exists(f"{ROOT}/data/youtube_state.json") else {}
n_music = sum(1 for r in rows if r["cat"] == "music"); n_ent = sum(1 for r in rows if r["cat"] == "entertainment")

md = [f"# 📺 IPTV Mundial\n",
      f"**{n(len(rows))} canais de TV** de **{len(bycountry)} países** + **{n(n_f + n_s + n_d)} filmes, séries e desenhos** em domínio público — tudo com guia de programação (EPG) e organizado por país e categoria.\n",
      f"_Última atualização: {today}_\n",
      "> ### ✅ Isto não é pirataria",
      "> Todos os canais desta lista são **transmissões públicas e gratuitas disponibilizadas pelas próprias emissoras** na internet (sinal aberto, canais FAST como Pluto TV / Samsung TV Plus / Roku, acervos de domínio público do Internet Archive). Nenhum stream é hospedado ou retransmitido aqui: o repositório apenas organiza links que já são de acesso público, a partir da base aberta do projeto [iptv-org](https://github.com/iptv-org/iptv). Não há canais pagos, nem conteúdo de assinatura (Netflix, Globoplay, HBO etc.). Se você é titular de um canal e quer removê-lo, abra uma *issue*.\n",
      "## 🚀 Como usar — 3 listas\n",
      "Adicione as três como playlists separadas no seu app (IPTV Smarters, TiviMate, GSE, iPlayTV, Flex IPTV, VLC, Kodi…) — assim TV, Filmes e Séries ficam em abas separadas. O EPG já vem configurado dentro das listas.\n",
      "| Divisão | Conteúdo | URL |", "|---|---|---|",
      f"| 📡 **TV ao vivo** | {n(cnt(f'{ROOT}/tv.m3u'))} canais — TV Aberta Brasil e Surf no topo, depois todos os países | `{RAW}/tv.m3u` |",
      f"| 🎬 **Filmes** | {n(cnt(f'{ROOT}/filmes.m3u'))} títulos — por categoria (premiados, gêneros, décadas, cinema aberto) | `{RAW}/filmes.m3u` |",
      f"| 📺 **Séries** | {n(cnt(f'{ROOT}/series.m3u'))} episódios — séries de TV clássicas e desenhos | `{RAW}/series.m3u` |",
      f"\nOu tudo numa lista só (grande, ~15 MB): `{RAW}/index.m3u`\n",
      "## ⭐ TV Aberta Brasil e 🏄 Surf\n", "| Lista | Canais | Playlist |", "|---|---:|---|",
      f"| ⭐ TV Aberta Brasil (Globo, SBT, Record, Band, RedeTV!, Cultura, TV Brasil, Gazeta, GloboNews, BandNews, Record News, SBT News, CNN Brasil, Jovem Pan…) | {cnt(f'{ROOT}/hubs/tv-aberta-brasil.m3u')} | `{RAW}/hubs/tv-aberta-brasil.m3u` |",
      f"| 🏄 Surf & Ação (Surf Cinema, SURFER TV, Fuel TV, Red Bull TV, Inside Outside, Outside TV, Nautical Channel, Extreme Sports) | {cnt(f'{ROOT}/hubs/surf.m3u')} | `{RAW}/hubs/surf.m3u` |",
      "",
      "## 🎵 Música e Entretenimento (destaque)\n", "| Lista | Canais | Playlist |", "|---|---:|---|",
      f"| 🎵 Música — todos os países | {n_music} | `{RAW}/hubs/musica-mundial.m3u` |",
      f"| 🎭 Entretenimento — todos os países | {n_ent} | `{RAW}/hubs/entretenimento-mundial.m3u` |",
      f"| 📺 Só canais 4K / UHD | {cnt(f'{ROOT}/hubs/4k-uhd.m3u')} | `{RAW}/hubs/4k-uhd.m3u` |",
      f"| 📺 Só canais Full HD (1080p ou mais) | {cnt(f'{ROOT}/hubs/full-hd.m3u')} | `{RAW}/hubs/full-hd.m3u` |",
      f"| 🎤 Vevo (todos os canais Vevo do mundo) | {cnt(f'{ROOT}/hubs/vevo.m3u')} | `{RAW}/hubs/vevo.m3u` |",
      f"| 🇧🇷 Música e Entretenimento — Brasil | {cnt(f'{ROOT}/hubs/musica-e-entretenimento-brasil.m3u')} | `{RAW}/hubs/musica-e-entretenimento-brasil.m3u` |",
      "\nDentro de cada país, Música e Entretenimento aparecem sempre como as primeiras categorias.\n",
      "## 🎬 Filmes, séries e desenhos (VOD)\n",
      "Filmes e séries: acervo de **domínio público** do [Internet Archive](https://archive.org) (títulos até 1963 ou com licença livre declarada): clássicos do cinema, ficção/terror, cinema mudo, séries de TV clássicas e animações antigas. Os arquivos ficam hospedados no próprio Archive.\n",
      "| Catálogo | Títulos | Playlist |", "|---|---:|---|",
      f"| 🎬 Filmes (por categoria) | {n(n_f)} | `{RAW}/vod/filmes.m3u` |",
      f"| 📺 Séries (episódios) | {n(n_s)} | `{RAW}/vod/series.m3u` |",
      f"| 📺 Desenhos | {n(n_d)} | `{RAW}/vod/desenhos.m3u` |",
      "\n**Categorias de filmes:** Premiados e Aclamados · Recentes (cinema aberto: Blender, Nina Paley, Kung Fury, Star Wreck, documentários CC) · 🇧🇷 Nacionais (memória: cinejornais e registros históricos) · Comédia · Drama · Terror · Ficção Científica · Faroeste · Noir e Suspense · Romance · Guerra · Aventura · Musical · Família · Animação · Documentário · Cinema Mudo · Clássicos por década. **Séries:** Comédia · Faroeste · Suspense e Crime · Ficção e Terror · Aventura · Drama · Game Shows e Variedades · Documentário · Desenhos — agrupadas por série, com temporada/episódio.\n",
      "\n> **Sobre filmes nacionais e recentes:** só entram obras que podem ser distribuídas legalmente — domínio público ou licença livre dada pelo próprio autor. Filmes brasileiros de ficção (Vera Cruz, Embrafilme, Cinema Novo…) e lançamentos recentes de estúdio ainda estão sob direitos autorais, mesmo quando alguém os sobe no Internet Archive com etiqueta \"CC\"; por isso ficam de fora. O que existe de legal está em Tela Brasil, Globoplay, +SBT etc., com login.\n",
      "\n> **Por que não tem Tela Brasil, +SBT, Globoplay, Band Play, PlayPlus?** Essas plataformas são gratuitas, mas exigem login (gov.br, conta da emissora) e entregam o vídeo com URL assinada por usuário. Não existe link público para colocar numa lista — e incluir seria burlar o acesso delas. Use os apps oficiais; aqui ficam só os sinais abertos e os canais FAST que as próprias emissoras publicam.\n",
      "\n## 📅 EPG (guia de programação)\n",
      f"Guia gerado diariamente neste repositório com o [iptv-org/epg](https://github.com/iptv-org/epg), com 3 dias de programação, sinopses e imagens. Os IDs batem com os `tvg-id` das playlists, então basta usar a lista que o guia carrega sozinho. Se o seu app pedir a URL do EPG separadamente:\n",
      f"```\n{RAW}/epg/guide.xml.gz\n```\n",
      f"Última geração: {epg_info.get('updated', '—')} — {n(epg_info.get('channels', 0))} canais com programação, {n(epg_info.get('programmes', 0))} programas.\n",
      "## ⏪ Replay (catchup)\n",
      f"Replay é um recurso do servidor de cada emissora, e pouquíssimos streams públicos oferecem. A cada atualização semanal todos os canais são sondados; os que têm arquivo recebem as tags `catchup` / `catchup-source` / `catchup-days` (compatíveis com TiviMate, IPTV Smarters, OTT Navigator, Kodi). Atualmente: **{n_cu} canais com replay**.\n",
      "## 🌎 Por país\n", "| País | Canais | Playlist |", "|---|---:|---|"]
for c in sorted(bycountry, key=ckey):
    cn, fl = countries.get(c, (c.upper(), ""))
    md.append(f"| {fl} {cn} | {len(bycountry[c])} | `{RAW}/countries/{c}.m3u` |")
md += ["\n## 🎯 Por categoria\n", "| Categoria | Canais | Playlist |", "|---|---:|---|"]
for c in sorted(bycat, key=catkey):
    md.append(f"| {CATPT.get(c, 'Geral')} | {len(bycat[c])} | `{RAW}/categories/{c}.m3u` |")
md += ["\n## ⚠️ Avisos\n",
       "- Em listas públicas, parte dos canais pode estar fora do ar em um dado momento — a lista é regenerada semanalmente.",
       "- Alguns canais só funcionam no país de origem (bloqueio de região imposto pela própria emissora, não pelo seu aparelho).",
       "- Problemas com um canal específico devem ser reportados à emissora ou ao projeto iptv-org.\n",
       "## 🔧 Como funciona\n",
       "| Workflow | Frequência | O que faz |", "|---|---|---|",
       "| `update.yml` | semanal (seg) | regenera canais, VOD e sonda replay |",
       "| `epg.yml` | diário | gera o guia de programação |",
       "\n## 📄 Licença\n", "Dados derivados dos projetos [iptv-org/iptv](https://github.com/iptv-org/iptv) e [iptv-org/epg](https://github.com/iptv-org/epg) (Unlicense). Conteúdo VOD: domínio público via Internet Archive."]
open(f"{ROOT}/README.md", "w", encoding="utf-8").write("\n".join(md) + "\n")
print(f"OK: {len(rows)} canais, {len(bycountry)} países, {len(bycat)} categorias")
