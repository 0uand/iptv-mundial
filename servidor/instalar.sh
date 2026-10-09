#!/usr/bin/env bash
# uandtv — INSTALADOR. Rode como root no VPS, de dentro desta pasta (servidor/):
#   sudo bash instalar.sh
# Copia scripts, serviços e nginx para os lugares certos. Pode rodar de novo para atualizar.
set -euo pipefail
AQUI="$(cd "$(dirname "$0")" && pwd)"
id uandtv >/dev/null 2>&1 || adduser --disabled-password --gecos "" uandtv
mkdir -p /srv/uandtv/bin /srv/uandtv/logs /var/www/uandtv
install -m 755 "$AQUI"/ingerir.sh "$AQUI"/transmitir.sh "$AQUI"/reiniciar-se-mudou.sh /srv/uandtv/bin/
[[ -f /srv/uandtv/programacao.txt ]] || install -m 644 "$AQUI"/programacao.exemplo.txt /srv/uandtv/programacao.txt
[[ -f /srv/uandtv/logo.png ]] || { [[ -f "$AQUI"/logo.png ]] && install -m 644 "$AQUI"/logo.png /srv/uandtv/logo.png; }
chown -R uandtv:uandtv /srv/uandtv /var/www/uandtv
install -m 644 "$AQUI"/uandtv-transmissao.service "$AQUI"/uandtv-ingestao.service "$AQUI"/uandtv-ingestao.timer /etc/systemd/system/
# permite ao usuário uandtv reiniciar só a própria transmissão
echo 'uandtv ALL=(root) NOPASSWD: /usr/bin/systemctl restart uandtv-transmissao.service' > /etc/sudoers.d/uandtv
chmod 440 /etc/sudoers.d/uandtv
install -m 644 "$AQUI"/nginx-uandtv.conf /etc/nginx/sites-available/uandtv
ln -sf /etc/nginx/sites-available/uandtv /etc/nginx/sites-enabled/uandtv
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx
systemctl daemon-reload
systemctl enable --now uandtv-ingestao.timer
systemctl enable uandtv-transmissao.service
echo
echo "Instalado. Próximos passos:"
echo "  1. coloque o logo em /srv/uandtv/logo.png e a programação em /srv/uandtv/programacao.txt"
echo "  2. sudo -u uandtv /srv/uandtv/bin/ingerir.sh      (primeira ingestão, acompanhe o progresso)"
echo "  3. systemctl start uandtv-transmissao && sleep 15 && curl -s http://localhost/live.m3u8"
echo "  URL do canal: http://$(curl -s -4 ifconfig.me 2>/dev/null || hostname -I | awk '{print $1}')/live.m3u8"
