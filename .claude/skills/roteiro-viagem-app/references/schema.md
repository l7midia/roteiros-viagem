# Schema de dados do app

Tudo vive em `const DATA = { p1: [dia, ...], p2: [dia, ...] }` (uma única linha JSON no `index.html`, linha ~470). Os campos abaixo foram extraídos do app Mendoza.

## Dia

| Campo | Tipo | Obrigatório | Notas |
|---|---|---|---|
| `label` | string `DD/MM` | sim | Chave do dia (usada em estado, remarcação, refeições). **Único dentro da fase.** Um dia de troca de hotel aparece nas duas fases (ex.: `09/09`). |
| `date` | string | sim | `"Domingo, 6 set"` — conferir dia da semana com o calendário real. |
| `title` | string | sim | Curto, com `—` ou `+` para combinar atrações. |
| `sub` | string | não | 1 frase de resumo do dia. |
| `route` | URL | sim | Google Maps Directions. Recalculada pelo motor ao remarcar paradas. |
| `waze` | URL | sim | `https://waze.com/ul?ll=<lat>,<lng>&navigate=yes` |
| `stops` | Parada[] | sim | Roteiro do dia (aparece na rota/mapa). |
| `lunchOptions` | Parada[] | não | Opções de almoço (carrossel "a definir"). |
| `dinnerOptions` | Parada[] | não | Opções de jantar. |
| `optional` | Parada[] | não | Opcionais fora da rota (acinzentados). Nos dias de almoço fixo, restaurantes de vinícola vão aqui. |

## Parada (stops / lunchOptions / dinnerOptions / optional)

| Campo | Tipo | Notas |
|---|---|---|
| `t` | `hotel\|famous\|boutique\|lunch\|dinner\|city\|mountain` | Tipo → cor do marcador (`TC`). |
| `badge` | `hotel\|famosa\|boutique\|almoço\|almoco\|jantar\|cidade\|montanha` | Texto/cor da etiqueta (`BC`). `almoco`/`almoço` ativa o destaque "Almoço/Jantar". |
| `time` | string | `~16h`, `13h – 14h30`. O motor lê o primeiro `\d+h` p/ ordenar; ≥18h = Jantar. |
| `name` | string | |
| `desc` | string | 1–3 frases com dica prática. |
| `lat`, `lng` | number | Obrigatórios p/ mapa/rota. |
| `hrs` | string | Resumo do horário do dia (`Dom: 9h–0h`, `24h (hotel)`). |
| `hours` | `{Seg..Dom: string}` | 7 chaves exatas: `Seg Ter Qua Qui Sex Sáb Dom`; fechado = `"FECHADO"`. |
| `st` | `ok\|warn\|nohr` | `ok` verde, `warn` amarelo (fecha cedo/atenção), `nohr` sem horário. |
| `stl` | string | Texto do status: `ABERTO`, `ABERTO ✓`, `FECHADO`… |
| `rating`, `rcount` | number | Nota Google e nº de avaliações. |
| `photos` | string[] | Caminhos locais `assets/photos/<slug>/N.jpg` (3–5). |
| `menuPhotos` | string[] | Fotos de cardápio (lightbox); vazio → botão de cardápio vira link do site. |
| `hasMenu` | bool | Mostra botão de cardápio. |
| `website`, `gmaps` | URL | `gmaps` = `https://maps.google.com/?cid=…`. |
| `phone`, `wa`, `ig` | string | `wa` só dígitos com DDI (`5492613996400`); `ig` sem `@`. |
| `price` | string | `~USD 50–80`, faixa `$$`. |
| `michelin` | `("star"\|"green"\|"reco")[]` | Tags ★ MICHELIN / 🌿 VERDE / ✦ RECOMENDADO. |
| `destaque` | bool | Realce visual do card. |
| `pinnedFiles` | `{label,url}[]` | Comprovantes/reservas fixados no sheet (ex.: `assets/reservas/x.jpeg`). |
| `infoImportante` | HTML | Painel "Informações importantes" (preços de menu, política de bebês, reserva). Classes: `info-panel`, `info-fx`, `info-fonte`, `info-items > info-item(name/desc/price)`, `info-extras > info-extra`. Informar cotação com a data. |

## Documentos

```js
const DOCS=[
  {cat:"🛡️ Seguro Viagem", groups:[
    {fam:"Família A", files:[{label:"Seguro — Fulano", url:"assets/docs/seguro-fulano.pdf"}]}
  ]},
  {cat:"🚗 Carro", groups:[...]},
  {cat:"🏨 Hotéis", groups:[...]}
];
```

## Estado do usuário (não vai em DATA)

- `localStorage["{{SLUG}}-plan"]` → `{status, moves, meals, splits, fx}`: realizado/pendente, remarcações, refeição escolhida por dia, contas divididas, câmbio.
- IndexedDB `{{SLUG}}-files` (store `files`, índice `sk` = `fase||dia||parada`): anexos que o usuário adiciona no aparelho.
- Consequência: estado é **por aparelho/navegador**; trocar de celular zera. Avisar o usuário.

## Constantes fora de DATA

- `HOTELS = {p1:{lat,lng}, p2:{lat,lng}}` — origem das rotas e ponto-base do mapa.
- `PHASE_NAME` — nomes das fases usados em modais de remarcação.
- `SPLIT_PEOPLE = [["chave","Nome"],...]`, `CUR`, `FOREIGN` (moedas com câmbio ajustável).
- `TC`/`BC`/`SC` — cores por tipo, etiquetas e status.
