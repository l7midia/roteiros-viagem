# -*- coding: utf-8 -*-
"""Aplica ao index.html as mudanças de código dos carrosséis de refeição (idempotente)."""
import os, re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
p = os.path.join(ROOT, 'index.html')
s = open(p, encoding='utf-8').read()
if 'function expandMeals' in s:
    print('já aplicado'); raise SystemExit


def rep(old, new, count=1):
    global s
    assert s.count(old) >= 1, 'não achei: ' + old[:70]
    s = s.replace(old, new) if count == 0 else s.replace(old, new, count)


# 1) janela do almoço (11h50) cai na seção "Tarde"
rep('''  const h=parseInt(m[1]);
  return h>=18?"Noite":h>=12?"Tarde":"Manhã";''', '''  const h=parseInt(m[1]);
  const mi=(t.match(/~?\\d+h(\\d{2})/)||[0,"0"])[1];
  return h>=18?"Noite":(h*60+parseInt(mi)>=11*60+45)?"Tarde":"Manhã";''')

# 2) selo "Sugestão da Tita"
rep('''  if(o.destaque) t.push('<span class="mc-tag t-dest">★ DESTAQUE</span>');''',
    '''  if(o.destaque) t.push('<span class="mc-tag t-dest">★ DESTAQUE</span>');
  if(o.tita) t.push('<span class="mc-tag t-tita">SUGESTÃO DA TITA</span>');''')
rep('.mc-tag.t-dest{background:var(--gold);color:#fff}', '.mc-tag.t-dest{background:var(--gold);color:#fff}\n.mc-tag.t-tita{background:#7A1F2B;color:#fff}')

# 3) cards: imagem com carregamento tardio + distância
rep('''<div class="mc-img"${ph0?` style="background-image:url('${ph0}')"`:""}>''', '''<div class="mc-img"${ph0?` data-bg="${ph0}"`:""}>''', 0)
rep('<div class="mc-meta">${et(o.hrs||"")}</div>', '<div class="mc-meta">${o.dist?et(o.dist)+" · ":""}${et(o.hrs||"")}</div>')
rep('<div class="mc-meta">${et(s.hrs||"")}</div>', '<div class="mc-meta">${s.dist?et(s.dist)+" · ":""}${et(s.hrs||"")}</div>')

# 4) nota do bloco "a definir"
rep('''    <div class="meal-note">Sugestões próximas — não entram no mapa nem na rota. Toque para ver detalhes e escolher.</div>''',
    '''    ${(day.mealNotes||{})[it.meal]?`<div class="meal-note">${et(day.mealNotes[it.meal])}</div>`:""}
    <div class="meal-note">Opções ordenadas pela distância em linha reta${(day.mealAnchors||{})[it.meal]?" até "+et(day.mealAnchors[it.meal]):""} — não entram no mapa nem na rota. Toque para ver detalhes e escolher.</div>''')

# 5) opcionais de refeição: um carrossel por refeição, com rótulo correto
i0 = s.index('    if(optMeal.length){')
i1 = s.index("      optH+='</div>';\n    }\n  }\n", i0) + len("      optH+='</div>';\n    }\n")
block = s[i0:i1]
new_block = '''    if(optMeal.length){
      ["almoço","jantar"].forEach(mk=>{
        const grp=optMeal.filter(x=>(x.s.meal||(mealKind(x.s.time)==="Jantar"?"jantar":"almoço"))===mk);
        if(!grp.length) return;
        const an=(day.mealAnchors||{})[mk];
        optH+=`<div class="opt-note" style="padding-top:2px">Opções de restaurantes (${mk}) — ordenadas pela distância em linha reta${an?" até "+et(an):""}; não entram no mapa nem na rota.</div><div class="meal-car">`;
        grp.forEach(({s,i})=>{
          const ph0=s.photos&&s.photos[0]?s.photos[0]:"";
          optH+=`<button class="mc-card" data-opt-idx="${i}">
          <div class="mc-img"${ph0?` data-bg="${ph0}"`:""}>
            ${s.rating?`<div class="mc-rate">★ ${s.rating}<span>(${Number(s.rcount||0).toLocaleString("pt-BR")})</span></div>`:""}
            ${tagsHtml(s)}
          </div>
          <div class="mc-body">
            <div class="mc-name">${et(s.name)}</div>
            <div class="mc-meta">${s.dist?et(s.dist)+" · ":""}${et(s.hrs||"")}</div>
            ${s.price?`<div class="mc-price">${et(s.price)}</div>`:""}
          </div>
        </button>`;
        });
        optH+='</div>';
      });
    }
'''
s = s[:i0] + new_block + s[i1:]

# 6) expansão das referências + carregamento tardio das imagens
helpers = '''// ─── Opções de refeição: PLACES guarda cada lugar uma vez; os dias só referenciam ───────────────────────────
const MEAL_WIN={"almoço":"11h50 – 14h","jantar":"18h30 – 20h30"};
const HKEYS=["Seg","Ter","Qua","Qui","Sex","Sáb","Dom"];
function fmtDist(m){ return m<1000?(Math.round(m/10)*10)+" m":(m/1000).toFixed(1).replace(".",",")+" km"; }
function expandMeals(){
  const mk=(r,meal,day)=>{
    const b=PLACES[r.p]; if(!b) return null;
    const dm=day.label.split("/").map(Number);
    const wd=(new Date(2026,dm[1]-1,dm[0]).getDay()+6)%7;
    const hv=b.hours?b.hours[HKEYS[wd]]:"";
    const an=(day.mealAnchors||{})[meal]||"";
    const o=Object.assign({},b,{time:MEAL_WIN[meal],badge:meal,t:"lunch",meal:meal,tita:!!(b.tita||r.t),
      hrs:hv?HKEYS[wd]+": "+hv:"",dist:r.s?"do roteiro":fmtDist(r.d)});
    if(!o.desc) o.desc=(b.tipo||"Restaurante")+". A "+fmtDist(r.d)+" em linha reta de "+an+". "+(b.addr||"");
    return o;
  };
  for(const p in DATA) DATA[p].forEach(d=>{
    [["lunchOptions","almoço"],["dinnerOptions","jantar"]].forEach(([k,meal])=>{
      if(d[k]) d[k]=d[k].map(r=>mk(r,meal,d)).filter(Boolean);
    });
    if(d.optMeals){ d.optional=(d.optional||[]).concat(d.optMeals.map(r=>mk(r,r.m,d)).filter(Boolean)); delete d.optMeals; }
  });
}
function lazyBg(root){
  const els=[...root.querySelectorAll(".mc-img[data-bg]")];
  const set=e=>{ e.style.backgroundImage="url('"+e.dataset.bg+"')"; e.removeAttribute("data-bg"); };
  if(!("IntersectionObserver" in window)){ els.forEach(set); return; }
  const io=new IntersectionObserver(es=>es.forEach(en=>{ if(en.isIntersecting){ set(en.target); io.unobserve(en.target); } }),{rootMargin:"200px"});
  els.forEach(e=>io.observe(e));
}
'''
rep('assignIds();\n', helpers + 'expandMeals();\nassignIds();\n')
rep('  cont.querySelectorAll(".mc-card[data-mi]")', '  lazyBg(cont);\n  cont.querySelectorAll(".mc-card[data-mi]")')
open(p, 'w', encoding='utf-8').write(s)
print('código do app atualizado')
