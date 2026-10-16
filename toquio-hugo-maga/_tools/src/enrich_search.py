# -*- coding: utf-8 -*-
# Busca no Google Places (New). A chave vem da variável de ambiente K (nunca é gravada em arquivo).
import json, os, sys, time, urllib.request
sys.path.insert(0, '.')
import data_japao as D

K = os.environ['K']
FIELDS = ",".join("places." + f for f in [
    "id", "displayName", "formattedAddress", "location", "rating", "userRatingCount", "regularOpeningHours",
    "internationalPhoneNumber", "websiteUri", "googleMapsUri", "photos", "businessStatus"])

queries = {}
for ph, days in D.DATA.items():
    for d in days:
        for s in d['stops'] + d.get('optional', []):
            if s.get('q'):
                queries.setdefault(s['q'], []).append((ph, d['label'], s['name']))
for ph, h in D.HOTELS.items():
    queries.setdefault(h['name'] + ', ' + h['addr'], []).append((ph, 'hotel', h['name']))

cache_file = 'places_cache.json'
cache = json.load(open(cache_file, encoding='utf-8')) if os.path.exists(cache_file) else {}


def search(q):
    body = json.dumps({"textQuery": q, "languageCode": "pt-BR", "regionCode": "JP", "pageSize": 3}).encode()
    req = urllib.request.Request("https://places.googleapis.com/v1/places:searchText", data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-Goog-Api-Key": K, "X-Goog-FieldMask": FIELDS})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r).get('places', [])


n = 0
for q in queries:
    if q in cache:
        continue
    try:
        cache[q] = search(q)
    except Exception as e:
        cache[q] = {"error": str(e)[:200]}
    n += 1
    time.sleep(0.15)
json.dump(cache, open(cache_file, 'w', encoding='utf-8'), ensure_ascii=False)
print('consultas novas:', n, '| únicas:', len(queries))
for q, uses in queries.items():
    r = cache[q]
    if isinstance(r, dict):
        print('ERRO', q, r)
        continue
    if not r:
        print('SEM RESULTADO |', q)
        continue
    p = r[0]
    print('%-55s -> %-38s | %s | %s(%s) | %.4f,%.4f' % (
        q[:55], p['displayName']['text'][:38], p.get('formattedAddress', '')[-34:], p.get('rating', '-'),
        p.get('userRatingCount', '-'), p['location']['latitude'], p['location']['longitude']))
