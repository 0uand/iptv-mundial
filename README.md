# 📺 IPTV Mundial

**16.052 canais de TV** de **176 países** + **0 lives do YouTube** + **2.537 filmes, séries e desenhos** em domínio público — tudo com guia de programação (EPG) e organizado por país e categoria.

_Última atualização: 09/10/2026_

> ### ✅ Isto não é pirataria
> Todos os canais desta lista são **transmissões públicas e gratuitas disponibilizadas pelas próprias emissoras** na internet (sinal aberto, canais FAST como Pluto TV / Samsung TV Plus / Roku, lives oficiais no YouTube e acervos de domínio público do Internet Archive). Nenhum stream é hospedado ou retransmitido aqui: o repositório apenas organiza links que já são de acesso público, a partir da base aberta do projeto [iptv-org](https://github.com/iptv-org/iptv). Não há canais pagos, nem conteúdo de assinatura (Netflix, Globoplay, HBO etc.). Se você é titular de um canal e quer removê-lo, abra uma *issue*.

## 🚀 Como usar — 3 listas

Adicione as três como playlists separadas no seu app (IPTV Smarters, TiviMate, GSE, iPlayTV, Flex IPTV, VLC, Kodi…) — assim TV, Filmes e Séries ficam em abas separadas. O EPG já vem configurado dentro das listas.

| Divisão | Conteúdo | URL |
|---|---|---|
| 📡 **TV ao vivo** | 16.083 canais — TV Aberta Brasil e Surf no topo, YouTube TV, depois todos os países | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/tv.m3u` |
| 🎬 **Filmes** | 1.989 títulos — clássicos em domínio público + shows e festivais | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/filmes.m3u` |
| 📺 **Séries** | 548 episódios — séries de TV clássicas e desenhos | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/series.m3u` |

Ou tudo numa lista só (grande, ~15 MB): `https://raw.githubusercontent.com/0uand/iptv-mundial/main/index.m3u`

## ⭐ TV Aberta Brasil e 🏄 Surf

| Lista | Canais | Playlist |
|---|---:|---|
| ⭐ TV Aberta Brasil (Globo, SBT, Record, Band, RedeTV!, Cultura, TV Brasil, Gazeta, GloboNews, BandNews, Record News, SBT News, CNN Brasil, Jovem Pan…) | 22 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/tv-aberta-brasil.m3u` |
| 🏄 Surf & Ação (Surf Cinema, SURFER TV, Fuel TV, Red Bull TV, Inside Outside, Outside TV, Nautical Channel, Extreme Sports) | 9 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/surf.m3u` |

No YouTube TV também entram World Surf League e Red Bull quando estão ao vivo; em Filmes há a seção 🏄 Surf com replays e highlights da WSL e do Red Bull Surf.

## 🎵 Música e Entretenimento (destaque)

| Lista | Canais | Playlist |
|---|---:|---|
| 🎵 Música — todos os países | 1189 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/musica-mundial.m3u` |
| 🎭 Entretenimento — todos os países | 1233 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/entretenimento-mundial.m3u` |
| 📺 Só canais 4K / UHD | 17 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/4k-uhd.m3u` |
| 📺 Só canais Full HD (1080p ou mais) | 4813 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/full-hd.m3u` |
| 🎤 Vevo (todos os canais Vevo do mundo) | 50 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/vevo.m3u` |
| 🇧🇷 Música e Entretenimento — Brasil | 45 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/hubs/musica-e-entretenimento-brasil.m3u` |

Dentro de cada país, Música e Entretenimento aparecem sempre como as primeiras categorias.

## ▶️ YouTube TV

Canais que transmitem ao vivo no YouTube (Dia TV, CazéTV, GE TV, CNN Brasil, Jovem Pan News, Lofi Girl, NASA, Sky News…). As URLs do YouTube expiram em ~6 h, por isso esta lista é **renovada automaticamente a cada 4 horas**; só entram canais que estejam ao vivo naquele momento (CazéTV e GE TV, por exemplo, só ficam ao vivo em jogos e eventos).

```
https://raw.githubusercontent.com/0uand/iptv-mundial/main/youtube.m3u
```

No ar na última verificação (2026-10-09 21:17 UTC): **0** de 46 canais monitorados. Lista completa em [`data/youtube.csv`](data/youtube.csv) — sugestões de canais são bem-vindas via *issue*.

## 🎬 Filmes, séries, desenhos, shows e festivais (VOD)

Filmes e séries: acervo de **domínio público** do [Internet Archive](https://archive.org) (títulos até 1963 ou com licença livre declarada): clássicos do cinema, ficção/terror, cinema mudo, séries de TV clássicas e animações antigas. Os arquivos ficam hospedados no próprio Archive.

Shows e festivais: vídeos **públicos dos canais oficiais** no YouTube — Coachella, BBC Radio 1 (Live Lounge, Big Weekend), BBC Music (Glastonbury, Proms), Capital FM (Summertime Ball, Jingle Bell Ball), Boiler Room, Cercle, Tiny Desk, KEXP — e surf (WSL, Red Bull). Como as URLs do YouTube expiram, esta seção é renovada periodicamente.

| Catálogo | Títulos | Playlist |
|---|---:|---|
| 🎬 Filmes (por categoria) | 1.989 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/vod/filmes.m3u` |
| 🎤 Shows, festivais e surf | 0 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/vod/shows.m3u` |
| 📺 Séries (episódios) | 328 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/vod/series.m3u` |
| 📺 Desenhos | 220 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/vod/desenhos.m3u` |

**Categorias de filmes:** Premiados e Aclamados · Recentes (cinema aberto: Blender, Nina Paley, Kung Fury, Star Wreck, documentários CC) · 🇧🇷 Nacionais (memória: cinejornais e registros históricos) · Comédia · Drama · Terror · Ficção Científica · Faroeste · Noir e Suspense · Romance · Guerra · Aventura · Musical · Família · Animação · Documentário · Cinema Mudo · Clássicos por década. **Séries:** Comédia · Faroeste · Suspense e Crime · Ficção e Terror · Aventura · Drama · Game Shows e Variedades · Documentário · Desenhos — agrupadas por série, com temporada/episódio.


> **Sobre filmes nacionais e recentes:** só entram obras que podem ser distribuídas legalmente — domínio público ou licença livre dada pelo próprio autor. Filmes brasileiros de ficção (Vera Cruz, Embrafilme, Cinema Novo…) e lançamentos recentes de estúdio ainda estão sob direitos autorais, mesmo quando alguém os sobe no Internet Archive com etiqueta "CC"; por isso ficam de fora. O que existe de legal está em Tela Brasil, Globoplay, +SBT etc., com login.


> **Por que não tem Tela Brasil, +SBT, Globoplay, Band Play, PlayPlus?** Essas plataformas são gratuitas, mas exigem login (gov.br, conta da emissora) e entregam o vídeo com URL assinada por usuário. Não existe link público para colocar numa lista — e incluir seria burlar o acesso delas. Use os apps oficiais; aqui ficam só os sinais abertos e os canais FAST que as próprias emissoras publicam.


## 📅 EPG (guia de programação)

Guia gerado diariamente neste repositório com o [iptv-org/epg](https://github.com/iptv-org/epg), com 3 dias de programação, sinopses e imagens. Os IDs batem com os `tvg-id` das playlists, então basta usar a lista que o guia carrega sozinho. Se o seu app pedir a URL do EPG separadamente:

```
https://raw.githubusercontent.com/0uand/iptv-mundial/main/epg/guide.xml.gz
```

Última geração: 2026-10-09 19:39 UTC — 259 canais com programação, 19.806 programas.

## ⏪ Replay (catchup)

Replay é um recurso do servidor de cada emissora, e pouquíssimos streams públicos oferecem. A cada atualização semanal todos os canais são sondados; os que têm arquivo recebem as tags `catchup` / `catchup-source` / `catchup-days` (compatíveis com TiviMate, IPTV Smarters, OTT Navigator, Kodi). Atualmente: **23 canais com replay**.

## 🌎 Por país

| País | Canais | Playlist |
|---|---:|---|
| 🇧🇷 Brasil | 566 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/br.m3u` |
| 🇵🇹 Portugal | 44 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pt.m3u` |
| 🇺🇸 Estados Unidos | 2407 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/us.m3u` |
| 🇬🇧 Reino Unido | 604 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/uk.m3u` |
| 🇪🇸 Espanha | 403 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/es.m3u` |
| 🇦🇷 Argentina | 219 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ar.m3u` |
| 🇦🇫 Afeganistão | 13 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/af.m3u` |
| 🇦🇱 Albânia | 23 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/al.m3u` |
| 🇩🇪 Alemanha | 415 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/de.m3u` |
| 🇦🇩 Andorra | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ad.m3u` |
| 🇦🇴 Angola | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ao.m3u` |
| 🇦🇬 Antigua and Barbuda | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ag.m3u` |
| 🇩🇿 Argélia | 7 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/dz.m3u` |
| 🇦🇲 Armênia | 12 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/am.m3u` |
| 🇦🇼 Aruba | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/aw.m3u` |
| 🇸🇦 Arábia Saudita | 49 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sa.m3u` |
| 🇦🇺 Austrália | 118 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/au.m3u` |
| 🇦🇿 Azerbaijão | 21 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/az.m3u` |
| 🇧🇸 Bahamas | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bs.m3u` |
| 🇧🇭 Bahrein | 4 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bh.m3u` |
| 🇧🇩 Bangladesh | 34 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bd.m3u` |
| 🇧🇧 Barbados | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bb.m3u` |
| 🇧🇾 Belarus | 32 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/by.m3u` |
| 🇧🇿 Belize | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bz.m3u` |
| 🇧🇯 Benin | 10 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bj.m3u` |
| 🇧🇴 Bolívia | 102 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bo.m3u` |
| 🇧🇶 Bonaire | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bq.m3u` |
| 🇻🇬 British Virgin Islands | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/vg.m3u` |
| 🇧🇳 Brunei | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bn.m3u` |
| 🇧🇬 Bulgária | 83 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bg.m3u` |
| 🇧🇫 Burkina Faso | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/bf.m3u` |
| 🇧🇪 Bélgica | 61 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/be.m3u` |
| 🇧🇦 Bósnia | 16 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ba.m3u` |
| 🇨🇻 Cabo Verde | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cv.m3u` |
| 🇨🇲 Camarões | 16 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cm.m3u` |
| 🇰🇭 Camboja | 39 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kh.m3u` |
| 🇨🇦 Canadá | 344 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ca.m3u` |
| 🇶🇦 Catar | 44 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/qa.m3u` |
| 🇰🇿 Cazaquistão | 63 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kz.m3u` |
| 🇹🇩 Chad | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/td.m3u` |
| 🇨🇱 Chile | 253 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cl.m3u` |
| 🇨🇳 China | 508 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cn.m3u` |
| 🇨🇾 Chipre | 13 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cy.m3u` |
| 🇨🇴 Colômbia | 217 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/co.m3u` |
| 🇰🇵 Coreia do Norte | 7 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kp.m3u` |
| 🇰🇷 Coreia do Sul | 81 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kr.m3u` |
| 🇨🇷 Costa Rica | 72 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cr.m3u` |
| 🇨🇮 Costa do Marfim | 14 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ci.m3u` |
| 🇭🇷 Croácia | 22 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/hr.m3u` |
| 🇨🇺 Cuba | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cu.m3u` |
| 🇨🇼 Curacao | 4 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cw.m3u` |
| 🇩🇰 Dinamarca | 252 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/dk.m3u` |
| 🇪🇬 Egito | 12 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/eg.m3u` |
| 🇸🇻 El Salvador | 37 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sv.m3u` |
| 🇦🇪 Emirados Árabes | 35 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ae.m3u` |
| 🇪🇨 Equador | 97 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ec.m3u` |
| 🇬🇶 Equatorial Guinea | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gq.m3u` |
| 🇪🇷 Eritrea | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/er.m3u` |
| 🇸🇰 Eslováquia | 107 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sk.m3u` |
| 🇸🇮 Eslovênia | 21 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/si.m3u` |
| 🇪🇪 Estônia | 17 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ee.m3u` |
| 🇪🇹 Etiópia | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/et.m3u` |
| 🇵🇭 Filipinas | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ph.m3u` |
| 🇫🇮 Finlândia | 51 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/fi.m3u` |
| 🇫🇷 França | 456 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/fr.m3u` |
| 🇬🇫 French Guiana | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gf.m3u` |
| 🇵🇫 French Polynesia | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pf.m3u` |
| 🇬🇲 Gambia | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gm.m3u` |
| 🇬🇭 Gana | 9 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gh.m3u` |
| 🇬🇪 Geórgia | 26 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ge.m3u` |
| 🇬🇷 Grécia | 72 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gr.m3u` |
| 🇬🇵 Guadeloupe | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gp.m3u` |
| 🇬🇺 Guam | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gu.m3u` |
| 🇬🇹 Guatemala | 52 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gt.m3u` |
| 🇬🇳 Guinea | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gn.m3u` |
| 🇬🇾 Guyana | 4 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/gy.m3u` |
| 🇭🇹 Haiti | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ht.m3u` |
| 🇳🇱 Holanda | 214 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/nl.m3u` |
| 🇭🇳 Honduras | 74 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/hn.m3u` |
| 🇭🇰 Hong Kong | 14 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/hk.m3u` |
| 🇭🇺 Hungria | 143 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/hu.m3u` |
| 🇫🇴 Ilhas Faroé | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/fo.m3u` |
| 🇮🇩 Indonésia | 168 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/id.m3u` |
| 🇮🇶 Iraque | 48 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/iq.m3u` |
| 🇮🇪 Irlanda | 10 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ie.m3u` |
| 🇮🇷 Irã | 138 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ir.m3u` |
| 🇮🇸 Islândia | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/is.m3u` |
| 🇮🇱 Israel | 61 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/il.m3u` |
| 🇮🇹 Itália | 416 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/it.m3u` |
| 🇾🇪 Iêmen | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ye.m3u` |
| 🇯🇲 Jamaica | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/jm.m3u` |
| 🇯🇵 Japão | 20 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/jp.m3u` |
| 🇯🇴 Jordânia | 17 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/jo.m3u` |
| 🇽🇰 Kosovo | 11 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/xk.m3u` |
| 🇰🇼 Kuwait | 13 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kw.m3u` |
| 🇱🇦 Laos | 9 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/la.m3u` |
| 🇱🇻 Letônia | 20 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lv.m3u` |
| 🇱🇹 Lituânia | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lt.m3u` |
| 🇱🇺 Luxemburgo | 14 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lu.m3u` |
| 🇱🇧 Líbano | 27 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lb.m3u` |
| 🇱🇾 Líbia | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ly.m3u` |
| 🇲🇴 Macau | 10 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mo.m3u` |
| 🇲🇰 Macedônia do Norte | 23 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mk.m3u` |
| 🇲🇻 Maldives | 13 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mv.m3u` |
| 🇲🇱 Mali | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ml.m3u` |
| 🇲🇹 Malta | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mt.m3u` |
| 🇲🇾 Malásia | 13 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/my.m3u` |
| 🇲🇦 Marrocos | 14 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ma.m3u` |
| 🇲🇶 Martinique | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mq.m3u` |
| 🇲🇷 Mauritania | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mr.m3u` |
| 🇲🇩 Moldávia | 27 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/md.m3u` |
| 🇲🇳 Mongólia | 99 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mn.m3u` |
| 🇲🇪 Montenegro | 4 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/me.m3u` |
| 🇲🇿 Moçambique | 7 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mz.m3u` |
| 🇲🇲 Myanmar | 18 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mm.m3u` |
| 🇲🇽 México | 411 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mx.m3u` |
| 🇲🇨 Mônaco | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/mc.m3u` |
| 🇳🇦 Namíbia | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/na.m3u` |
| 🇳🇵 Nepal | 19 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/np.m3u` |
| 🇳🇨 New Caledonia | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/nc.m3u` |
| 🇳🇮 Nicarágua | 16 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ni.m3u` |
| 🇳🇪 Niger | 4 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ne.m3u` |
| 🇳🇬 Nigéria | 37 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ng.m3u` |
| 🇳🇴 Noruega | 196 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/no.m3u` |
| 🇳🇿 Nova Zelândia | 78 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/nz.m3u` |
| 🇴🇲 Omã | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/om.m3u` |
| 🇵🇸 Palestine | 21 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ps.m3u` |
| 🇵🇦 Panamá | 17 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pa.m3u` |
| 🇵🇬 Papua New Guinea | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pg.m3u` |
| 🇵🇰 Paquistão | 106 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pk.m3u` |
| 🇵🇾 Paraguai | 75 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/py.m3u` |
| 🇵🇪 Peru | 255 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pe.m3u` |
| 🇵🇱 Polônia | 164 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pl.m3u` |
| 🇵🇷 Porto Rico | 22 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/pr.m3u` |
| 🇰🇬 Quirguistão | 11 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kg.m3u` |
| 🇰🇪 Quênia | 18 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ke.m3u` |
| 🇨🇩 RD Congo | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cd.m3u` |
| 🇨🇬 Republic of the Congo | 5 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cg.m3u` |
| 🇩🇴 República Dominicana | 239 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/do.m3u` |
| 🇨🇿 República Tcheca | 73 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/cz.m3u` |
| 🇷🇴 Romênia | 145 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ro.m3u` |
| 🇷🇼 Ruanda | 9 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/rw.m3u` |
| 🇷🇺 Rússia | 1361 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ru.m3u` |
| 🇰🇳 Saint Kitts and Nevis | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/kn.m3u` |
| 🇱🇨 Saint Lucia | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lc.m3u` |
| 🇼🇸 Samoa | 1 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ws.m3u` |
| 🇸🇲 San Marino | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sm.m3u` |
| 🇸🇳 Senegal | 11 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sn.m3u` |
| 🇸🇬 Singapura | 21 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sg.m3u` |
| 🇸🇽 Sint Maarten | 7 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sx.m3u` |
| 🇸🇴 Somalia | 11 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/so.m3u` |
| 🇱🇰 Sri Lanka | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/lk.m3u` |
| 🇸🇩 Sudão | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sd.m3u` |
| 🇸🇪 Suécia | 231 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/se.m3u` |
| 🇨🇭 Suíça | 29 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ch.m3u` |
| 🇷🇸 Sérvia | 47 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/rs.m3u` |
| 🇸🇾 Síria | 15 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/sy.m3u` |
| 🇹🇭 Tailândia | 93 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/th.m3u` |
| 🇹🇼 Taiwan | 43 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tw.m3u` |
| 🇹🇯 Tajiquistão | 17 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tj.m3u` |
| 🇹🇿 Tanzânia | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tz.m3u` |
| 🇹🇬 Togo | 8 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tg.m3u` |
| 🇹🇹 Trinidad e Tobago | 2 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tt.m3u` |
| 🇹🇳 Tunísia | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tn.m3u` |
| 🇹🇲 Turcomenistão | 16 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tm.m3u` |
| 🇹🇷 Turkiye | 225 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/tr.m3u` |
| 🇺🇦 Ucrânia | 224 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ua.m3u` |
| 🇺🇬 Uganda | 14 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ug.m3u` |
| 🇺🇾 Uruguai | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/uy.m3u` |
| 🇺🇿 Uzbequistão | 37 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/uz.m3u` |
| 🇻🇪 Venezuela | 80 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/ve.m3u` |
| 🇻🇳 Vietnã | 112 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/vn.m3u` |
| 🇪🇭 Western Sahara | 3 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/eh.m3u` |
| 🇿🇦 África do Sul | 12 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/za.m3u` |
| 🇦🇹 Áustria | 46 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/at.m3u` |
| 🇮🇳 Índia | 1423 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/countries/in.m3u` |

## 🎯 Por categoria

| Categoria | Canais | Playlist |
|---|---:|---|
| Música | 1189 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/music.m3u` |
| Entretenimento | 1233 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/entertainment.m3u` |
| Animação | 186 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/animation.m3u` |
| Automotivo | 36 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/auto.m3u` |
| Ciência | 26 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/science.m3u` |
| Clima | 20 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/weather.m3u` |
| Clássicos | 74 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/classic.m3u` |
| Compras | 90 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/shop.m3u` |
| Comédia | 213 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/comedy.m3u` |
| Culinária | 77 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/cooking.m3u` |
| Cultura | 199 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/culture.m3u` |
| Documentários | 348 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/documentary.m3u` |
| Educação | 221 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/education.m3u` |
| Esportes | 672 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/sports.m3u` |
| Estilo de vida | 152 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/lifestyle.m3u` |
| Família | 72 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/family.m3u` |
| Filmes | 996 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/movies.m3u` |
| Geral | 6904 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/general.m3u` |
| Infantil | 470 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/kids.m3u` |
| Legislativo | 200 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/legislative.m3u` |
| Negócios | 107 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/business.m3u` |
| Notícias | 1753 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/news.m3u` |
| Outdoor | 97 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/outdoor.m3u` |
| Pública | 6 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/public.m3u` |
| Relax | 16 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/relax.m3u` |
| Séries | 629 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/series.m3u` |
| Viagem | 66 | `https://raw.githubusercontent.com/0uand/iptv-mundial/main/categories/travel.m3u` |

## ⚠️ Avisos

- Em listas públicas, parte dos canais pode estar fora do ar em um dado momento — a lista é regenerada semanalmente.
- Alguns canais só funcionam no país de origem (bloqueio de região imposto pela própria emissora, não pelo seu aparelho).
- Problemas com um canal específico devem ser reportados à emissora ou ao projeto iptv-org.

## 🔧 Como funciona

| Workflow | Frequência | O que faz |
|---|---|---|
| `update.yml` | semanal (seg) | regenera canais, VOD e sonda replay |
| `youtube.yml` | a cada 4 h | renova as lives do YouTube (o YouTube costuma bloquear os IPs do GitHub; quando isso acontece a lista anterior é mantida) |
| `epg.yml` | diário | gera o guia de programação |

## 📄 Licença

Dados derivados dos projetos [iptv-org/iptv](https://github.com/iptv-org/iptv) e [iptv-org/epg](https://github.com/iptv-org/epg) (Unlicense). Conteúdo VOD: domínio público via Internet Archive.
