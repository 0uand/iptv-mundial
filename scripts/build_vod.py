#!/usr/bin/env python3
"""Catálogo VOD legal, organizado por categorias.

Fontes (todas públicas, hospedadas no Internet Archive):
  - Domínio público: filmes até 1963 (sem renovação de copyright nos EUA) das coleções
    feature_films, SciFi_Horror, silent_films; séries de classic_tv; desenhos de animationandcartoons.
  - Cinema aberto recente: lista curada de filmes lançados pelos próprios autores sob licença livre
    (Blender Foundation, Nina Paley, Star Wreck etc.).
  - Memória nacional: cinejornais e registros históricos brasileiros.

Saída: vod/filmes.m3u, vod/series.m3u, vod/desenhos.m3u, vod/catalog.json (cache de arquivos).
Categorias de filme: Premiados e Aclamados · Recentes (cinema aberto) · Nacionais (memória) ·
Comédia · Drama · Terror · Ficção Científica · Faroeste · Noir e Suspense · Romance · Guerra ·
Aventura · Documentário · Cinema Mudo · Animação · Musical · Família · (década) para o restante.
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{ROOT}/vod"; CACHE = f"{OUT}/catalog.json"
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "iptv-mundial/1.0 (+https://github.com/0uand/iptv-mundial)"}
BLOCK = re.compile(r"\b(xxx|porn|adult|erotic|nudist|nudie|stag film|sex)\b", re.I)

# ---------- fontes ----------
QUERIES = [  # (query, saída, limite, regra de licença)
    ("collection:feature_films AND mediatype:movies", "filmes", 3000, "pd"),
    ("collection:SciFi_Horror AND mediatype:movies", "filmes", 500, "pd"),
    ("collection:silent_films AND mediatype:movies", "filmes", 400, "pd"),
    ("collection:classic_tv AND mediatype:movies", "series", 1500, "pd"),
    ("collection:animationandcartoons AND mediatype:movies", "desenhos", 600, "pd"),
    ("mediatype:movies AND (title:cinejornal OR subject:cinejornal OR subject:\"Agencia Nacional\" OR subject:\"Agência Nacional\" OR title:\"Agência Nacional\")", "filmes", 60, "memoria"),
]
# cinema aberto recente — identificadores conhecidos (obras publicadas sob licença livre pelos autores)
OPEN_FILMS = ["Sita_Sings_the_Blues", "BigBuckBunny_124", "Sintel", "ElephantsDream", "Tears-of-Steel", "CosmosLaundromatFirstCycle",
              "Caminandes1LlamaDrama", "CaminandesLlamigos", "agent327operationbarbershop", "spring_blenderopenmovie", "sprite-fright",
              "charge-blender-open-movie-1608p", "hero_20260106", "Star_Wreck_In_the_Pirkinning_VOScastellano", "seder-masochism-final-05-18-18",
              "PioneerOneS01E01720pHD", "valkaama", "thecosmonaut-s008", "Route_66_-_an_American_badDream", "NastyOldPeople",
              "RipRemixManifesto", "STEAL_THIS_FILM", "StealThisFilmII", "Good_Copy_Bad_Copy-film", "TpbAfkThePirateBayAwayFromKeyboard",
              "KungFury", "EverythingIsARemix1", "zeitgeist_movie", "CopyingIsNotTheft"]

# ---------- categorias ----------
PREMIADOS = re.compile(r"^(?:the )?(metropolis|nosferatu|the cabinet of dr\.? caligari|battleship potemkin|m \(1931\)|m$|the general|safety last|sherlock jr|the kid|the gold rush|the phantom of the opera|steamboat bill|our hospitality|things to come|the 39 steps|the lady vanishes|the man who knew too much|sabotage|jamaica inn|his girl friday|the front page|meet john doe|a star is born|nothing sacred|love affair|penny serenade|made for each other|of mice and men|the little princess|scarlet street|detour|d\.?o\.?a\.?|kansas city confidential|the hitch-hiker|suddenly|beat the devil|the stranger|cyrano de bergerac|charade|night of the living dead|carnival of souls|the little shop of horrors|house on haunted hill|the last man on earth|royal wedding|father's little dividend|life with father|the inspector general|till the clouds roll by|algiers|the jungle book|rain|stage door canteen|dressed to kill|scrooge|a farewell to arms|the outlaw|the scarlet pimpernel|the private life of henry viii|the lost world|the big trail|the great train robbery|intolerance|the birth of a nation|way down east|broken blossoms|the thief of bagdad|the mark of zorro|the hunchback of notre dame|the lodger|blackmail|the iron mask|the black pirate|the wind|sunrise|the last laugh|the passion of joan of arc|un chien andalou|l'age d'or|the blue angel|vampyr|freaks|white zombie|the most dangerous game|the old dark house|king of the zombies|the man with the golden arm|angel and the badman|mclintock|santa fe trail|the inspector general|africa screams|my man godfrey|the lady eve|sullivan's travels|the philadelphia story|it's a wonderful life|the big lift|one-eyed jacks|the terror|dementia 13|plan 9 from outer space|reefer madness|the brain that wouldn't die|horror express|the last time i saw paris|becket|the man who shot|the great dictator|modern times|city lights|a trip to the moon|le voyage dans la lune|the 400 blows|rashomon|seven samurai|ikiru|tokyo story|late spring|bicycle thieves|rome,? open city|la strada|nights of cabiria|the seventh seal|wild strawberries|breathless|hiroshima mon amour|jules and jim|8 1/2|la dolce vita)\b", re.I)
GENRES = [  # (categoria, regex sobre subject+title+description)
    ("Cinema Mudo",        r"\b(silent|mudo)\b"),
    ("Terror",             r"\b(horror|terror|zombie|vampire|werewolf|ghost|haunted|monster|frankenstein|dracula|mummy)\b"),
    ("Ficção Científica",  r"\b(sci-?fi|science fiction|space|alien|robot|atomic|outer space|planet|rocket|future)\b"),
    ("Faroeste",           r"\b(western|cowboy|faroeste|outlaw|ranch|sheriff|gunfighter|rodeo)\b"),
    ("Noir e Suspense",    r"\b(noir|thriller|suspense|mystery|detective|crime|murder|gangster|spy|espionage|heist)\b"),
    ("Guerra",             r"\b(war|wwii|world war|combat|battle|soldier|army|navy|nazi|propaganda)\b"),
    ("Comédia",            r"\b(comedy|comedia|comédia|slapstick|farce|laurel|hardy|chaplin|keaton|lloyd|stooges|abbott|costello)\b"),
    ("Musical",            r"\b(musical|music|song|dance|jazz|swing|opera|concert|band)\b"),
    ("Romance",            r"\b(romance|romantic|love story)\b"),
    ("Aventura",           r"\b(adventure|jungle|pirate|swashbuckl|treasure|safari|expedition|tarzan)\b"),
    ("Documentário",       r"\b(documentary|documentário|newsreel|educational|instructional|industrial film|history)\b"),
    ("Família",            r"\b(family|children|kids|fairy tale|christmas|lassie|shirley temple)\b"),
    ("Animação",           r"\b(animation|animated|cartoon|desenho)\b"),
    ("Drama",              r"\b(drama|melodrama|tragedy)\b"),
]
SERIES_GENRES = [
    ("Comédia",   r"\b(comedy|sitcom|humor|laugh)\b"),
    ("Faroeste",  r"\b(western|cowboy|lone ranger|cisco kid|annie oakley|roy rogers|gene autry)\b"),
    ("Suspense e Crime", r"\b(mystery|crime|detective|thriller|suspense|dragnet|police|racket)\b"),
    ("Ficção e Terror", r"\b(sci-?fi|science fiction|space|horror|one step beyond|outer limits|tales of tomorrow|flash gordon|rocky jones)\b"),
    ("Aventura",  r"\b(adventure|jungle|sea hunt|ramar|captain|ranger)\b"),
    ("Drama",     r"\b(drama|anthology|playhouse|theatre|theater|studio one)\b"),
    ("Game Shows e Variedades", r"\b(game show|quiz|variety|talk show|what's my line|you bet your life|ed sullivan|groucho)\b"),
    ("Documentário", r"\b(documentary|educational|newsreel|history)\b"),
]

def get(url, retries=3):
    for i in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return json.load(r)
        except Exception:
            if i == retries - 1: raise
            time.sleep(2 * (i + 1))

FIELDS = "&".join(f"fl[]={f}" for f in ("identifier", "title", "year", "date", "description", "subject", "language", "downloads", "runtime", "licenseurl", "creator"))
def search(q, rows):
    return get(f"https://archive.org/advancedsearch.php?q={urllib.parse.quote(q)}&{FIELDS}&sort[]=downloads+desc&rows={rows}&output=json")["response"]["docs"]
def item(identifier):
    try: return get(f"https://archive.org/metadata/{identifier}/metadata").get("result") or {}
    except Exception: return {}

def best_file(identifier):
    files = get(f"https://archive.org/metadata/{identifier}/files").get("result", [])
    cands = [f for f in files if f.get("name", "").lower().endswith(".mp4")] or \
            [f for f in files if f.get("name", "").lower().endswith((".m4v", ".ogv", ".mkv"))]
    if not cands: return None
    f = max(cands, key=lambda f: (("h.264" in f["name"].lower() or "512kb" in f["name"].lower() or f["name"].lower().endswith(".mp4")), int(f.get("size", 0) or 0)))
    return f"https://archive.org/download/{identifier}/{urllib.parse.quote(f['name'])}", int(f.get("size", 0) or 0)

def s(v):
    if isinstance(v, list): v = " ".join(str(x) for x in v)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>|[\r\n,\"]+", " ", str(v or ""))).strip()
def year(d):
    m = re.search(r"\d{4}", s(d.get("year")) + " " + s(d.get("date")))
    return int(m.group(0)) if m else 0
def runtime_min(d):
    m = re.match(r"(?:(\d+):)?(\d+):(\d+)", s(d.get("runtime")))
    if not m: return 0
    h, mi = int(m.group(1) or 0), int(m.group(2)); return h * 60 + mi

# ---------- coleta ----------
items, seen = [], set()
def add(d, out, rule):
    ident = d["identifier"]
    if ident in seen: return
    text = " ".join(s(d.get(k)) for k in ("title", "description", "subject"))
    if BLOCK.search(text): return
    y = year(d); lic = s(d.get("licenseurl"))
    if rule == "pd" and (not y or y > 1963) and not ("publicdomain" in lic and y and y <= 1977): return
    seen.add(ident); items.append((out, rule, d))

for q, out, rows, rule in QUERIES:
    for d in search(q, rows): add(d, out, rule)
for ident in OPEN_FILMS:
    m = item(ident)
    if m.get("identifier"): add(dict(m, identifier=m["identifier"]), "filmes", "open")

cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
todo = [it for it in items if it[2]["identifier"] not in cache]
print(f"{len(items)} itens, {len(todo)} para resolver arquivo", flush=True)
with ThreadPoolExecutor(max_workers=16) as ex:
    futs = {ex.submit(best_file, it[2]["identifier"]): it for it in todo}
    for n, fut in enumerate(as_completed(futs), 1):
        it = futs[fut]
        try: res = fut.result()
        except Exception: res = None
        cache[it[2]["identifier"]] = {"url": res[0], "size": res[1]} if res else None
        if n % 300 == 0: print(f"  {n}/{len(todo)}", flush=True)
json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=0)

# ---------- classificação ----------
def film_category(d, rule):
    title = s(d.get("title")); text = f"{title} {s(d.get('subject'))} {s(d.get('description'))[:400]}"
    y = year(d)
    if rule == "memoria": return "Movies | 🇧🇷 Nacionais · Memória (cinejornais e registros históricos)"
    if rule == "open": return "Movies | Recentes · cinema aberto (licença livre)"
    if PREMIADOS.search(re.sub(r"\s*\(.*?\)\s*", " ", title).strip()): return "Movies | Premiados e Aclamados"
    for cat, rx in GENRES:
        if re.search(rx, text, re.I): return f"Movies | {cat}"
    dec = f"Anos {y // 10 * 10}" if y else "Clássicos"
    return f"Movies | Clássicos · {dec}"
def series_genre(show, d):
    text = f"{show} {s(d.get('subject'))} {s(d.get('description'))[:300]}"
    for cat, rx in SERIES_GENRES:
        if re.search(rx, text, re.I): return cat
    return "Clássicas"

def show_name(t):
    t = re.sub(r"\s*\(.*?\)\s*", " ", t)
    t = re.split(r"\s+-\s+|:\s+|\s+[Ss]\d{1,2}\s*[Ee]\d{1,3}|\s+[Ee]p(?:isode)?\.?\s*\d+", t, maxsplit=1)[0].strip()
    return re.sub(r"^\d+\s+", "", t)[:60] or t

films, series, cartoons = [], [], []
for out, rule, d in items:
    c = cache.get(d["identifier"])
    if not c or not c["url"] or c["size"] < 5_000_000: continue
    if out == "filmes":
        if rule == "pd" and runtime_min(d) and runtime_min(d) < 40: continue  # curta demais para "filme"
        if c["size"] < 50_000_000 and rule == "open" and "Caminandes" not in d["identifier"] and "BigBuck" not in d["identifier"]: continue
        films.append((film_category(d, rule), d, c))
    elif out == "series": series.append((d, c))
    else: cartoons.append((d, c))

CAT_ORDER = ["Premiados e Aclamados", "Recentes", "Nacionais", "Comédia", "Drama", "Terror", "Ficção Científica", "Faroeste", "Noir e Suspense", "Romance", "Guerra", "Aventura", "Musical", "Família", "Animação", "Documentário", "Cinema Mudo", "Clássicos"]
def cat_key(g):
    for i, k in enumerate(CAT_ORDER):
        if k in g: return (i, g)
    return (99, g)

def write_films():
    films.sort(key=lambda r: (cat_key(r[0]), s(r[1].get("title")).lower()))
    with open(f"{OUT}/filmes.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for grp, d, c in films:
            ident = d["identifier"]; y = year(d)
            title = s(d.get("title")) + (f" ({y})" if y else "")
            # várias convenções de "filme" ao mesmo tempo: tvg-type/type=movie, grupo "Movies", URL com /movie/ (fragmento, não vai ao servidor) e extensão .mp4
            url = c["url"] + f"#/movie/{ident}.mp4"
            f.write(f'#EXTINF:-1 tvg-id="ia.{ident}" tvg-name="{title}" tvg-logo="https://archive.org/services/img/{ident}" tvg-type="movie" type="movie" group-title="{grp}",{title}\n{url}\n')

def write_series(path, rows, label):
    ep_counter = {}
    rows = sorted(rows, key=lambda r: (show_name(s(r[0].get("title"))).lower(), year(r[0]), s(r[0].get("title")).lower()))
    with open(path, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for d, c in rows:
            ident = d["identifier"]; base = s(d.get("title")); show = show_name(base)
            m = re.search(r"\b[Ss](\d{1,2})\s*[Ee](\d{1,3})\b", base) or re.search(r"\b(?:Season|Temporada)\s*(\d+).*?\b(?:Episode|Ep\.?|Epis[oó]dio)\s*(\d+)", base, re.I)
            if m: season, ep = int(m.group(1)), int(m.group(2))
            else: ep_counter[show] = ep_counter.get(show, 0) + 1; season, ep = 1, ep_counter[show]
            genre = series_genre(show, d) if label == "Séries" else "Desenhos"
            grp = f"Series | {genre}" if label == "Séries" else f"Series | {genre}"
            sid = re.sub(r"[^a-z0-9]+", "-", show.lower()).strip("-")
            url = c["url"] + f"#/series/{ident}.mp4"
            f.write(f'#EXTINF:-1 tvg-id="ia.{ident}" tvg-logo="https://archive.org/services/img/{ident}" tvg-type="serie" type="series" tvg-serie="{sid}" serie-title="{show}" tvg-season="{season}" tvg-episode="{ep}" group-title="{grp}",{show} S{season:02d}E{ep:02d} - {base}\n{url}\n')

write_films(); write_series(f"{OUT}/series.m3u", series, "Séries"); write_series(f"{OUT}/desenhos.m3u", cartoons, "Séries")
from collections import Counter
print("OK filmes:", len(films), "séries:", len(series), "desenhos:", len(cartoons))
for g, n in sorted(Counter(g for g, _, _ in films).items(), key=lambda kv: cat_key(kv[0])): print(f"  {n:5d}  {g}")
