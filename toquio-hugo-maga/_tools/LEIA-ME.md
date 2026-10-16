# App do Japão (Hugo & Marília) — passagem de bastão

Repositório: `l7midia/roteiros-viagem` (antigo `mendoza-roteiro-2026`). Branch de trabalho: `claude/web-app-v2-link-4l6moc`.
App: `toquio-hugo-maga/index.html` (arquivo único, sem build). Link do casal: https://l7midia.github.io/roteiros-viagem/toquio-hugo-maga/
Mendoza: https://l7midia.github.io/roteiros-viagem/mendoza.html (o `v2.html` antigo redireciona).

## Estado
- **No ar (master, PR #1):** versão v1 com roteiro de 20 dias, 6 abas, guia da viagem, botão único do Google Maps (transporte público).
- **Só na branch, ainda sem merge:** dados do Google Places (coordenadas, nota, horários, telefone), mapa do dia, avisos de dia fechado, sites e Instagram verificados, hotéis com site/telefone, ferramenta de fotos.
- **Falta:** fotos (174 em 58 lugares), merge na master, decisões abaixo.

## 1. Fotos (precisa do seu computador: a nuvem bloqueia `lh3.googleusercontent.com`)
Pré-requisito: chave da Google Places API (projeto com faturamento ativo e **Places API (New)** ativada).

```bash
git clone https://github.com/l7midia/roteiros-viagem.git && cd roteiros-viagem
git checkout claude/web-app-v2-link-4l6moc
export GOOGLE_PLACES_API_KEY='SUA_CHAVE'        # PowerShell:  $env:GOOGLE_PLACES_API_KEY='SUA_CHAVE'
python3 toquio-hugo-maga/_tools/fetch_photos.py
```
Esperado: `lugares com foto: 58 | paradas atualizadas: ~65 | falhas: 0`. O script grava JPGs em `toquio-hugo-maga/assets/photos/<lugar>/N.jpg` (720px) e preenche `photos` no `DATA` do `index.html`. Se houver falhas, rode de novo (ele pula o que já baixou).

Teste local: `cd toquio-hugo-maga && python3 -m http.server 8000` e abra `http://localhost:8000` no navegador (modo celular). Confira o carrossel de fotos na ficha de uma parada.

Depois: `git add toquio-hugo-maga && git commit -m "Add place photos to Japan app" && git push`.
**Nunca** grave a chave em arquivo nem em commit (o repositório é público).

## 2. Publicar
Abra PR da branch para `master` e faça o merge (o Pages publica em 1–2 min). Depois abra no celular: o link do Japão e o do Mendoza (`/mendoza.html`).

## 3. Decisões pendentes (levar para quem revisa o roteiro)
1. **19/10 (segunda), jantar no Kanda Matsuya 20h:** fechado às segundas (Google e Instagram do restaurante). Trocar? (o PDF cita Ichiran Akihabara).
2. **21/10 (quarta), almoço no Tsuta:** fechado às quartas; fica em Yoyogi-Uehara, não em Shinjuku. Trocar? (alternativa do PDF: Gyukatsu Motomura).
3. **29/10, saída de Hiroshima:** sair 9h20 não fecha com o Shinkansen das 10h03 (bonde 20–25 min + estar nas catracas 20 min antes). Sugerido sair ~8h50 ou ir de táxi.
4. **24/10, Shoraian "jantar" 17h30:** Google mostra funcionamento até 19h; reserva a confirmar; Bosque de Bambu às 19h30.
5. Reservas em aberto: Sushi Tokyo Ten (21/10), Shoraian (24/10), Mishima-tei (25/10), Mouriya Honten (01/11), 400°C Pizza (02/11); Shibuya Sky (20/10) sem ingresso; jantar do ryokan (22/10) a confirmar.
6. Horários que eu estimei (marcados com `~`): Chureito ~9h15, chegada à Universal ~9h, almoço na Universal ~12h30, Halloween ~19h, jantar em Umeda ~18h30.

Para aplicar uma troca: edite a parada no `DATA` (linha única `const DATA=...` do `index.html`) ou em `_tools/src/data_japao.py` e rode o `build_japao.py` (ajuste os caminhos absolutos no topo dele).

## 4. Pendências de conteúdo
- Anexar comprovantes de hotel e reservas (PDF) — o app aceita anexos por parada ("Reservas & Ingressos"); lembrar o Rafael.
- Instagram de Daikokuya, Ichiran, Sushi Tokyo Ten (só Roppongi), Shoraian e Mizuno: não achados. Menchirashi: o perfil do PDF é de food truck, removido. Ten Yokota Asue: perfil vem do cadastro do Google, não confirmado por busca.
- Links do PDF descartados por suspeita: Gyukatsu Motomura, Daikokuya (Instagram de Shibuya), Mizuno e Harukoma (instagram.com/popular/...), Kushikatsu Daruma (domínio .pt).
- Crédito das fotos: os termos do Google pedem atribuição; avaliar uma linha "Fotos: Google Maps" no Guia.

## 5. Segurança e privacidade
- Chave colada no chat da sessão anterior: **restringir** (só Places API) ou **trocar** depois da viagem. Definir cota diária da Places API (ex.: 1.000/dia) em APIs e serviços → Cotas.
- App com `noindex`; sem códigos de reserva, nomes de reserva nem números de voo. Link só para o casal.
- Orçamento no Google Cloud só alerta; quem limita gasto é a cota.

## 6. Fontes no repositório
`_tools/src/`: `data_japao.py` (roteiro do PDF), `guia_japao.py` (guia), `build_japao.py` (monta o app a partir do template da skill), `enrich_search.py` / `enrich_apply.py` (Places), `places_cache.json` (respostas do Places), `link_labels.json` (links do PDF). Skill reutilizável: `.claude/skills/roteiro-viagem-app/` (com `references/variante-multifase-transporte-publico.md`).
