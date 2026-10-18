# -*- coding: utf-8 -*-
"""Monta os carrosséis de refeição (a definir / opcionais) do app do Japão.
Uso: K=<chave> python build_meals.py   (a chave vem da variável de ambiente K e nunca é gravada)
Regras: raio <= 5 km da âncora, nota > 4,5 (>= 4,6), > 50 avaliações, aberto >= 60 min na janela
(almoço 11h50-14h, jantar 18h30-20h30) no dia da semana da data; ordenado pela distância da âncora.
Sugestões da Tita (PDF) entram se estiverem abertas na janela e a <= 5 km, mesmo abaixo da nota."""
import datetime, json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meals_lib as L
from tita_lists import TITA

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
OUT = os.environ.get('MEALS_OUT', os.path.join(L.CACHE_DIR, 'meals_result.json'))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
DATA = json.loads(re.search(r'const DATA=(\{.*?\});\n', html, re.S).group(1))
HOTELS = json.loads(re.search(r'const HOTELS=(\{.*?\});\n', html, re.S).group(1))

SKIP_DAYS = {'16/10', '17/10', '05/11', '31/10'}
NO_LUNCH = {'18/10'}
NO_DINNER = {'22/10'}
STAY = {('19/10', 'jantar'), ('20/10', 'jantar'), ('03/11', 'jantar'), ('04/11', 'almoço'), ('02/11', 'almoço'),
        ('27/10', 'almoço'), ('24/10', 'jantar'), ('26/10', 'almoço'), ('29/10', 'jantar'), ('01/11', 'almoço')}
MOVE = {('18/10', 'jantar'): 'Ginza Kagari', ('19/10', 'almoço'): 'Daikokuya', ('20/10', 'almoço'): 'Menchirashi',
        ('30/10', 'almoço'): 'Mizuno', ('02/11', 'jantar'): 'Ten Yokota Asue', ('04/11', 'jantar'): 'Ginza Kyubey'}
CONVERT = {('23/10', 'jantar'), ('24/10', 'almoço'), ('25/10', 'almoço'), ('25/10', 'jantar'), ('26/10', 'jantar'),
           ('27/10', 'jantar'), ('28/10', 'almoço'), ('30/10', 'jantar'), ('01/11', 'jantar'), ('03/11', 'almoço')}
# parte do nome da parada usada como âncora quando a refeição já tem parada própria (STAY)
ANCHOR_STOP_KEY = {
    ('19/10', 'jantar'): 'Kappabashi', ('20/10', 'jantar'): 'Shibuya Sky', ('03/11', 'jantar'): 'Nezu',
    ('04/11', 'almoço'): 'Rare Tendon', ('02/11', 'almoço'): '400', ('27/10', 'almoço'): 'Okonomimura',
    ('24/10', 'jantar'): 'Shoraian', ('26/10', 'almoço'): 'Nara', ('29/10', 'jantar'): 'Dotonbori', ('01/11', 'almoço'): 'Kobe'}
BASE_Q = ["restaurant", "sushi", "ramen", "tempura", "udon soba", "tonkatsu", "yakiniku", "izakaya", "okonomiyaki",
          "kaiseki", "unagi eel", "yakitori", "gyukatsu beef cutlet", "seafood", "curry", "teishoku set lunch"]
EXTRA_Q = {'kyoto': ["yudofu tofu", "obanzai", "kyoto cuisine"], 'osaka': ["takoyaki", "kushikatsu", "kitsune udon"],
           'hiroshima': ["oyster", "anago conger eel", "hiroshima okonomiyaki"], 'nara': ["kakinoha sushi", "kamameshi", "soba"],
           'kobe': ["kobe beef steak", "teppanyaki"], 'fuji': ["houtou noodles", "trout", "soba"],
           'tokyo': ["monjayaki", "soba", "tendon"]}


def city_of(lat, lng):
    if 138 < lng < 139.0: return 'fuji'
    if lng > 139: return 'tokyo'
    if lat > 34.85 and 135.5 < lng < 136.0: return 'kyoto'
    if lat < 34.8 and lng > 135.7: return 'nara'
    if lat < 34.8 and 135.4 < lng < 135.7: return 'osaka'
    if 135.1 < lng < 135.4: return 'kobe'
    return 'hiroshima'


# rótulo da âncora mostrado no app (a coordenada continua sendo a da parada)
LABEL = {('19/10', 'jantar'): 'Kappabashi / Ueno / Akihabara', ('20/10', 'jantar'): 'Shibuya Sky', ('24/10', 'jantar'): 'Shoraian',
         ('24/10', 'almoço'): 'Arashiyama', ('25/10', 'almoço'): 'Mercado Nishiki', ('25/10', 'jantar'): 'Estação de Kyoto',
         ('23/10', 'almoço'): 'Estação de Kyoto', ('26/10', 'almoço'): 'Nara', ('27/10', 'almoço'): 'Okonomimura',
         ('01/11', 'almoço'): 'Mouriya Honten (Kobe)', ('03/11', 'jantar'): 'Santuário Nezu / Ueno', ('04/11', 'almoço'): 'Rare Tendon'}


def dday(label):
    d, m = [int(x) for x in label.split('/')]
    return datetime.date(2026, m, d)


def has_latin(s): return bool(re.search(r'[A-Za-z]', s or ''))


def norm(s): return re.sub(r'[^a-z0-9]+', '', L.slug(s))


def stop_by_key(day, key):
    for s in day['stops']:
        if key in s['name'] and 'lat' in s: return s
    return None


def attraction_anchor(day, win):
    st = []
    for s in day['stops']:
        m = re.search(r'(\d{1,2})h(\d{2})?', s.get('time') or '')
        if m and 'lat' in s and not (s.get('t') == 'lunch' or s.get('badge') in ('almoço', 'jantar')):
            st.append((int(m.group(1)) * 60 + int(m.group(2) or 0), s))
    inw = [x for x in st if win[0] <= x[0] < win[1]]
    if inw: return inw[0][1]
    before = [x for x in st if x[0] < win[0]]
    if before: return before[-1][1]
    after = [x for x in st if x[0] >= win[1]]
    return after[0][1] if after else None


def day_hours(p):
    """horários 24h por dia (Seg..Dom) a partir de regularOpeningHours.periods (independente de idioma)."""
    per = (p.get('regularOpeningHours') or {}).get('periods') or []
    if not per: return None
    if len(per) == 1 and 'close' not in per[0]: return {k: '24h' for k in L.KEYS}
    by = {i: [] for i in range(7)}
    for x in per:
        o, c = x.get('open'), x.get('close')
        if o and c: by[o['day']].append((o.get('hour', 0) * 60 + o.get('minute', 0), c.get('hour', 0) * 60 + c.get('minute', 0)))
    out = {}
    for i, k in enumerate(L.KEYS):
        iv = sorted(by[(i + 1) % 7])
        out[k] = ', '.join('%02d:%02d – %02d:%02d' % (a // 60, a % 60, (b // 60) % 24, b % 60) for a, b in iv) if iv else 'FECHADO'
    return out


def to_place(p, tita=False):
    return {"name": p['displayName']['text'], "lat": round(p['location']['latitude'], 6), "lng": round(p['location']['longitude'], 6),
            "gmaps": p.get('googleMapsUri'), "rating": p.get('rating'), "rcount": p.get('userRatingCount'), "hours": day_hours(p),
            "phone": p.get('internationalPhoneNumber'), "website": p.get('websiteUri'),
            "addr": p.get('shortFormattedAddress') or p.get('formattedAddress'), "tipo": L.tipo_pt(p),
            "photoNames": [x['name'] for x in (p.get('photos') or [])[:3]], "tita": bool(tita)}


# ── Sugestões da Tita: resolve cada nome (todas as filiais) por cidade ──────────────────────────
CITY_C = {'tokyo': (35.68, 139.76), 'kyoto': (35.01, 135.76), 'osaka': (34.68, 135.50)}
tita_pool = {}
for city, names in TITA.items():
    lat, lng = CITY_C[city]
    pool = {}

    def find(nm, lat=lat, lng=lng, city=city):
        brand = re.split(r'\s[-–—]\s', nm)[0].strip()
        toks = [t for t in L.slug(brand).split('-') if len(t) > 1][:3]
        res = []
        for p in L.text_search(brand + ' ' + city, lat, lng, 30000, None, 1):
            n = norm(p['displayName']['text'])
            if toks and all(t in n for t in toks[:2]):
                res.append((p['id'], (nm, p)))
        return res
    with ThreadPoolExecutor(8) as ex:
        for rr in ex.map(find, names):
            for pid, v in rr: pool[pid] = v
    tita_pool[city] = list(pool.values())
    miss = [nm for nm in names if not any(nm == x[0] for x in pool.values())]
    print('Tita', city, '| nomes', len(names), '| lugares/filiais', len(pool), '| sem achado:', miss)

slots, report = [], []
for ph, days in DATA.items():
    for d in days:
        lab = d['label']
        if lab in SKIP_DAYS: continue
        date = dday(lab)
        for meal in ('almoço', 'jantar'):
            if (meal == 'almoço' and lab in NO_LUNCH) or (meal == 'jantar' and lab in NO_DINNER): continue
            win = L.LUNCH if meal == 'almoço' else L.DINNER
            key = (lab, meal)
            mode = 'stay' if key in STAY else 'move' if key in MOVE else 'convert' if key in CONVERT else 'none'
            lo, hi = (600, 870) if meal == 'almoço' else (1020, 1500)
            meal_stops = []
            for s in d['stops']:
                m = re.search(r'(\d{1,2})h(\d{2})?', s.get('time') or '')
                t = int(m.group(1)) * 60 + int(m.group(2) or 0) if m else None
                if t is not None and lo <= t < hi and (s.get('t') == 'lunch' or s.get('badge') in ('almoço', 'jantar')):
                    meal_stops.append(s)
            if key == ('26/10', 'jantar'):
                a_lat, a_lng, a_name = HOTELS['p3']['lat'], HOTELS['p3']['lng'], 'hotel em Kyoto'
            elif key == ('28/10', 'jantar'):
                h = stop_by_key([x for x in DATA['p4'] if x['label'] == '27/10'][0], 'Hondori')
                a_lat, a_lng, a_name = h['lat'], h['lng'], 'Hondori'
            elif mode in ('move', 'convert') and meal_stops and 'lat' in meal_stops[0]:
                s = meal_stops[0]
                a_lat, a_lng = s['lat'], s['lng']
                a_name = re.sub(r'^(Almoço|Jantar)( em| na região de| —)? ?', '', s['name']).strip() or s['name']
            elif key in ANCHOR_STOP_KEY and stop_by_key(d, ANCHOR_STOP_KEY[key]):
                s = stop_by_key(d, ANCHOR_STOP_KEY[key])
                a_lat, a_lng, a_name = s['lat'], s['lng'], re.sub(r'^(Almoço|Jantar) — ', '', s['name'])
            else:
                s = attraction_anchor(d, win)
                a_lat, a_lng, a_name = s['lat'], s['lng'], s['name']
            a_name = re.sub(r'^(Manhã em|Chegada em|Tarde em|Passeio por) ', '', a_name)
            a_name = a_name.split(' + ')[0].split(' (')[0].strip()
            a_name = LABEL.get(key, a_name)
            city = city_of(a_lat, a_lng)
            cand = {}
            with ThreadPoolExecutor(8) as ex:
                for res in ex.map(lambda q: L.text_search(q, a_lat, a_lng, 5000, 4.5, 2), BASE_Q + EXTRA_Q.get(city, [])):
                    for p in res:
                        cand[p['id']] = p
            moved = [s for s in d['stops'] if MOVE[key] in s['name']][0] if mode == 'move' else None
            ok = []
            for p in cand.values():
                if not L.is_meal_place(p) or p.get('businessStatus') != 'OPERATIONAL': continue
                if (p.get('rating') or 0) < 4.6 or (p.get('userRatingCount') or 0) < 51: continue
                dm = L.hav((a_lat, a_lng), (p['location']['latitude'], p['location']['longitude']))
                if dm > 5000: continue
                ov = L.open_overlap(p, date, win)
                if ov is None or ov < 60: continue
                if moved and L.hav((moved['lat'], moved['lng']), (p['location']['latitude'], p['location']['longitude'])) < 40: continue
                ok.append((dm, p))
            ok.sort(key=lambda x: x[0])
            lat_ok = [x for x in ok if has_latin(x[1]['displayName']['text'])]
            chosen = (lat_ok if len(lat_ok) >= 20 else ok)[:20]
            ids = {p['id'] for _, p in chosen}
            best_tita = {}   # uma filial por nome da Tita: a mais próxima da âncora e aberta na janela
            if city in tita_pool:
                for nm, p in tita_pool[city]:
                    dm = L.hav((a_lat, a_lng), (p['location']['latitude'], p['location']['longitude']))
                    if dm > 5000 or p.get('businessStatus') != 'OPERATIONAL': continue
                    ov = L.open_overlap(p, date, win)
                    if ov is None or ov < 60: continue
                    if moved and L.hav((moved['lat'], moved['lng']), (p['location']['latitude'], p['location']['longitude'])) < 40: continue
                    if nm not in best_tita or dm < best_tita[nm][0]: best_tita[nm] = (dm, p)
            tita_cards = []
            for nm, (dm, p) in best_tita.items():
                if p['id'] in ids:
                    for i, (d0, q0) in enumerate(chosen):
                        if q0['id'] == p['id']: chosen[i] = (d0, dict(q0, _tita=True))
                else:
                    tita_cards.append((dm, dict(p, _tita=True)))
            allc = sorted(chosen + tita_cards, key=lambda x: x[0])
            slots.append({"day": lab, "ph": ph, "meal": meal, "mode": mode, "anchor": {"name": a_name, "lat": a_lat, "lng": a_lng},
                          "city": city, "moved": moved['name'] if moved else None,
                          "cards": [{"id": p['id'], "d": round(dm), "t": bool(p.get('_tita')), "place": to_place(p, p.get('_tita'))} for dm, p in allc]})
            n_t = sum(1 for _, p in allc if p.get('_tita'))
            report.append((lab, meal, mode, a_name[:30], city, len(cand), len(ok), len(allc), n_t))
            print('%-6s %-6s %-8s | ancora %-30s %-9s | cand %3d aprov %3d -> cards %2d (Tita %d)%s' % (
                lab, meal, mode, a_name[:30], city, len(cand), len(ok), len(allc), n_t, '  <<< MENOS DE 20' if len(allc) < 20 else ''))
json.dump({"slots": slots, "report": report}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print('requisicoes novas:', L.STATS['req'], '| em cache:', L.STATS['cache'], '| lugares unicos:', len({c['id'] for s in slots for c in s['cards']}))
