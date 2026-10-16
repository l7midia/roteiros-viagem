# Variante: várias fases + transporte público (Japão 2026)

Implementação de referência: `toquio-hugo-maga/index.html` (6 hospedagens, 20 dias, sem carro). Use como base quando a viagem **não for de carro** ou tiver **mais de 2 hospedagens**. O motor do `template/` continua valendo para 2 fases de carro.

## O que muda em relação ao template
- **N abas**: `PHASES=[["p1","🗼 Tóquio · 16–22/10"],...]` gera as abas (`buildTabs()`), roláveis na horizontal; `PHASE_NAME` deriva de `PHASES`.
- **`HOTELS`** guarda `{name, addr, din, dout, gmaps?}` (sem lat/lng). O dia mostra a linha do hotel com check-in/out; a origem da rota é o texto "nome, endereço".
- **Só Google Maps** (sem Waze/WhatsApp): botão único do dia = rota em transporte público (`travelmode=transit`, origem = hotel ou `day.origin`, destino = 1ª parada com `q`). Na ficha da parada: "Ver no Google Maps" (busca por `q` ou `gmaps`), "Como chegar" (transit), site, Instagram.
- **Paradas sem coordenadas**: usam `q` (consulta de busca, ex. `"Senso-ji Temple, Asakusa, Tokyo"`). Sem `lat/lng` o mapa do dia fica oculto; com Places API dá para enriquecer depois.
- **Painel do dia** (`day.guide`): `importante[]` (aberto), `locomover[]`, `comer[]`, `dica`.
- **Guia da viagem** (📖) no lugar de Documentos/Resumo: HTML embutido (`GUIDE_HTML`) com checklist, voos, hotéis, imigração, dinheiro/tax free, transporte, apps, clima, etiqueta e listas de restaurantes com links.
- Dividir conta e Resumo 💰 removidos (casal). Moeda em `CUR`/`ja-JP`.
- `status` (`st`/`stl`) reaproveitado para **estado de reserva**: `RESERVA CONFIRMADA`, `A CONFIRMAR`, `INGRESSO COMPRADO`, `BILHETE COMPRADO`.
- Novas etiquetas: `passeio`, `templo`, `natureza`, `transporte`, `ingresso`.

## Regras de conteúdo aprendidas
- Horário que o PDF/briefing não dá e eu deduzi vai com `~` (ex.: `~9h15`) e isso deve ser dito ao cliente.
- Voo que cruza a meia-noite: usar `time:null` e a data no nome da parada, senão a linha do tempo (Manhã/Tarde/Noite) fica fora de ordem.
- Dados sensíveis (código de reserva, número de voo, nome na reserva) **ficam fora** do app público; manter `<meta name="robots" content="noindex,nofollow">` e compartilhar o link só com a pessoa.
- Links copiados de PDF de agência: conferir se o domínio faz sentido (houve link de restaurante apontando para site de tradução e perfis `instagram.com/popular/...` inválidos); na dúvida, omitir e deixar só a busca no Maps.
- Ambiente cloud: sem API de lugares conectada e sites externos bloqueados (DNS); só `WebSearch`. Para nota/foto/coordenadas é preciso uma chave Google Places como segredo do ambiente.
