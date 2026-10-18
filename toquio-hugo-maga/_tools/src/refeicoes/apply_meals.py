# -*- coding: utf-8 -*-
"""Aplica o resultado de build_meals.py ao index.html do app do Japão.
Uso: K=<chave> python apply_meals.py [--photos]   (--photos baixa as fotos; a chave vem de K e nunca é gravada)
- PLACES guarda cada lugar uma única vez; os dias só referenciam (lunchOptions / dinnerOptions / optMeals).
- Refeição sem lugar fixo -> carrossel 'a definir'; refeição já definida (reserva etc.) -> 'Opcionais do dia'."""
import io, json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meals_lib as L

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
RES = json.load(open(os.environ.get('MEALS_OUT', os.path.join(L.CACHE_DIR, 'meals_result.json')), encoding='utf-8'))
IG = {}
ig_file = os.path.join(L.CACHE_DIR, 'instagram.json')
if os.path.exists(ig_file):
    IG = json.load(open(ig_file, encoding='utf-8'))
html_path = os.path.join(ROOT, 'index.html')
html = open(html_path, encoding='utf-8').read()
m = re.search(r'const DATA=(\{.*?\});\n', html, re.S)
DATA = json.loads(m.group(1))
DO_PHOTOS = '--photos' in sys.argv
MAX_CARDS = int(os.environ.get('MAX_CARDS', '10'))   # máximo de opções por carrossel (as de maior nota)
PH_DIR = os.path.join(ROOT, 'assets', 'photos')
MEALKEY = {'almoço': 'lunchOptions', 'jantar': 'dinnerOptions'}


def _norm(x): return re.sub(r'[^a-z0-9]', '', L.slug(x))


def _same_place(a, b):
    """Mesmo restaurante com dois cadastros no Google: nome igual, ou um contido no outro (>=8 letras) a menos de 100 m."""
    na, nb = _norm(a['name']), _norm(b['name'])
    if na and na == nb: return True
    near = L.hav((a['lat'], a['lng']), (b['lat'], b['lng'])) < 100
    short, long_ = (na, nb) if len(na) <= len(nb) else (nb, na)
    return near and len(short) >= 8 and short in long_


def trim(cards, reserve=0):
    """Fica com as MAX_CARDS-reserve de maior nota (desempate: mais avaliações), sem cadastros duplicados, e reordena pela distância."""
    top = []
    for c in sorted(cards, key=lambda c: (-(c['place'].get('rating') or 0), -(c['place'].get('rcount') or 0))):
        if any(_same_place(c['place'], t['place']) for t in top): continue
        top.append(c)
        if len(top) >= MAX_CARDS - reserve: break
    return sorted(top, key=lambda c: c['d'])


def day_of(ph, lab): return [d for d in DATA[ph] if d['label'] == lab][0]


def photos_for(pid, place):
    from PIL import Image
    sl = (L.slug(place['name']) if re.search(r'[A-Za-z]', place['name']) else 'lugar')[:40] + '-' + pid[-6:].lower()
    out = []
    for i, nm in enumerate(place.get('photoNames') or [], 1):
        rel = 'assets/photos/%s/%d.jpg' % (sl, i)
        f = os.path.join(ROOT, rel)
        if not os.path.exists(f):
            if not DO_PHOTOS: continue
            os.makedirs(os.path.dirname(f), exist_ok=True)
            try:
                raw = urllib.request.urlopen('https://places.googleapis.com/v1/%s/media?maxWidthPx=720&key=%s' % (nm, L.K), timeout=40).read()
                im = Image.open(io.BytesIO(raw)).convert('RGB')
                im.save(f, 'JPEG', quality=74, optimize=True, progressive=True)
            except Exception as e:
                print('falha foto', sl, i, str(e).replace(L.K, '[CHAVE]')[:80]); continue
        out.append(rel)
    return out


# baixa as fotos em paralelo (3 por lugar, 720 px, JPEG recomprimido)
for s_ in RES['slots']:
    s_['cards'] = trim(s_['cards'], 1 if s_['mode'] == 'move' else 0)
uniq = {}
for s_ in RES['slots']:
    for c_ in s_['cards']:
        uniq.setdefault(c_['id'], c_['place'])
with ThreadPoolExecutor(12) as ex:
    PHOTO = dict(zip(uniq, ex.map(lambda kv: photos_for(*kv), uniq.items())))

PLACES = {}
fixed_removed = []
for s in RES['slots']:
    d = day_of(s['ph'], s['day'])
    meal, mode = s['meal'], s['mode']
    refs = []
    # lugar(es) que já estavam no roteiro
    if mode in ('move', 'convert'):
        lo, hi = (600, 870) if meal == 'almoço' else (1020, 1500)
        target = None
        for st in d['stops']:
            mm = re.search(r'(\d{1,2})h(\d{2})?', st.get('time') or '')
            t = int(mm.group(1)) * 60 + int(mm.group(2) or 0) if mm else None
            if mode == 'move' and s['moved'] and st['name'] == s['moved']: target = st; break
            if mode == 'convert' and t is not None and lo <= t < hi and (st.get('t') == 'lunch' or st.get('badge') in ('almoço', 'jantar')):
                target = st; break
        assert target, (s['day'], meal, mode)
        d['stops'].remove(target)
        fixed_removed.append((s['day'], meal, mode, target['name']))
        if mode == 'move':
            pid = 'rot-' + L.slug(target['name'])[:40]
            PLACES[pid] = {k: target[k] for k in ('name', 'lat', 'lng', 'gmaps', 'rating', 'rcount', 'hours', 'phone', 'website', 'ig', 'photos', 'desc', 'price') if target.get(k) is not None}
            PLACES[pid]['name'] = re.sub(r'^(Almoço|Jantar) — ', '', target['name'])
            PLACES[pid]['tita'] = True
            PLACES[pid]['tipo'] = 'Sugestão do roteiro'
            refs.append({'p': pid, 's': 1, 't': 1, 'd': 0})
        else:
            d.setdefault('mealNotes', {})[meal] = target['desc']
    d.setdefault('mealAnchors', {})[meal] = s['anchor']['name']
    for c in s['cards']:
        pl = dict(c['place'])
        pid = c['id']
        if pid not in PLACES:
            ph = PHOTO[pid]
            pl.pop('photoNames', None)
            if ph: pl['photos'] = ph
            if IG.get(pid): pl['ig'] = IG[pid]
            PLACES[pid] = {k: v for k, v in pl.items() if v not in (None, '', [])}
        ref = {'p': pid, 'd': c['d']}
        if c['t']: ref['t'] = 1
        refs.append(ref)
    refs.sort(key=lambda r: r['d'])
    if mode == 'stay':
        for r in refs: r['m'] = meal
        d.setdefault('optMeals', []).extend(refs)
    else:
        d[MEALKEY[meal]] = refs

new_data = json.dumps(DATA, ensure_ascii=False)
html = html[:m.start(1)] + new_data + html[m.end(1):]
places_line = 'const PLACES=' + json.dumps(PLACES, ensure_ascii=False, separators=(',', ':')) + ';\n'
if 'const PLACES=' in html:
    html = re.sub(r'const PLACES=\{.*?\};\n', lambda _: places_line, html, count=1, flags=re.S)
else:
    html = html.replace(new_data + ';\n', new_data + ';\n' + places_line, 1)
open(html_path, 'w', encoding='utf-8').write(html)
print('lugares únicos:', len(PLACES), '| cards:', sum(len(s['cards']) for s in RES['slots']), '| paradas removidas:')
for r in fixed_removed: print('  ', r)
print('fotos locais referenciadas:', sum(len(p.get('photos', [])) for p in PLACES.values()))
