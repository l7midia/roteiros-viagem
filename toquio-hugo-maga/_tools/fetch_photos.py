# -*- coding: utf-8 -*-
"""Baixa as fotos do Google Places para assets/photos/ e liga ao app (index.html).

Uso:  GOOGLE_PLACES_API_KEY=... python3 _tools/fetch_photos.py        (rodar na pasta toquio-hugo-maga)
Pré-requisito: o ambiente precisa liberar o host lh3.googleusercontent.com (as fotos são redirecionadas para lá).
A chave nunca é gravada em arquivo.  --offline-test cria arquivos vazios só para testar o encaixe no index.html.
"""
import json, os, sys, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
KEY = os.environ.get('GOOGLE_PLACES_API_KEY') or os.environ.get('K')
OFFLINE = '--offline-test' in sys.argv
if not KEY and not OFFLINE:
    sys.exit('Defina GOOGLE_PLACES_API_KEY')

todo = json.load(open(os.path.join(HERE, 'photos_todo.json'), encoding='utf-8'))
html_path = os.path.join(ROOT, 'index.html')
lines = open(html_path, encoding='utf-8').read().split('\n')
i = next(n for n, l in enumerate(lines) if l.startswith('const DATA='))
DATA = json.loads(lines[i][len('const DATA='):-1])

done, fail = {}, 0
for q, info in todo.items():
    paths = []
    for n, name in enumerate(info['photos'], 1):
        rel = 'assets/photos/%s/%d.jpg' % (info['slug'], n)
        f = os.path.join(ROOT, rel)
        if not os.path.exists(f):
            os.makedirs(os.path.dirname(f), exist_ok=True)
            try:
                if OFFLINE:
                    open(f, 'wb').write(b'x')
                else:
                    u = 'https://places.googleapis.com/v1/%s/media?maxWidthPx=720&key=%s' % (name, KEY)
                    open(f, 'wb').write(urllib.request.urlopen(u, timeout=40).read())
            except Exception as e:
                fail += 1
                print('falha', rel, str(e)[:80])
                continue
        paths.append(rel)
    if paths:
        done[q] = paths

n_stops = 0
for days in DATA.values():
    for d in days:
        for s in d.get('stops', []) + d.get('optional', []):
            if s.get('q') in done:
                s['photos'] = done[s['q']]
                n_stops += 1
lines[i] = 'const DATA=' + json.dumps(DATA, ensure_ascii=False) + ';'
open(html_path, 'w', encoding='utf-8').write('\n'.join(lines))
print('lugares com foto:', len(done), '| paradas atualizadas:', n_stops, '| falhas:', fail)
