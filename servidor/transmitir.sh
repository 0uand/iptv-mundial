#!/usr/bin/env bash
# uandtv — TRANSMISSÃO: lê os arquivos prontos (lista.txt) em loop infinito e publica
# um stream HLS ao vivo em /var/www/uandtv/live.m3u8, SEM reencodar (-c copy).
# Como todos os arquivos saíram da ingestão no mesmo formato, a emenda é invisível.
# Gerenciado pelo systemd (uandtv-transmissao.service), que reinicia se cair.
set -euo pipefail

BASE="${UANDTV_BASE:-/srv/uandtv}"
LISTA="$BASE/lista.txt"
WWW="${UANDTV_WWW:-/var/www/uandtv}"
SEG=6          # segundos por pedaço HLS
JANELA=10      # pedaços mantidos na playlist (~60 s de buffer para o app)

mkdir -p "$WWW"
[[ -s "$LISTA" ]] && grep -q '^file' "$LISTA" || { echo "lista.txt vazia — rode ingerir.sh primeiro"; exit 1; }

# -re            : lê na velocidade real (1x), senão o ffmpeg dispararia a 100x
# -stream_loop -1: repete a playlist para sempre
# -f concat      : emenda os arquivos da lista
# -c copy        : copia os pacotes de vídeo/áudio como estão (CPU ~0)
# hls_flags      : delete_segments (apaga pedaços velhos), omit_endlist (nunca "termina" = ao vivo),
#                  program_date_time (relógio na playlist), independent_segments
exec ffmpeg -hide_banner -loglevel warning -nostdin \
  -re -fflags +genpts -stream_loop -1 -f concat -safe 0 -i "$LISTA" \
  -map 0:v:0 -map 0:a:0? -c copy \
  -f hls -hls_time "$SEG" -hls_list_size "$JANELA" \
  -hls_flags delete_segments+omit_endlist+program_date_time+independent_segments+temp_file \
  -hls_segment_type mpegts -hls_segment_filename "$WWW/seg_%06d.ts" \
  "$WWW/live.m3u8"
