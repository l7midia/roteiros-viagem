# Backup offline (PDF + DOCX)

Gerar a partir do `DATA` embutido — mais confiável que raspar o DOM.

## 1. Extrair o JSON

```python
import json
c = open('index.html', encoding='utf-8').read()
s = c.index('const DATA=') + len('const DATA=')
e = c.index('\n', s)
data = json.loads(c[s:e].rstrip(';'))   # {'p1': [...], 'p2': [...]}
```

## 2. PDF (Playwright/Chromium — funciona no ambiente cloud)

1. Gerar `roteiro_print.html` (capa + um bloco por dia, paradas com horário, descrição, link Maps, site, telefone, Instagram e horários por dia da semana; opções de almoço/jantar em subseção). CSS `@page { size: A4; margin: 22mm 18mm }`, serifa, dourado `#B8860B`.
2. Imprimir: `NODE_PATH=/opt/node22/lib/node_modules node` + `chromium.launch({executablePath:'/opt/pw-browsers/chromium'})` → `page.pdf({format:'A4', printBackground:true})`.

## 3. DOCX

`docx` (npm) não vem instalado: `npm install docx` numa pasta de trabalho. Estrutura: Título → Título de fase → Heading1 (data) → Heading2 (título do dia) → resumo + links → bloco por parada. Validar com `validate.py` da skill `docx`.

## Observações do ambiente cloud

- `soffice` (LibreOffice) **não converte nada** no container (falha até com .txt) e `pandoc`/`pdftoppm` não estão instalados → não depender deles para verificar. Validar o PDF por screenshot do HTML via Playwright.
- Salvar os arquivos finais na raiz do repo (ex.: `Roteiro-<Destino>-<MesAno>.pdf/.docx`), commitar e enviar ao usuário.
