# -*- coding: utf-8 -*-
"""Etapa 1 do Instagram: procura o perfil no site oficial do próprio lugar (campo websiteUri do Places).
Só aceita link instagram.com/<perfil> que apareça na página do restaurante; não adivinha. Saída: instagram.json."""
import json, os, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meals_lib as L

RES = json.load(open(os.environ.get('MEALS_OUT', os.path.join(L.CACHE_DIR, 'meals_result.json')), encoding='utf-8'))
OUT = os.path.join(L.CACHE_DIR, 'instagram.json')
RESERVED = {'p', 'reel', 'reels', 'explore', 'accounts', 'tv', 'stories', 'about', 'legal', 'privacy', 'developer', 'direct', 'web', 'share', 'sharer', 'intent', 'oauth', 'login'}
RX = re.compile(r'instagram\.com/([A-Za-z0-9._]{2,30})', re.I)
places = {}
for s in RES['slots']:
    for c in s['cards']:
        places[c['id']] = c['place']
prev = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {}


def norm(x): return re.sub(r'[^a-z0-9]', '', x.lower())


def handles_in(text):
    out = []
    for m in RX.finditer(text):
        h = m.group(1).rstrip('.')
        if h.lower() in RESERVED: continue
        out.append(h)
    return out


def one(item):
    pid, pl = item
    if pid in prev: return pid, prev[pid], 'cache'
    w = pl.get('website') or ''
    if not w: return pid, None, 'sem site'
    if 'instagram.com/' in w:
        hs = handles_in(w)
        return pid, (hs[0] if hs else None), 'site é o instagram'
    try:
        req = urllib.request.Request(w, headers={'User-Agent': 'Mozilla/5.0 (roteiro-viagem)'})
        raw = urllib.request.urlopen(req, timeout=10).read(600000)
        txt = raw.decode('utf-8', 'ignore')
    except Exception as e:
        return pid, None, 'site falhou'
    hs = handles_in(txt)
    if not hs: return pid, None, 'sem link'
    uniq = list(dict.fromkeys(h.lower() for h in hs))
    if len(uniq) == 1: return pid, hs[0], 'site oficial'
    nm = norm(pl['name'])
    best = [h for h in uniq if norm(h) and (norm(h) in nm or nm[:6] in norm(h))]
    return (pid, next(h for h in hs if h.lower() == best[0]), 'site oficial (casou nome)') if best else (pid, None, 'ambíguo')


with ThreadPoolExecutor(16) as ex:
    rows = list(ex.map(one, places.items()))
found = {pid: h for pid, h, _ in rows if h}
json.dump({**prev, **found}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
from collections import Counter
print('lugares:', len(places), '| com instagram:', len(found), '|', dict(Counter(r[2] for r in rows)))
