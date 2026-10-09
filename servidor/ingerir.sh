#!/usr/bin/env bash
# uandtv — INGESTÃO: baixa cada item de programacao.txt e gera um arquivo padronizado
# (1280x720, 30 fps, H.264 + AAC, MPEG-TS) com o logo queimado no canto inferior direito.
# Roda uma vez por vídeo; vídeos já prontos são pulados. Depois reescreve a lista de
# reprodução (lista.txt) na ordem de programacao.txt.
#
# Uso:  ingerir.sh            (processa o que falta)
#       ingerir.sh --refazer  (apaga os prontos e reencoda tudo — use ao trocar o logo)
set -euo pipefail

BASE="${UANDTV_BASE:-/srv/uandtv}"
PROG="$BASE/programacao.txt"
LOGO="$BASE/logo.png"
BRUTO="$BASE/bruto"      # downloads originais (podem ser apagados depois)
PRONTO="$BASE/pronto"    # arquivos padronizados com logo, prontos para o loop
LISTA="$BASE/lista.txt"  # playlist que o transmitir.sh lê
LOG="$BASE/logs/ingestao.log"

# Padrão de vídeo. Tudo igual em todos os arquivos = emenda invisível no loop.
LARGURA=1280; ALTURA=720; FPS=30; VBITRATE=2500k; ABITRATE=128k
# Logo: largura em pixels e margem até as bordas (em px, no quadro 1280x720)
LOGO_LARGURA=160; MARGEM=40

mkdir -p "$BRUTO" "$PRONTO" "$(dirname "$LOG")"
exec > >(tee -a "$LOG") 2>&1
echo "== $(date '+%F %T') ingestão iniciada"

[[ -f "$PROG" ]] || { echo "ERRO: $PROG não existe"; exit 1; }
[[ -f "$LOGO" ]] || { echo "ERRO: $LOGO não existe (PNG com fundo transparente)"; exit 1; }
[[ "${1:-}" == "--refazer" ]] && { echo "apagando prontos para reencodar"; rm -f "$PRONTO"/*.ts; }

# id estável para cada linha da programação (hash da URL/caminho)
idde() { printf '%s' "$1" | sha1sum | cut -c1-12; }

ordem=()
while IFS= read -r linha || [[ -n "$linha" ]]; do
  linha="${linha%%#*}"; linha="$(echo "$linha" | xargs)"   # tira comentários e espaços
  [[ -z "$linha" ]] && continue
  id="$(idde "$linha")"
  saida="$PRONTO/$id.ts"
  ordem+=("$saida")
  if [[ -s "$saida" ]]; then echo "ok    $id  (já pronto)  $linha"; continue; fi

  # 1) obter o arquivo bruto: URL → yt-dlp; caminho local → usa direto
  if [[ "$linha" =~ ^https?:// ]]; then
    bruto="$BRUTO/$id.mp4"
    if [[ ! -s "$bruto" ]]; then
      echo "baixa $id  $linha"
      yt-dlp -q --no-warnings -f "bv*[height<=1080]+ba/b[height<=1080]/b" \
        --merge-output-format mp4 -o "$bruto" "$linha" || { echo "FALHA download $linha"; continue; }
    fi
  else
    bruto="$linha"
    [[ -f "$bruto" ]] || { echo "FALHA arquivo não encontrado: $bruto"; continue; }
  fi

  # 2) padronizar + queimar o logo
  #    scale/pad: cabe em 1280x720 mantendo proporção, faixas pretas se preciso
  #    overlay: logo redimensionado para LOGO_LARGURA, a MARGEM px da borda inferior direita
  #    -g 60 / keyint_min 60 / sc_threshold 0: keyframe fixo a cada 2 s, para o HLS cortar certinho
  echo "codif $id  → $saida"
  ffmpeg -hide_banner -loglevel error -nostdin -y \
    -i "$bruto" -i "$LOGO" \
    -filter_complex "\
      [0:v]scale=${LARGURA}:${ALTURA}:force_original_aspect_ratio=decrease,\
           pad=${LARGURA}:${ALTURA}:(ow-iw)/2:(oh-ih)/2,fps=${FPS}[v];\
      [1:v]scale=${LOGO_LARGURA}:-1[logo];\
      [v][logo]overlay=W-w-${MARGEM}:H-h-${MARGEM},format=yuv420p[out]" \
    -map "[out]" -map "0:a:0?" \
    -c:v libx264 -preset medium -profile:v high -level 4.0 -b:v "$VBITRATE" -maxrate "$VBITRATE" -bufsize 5000k \
    -g $((FPS*2)) -keyint_min $((FPS*2)) -sc_threshold 0 \
    -c:a aac -b:a "$ABITRATE" -ar 48000 -ac 2 \
    -af "aresample=async=1:first_pts=0" \
    -f mpegts "$saida.tmp" && mv "$saida.tmp" "$saida" \
    || { echo "FALHA codificação $linha"; rm -f "$saida.tmp"; continue; }
done < "$PROG"

# 3) reescrever a playlist do loop na ordem da programação
{
  echo "ffconcat version 1.0"
  for f in "${ordem[@]}"; do [[ -s "$f" ]] && echo "file '$f'" || true; done
} > "$LISTA.tmp" && mv "$LISTA.tmp" "$LISTA"
echo "lista: $(grep -c '^file' "$LISTA") vídeos prontos"
echo "== $(date '+%F %T') ingestão concluída"
