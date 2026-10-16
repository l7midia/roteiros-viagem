# Lições aprendidas (do histórico real do projeto Mendoza)

Cada item é um erro que já aconteceu — evitar de saída.

## Dados
- **Fotos do Google Places expiram.** Os links quebraram em produção. Sempre baixar para `assets/photos/<slug>/N.jpg` e referenciar o caminho local.
- **Dia da semana errado = parada "aberta" que está fechada.** Conferir `date` com o calendário e reorganizar o roteiro por horário de funcionamento (houve commit inteiro só para corrigir isso).
- **Reserva confirmada manda.** Sincronizar `time` da parada com o horário da reserva e anexar o comprovante em `pinnedFiles`.
- **Combinações mal modeladas**: atração que inclui almoço (ex.: vinícola + restaurante do mesmo lugar) → dois cards distintos, senão o horário/mapa mentem.
- **Dia de translado** precisa de título/rota coerentes (houve rota apontando para o destino errado no dia da troca de hotel).
- **Opções de refeição**: em dia de almoço fixo na vinícola, restaurantes viram `optional`, não carrossel de "a definir" (removido dos dias 07/09 e 08/09 por confundir).
- **WhatsApp**: só dígitos com DDI; conferir cada número (9 estavam errados). Instagram sem `@`.
- **Substituições de atração** acontecem (Termas de Cacheuta → Bodega El Enemigo; Escala Humana → mirante Cristo Rey): manter o roteiro editável e rever horários vizinhos ao trocar.
- **Preços**: guardar com data da cotação (`info-fx`) e fonte (`info-fonte`); marcar "não confirmado" quando não houver resposta por escrito (ex.: política de bebês).

## Mapas
- Sem API key: usar **Leaflet + OpenStreetMap**. O provedor anterior exigia key e quebrou.
- Rotas = links externos (Google Maps / Waze), não rotas embutidas.

## Interface
- Header quebrava no mobile → reduzir fontes/gaps em ≤400px.
- Modais sobrepostos → `closeStackedModals()` antes de abrir outro.
- Dots do carrossel não atualizavam no mobile → função `updatePhotoScroll` precisa existir e ser chamada no scroll.
- Clique em anexo fixado não abria em alguns navegadores → abrir via handler dedicado, não `<a target=_blank>` dentro do sheet.
- PDF embutido borrado / só 1ª página → renderizar todas as páginas em alta resolução.
- Mascote do Waze: usar sprite recortado (`background-size:62px 18px; background-position:-43px 0`); a logomarca completa ficava cortada (7 commits para acertar).
- Dark mode: testar contraste de **todas** as etiquetas.

## Processo
- Publicar cedo no GitHub Pages e testar o link no celular; só então enviar a terceiros.
- `index.html` é o oficial; versões antigas (`v2.html`) podem coexistir, mas o link divulgado deve ser um só e estável.
- Estado do usuário é local ao aparelho — quem remarcar paradas num celular não vê no de outro.
- **Backup offline desde o início** (PDF/DOCX gerados do `DATA`), pois é o único arquivo do roteiro.
