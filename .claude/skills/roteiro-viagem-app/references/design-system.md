# Design system do app

Estilo "iOS nativo + dourado de vinícola". Manter para que toda viagem tenha a mesma cara; trocar só `--gold` se quiser identidade própria.

## Tokens (`:root`)

| Token | Light | Dark (`html.dark`) | Uso |
|---|---|---|---|
| `--bg` | `#F2F2F7` | `#1C1C1E` | fundo geral |
| `--bg2` | `#FFF` | `#2C2C2E` | cards / header |
| `--bg3` / `--bg4` | `#F2F2F7` / `#E5E5EA` | `#3A3A3C` / `#48484A` | superfícies secundárias |
| `--sep` | `rgba(60,60,67,.18)` | `rgba(255,255,255,.12)` | divisores 0.5px |
| `--gold` | `#B8860B` | `#D4A843` | acento, aba ativa, datas |
| `--cr` | `#000` | `#FFF` | texto principal |
| `--t2` / `--t3` | `rgba(60,60,67,.6)` / `.38` | `rgba(255,255,255,.6)` / `.38` | texto secundário / terciário |
| `--blue` | `#007AFF` | `#0A84FF` | links/ações |

Tipografia: títulos `Fraunces` (serif, peso 300, itálico dourado no destaque do logo); corpo `Plus Jakarta Sans`, 15px/1.55; fallback `-apple-system`.

## Cores por tipo de parada (`TC`, marcadores/mapa)

hotel `#C06060` · famous `#A090D4` · boutique `#5AAF78` · lunch/almoco `#CF8050` · city/cidade `#909090` · mountain/montanha `#6898C0`. Rota no mapa: `#C49A4A` tracejada. Marcadores numerados usam `STOP_COLORS` (8 cores cíclicas).

## Etiquetas (`.b-*`) e status (`.s-*`)

`b-hotel` vermelho · `b-famous` roxo · `b-boutique` verde · `b-almoco` laranja · `b-jantar` azul-índigo · `b-cidade` cinza · `b-montanha` azul · `b-opcional` lilás. Cada uma tem variante `html.dark` com **contraste reforçado** (bug real: etiquetas ilegíveis no dark mode). Status: `s-ok` verde, `s-warn` amarelo, `s-nohr` cinza.

## Layout

- Header fixo: logo (esq.) + ícones 📄 docs, 💰 resumo, 🌙 tema; texto `.pax` (dir.). **Em ≤400px** reduzir logo e `.pax` e não deixar o header quebrar linha.
- Abas de fase (`.ptab`) com borda inferior dourada na ativa.
- Barra de dias (`.dnav`) sticky, pílulas horizontais com scroll (sem scrollbar).
- Cabeçalho do dia: data em caixa-alta dourada, título grande, resumo, botões **Google Maps** (azul) e **Waze** (ciano, ícone do mascote via sprite `waze-logo.png`).
- Mini-carrossel das paradas (`.sp-*`) com número, horário e nome sobre gradiente.
- Lista em timeline: seções por período (Manhã / Tarde / Noite / Todo o dia), ponto colorido, etiqueta + status + horário + descrição + "ver detalhes ›".
- Bottom sheet (`.sheet`) para detalhe; modais (`.rs-modal`) para remarcar, docs, dividir conta, resumo, info. **Só um modal por vez** — fechar os empilhados antes de abrir outro (bug real: sobreposição).
- Cards de almoço: **sem gradiente/brilho**, só o badge destaca.

## Interações

- Botões usam `onTap` (touch-action: manipulation) — não usar `click` puro em elementos dentro de rolagem horizontal.
- Visualizador de PDF embutido renderiza **todas as páginas** (pdf.js); botão ⤢ abre o PDF completo em nova aba **sem perder a aba/dia atual**.
- Lightbox para fotos (setas, contador, swipe).
