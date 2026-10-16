---
name: roteiro-viagem-app
description: Cria um web app de roteiro de viagem (mobile-first, arquivo único, publicado no GitHub Pages) idêntico em estrutura e premissas ao app "Mendoza 2026". Use quando o usuário quiser montar o roteiro de uma nova viagem, replicar o app do Mendoza para outro destino, ou gerar o backup offline (PDF/DOCX) de um roteiro.
---

# Roteiro de viagem — web app

Replica o app que funcionou "perfeitamente" na viagem a Mendoza (Set/2026): um único `index.html`, sem build, sem backend, abre no celular e funciona dentro do carro. O **motor** (HTML/CSS/JS) é invariável; o que muda a cada viagem são os **dados** (`DATA`) e um punhado de constantes.

## Premissas (não negociar)

1. **Arquivo único, sem build/framework.** HTML + CSS + JS num `index.html`; dados embutidos no próprio arquivo. Só dependências por CDN: Leaflet (mapa/OSM, sem API key), Google Fonts.
2. **Mobile-first, estilo iOS** (fundo `#F2F2F7`, header com blur, bottom sheet, dark mode via `html.dark`). Testar sempre em ~390px de largura.
3. **Dados ≠ código.** Todo conteúdo da viagem vive em `const DATA = {...}`. Nunca editar o motor para mudar conteúdo.
4. **Duas fases (abas)** = duas regiões/hotéis (ex.: campo → cidade). Chaves internas `p1`/`p2`.
5. **Cada dia** = título, resumo, links de rota (Google Maps + Waze), paradas, opções de almoço e jantar, opcionais.
6. **Estado do usuário só no aparelho** (`localStorage` + IndexedDB). Sem login, sem servidor. Ver `references/schema.md`.
7. **Produto final = link do GitHub Pages** (`https://<usuario>.github.io/<repo>/`), não o código. Sempre entregar esse link + backup offline.
8. **Dado só entra se verificado**: horário de funcionamento confere com o dia da semana; reservas confirmadas viram o horário oficial da parada; fotos são cópias locais.

## Fluxo de trabalho

1. **Briefing** (perguntar só o que faltar): destino, datas, nº de pessoas (e quem divide a conta), 2 regiões/hotéis com coordenadas, moeda local + locale, reservas já feitas, preferências (vinícolas, restaurantes, ritmo), documentos a anexar (seguro, carro, hotel).
2. **Criar repo** novo e copiar `template/` para a raiz (ver "Template"). Preencher placeholders `{{...}}` (lista abaixo).
3. **Montar `DATA`** dia a dia seguindo `references/schema.md`. Ordem sugerida: hotéis → âncoras fixas (reservas) → paradas do dia por horário de funcionamento → opções de almoço/jantar → opcionais.
4. **Enriquecer** cada parada (lat/lng, rating, horários por dia da semana, telefone, WhatsApp, Instagram, site, `gmaps`). Baixar 3–5 fotos para `assets/photos/<slug>/N.jpg` (nunca hotlink — ver lições).
5. **Rotas**: gerar `route` (Google Maps `dir/?api=1&travelmode=driving&origin=…&destination=…&waypoints=…`) e `waze` por dia, partindo do hotel da fase.
6. **Documentos**: PDFs em `assets/docs/`, listados em `DOCS` (categoria → grupo/família → arquivos). Comprovantes de reserva em `assets/reservas/` via `pinnedFiles`.
7. **Testar no navegador** (Playwright/Chromium, viewport 390×800): sem erros de console, abas, navegação de dias, bottom sheet, modais (docs 📄, resumo 💰, dividir conta), dark mode.
8. **Publicar**: ativar GitHub Pages (branch principal, raiz). Conferir que `https://<usuario>.github.io/<repo>/` abre.
9. **Backup offline**: gerar PDF + DOCX a partir do `DATA` (ver `references/backup-offline.md`) e commitar no repo.

## Template

`template/index.html` é o motor genérico (extraído do app Mendoza, testado sem erros) com um `DATA` de exemplo mínimo. `template/waze-logo.png` é obrigatório na raiz (ícone do botão Waze). Pastas esperadas: `assets/photos/`, `assets/docs/`, `assets/reservas/`.

Placeholders a substituir (busca por `{{`):

| Placeholder | Exemplo (Mendoza) |
|---|---|
| `{{VIAGEM}}` / `{{MES_ANO}}` | `Mendoza` / `Set 2026` (título da aba) |
| `{{DESTINO}}` / `{{ANO}}` | `Mendoza` / `V2` (logo do header) |
| `{{FASE_1}}` / `{{DATAS_1}}` | `Valle de Uco` / `06–09/09` |
| `{{FASE_2}}` / `{{DATAS_2}}` | `Mendoza Centro` / `09–15/09` |
| `{{PAX}}` | `4 adultos · 2 bebês` |
| `{{SLUG}}` | `mendoza2026` (prefixo de IndexedDB e localStorage — **único por viagem**, senão estados de viagens diferentes se misturam) |
| `{{MOEDA_LOCAL}}` / `{{LOCALE}}` | `ARS` / `es-AR` |

Constantes além dos placeholders (editar no `index.html`): `HOTELS` (lat/lng do hotel de cada fase — origem das rotas e mapa), `SPLIT_PEOPLE` (chave curta + nome de quem divide contas), `DOCS`, cores de `TC`/`BC` se quiser novos tipos de parada.

## Funcionalidades do motor (já prontas — não reescrever)

- Abas de fase + navegação horizontal de dias + mapa Leaflet do dia com marcadores numerados.
- Cards de parada com badge de tipo, status de funcionamento (`ok/warn/nohr`), horário, rating, foto; "ver detalhes" abre bottom sheet com carrossel de fotos + lightbox, horários da semana, descrição, botões (Maps, Waze, WhatsApp, Instagram, site, cardápio).
- **Realizado / Remarcar**: marca parada como feita; "Remarcar" move a parada para outro dia e **recalcula a rota** automaticamente.
- **Refeições a definir**: carrossel de opções de almoço/jantar por dia; o escolhido fica salvo.
- **Opcionais** do dia (acinzentados, fora da rota).
- **Documentos** (📄): seguro/carro/hotel por família, PDF renderizado dentro do app.
- **Dividir a conta** (🧮) estilo Splitwise com quem bebeu, câmbio ajustável e quem pagou; **Resumo** (💰) com acerto final.
- Anexos locais por parada (IndexedDB).

## Regras de conteúdo

- Idioma pt-BR; descrições curtas (1–3 frases) com dica prática (reserva, preço `$$`, distância do hotel).
- `time` em formato `~16h`, `13h – 14h30` (o motor interpreta `\d+h` para ordenar e para classificar Almoço/Jantar: ≥18h = Jantar).
- `hours` sempre com as 7 chaves `Seg Ter Qua Qui Sex Sáb Dom`; `st` = `ok | warn | nohr` e `stl` = texto do status (`ABERTO ✓`, `FECHADO`...). **Recalcular `st` conforme o dia da semana real da data** (erro clássico: dia da semana trocado → parada fechada no roteiro).
- Nunca colocar duas âncoras no mesmo horário; dias de vinícola com almoço incluso → restaurantes vão como `optional`, não como parada.
- Atrações combinadas com almoço (ex.: vinícola + restaurante) viram **cards distintos**.

Detalhes de campos em `references/schema.md`; tokens visuais em `references/design-system.md`; erros reais que custaram tempo em `references/lessons-learned.md`.
