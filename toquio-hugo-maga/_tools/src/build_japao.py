# -*- coding: utf-8 -*-
import json, re, sys, urllib.parse, importlib.util
sys.path.insert(0, '.')
import data_japao as D
import guia_japao as G

REPO = '/home/user/mendoza-roteiro-2026/'
t = open(REPO + '.claude/skills/roteiro-viagem-app/template/index.html', encoding='utf-8').read()


def R(a, b, n=1):
    global t
    assert t.count(a) == n, (a[:70], t.count(a))
    t = t.replace(a, b)


def between(start, end, new, keep_end=True):
    global t
    i = t.index(start)
    j = t.index(end, i)
    t = t[:i] + new + (t[j:] if keep_end else t[j + len(end):])


# ── dados
def maps_dir(origin, dest):
    return ("https://www.google.com/maps/dir/?api=1&travelmode=transit&origin=" + urllib.parse.quote(origin) +
            "&destination=" + urllib.parse.quote(dest))


ENR = json.load(open('enriched.json', encoding='utf-8'))
SRC_HOTELS = ENR['HOTELS']
OV = {
    "Kanda Matsuya, Kanda, Tokyo": dict(ig="kanda_matsuya"),
    "Tsuta Shinjuku, Tokyo": dict(ig="tsutajapanofficial"),
    "Mishima-tei Teramachi, Kyoto": dict(website="https://www.mishima-tei.co.jp/", ig="mishima_tei"),
    "Okonomimura, Hiroshima": dict(ig="okonomimura_official"),
    "Mouriya Honten, Kobe": dict(ig="kobebeef_mouriya"),
    "400°C Pizza Kagurazaka, Tokyo": dict(ig="kagurazaka400do"),
    "Yakiniku Ushigoro Ginza, Kirarito Ginza, Tokyo": dict(ig="ushigoro_yakiniku"),
    "Rare Tendon Ginza Mitsuyoshi, Tokyo": dict(ig="rare_ten_mitsuyoshi"),
    "Ginza Kyubey, Tokyo": dict(ig="ginza_kyubey"),
    "Universal Studios Japan, Osaka": dict(ig="universal_studios_japan"),
    "Super Nintendo World, Universal Studios Japan, Osaka": dict(ig="universal_studios_japan"),
    "teamLab Biovortex Kyoto": dict(ig="teamlabkyoto"),
    "Shibuya Sky, Tokyo": dict(ig="shibuya_sky"),
    "Umeda Sky Building, Osaka": dict(ig="umeda_skybuilding"),
}
PC = json.load(open('places_cache.json', encoding='utf-8'))
for k, h in SRC_HOTELS.items():
    p = PC[h['name'] + ', ' + h['addr']][0]
    h['website'] = p.get('websiteUri')
    h['phone'] = p.get('internationalPhoneNumber')
for _ph, _days in ENR['DATA'].items():
    for _d in _days:
        for _s in _d['stops'] + _d.get('optional', []):
            _s.update(OV.get(_s.get('q'), {}))
DATA = {}
for ph, days in ENR['DATA'].items():
    h = SRC_HOTELS[ph]
    hq = h['name'] + ', ' + h['addr']
    out = []
    for d in days:
        d = dict(d)
        g = d.pop('guide', None)
        dest_q = d.pop('dest_q', None)
        origin = d.get('origin') or hq
        d['origin'] = origin
        d['route'] = maps_dir(origin, dest_q or (d['stops'][0].get('q') if d['stops'] else hq))
        if g:
            d['guide'] = g
        d.setdefault('stops', [])
        out.append(d)
    DATA[ph] = out

# ── substituições de marcação
R('<title>{{VIAGEM}} · {{MES_ANO}}</title>', '<meta name="robots" content="noindex,nofollow">\n<title>Japão · Hugo &amp; Marília 2026</title>')
R('''    <button class="theme-btn" id="docsBtn" aria-label="Documentos da viagem">📄</button>
    <button class="theme-btn" id="summaryBtn" aria-label="Resumo da viagem">💰</button>
    <div class="logo">{{DESTINO}} <em>·</em> {{ANO}}</div>''',
  '''    <button class="theme-btn" id="docsBtn" aria-label="Guia da viagem">📖</button>
    <div class="logo">Japão <em>·</em> 2026</div>''')
R('<div class="pax">{{PAX}}</div>', '<div class="pax">Hugo &amp; Marília</div>')
between('<div class="ptabs">', '<div class="main" id="main">', '<div class="ptabs" id="ptabs"></div>\n')

# ── CSS
R('.ptabs{display:flex;background:var(--bg2);border-bottom:.5px solid var(--sep);flex-shrink:0}',
  '.ptabs{display:flex;overflow-x:auto;-webkit-overflow-scrolling:touch;scrollbar-width:none;background:var(--bg2);border-bottom:.5px solid var(--sep);flex-shrink:0}\n.ptabs::-webkit-scrollbar{display:none}')
R('.ptab{flex:1;padding:10px 8px;', '.ptab{flex:0 0 auto;white-space:nowrap;padding:10px 14px;')
R('.nbtn-gm{background:#1a73e8;color:#fff}',
  '.nbtn-gm{background:#1a73e8;color:#fff}\n.navbtns .nbtn{flex:1;justify-content:center;padding:12px 14px;font-size:14px}')
extra_css = '''
.ab.gm{background:#1a73e8;border-color:#1a73e8;color:#fff}
.b-templo{background:rgba(190,70,40,.1);color:#A83A1A}
html.dark .b-templo{background:rgba(230,120,80,.2);color:#F2B09A}
.hotelline{margin-top:12px;font-size:12.5px;color:var(--t2);line-height:1.5}
.hotelline a{color:var(--blue);text-decoration:none;font-weight:600}
.daybox{background:var(--bg2);padding:0 16px;border-top:.5px solid var(--sep)}
.dsec{border-bottom:.5px solid var(--sep)}
.dsec:last-child{border-bottom:none}
.dsec summary{padding:13px 0;font-size:13.5px;font-weight:700;color:var(--cr);cursor:pointer;list-style:none;touch-action:manipulation}
.dsec summary::-webkit-details-marker{display:none}
.dsec summary::after{content:"+";float:right;color:var(--t3);font-weight:500}
.dsec[open] summary::after{content:"–"}
.dsec ul{padding:0 0 12px 18px;font-size:13px;color:var(--t2);line-height:1.6}
.dsec li{margin-bottom:5px}
.dsec p{padding:0 0 10px;font-size:13px;color:var(--t2);line-height:1.6}
.dsec a{color:var(--blue);text-decoration:none}
.dsec.imp summary{color:#B26A00}
html.dark .dsec.imp summary{color:#F0B050}
'''
R('</style>\n</head>', extra_css + '</style>\n</head>')

# ── JS: constantes e hotéis
R('const BC={famosa:"b-famous",',
  'const BC={passeio:"b-montanha",templo:"b-templo",natureza:"b-boutique",transporte:"b-cidade",ingresso:"b-famous",famosa:"b-famous",')
hot = {k: dict(name=v['name'], addr=v['addr'], din=v['din'], dout=v['dout'], gmaps=v.get('gmaps'), lat=v.get('lat'), lng=v.get('lng')) for k, v in SRC_HOTELS.items()}
between('const HOTELS={', '// ─── Roteiro: status', 'const HOTELS=' + json.dumps(hot, ensure_ascii=False) + ';\nconst PHASES=' + json.dumps(D.PHASES, ensure_ascii=False) + ';\n\n')
R('const PHASE_NAME={p1:"{{FASE_1}}",p2:"{{FASE_2}}"};', 'const PHASE_NAME=Object.fromEntries(PHASES.map(([k,l])=>[k,l.replace(/^\\S+\\s+/,"")]));')

# rota (transporte público, somente Google Maps)
between('// Regenera os links de rota (Google Maps/Waze)', '// Reordena as paradas do dia',
'''// Regenera o link de rota do dia (Google Maps, transporte público) a partir da primeira parada atual.
function mapsDirUrl(o,d){ return "https://www.google.com/maps/dir/?api=1&travelmode=transit&origin="+encodeURIComponent(o)+"&destination="+encodeURIComponent(d); }
function rebuildRouteUrl(day,phase){
  const first=(day.stops||[]).find(s=>s.q);
  if(!first) return;
  const h=HOTELS[phase];
  day.route=mapsDirUrl(day.origin||(h?h.name+", "+h.addr:""),first.q);
}

''')

# initMap: sem coordenadas, o mapa fica oculto
R('  const pts=stops.filter(s=>s.lat&&s.lng);\n  if(!pts.length){', '  const pts=stops.filter(s=>s.lat&&s.lng);\n  if(!pts.length||!HOTELS[phase]||HOTELS[phase].lat==null){')
R('  const isHotelFirst=pts.length>0&&Math.abs(pts[0].lat-hotel.lat)<0.005&&Math.abs(pts[0].lng-hotel.lng)<0.005;',
  '  const hotelPerto=Math.abs(pts[0].lat-hotel.lat)<0.5&&Math.abs(pts[0].lng-hotel.lng)<0.5;\n  const isHotelFirst=!hotelPerto||(Math.abs(pts[0].lat-hotel.lat)<0.005&&Math.abs(pts[0].lng-hotel.lng)<0.005);')

R('  const el=document.getElementById("day-map");\n  if(!el) return;', '  const el=document.getElementById("day-map");\n  if(!el) return;\n  if(typeof L==="undefined"){el.parentElement.style.display="none";return;}')

# ── renderDay: um único botão Google Maps + hotel + painel do dia
between('  let navH="";', '  const stops=day.stops||[];',
'''  let navH="";
  if(day.route) navH=`<div class="navbtns"><a class="nbtn nbtn-gm" href="${eu(day.route)}">${LOGO.gm} Google Maps</a></div>`;
  const hh=HOTELS[ph];
  const hotelH=hh?`<div class="hotelline">🏨 <a href="${eu(hh.gmaps||("https://www.google.com/maps/search/?api=1&query="+encodeURIComponent(hh.name+", "+hh.addr)))}">${et(hh.name)}</a> · check-in ${hh.din} · check-out ${hh.dout}</div>`:"";
  const g=day.guide||{};
  const lst=a=>"<ul>"+a.map(x=>"<li>"+et(x)+"</li>").join("")+"</ul>";
  let boxH="";
  if(g.importante&&g.importante.length) boxH+=`<details class="dsec imp" open><summary>📌 Importante</summary>${lst(g.importante)}</details>`;
  if(g.locomover&&g.locomover.length) boxH+=`<details class="dsec"><summary>🚆 Como se locomover</summary>${lst(g.locomover)}</details>`;
  if(g.comer&&g.comer.length) boxH+=`<details class="dsec"><summary>🍜 Onde comer</summary>${lst(g.comer)}</details>`;
  if(g.dica) boxH+=`<details class="dsec"><summary>💡 Dica</summary><p>${et(g.dica)}</p></details>`;
  if(boxH) boxH=`<div class="daybox">${boxH}</div>`;

''', keep_end=True)
R('      ${navH}\n    </div>\n    ${mapH}', '      ${navH}${hotelH}\n    </div>\n    ${boxH}\n    ${mapH}')

# ── ficha da parada: ações (só Google Maps; sem Waze/WhatsApp/dividir conta)
between('  // action buttons — use eu() for all URLs', '  if(s.infoImportante){',
'''  // action buttons — use eu() for all URLs, NO target=_blank (iOS deep links need direct navigation)
  const mq=s.q?encodeURIComponent(s.q):"";
  let actsMain="", actsSpecial="";
  if(s.gmaps||s.q) actsMain+=`<a class="ab gm" href="${eu(s.gmaps||("https://www.google.com/maps/search/?api=1&query="+mq))}">${LOGO.gm} Ver no Google Maps</a>`;
  if(s.q)       actsMain+=`<a class="ab ap" href="https://www.google.com/maps/dir/?api=1&amp;travelmode=transit&amp;destination=${mq}">🚆 Como chegar</a>`;
  if(s.website) actsMain+=`<a class="ab ap" href="${eu(s.website)}">🌐 Site oficial</a>`;
  if(s.ig)      actsMain+=`<a class="ab ig" href="https://www.instagram.com/${eu(s.ig)}/">${LOGO.ig} Instagram</a>`;
  if(s.phone)   actsMain+=`<a class="ab ap" href="tel:${eu(s.phone)}">📞 ${et(s.phone)}</a>`;

''', keep_end=True)

# ── remover Resumo/💰; Documentos → Guia
R('''document.getElementById("summaryBtn").addEventListener("click",function(){
  closeStackedModals();
  renderSummary();
  document.getElementById("summaryModal").classList.add("open");
});
''', '')
R('''document.getElementById("docsBtn").addEventListener("click",function(){
  closeStackedModals();
  renderDocsModal();
  document.getElementById("docsModal").classList.add("open");
});''',
  '''const GUIDE_HTML=%s;
document.getElementById("docsBtn").addEventListener("click",function(){
  closeStackedModals();
  document.getElementById("infoTitle").textContent="📖 Guia da viagem";
  document.getElementById("infoBody").innerHTML=GUIDE_HTML;
  document.getElementById("infoModal").classList.add("open");
});''' % json.dumps(G.build(SRC_HOTELS), ensure_ascii=False).replace('</', '<\\/'))

# ── abas dinâmicas
between('function setPhase(p){', '\nfunction setDay(i){',
'''function buildTabs(){
  const el=document.getElementById("ptabs");
  el.innerHTML=PHASES.map(([k,l],i)=>`<button class="ptab${i===0?" a":""}" id="tab-${k}">${et(l)}</button>`).join("");
  PHASES.forEach(([k])=>onTap(document.getElementById("tab-"+k),()=>setPhase(k)));
}
function setPhase(p){
  ph=p; di=0;
  PHASES.forEach(([k])=>{
    const b=document.getElementById("tab-"+k);
    b.classList.toggle("a",k===p);
    if(k===p) b.scrollIntoView({behavior:"smooth",block:"nearest",inline:"center"});
  });
  renderDay();
}
''')
R('// ─── init ──────────────────────────────────────────────────────────────────\nrenderDay();',
  '// ─── init ──────────────────────────────────────────────────────────────────\nbuildTabs();\nrenderDay();')

# ── identificadores / moeda
t = t.replace('{{SLUG}}', 'toquio-hugo-maga')
R('{{MOEDA_LOCAL}}', 'JPY')
R('{{LOCALE}}', 'ja-JP')

# ── dados
lines = t.split('\n')
idx = [i for i, l in enumerate(lines) if l.startswith('const DATA=')]
assert len(idx) == 1
lines[idx[0]] = 'const DATA=' + json.dumps(DATA, ensure_ascii=False) + ';'
t = '\n'.join(lines)

assert '{{' not in t, re.findall(r'\{\{[A-Z_0-9]+\}\}', t)
open(REPO + 'toquio-hugo-maga/index.html', 'w', encoding='utf-8').write(t)
print('ok', len(t))
