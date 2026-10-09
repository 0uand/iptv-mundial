# YouTube TV — resolvedor de casa

O YouTube amarra cada URL de live ao **IP de quem resolveu** e ela expira em ~6 h.
Resolvido num servidor (GitHub Actions, nuvem), o link **não toca** na sua TV.
Solução: rodar o resolvedor no seu Mac, na mesma rede da Apple TV, a cada 4 h.

**Instalar (Mac):**
```
bash <(curl -fsSL https://raw.githubusercontent.com/0uand/iptv-mundial/main/scripts/home/instalar-mac.sh)
```
Na primeira publicação o git pede usuário (`0uand`) e senha — cole um token criado em
https://github.com/settings/personal-access-tokens/new (repo `iptv-mundial`, Contents: Read and write).

Depois disso roda sozinho (launchd, a cada 4 h, inclusive ao ligar o Mac). Log: `~/Library/Logs/iptv-youtube.log`.
O Mac precisa estar ligado (pode estar com a tela bloqueada; em suspensão o agendamento espera acordar).
