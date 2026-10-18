# -*- coding: utf-8 -*-
"""Utilitários para montar os carrosséis de refeição a partir do Google Places (New).
A chave vem da variável de ambiente K (nunca é gravada em arquivo). Respostas ficam em cache local (CACHE_DIR)."""
import datetime, hashlib, json, math, os, re, time, unicodedata, urllib.request

K = os.environ.get('K', '')
CACHE_DIR = os.environ.get('MEALS_CACHE', os.path.join(os.path.dirname(os.path.abspath(__file__)), '_cache'))
os.makedirs(CACHE_DIR, exist_ok=True)
STATS = {'req': 0, 'cache': 0}

FIELDS = ",".join(["nextPageToken"] + ["places." + f for f in [
    "id", "displayName", "formattedAddress", "shortFormattedAddress", "location", "rating", "userRatingCount",
    "regularOpeningHours", "internationalPhoneNumber", "websiteUri", "googleMapsUri", "photos", "businessStatus",
    "primaryType", "primaryTypeDisplayName", "types"]])

LUNCH = (11 * 60 + 50, 14 * 60)
DINNER = (18 * 60 + 30, 20 * 60 + 30)
KEYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def hav(a, b):
    R = 6371000.0
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def post(url, body, fields=FIELDS):
    key = hashlib.md5((url + json.dumps(body, sort_keys=True) + fields).encode()).hexdigest()
    f = os.path.join(CACHE_DIR, key + '.json')
    if os.path.exists(f):
        STATS['cache'] += 1
        return json.load(open(f, encoding='utf-8'))
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method='POST',
                                 headers={'Content-Type': 'application/json', 'X-Goog-Api-Key': K, 'X-Goog-FieldMask': fields})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = json.load(r)
            break
        except Exception as e:
            msg = str(e).replace(K, '[CHAVE]')
            if attempt == 2:
                raise RuntimeError(msg)
            time.sleep(1.5)
    STATS['req'] += 1
    json.dump(data, open(f, 'w', encoding='utf-8'), ensure_ascii=False)
    time.sleep(0.05)
    return data


def box(lat, lng, radius_m):
    dlat = radius_m / 111320.0
    dlng = radius_m / (111320.0 * math.cos(math.radians(lat)))
    return {"rectangle": {"low": {"latitude": lat - dlat, "longitude": lng - dlng},
                          "high": {"latitude": lat + dlat, "longitude": lng + dlng}}}


def text_search(query, lat, lng, radius_m=5000, min_rating=None, max_pages=2, lang='en'):
    out, token = [], None
    for _ in range(max_pages):
        body = {"textQuery": query, "languageCode": lang, "regionCode": "JP", "pageSize": 20,
                "locationRestriction": box(lat, lng, radius_m)}
        if min_rating:
            body["minRating"] = min_rating
        if token:
            body["pageToken"] = token
        r = post("https://places.googleapis.com/v1/places:searchText", body)
        out += r.get('places', [])
        token = r.get('nextPageToken')
        if not token:
            break
    return out


def parse_hours(p):
    wd = (p.get('regularOpeningHours') or {}).get('weekdayDescriptions')
    if not wd or len(wd) != 7:
        return None
    out = {}
    for k, line in zip(KEYS, wd):
        m = re.match(r'^[^:]+:\s*(.*)$', re.sub(r'\s+', ' ', line.replace(' ', ' ').replace(' ', ' ')))
        v = m.group(1).strip() if m else line
        if re.search(r'closed|fechado', v, re.I):
            v = 'FECHADO'
        elif re.search(r'24 hours|24 horas', v, re.I):
            v = '24h'
        out[k] = v
    return out


def open_overlap(p, date, win):
    """Minutos em que o lugar fica aberto dentro da janela (win=(ini,fim) em minutos) no dia `date`. None se sem horário."""
    roh = p.get('regularOpeningHours') or {}
    periods = roh.get('periods')
    if not periods:
        return None
    g = (date.weekday() + 1) % 7  # Google: 0=domingo
    if len(periods) == 1 and 'close' not in periods[0]:
        return win[1] - win[0]  # sempre aberto
    best = 0
    for per in periods:
        o, c = per.get('open'), per.get('close')
        if not o or not c:
            continue
        # intervalo absoluto em minutos desde domingo 00:00
        a = o['day'] * 1440 + o.get('hour', 0) * 60 + o.get('minute', 0)
        b = c['day'] * 1440 + c.get('hour', 0) * 60 + c.get('minute', 0)
        if b <= a:
            b += 7 * 1440
        ws = g * 1440 + win[0]
        we = g * 1440 + win[1]
        for off in (0, 7 * 1440, -7 * 1440):
            lo, hi = max(a + off, ws), min(b + off, we)
            if hi > lo:
                best = max(best, hi - lo)
    return best


MEAL_OK_PRIMARY = {'restaurant', 'steak_house', 'diner', 'food_court', 'buffet_restaurant', 'izakaya'}


def is_meal_place(p):
    pt = p.get('primaryType') or ''
    types = p.get('types') or []
    if pt.endswith('_restaurant') or pt in MEAL_OK_PRIMARY:
        return True
    if pt in ('', None):
        return any(t.endswith('_restaurant') or t == 'restaurant' for t in types)
    return False


PT_TYPE = {'japanese_restaurant': 'Restaurante japonês', 'sushi_restaurant': 'Restaurante de sushi', 'ramen_restaurant': 'Ramen',
           'seafood_restaurant': 'Frutos do mar', 'barbecue_restaurant': 'Yakiniku / churrasco', 'steak_house': 'Casa de carnes',
           'restaurant': 'Restaurante', 'izakaya': 'Izakaya', 'fast_food_restaurant': 'Refeição rápida', 'vegetarian_restaurant': 'Vegetariano',
           'italian_restaurant': 'Restaurante italiano', 'chinese_restaurant': 'Restaurante chinês', 'korean_restaurant': 'Restaurante coreano',
           'hamburger_restaurant': 'Hambúrguer', 'pizza_restaurant': 'Pizzaria', 'noodle_restaurant': 'Macarrão', 'french_restaurant': 'Restaurante francês',
           'indian_restaurant': 'Restaurante indiano', 'buffet_restaurant': 'Buffet', 'diner': 'Lanchonete', 'food_court': 'Praça de alimentação'}


# nomes em inglês que o Google devolve como tipo principal
PT_DISPLAY = {"Yakiniku restaurant": "Yakiniku (carne na grelha)", "Tonkatsu restaurant": "Tonkatsu (porco empanado)", "Halal restaurant": "Restaurante halal", "Izakaya restaurant": "Izakaya", "Japanese curry restaurant": "Curry japonês", "Yakitori restaurant": "Yakitori (espetinhos)", "Oyster bar restaurant": "Ostras", "Asian restaurant": "Restaurante asiático", "Vegan restaurant": "Restaurante vegano", "Thai restaurant": "Restaurante tailandês"}


def tipo_pt(p):
    pt = p.get('primaryType') or ''
    if pt in PT_TYPE:
        return PT_TYPE[pt]
    d = (p.get('primaryTypeDisplayName') or {}).get('text')
    return PT_DISPLAY.get(d, d) or 'Restaurante'


def fmt_dist(m):
    return ('%d m' % (round(m / 10.0) * 10)) if m < 1000 else ('%.1f km' % (m / 1000.0)).replace('.', ',')
