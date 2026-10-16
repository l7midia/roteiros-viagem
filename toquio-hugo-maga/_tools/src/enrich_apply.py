# -*- coding: utf-8 -*-
# Aplica os dados do Google Places ao roteiro. A chave vem de K (variável de ambiente), nunca é gravada.
import copy, datetime, json, math, os, re, sys, unicodedata, urllib.request
sys.path.insert(0, '.')
import data_japao as D

K = os.environ['K']
REPO = '/home/user/mendoza-roteiro-2026/'
PH_DIR = REPO + 'toquio-hugo-maga/assets/photos/'
cache = json.load(open('places_cache.json', encoding='utf-8'))

FIELDS = ",".join("places." + f for f in [
    "id", "displayName", "formattedAddress", "location", "rating", "userRatingCount", "regularOpeningHours",
    "internationalPhoneNumber", "websiteUri", "googleMapsUri", "photos", "businessStatus"])


def search(q, n=5):
    body = json.dumps({"textQuery": q, "languageCode": "pt-BR", "regionCode": "JP", "pageSize": n}).encode()
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Goog-Api-Key": K, "X-Goog-FieldMask": FIELDS})
    return json.load(urllib.request.urlopen(req, timeout=30)).get('places', [])


# correções de casamento
for q in list(cache):
    if isinstance(cache[q], dict):  # erro anterior
        cache[q] = search(q)
res = search("Ten Yokota Asue Yaesu Tokyo")
cache["Ten Yokota Asue, Tokyo"] = [p for p in res if '明日' in p['displayName']['text']] or cache["Ten Yokota Asue, Tokyo"]

AIRPORTS = {"Guarulhos International Airport", "Dallas Fort Worth International Airport", "John F. Kennedy International Airport"}
STATIONS = {"Kyoto Station, Kyoto", "Kyoto Station", "Hiroshima Station", "Osaka Station", "Shin-Osaka Station", "Kawaguchiko Station",
            "Busta Shinjuku, Tokyo", "Haneda Airport Terminal 3, Tokyo", "Ura-Namba, Osaka", "Kitashinchi, Osaka", "Kabukicho, Shinjuku, Tokyo"}
AREA_PHOTOS = {"Akihabara, Tokyo", "Hanamikoji Street, Gion, Kyoto", "Pontocho Alley, Kyoto", "Dotonbori, Osaka", "Naramachi, Nara",
               "Hondori Shopping Street, Hiroshima", "Omotesando Shopping Street, Miyajima"}
COORDS_ONLY = STATIONS | AREA_PHOTOS


def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def hav(a, b):
    R = 6371
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = p2 - p1, math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def clean(v):
    return re.sub(r'\s+', ' ', v.replace(' ', ' ').replace(' ', ' ')).strip()


def parse_hours(p):
    wd = (p.get('regularOpeningHours') or {}).get('weekdayDescriptions')
    if not wd or len(wd) != 7:
        return None
    out = []
    for line in wd:
        m = re.match(r'^[^:]+:\s*(.*)$', clean(line))
        v = m.group(1) if m else clean(line)
        if re.search(r'fechado', v, re.I):
            v = 'FECHADO'
        elif re.search(r'24 horas', v, re.I):
            v = '24h'
        out.append(v)
    return out  # segunda..domingo


KEYS = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]


def start_min(t):
    if not t:
        return None
    m = re.search(r'(\d{1,2})h(\d{2})?', t)
    return int(m.group(1)) * 60 + int(m.group(2) or 0) if m else None


def status_for(hours, date, t):
    v = hours[date.weekday()]
    if v == 'FECHADO':
        return 'warn', 'FECHADO NESTE DIA'
    if v == '24h':
        return 'ok', 'ABERTO 24H'
    st = start_min(t)
    iv = re.findall(r'(\d{1,2}):(\d{2})\s*[–—-]\s*(\d{1,2}):(\d{2})', v)
    if st is None or not iv:
        return None
    for a, b, c, d in iv:
        a, c = int(a) * 60 + int(b), int(c) * 60 + int(d)
        if c <= a:
            c += 1440
        if a <= st < c or a <= st + 1440 < c:
            return 'ok', 'ABERTO ✓'
    return 'warn', 'CONFIRA O HORÁRIO'


downloaded = {}


def photos_for(p, key):
    sl = slug(p['displayName']['text']) or slug(key)
    if sl in downloaded:
        return downloaded[sl]
    os.makedirs(PH_DIR + sl, exist_ok=True)
    paths = []
    for i, ph in enumerate((p.get('photos') or [])[:3], 1):
        f = '%s%s/%d.jpg' % (PH_DIR, sl, i)
        if not os.path.exists(f):
            try:
                url = "https://places.googleapis.com/v1/%s/media?maxWidthPx=720&key=%s" % (ph['name'], K)
                data = urllib.request.urlopen(url, timeout=40).read()
                open(f, 'wb').write(data)
            except Exception as e:
                print('  falha foto', sl, i, str(e)[:60])
                continue
        paths.append('assets/photos/%s/%d.jpg' % (sl, i))
    downloaded[sl] = paths
    return paths


DATA = copy.deepcopy(D.DATA)
HOTELS = {k: dict(v) for k, v in D.HOTELS.items()}
MESN = {10: 10, 11: 11}
report = []

for ph, days in DATA.items():
    for d in days:
        dd, mm = [int(x) for x in d['label'].split('/')]
        date = datetime.date(2026, mm, dd)
        for s in d['stops'] + d.get('optional', []):
            q = s.get('q')
            if not q or q in AIRPORTS:
                continue
            res = cache.get(q)
            if not res:
                report.append(('SEM RESULTADO', d['label'], s['name']))
                continue
            p = res[0]
            s['lat'] = round(p['location']['latitude'], 6)
            s['lng'] = round(p['location']['longitude'], 6)
            if q in COORDS_ONLY:
                if q in AREA_PHOTOS:
                    ph_ = photos_for(p, q)
                    if ph_:
                        s['photos'] = ph_
                continue
            if p.get('googleMapsUri'):
                s['gmaps'] = p['googleMapsUri']
            if p.get('rating') and p.get('userRatingCount', 0) >= 30:
                s['rating'] = p['rating']
                s['rcount'] = p['userRatingCount']
            h = parse_hours(p)
            if h:
                s['hours'] = dict(zip(KEYS, h))
                s['hrs'] = '%s: %s' % (KEYS[date.weekday()], h[date.weekday()])
                if 'st' not in s:
                    r = status_for(h, date, s.get('time'))
                    if r:
                        s['st'], s['stl'] = r
                        if r[0] == 'warn':
                            report.append(('ATENÇÃO', d['label'], '%s (%s) hoje: %s' % (s['name'], s.get('time'), h[date.weekday()])))
            if p.get('internationalPhoneNumber'):
                s['phone'] = p['internationalPhoneNumber']
            w = p.get('websiteUri') or ''
            if 'instagram.com/' in w:
                m = re.search(r'instagram\.com/([^/?#]+)', w)
                if m and not s.get('ig'):
                    s['ig'] = m.group(1)
            elif w and not s.get('website'):
                s['website'] = w
            ph_ = photos_for(p, q)
            if ph_:
                s['photos'] = ph_
            report.append(('OK', d['label'], '%s -> %s' % (s['name'][:38], p['displayName']['text'][:34])))
        # remove coordenadas distantes (>60 km) do agrupamento do dia
        pts = [(s['lat'], s['lng']) for s in d['stops'] + d.get('optional', []) if 'lat' in s]
        if len(pts) >= 3:
            med = (sorted(x[0] for x in pts)[len(pts) // 2], sorted(x[1] for x in pts)[len(pts) // 2])
            for s in d['stops'] + d.get('optional', []):
                if 'lat' in s and hav(med, (s['lat'], s['lng'])) > 60:
                    report.append(('LONGE', d['label'], s['name'] + ' (sem marcador no mapa)'))
                    del s['lat'], s['lng']

for ph, h in HOTELS.items():
    q = h['name'] + ', ' + h['addr']
    p = cache[q][0]
    h['lat'] = round(p['location']['latitude'], 6)
    h['lng'] = round(p['location']['longitude'], 6)
    if not h.get('gmaps') and p.get('googleMapsUri'):
        h['gmaps'] = p['googleMapsUri']

json.dump({'DATA': DATA, 'HOTELS': HOTELS}, open('enriched.json', 'w', encoding='utf-8'), ensure_ascii=False)
for r in report:
    if r[0] != 'OK':
        print(*r)
print('fotos (pastas):', len(downloaded), '| arquivos:', sum(len(v) for v in downloaded.values()))
