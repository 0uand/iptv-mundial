#!/usr/bin/env bash
# Reinicia a transmissão só se lista.txt mudou desde a última vez (evita cortes à toa).
BASE="${UANDTV_BASE:-/srv/uandtv}"
atual="$(sha1sum "$BASE/lista.txt" 2>/dev/null | cut -c1-40)"
antes="$(cat "$BASE/.lista.sha1" 2>/dev/null || true)"
if [[ -n "$atual" && "$atual" != "$antes" ]]; then
  echo "$atual" > "$BASE/.lista.sha1"
  echo "lista mudou — reiniciando transmissão"
  sudo -n systemctl restart uandtv-transmissao.service || true
fi
