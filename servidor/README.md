# uandtv — servidor de transmissão 24h

Scripts para rodar a uandtv como canal de verdade (stream HLS com logo queimado na imagem) num VPS Ubuntu.
O manual completo, passo a passo, está no guia "uandtv — servidor de transmissão 24h" (Claude Docs).

| Arquivo | Papel |
| --- | --- |
| `instalar.sh` | instala tudo no VPS (`sudo bash instalar.sh`) |
| `ingerir.sh` | baixa e padroniza cada vídeo de `programacao.txt` com o logo (roda 1x por vídeo) |
| `transmitir.sh` | loop infinito dos arquivos prontos → `/var/www/uandtv/live.m3u8` (sem reencodar) |
| `reiniciar-se-mudou.sh` | reinicia a transmissão só quando a grade muda |
| `uandtv-*.service/.timer` | systemd: transmissão sempre viva, ingestão a cada hora |
| `nginx-uandtv.conf` | serve o HLS na porta 80 |
| `programacao.exemplo.txt` | modelo da grade |
| `logo.png` | marca d'água provisória (troque pelo PNG em Helvetica Neue Bold) |

Conteúdo: só o que você tem direito de reencodar e redistribuir (produção própria, licenciado, Creative Commons, domínio público).
