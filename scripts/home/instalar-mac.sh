#!/usr/bin/env bash
# Instala o "YouTube TV" da sua lista no seu Mac: a cada 4 h resolve as lives do YouTube
# na sua rede de casa e publica youtube.m3u no GitHub (0uand/iptv-mundial).
# Uso:  bash <(curl -fsSL https://raw.githubusercontent.com/0uand/iptv-mundial/main/scripts/home/instalar-mac.sh)
set -e
REPO="https://github.com/0uand/iptv-mundial.git"
DIR="$HOME/iptv-mundial"
echo "▶ Verificando ferramentas…"
command -v git >/dev/null || { echo "Instale o Xcode Command Line Tools: xcode-select --install"; exit 1; }
if ! command -v yt-dlp >/dev/null; then
  if command -v brew >/dev/null; then brew install yt-dlp; else python3 -m pip install --user -q yt-dlp; export PATH="$HOME/Library/Python/3.9/bin:$HOME/.local/bin:$PATH"; fi
fi
command -v yt-dlp >/dev/null || { echo "yt-dlp não encontrado no PATH. Instale com: brew install yt-dlp"; exit 1; }
echo "▶ Clonando/atualizando o repositório em $DIR…"
if [ -d "$DIR/.git" ]; then git -C "$DIR" pull -q --rebase; else git clone -q "$REPO" "$DIR"; fi
git -C "$DIR" config user.name "uand-mac"; git -C "$DIR" config user.email "uandboard@gmail.com"
git -C "$DIR" config credential.helper osxkeychain
echo
echo "▶ Autorização do GitHub (uma vez só):"
echo "  1. Abra https://github.com/settings/personal-access-tokens/new"
echo "  2. Repository access: Only select repositories → iptv-mundial"
echo "  3. Permissions → Contents: Read and write   → Generate token"
echo "  Na primeira publicação o git vai pedir usuário (0uand) e senha (cole o token). Fica salvo no Keychain."
echo
echo "▶ Primeira execução (2–5 min)…"
bash "$DIR/scripts/home/atualizar.sh"
echo "▶ Agendando a cada 4 h (launchd)…"
PLIST="$HOME/Library/LaunchAgents/br.uand.iptv-youtube.plist"
cat > "$PLIST" <<PL
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0"><dict>
  <key>Label</key><string>br.uand.iptv-youtube</string>
  <key>ProgramArguments</key><array><string>/bin/bash</string><string>$DIR/scripts/home/atualizar.sh</string></array>
  <key>StartInterval</key><integer>14400</integer>
  <key>RunAtLoad</key><true/>
  <key>StandardOutPath</key><string>$HOME/Library/Logs/iptv-youtube.log</string>
  <key>StandardErrorPath</key><string>$HOME/Library/Logs/iptv-youtube.log</string>
  <key>EnvironmentVariables</key><dict><key>PATH</key><string>/opt/homebrew/bin:/usr/local/bin:$HOME/Library/Python/3.9/bin:$HOME/.local/bin:/usr/bin:/bin</string></dict>
</dict></plist>
PL
launchctl unload "$PLIST" 2>/dev/null || true
launchctl load "$PLIST"
echo "✅ Pronto. Log em ~/Library/Logs/iptv-youtube.log. Para desinstalar: launchctl unload $PLIST && rm $PLIST"
