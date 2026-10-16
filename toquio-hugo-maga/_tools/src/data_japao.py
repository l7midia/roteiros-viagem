# -*- coding: utf-8 -*-
# Conteúdo do roteiro Japão (Hugo & Marília) extraído do PDF da agência. Sem códigos de reserva nem números de voo.
import datetime

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
MESES = {10: "out", 11: "nov"}


def dt(d, m):
    x = datetime.date(2026, m, d)
    return "%s, %d %s" % (DIAS[x.weekday()], d, MESES[m])


def S(time, name, desc, badge, q=None, t="city", **kw):
    s = dict(time=time, name=name, desc=desc, badge=badge, t=t)
    if q:
        s["q"] = q
    s.update(kw)
    return s


def ALM(time, name, desc, q, **kw):
    return S(time, name, desc, "almoço", q, t="lunch", **kw)


def JAN(time, name, desc, q, **kw):
    return S(time, name, desc, "jantar", q, t="lunch", **kw)


OK = dict(st="ok")
HOTELS = {
    "p1": dict(name="Hotel Henn Tokyo Ginza", addr="2 Chome-2-1 Tsukiji, Chuo City, Tokyo 104-0045", din="18/10", dout="22/10",
               gmaps="https://www.google.com/maps/place/data=!4m2!3m1!1s0x60188960138fe8c9:0x631c10e9a14fca22"),
    "p2": dict(name="Lakeland Hotel Mizunosato (ryokan)", addr="1070 Kodachi, Fujikawaguchiko, Minamitsuru District, Yamanashi", din="22/10", dout="23/10"),
    "p3": dict(name="Daiwa Roynet Hotel Kyoto Ekimae Premier", addr="707-2 Higashishiokojicho, Karasuma-dori, Shimogyo-ku, Kyoto", din="23/10", dout="27/10"),
    "p4": dict(name="Hotel Vista", addr="6-15 Teppocho, Naka Ward, Hiroshima", din="27/10", dout="29/10"),
    "p5": dict(name="Travelodge Honmachi Osaka", addr="3 Chome-2-6 Azuchimachi, Chuo Ward, Osaka", din="29/10", dout="02/11"),
    "p6": dict(name="Daiwa Roynet Hotel Tokyo Kyobashi Premier", addr="2 Chome-8-20 Kyobashi, Chuo City, Tokyo", din="02/11", dout="05/11"),
}
PHASES = [
    ("p1", "🗼 Tóquio · 16–22/10"), ("p2", "🗻 Monte Fuji · 22–23/10"), ("p3", "⛩️ Kyoto · 23–27/10"),
    ("p4", "🕊️ Hiroshima · 27–29/10"), ("p5", "🏯 Osaka · 29/10–02/11"), ("p6", "🗼 Tóquio · 02–05/11"),
]

TOKYO_DAYS = []
DATA = {k: [] for k, _ in PHASES}

# ───────────────────────── p1 · Tóquio (16–22/10)
DATA["p1"].append(dict(
    label="16/10", date=dt(16, 10), title="Embarque — São Paulo → Dallas → Tóquio",
    sub="Dois voos pela American até Tóquio, com conexão em Dallas.",
    origin="Aeroporto de Guarulhos GRU", dest_q="Haneda Airport Terminal 3, Tokyo",
    stops=[
        S("22h", "16/10 · 22h — Voo São Paulo (GRU) → Dallas (DFW)", "American. Embarque 16/10 às 22h, chegada 17/10 às 6h20.", "transporte", q="Guarulhos International Airport"),
        S(None, "17/10 · 10h30 — Voo Dallas (DFW) → Tóquio Haneda (HND)", "American. Embarque 17/10 às 10h30, chegada 18/10 às 14h20 (horário do Japão). Na conexão em Dallas é preciso passar pela imigração dos EUA, retirar as malas e despachar de novo.", "transporte", q="Dallas Fort Worth International Airport"),
    ],
    guide=dict(importante=["Visto americano válido é obrigatório por causa da conexão em Dallas.",
                           "Preencham o Visit Japan Web antes do embarque e salvem os dois QR Codes (imigração e alfândega) em print.",
                           "Passaporte com chip válido durante toda a viagem. Instalem o eSIM ainda no Brasil."]),
))
DATA["p1"].append(dict(
    label="18/10", date=dt(18, 10), title="Chegada em Tóquio + Ginza",
    sub="Primeiro contato com Tóquio, com o dia bem tranquilo: chegada, hotel e uma caminhada leve por Ginza.",
    origin="Haneda Airport Terminal 3, Tokyo", dest_q="Hotel Henn Tokyo Ginza",
    stops=[
        S("14h20", "Chegada em Tóquio (Haneda, Terminal 3)", "Terminal internacional. Antes de pousar, deixem abertos no celular os dois QR Codes do Visit Japan Web (imigração e alfândega). Contem 1h a 1h30 entre o pouso e a saída com as malas. No saguão, saquem ienes num caixa da 7-Eleven (Seven Bank): ¥20.000 a ¥30.000 bastam para os primeiros dias. Se o eSIM ainda não estiver ativo, ativem no Wi-Fi do aeroporto.", "transporte", q="Haneda Airport Terminal 3, Tokyo"),
        S("18h", "Passeio leve por Ginza", "Depois de se instalarem, descansem. Se estiverem dispostos: caminhada pela Chuo-dori (a avenida principal de Ginza), subida ao jardim do terraço do Ginza Six (gratuito) para ver as luzes acendendo, uma volta pela Itoya (a papelaria mais famosa de Tóquio) e pela Uniqlo de Ginza, loja-conceito de vários andares.", "passeio", q="Ginza Six, Tokyo"),
        JAN("20h", "Jantar — Ginza Kagari", "Sugestão: ramen cremoso de frango, famoso em Ginza.", "Ginza Kagari Honten, Ginza, Tokyo", ig="kagari_honten"),
    ],
    guide=dict(
        locomover=["Haneda Terminal 3 → Higashi-Ginza: linha Keikyu, dentro do terminal (sigam as placas vermelhas). Peguem trem com destino a Asakusa, Oshiage ou Narita, que segue direto pela linha Toei Asakusa, sem baldeação. Se o trem terminar em Shinagawa, troquem lá para a linha Asakusa.",
                   "Alternativa de táxi: cerca de 30 a 40 minutos, dependendo do trânsito, por ¥8.000 a ¥10.000 (sujeito a pedágios).",
                   "Para os passeios por Ginza, usem o Google Maps conforme o ponto onde estiverem."],
        comer=["Ginza Kagari: famoso pelo ramen cremoso de frango."],
        dica="Não tentem fazer muita coisa hoje! O ideal é descansar, se hidratar e começar a se adaptar ao fuso horário. Se estiverem com energia, uma caminhada leve já é suficiente.",
        importante=["Tenham os documentos de entrada e o endereço do hotel à mão para a imigração.",
                    "Antes de sair do aeroporto, confirmem que o eSIM está funcionando e que conseguem acessar mapas e reservas pelo celular."]),
))
DATA["p1"].append(dict(
    label="19/10", date=dt(19, 10), title="Asakusa, Kappabashi, Ueno e Akihabara",
    sub="Dois lados diferentes de Tóquio: o tradicional de Asakusa e o universo moderno de Akihabara.",
    origin=None, dest_q="Senso-ji Temple, Asakusa, Tokyo",
    stops=[
        S("9h", "Manhã em Asakusa — Templo Senso-ji", "Comecem pelo Templo Senso-ji, um dos mais tradicionais de Tóquio. Passem pelo portão Kaminarimon e caminhem pela Nakamise Street, cheia de lojinhas, doces japoneses e souvenirs. Depois, explorem as ruazinhas de Asakusa e caminhem até a Ponte Azuma, com vista do rio Sumida e da Tokyo Skytree.", "templo", q="Senso-ji Temple, Asakusa, Tokyo"),
        ALM("13h", "Almoço — Daikokuya", "Sugestão: Daikokuya, famoso pelo tempurá servido sobre arroz (tendon). Fica por Asakusa mesmo.", "Daikokuya Tempura Asakusa, Tokyo"),
        S("14h", "Kappabashi, Ueno (Ameyoko) e Akihabara", "Depois do almoço, sigam para Ameyoko, em Ueno, um mercado de rua cheio de lojinhas, comidas e produtos japoneses. Em seguida, conheçam Akihabara, o bairro dos eletrônicos, animes, videogames e fliperamas; entrem nas lojas que chamarem atenção, sem compromisso de conhecer tudo. Se estiverem cansados, podem ir direto de Asakusa para Akihabara, deixando Ueno de fora.", "passeio", q="Akihabara, Tokyo"),
        JAN("20h", "Jantar — Kanda Matsuya", "Sugestão: restaurante histórico especializado em soba artesanal, na região de Kanda.", "Kanda Matsuya, Kanda, Tokyo", website="http://www.kanda-matsuya.jp/"),
    ],
    guide=dict(
        locomover=["Hotel → Asakusa: caminhem até Higashi-Ginza e peguem a linha Toei Asakusa até Asakusa (cerca de 15 min).",
                   "Asakusa → Kappabashi: caminhada de 10–15 min.",
                   "Kappabashi → Ueno: linha Ginza, de Tawaramachi até Ueno (cerca de 5 min).",
                   "Ueno → Akihabara: JR Yamanote (cerca de 5 min).",
                   "Akihabara → Kanda: caminhada de 10–15 min.",
                   "Kanda → Hotel: linha Ginza até Ginza e caminhada até o hotel."],
        comer=["Daikokuya (Asakusa): tradicional tempurá servido sobre arroz.",
               "Kanda Matsuya (Kanda): restaurante histórico, especializado em soba artesanal.",
               "Ichiran (Akihabara): ramen japonês, ótimo para uma refeição rápida."],
        dica="Aproveitem para experimentar as comidinhas de rua e explorar as lojas sem pressa. Em Kappabashi, vale ver as famosas réplicas de comida japonesa."),
))
DATA["p1"].append(dict(
    label="20/10", date=dt(20, 10), title="Meiji Jingu, Harajuku e Shibuya",
    sub="O lado mais moderno e descolado de Tóquio, começando por um santuário cercado de floresta.",
    origin=None, dest_q="Meiji Jingu, Shibuya, Tokyo",
    stops=[
        S("9h", "Meiji Jingu e Harajuku", "Comecem pelo Santuário Meiji Jingu, um dos mais importantes de Tóquio, cercado por uma enorme área verde, com caminhada tranquila entre as árvores e os portões torii. Depois, sigam para Harajuku e a Takeshita Street, cheia de lojas diferentes, moda japonesa e comidinhas. Vale experimentar os crepes da Marion Crepes!", "templo", q="Meiji Jingu, Shibuya, Tokyo"),
        ALM("12h", "Almoço — Menchirashi", "Sugestão: udon artesanal em Harajuku, ótimo para o almoço.", "Menchirashi Harajuku, Tokyo"),
        S("14h", "Tarde em Shibuya", "Depois do almoço, sigam pela Cat Street, uma rua com lojas de moda, tênis e marcas japonesas, até Shibuya. Por lá, conheçam o Shibuya Crossing, a estátua de Hachiko e o shopping Shibuya PARCO, onde ficam a Nintendo Tokyo e o Pokémon Center.", "passeio", q="Shibuya Crossing, Tokyo"),
        S("16h", "Shibuya Sky (pôr do sol)", "Se conseguirem ingresso para as 16h, subam ao Shibuya Sky para acompanhar o pôr do sol e ver Tóquio se iluminando: uma das vistas mais bonitas da cidade. Comprem o ingresso com antecedência.", "passeio", q="Shibuya Sky, Tokyo", st="warn", stl="COMPRAR INGRESSO"),
        JAN("20h", "Jantar — Ichiran Shibuya", "Sugestão: ramen tonkotsu.", "Ichiran Shibuya, Tokyo", website="https://ichiran.com/shop/tokyo/shibuya/"),
    ],
    guide=dict(
        locomover=["Hotel → Meiji Jingu: linha Ginza direto até Omotesando (uns 16 min) e caminhada até o santuário.",
                   "Meiji Jingu → Harajuku: caminhada de 10 min.",
                   "Harajuku → Omotesando → Cat Street: façam tudo a pé.",
                   "Cat Street → Shibuya: caminhada de 15–20 min.",
                   "Shibuya → Hotel: linha Ginza até Ginza e caminhada até o hotel."],
        comer=["Menchirashi (Harajuku): udon artesanal, ótimo para o almoço.",
               "Kaiten Sushi Ginza Onodera: sushi na esteira, opção na região de Omotesando.",
               "Ichiran Shibuya: ramen, sugestão para o jantar."],
        dica="Explorem Harajuku, Omotesando e Shibuya caminhando! Para subir ao Shibuya Sky, comprem o ingresso antecipadamente, principalmente para o pôr do sol."),
))
DATA["p1"].append(dict(
    label="21/10", date=dt(21, 10), title="Shinjuku Gyoen e Shinjuku",
    sub="Um dos bairros mais vibrantes de Tóquio, com parque, letreiros gigantes e Kabukicho. Amanhã o dia começa cedo rumo ao Monte Fuji.",
    origin=None, dest_q="Shinjuku Gyoen National Garden, Tokyo",
    stops=[
        S("9h", "Shinjuku Gyoen", "ANTES de sair: peçam na recepção o envio das malas grandes diretamente para o hotel de Kyoto, onde chegam em 23/10. Separem apenas uma mochila ou mala pequena com o necessário para a noite no Monte Fuji. Confirmem com os dois hotéis o prazo de entrega e o recebimento. Depois, comecem pelo Shinjuku Gyoen, um dos jardins mais bonitos de Tóquio, com paisagens japonesas, lagos e áreas verdes. Um passeio tranquilo para aproveitar a manhã a dois.", "natureza", q="Shinjuku Gyoen National Garden, Tokyo"),
        ALM("11h30", "Almoço — Tsuta", "Sugestão: Tsuta, famoso pelo ramen elaborado (atenção: fica em Yoyogi-Uehara, um bairro próximo de Shinjuku, a ir de trem). Outra opção: Gyukatsu Motomura (carne empanada japonesa).", "Tsuta Shinjuku, Tokyo", website="https://www.tsuta79.tokyo/"),
        S("15h", "Shinjuku", "Explorem Shinjuku, um dos bairros mais movimentados de Tóquio, cheio de lojas, telões e ruas iluminadas. Vale conhecer o famoso gato 3D, a região de Kabukicho (com a cabeça do Godzilla) e lojas como Don Quijote, Bic Camera e Isetan. Aproveitem para localizar o Busta Shinjuku, terminal de ônibus de onde saem amanhã às 7h15 para o Monte Fuji: fica junto à estação Shinjuku, próximo à saída New South.", "passeio", q="Kabukicho, Shinjuku, Tokyo"),
        JAN("18h", "Jantar — Sushi Tokyo Ten", "Sugestão prioritária: experiência de omakase. A agência está tentando a reserva, que ainda não está confirmada.", "Sushi Tokyo Ten, Ginza, Tokyo", website="https://sushitokyo-ten.com/", st="warn", stl="RESERVA A CONFIRMAR"),
    ],
    guide=dict(
        locomover=["Hotel → Shinjuku Gyoen: linha Marunouchi direto de Ginza até Shinjuku-gyoemmae.",
                   "Shinjuku Gyoen → Kabukicho: caminhada de cerca de 20 min, passando pela região comercial.",
                   "Kabukicho → Busta Shinjuku: caminhada de 15–20 min até a saída sul da estação Shinjuku.",
                   "Shinjuku → Hotel: linha Marunouchi até Ginza e caminhada até o hotel."],
        comer=["Tsuta: famoso pelo ramen elaborado, opção para o almoço.",
               "Gyukatsu Motomura: carne empanada japonesa, outra opção de almoço.",
               "Sushi Tokyo Ten: sugestão prioritária para o jantar (omakase). Reserva ainda não confirmada."],
        dica="Amanhã vocês seguem para o Monte Fuji bem cedo! Deixem uma mala pequena separada para a noite em Kawaguchiko e organizem o envio das malas grandes para o hotel de Kyoto. Confirmem também a plataforma de embarque no Busta Shinjuku e deixem os bilhetes do ônibus salvos no celular."),
))

# ───────────────────────── p2 · Monte Fuji (22–23/10)
DATA["p2"].append(dict(
    label="22/10", date=dt(22, 10), title="Monte Fuji — Chureito, Oshino Hakkai e ryokan",
    sub="Vocês deixam a agitação de Tóquio para uma das regiões mais bonitas do Japão: pagoda com o Fuji ao fundo, vila de águas cristalinas e uma noite em ryokan com onsen.",
    origin="Hotel Henn Tokyo Ginza", dest_q="Busta Shinjuku, Tokyo",
    stops=[
        S("6h15", "Saída para o Busta Shinjuku", "Saiam do hotel por volta das 6h15 e sigam de táxi para o terminal Busta Shinjuku (25–35 min, dependendo do trânsito). Façam o checkout do hotel em Tóquio. Ônibus Shinjuku Express já comprado: saída às 7h15, chegada às 8h50 na parada Chuo Expressway Shimoyoshida. Deixem os bilhetes salvos no celular.", "transporte", q="Busta Shinjuku, Tokyo", st="ok", stl="BILHETE COMPRADO"),
        S("~9h15", "Pagoda Chureito (Parque Arakurayama Sengen)", "Da parada, caminhem cerca de 20 minutos até o Parque Arakurayama Sengen. Depois, são aproximadamente 398 degraus até o mirante do famoso Pagoda Chureito, com uma das vistas mais bonitas do Monte Fuji. Subam com calma e aproveitem a paisagem!", "natureza", q="Chureito Pagoda, Fujiyoshida"),
        S("10h30", "Oshino Hakkai", "Sigam de táxi para Oshino Hakkai, vila tradicional conhecida pelas lagoas de águas cristalinas e pelas vistas do Monte Fuji. Passeiem pelas lojinhas, experimentem as comidinhas locais (soba, espetinhos) e aproveitem para almoçar por lá. Atenção: não há ponto de táxi no pagode; desçam até a estação Shimoyoshida ou chamem pelo app GO.", "natureza", q="Oshino Hakkai, Yamanashi"),
        S("15h", "Check-in — Lakeland Hotel Mizunosato", "Hotel às margens do Lago Kawaguchi, com check-in a partir das 15h. Aproveitem a tarde para descansar, admirar a paisagem e viver a experiência do onsen, o tradicional banho termal japonês.", "hotel", q="Lakeland Hotel Mizunosato, Fujikawaguchiko", t="hotel"),
        JAN("19h", "Jantar no ryokan", "Confirmem se o jantar está incluído na hospedagem e o horário de serviço.", "Lakeland Hotel Mizunosato, Fujikawaguchiko", st="warn", stl="CONFIRMAR HORÁRIO"),
    ],
    guide=dict(
        locomover=["Hotel → Busta Shinjuku: saiam cedo e peguem um táxi até o terminal. O ônibus parte às 7h15.",
                   "Shinjuku → Shimoyoshida: ônibus direto até a parada Chuo Expressway Shimoyoshida, chegada prevista às 8h50.",
                   "Shimoyoshida → Pagoda Chureito: caminhada de 20–25 min até a entrada do parque, seguida da subida de escadas.",
                   "Chureito → Oshino Hakkai: desçam até a estação Shimoyoshida ou chamem pelo app GO.",
                   "Oshino Hakkai → Kawaguchiko: táxi de cerca de 20–25 min.",
                   "Kawaguchiko → Hotel Mizunosato: táxi ou transporte do hotel, se disponível."],
        comer=["Oshino Hakkai: soba, espetinhos e comidinhas típicas nas lojinhas da vila.",
               "Ryokan: confirmem se o jantar está incluído e o horário de serviço."],
        dica="A visibilidade do Monte Fuji depende muito do clima, e as manhãs costumam oferecer melhores chances de vê-lo sem nuvens. Levem um casaco mais quente (na região do Fuji pode fazer menos de 5°C à noite) e deixem as malas grandes seguindo para Kyoto, viajando só com o necessário para esta noite.",
        importante=["Amanhã vocês saem cedo de Kawaguchiko para Mishima e seguem de Shinkansen para Kyoto. Deixem os bilhetes salvos e peçam na recepção ajuda para organizar o táxi até a estação."]),
))

# ───────────────────────── p3 · Kyoto (23–27/10)
DATA["p3"].append(dict(
    label="23/10", date=dt(23, 10), title="Fuji → Kyoto, Kiyomizu-dera e Gion",
    sub="Despedida do Fuji e chegada a Kyoto, com um dos templos mais emblemáticos da cidade e a noite em Pontocho.",
    origin="Lakeland Hotel Mizunosato, Fujikawaguchiko", dest_q="Kawaguchiko Station",
    stops=[
        S("8h45", "Checkout + viagem para Kyoto", "Se o céu estiver limpo, admirem o Monte Fuji logo cedo, quando a vista costuma ser mais bonita. Depois, café da manhã e checkout do ryokan. Ônibus Fujiyama Connect às 9h20 de Kawaguchiko (chegada em Mishima, saída Norte, às 10h50) e Shinkansen às 11h46 de Mishima, com chegada a Kyoto às 13h37. Todos os bilhetes já estão comprados. Para o almoço, comprem um ekiben (marmita japonesa) antes de embarcar no Shinkansen.", "transporte", q="Kawaguchiko Station", st="ok", stl="BILHETES COMPRADOS"),
        S("13h37", "Chegada em Kyoto", "Sigam caminhando até o Daiwa Roynet Hotel Kyoto Ekimae Premier (a poucos minutos da estação), deixem as bagagens e descansem um pouquinho.", "hotel", q="Daiwa Roynet Hotel Kyoto Ekimae Premier", t="hotel"),
        S("15h15", "Kiyomizu-dera + Sannenzaka, Ninenzaka e Santuário Yasaka", "Comecem Kyoto por um dos templos mais emblemáticos da cidade! O Kiyomizu-dera é famoso pela enorme varanda de madeira sobre a encosta, com vista linda da cidade. Depois, desçam a pé pelas charmosas ruas de Sannenzaka e Ninenzaka, com construções tradicionais de madeira, lojinhas, cerâmicas, doces japoneses e casas de chá, e continuem até o Santuário Yasaka.", "templo", q="Kiyomizu-dera, Kyoto"),
        S("17h30", "Gion ao entardecer", "Sigam para Gion, o bairro tradicional das casas de chá e das geikos e maikos. Caminhem pela Hanamikoji observando a arquitetura e a atmosfera. Para uma pausa doce, a Kagizen Yoshifusa é uma opção tradicional, desde que ainda esteja aberta quando chegarem.", "passeio", q="Hanamikoji Street, Gion, Kyoto"),
        JAN("19h", "Jantar em Pontocho", "Pontocho é uma rua supercharmosa, cheia de restaurantes e izakayas, próxima ao rio Kamo.", "Pontocho Alley, Kyoto"),
    ],
    guide=dict(
        locomover=["Hotel → Kawaguchiko Station: peçam um táxi na recepção. O ônibus Fujiyama Connect sai às 9h20.",
                   "Kawaguchiko → Mishima: ônibus Fujiyama Connect até Mishima Station (saída Norte), chegada às 10h50.",
                   "Mishima → Kyoto: Shinkansen às 11h46, chegada às 13h37.",
                   "Kyoto Station → Hotel: a poucos minutos de caminhada.",
                   "Hotel → Kiyomizu-dera: recomendo táxi (15–25 min), seguido de caminhada até o templo.",
                   "Kiyomizu-dera → Sannenzaka → Ninenzaka → Yasaka → Gion: tudo a pé.",
                   "Gion → Pontocho: caminhada de 10–15 min.",
                   "Pontocho → Hotel: táxi de cerca de 15 min ou trem pela linha Keihan até Shichijo, seguido de caminhada."],
        comer=["Almoço: comprem um ekiben (marmita japonesa) antes de embarcar no Shinkansen.",
               "Kagizen Yoshifusa (Gion): tradicional casa de doces japoneses, caso ainda esteja aberta.",
               "Pontocho: ótima região para jantar, com restaurantes em ruas estreitas e charmosas."]),
))
DATA["p3"].append(dict(
    label="24/10", date=dt(24, 10), title="Kinkaku-ji, Arashiyama e Bosque de Bambu iluminado",
    sub="Dia com um começo mais calmo e uma experiência especial à noite: o Bosque de Bambu de Arashiyama iluminado.",
    origin=None, dest_q="Kinkaku-ji, Kyoto",
    stops=[
        S("10h", "Kinkaku-ji — Pavilhão Dourado", "Tomem café sem pressa e saiam por volta das 10h. Comecem pelo famoso Kinkaku-ji, um dos templos mais bonitos de Kyoto, conhecido pela fachada dourada refletida no lago. A visita leva cerca de 1 hora.", "templo", q="Kinkaku-ji, Kyoto"),
        ALM("13h", "Almoço em Arashiyama", "Aproveitem para almoçar e conhecer as lojinhas da rua principal. Por aqui há opções de soba, tofu japonês e doces de matcha.", "Arashiyama Togetsukyo, Kyoto"),
        S("14h", "Templo Tenryu-ji e Ponte Togetsukyo", "Visitem os jardins do Templo Tenryu-ji, com seu lago e as montanhas ao fundo. Depois, caminhem até a Ponte Togetsukyo e aproveitem a paisagem às margens do rio Hozu. O Bosque de Bambu fica para a noite, quando vocês vão conhecê-lo de uma maneira completamente diferente!", "templo", q="Tenryu-ji, Arashiyama, Kyoto"),
        JAN("17h30", "Shoraian — jantar", "Passem o fim de tarde em Arashiyama. Sugestão: o Shoraian, restaurante especializado em tofu japonês, para uma experiência gastronômica especial (a confirmar horário e reserva).", "Shoraian, Arashiyama, Kyoto", website="https://www.shoraian.jp/", st="warn", stl="A CONFIRMAR"),
        S("19h30", "Arashiyama Bamboo Light-up (Tsukitouro)", "O Bosque de Bambu de Arashiyama iluminado, com instalações de luz que transformam a paisagem. O evento está previsto das 18h às 21h, com última entrada às 20h40. Sugestão: chegar por volta das 19h30, mas confiram as orientações do ingresso comprado. Deixem o QR Code salvo no celular e levem um casaco, porque a temperatura pode cair à noite.", "ingresso", q="Arashiyama Bamboo Grove, Kyoto", st="ok", stl="INGRESSO COMPRADO"),
    ],
    guide=dict(
        locomover=["Hotel → Kinkaku-ji: recomendo táxi (25–30 min), mais prático do que combinar ônibus e metrô.",
                   "Kinkaku-ji → Arashiyama: táxi de 20–30 min. Alternativa: trem Randen, embarcando em Kitano-Hakubaicho e fazendo baldeação em Katabiranotsuji até Arashiyama.",
                   "Arashiyama → Tenryu-ji → Ponte Togetsukyo: passeios a pé.",
                   "Arashiyama → Floresta de Bambus: caminhada de 10–15 min a partir da região da ponte.",
                   "Arashiyama → Hotel: caminhem até a estação JR Saga-Arashiyama e peguem a linha JR Sagano até Kyoto Station (15–20 min), depois a pé até o hotel."],
        comer=["Almoço em Arashiyama: restaurantes e cafés da região.",
               "Shoraian: tofu japonês, mediante confirmação de horário e reserva."],
        importante=["O ingresso para o Arashiyama Tsukitouro já está comprado. O evento acontece das 18h às 21h, com última entrada prevista às 20h40. Deixem o QR Code salvo no celular e confiram as instruções do ingresso."]),
))
DATA["p3"].append(dict(
    label="25/10", date=dt(25, 10), title="Fushimi Inari, Nishiki e teamLab",
    sub="Começo cedo entre os milhares de portões vermelhos e, à tarde, uma exposição imersiva de arte e luz.",
    origin=None, dest_q="Fushimi Inari Taisha, Kyoto",
    stops=[
        S("7h", "Fushimi Inari + Mercado Nishiki", "Comecem cedo pelo Santuário Fushimi Inari, famoso pelos milhares de portões vermelhos que formam caminhos pela montanha. Sugestão: chegar por volta das 7h, antes das multidões. Caminhem pelos portões e, se estiverem dispostos, subam até o mirante de Yotsutsuji; não é preciso fazer a trilha inteira. Depois, Mercado Nishiki, a cozinha de Kyoto, cheio de comidas típicas, doces e produtos japoneses, e as galerias comerciais de Teramachi e Shinkyogoku, ótimas para compras.", "templo", q="Fushimi Inari Taisha, Kyoto"),
        ALM("14h", "Almoço", "Experimentem as comidinhas do Mercado Nishiki ou escolham um restaurante na região. Para uma experiência especial, o Mishima-tei é famoso pelo sukiyaki de wagyu e exige reserva.", "Mishima-tei Teramachi, Kyoto", website="https://kyoto-mishimatei.com/"),
        S("16h30", "teamLab Biovortex Kyoto", "Depois do almoço, voltem ao hotel para descansar. Às 16h15 saiam a pé para o teamLab Biovortex Kyoto (7 ou 8 minutos da saída Hachijo da estação). A entrada é às 16h30 e a visita média passa de 2h30: são mais de 50 obras imersivas em quatro andares. Deixem os ingressos e QR Codes salvos no celular.", "ingresso", q="teamLab Biovortex Kyoto", st="ok", stl="INGRESSO COMPRADO"),
        JAN("20h", "Jantar na região da Estação de Kyoto", "A região da estação tem várias opções de restaurantes e lojas, especialmente nos centros comerciais próximos.", "Kyoto Station, Kyoto"),
    ],
    guide=dict(
        locomover=["Hotel → Fushimi Inari: caminhem até Kyoto Station e peguem a linha JR Nara (trem local) até Inari, cerca de 5 min. O santuário fica em frente à estação.",
                   "Fushimi Inari → Mercado Nishiki: caminhem até Fushimi-Inari Station (Keihan), peguem o trem até Gion-Shijo e sigam a pé por 10–15 min.",
                   "Nishiki → Teramachi e Shinkyogoku: tudo caminhando, pois as galerias ficam próximas.",
                   "Centro → teamLab: caminhem até Shijo Station e peguem a linha Karasuma até Kyoto Station; depois a pé até o museu, na região sul da estação.",
                   "teamLab → Hotel: retorno a pé, 10–15 min."],
        comer=["Almoço: algum restaurante próximo aos passeios da manhã.",
               "Jantar: a região da Kyoto Station tem ótimas opções, especialmente nos centros comerciais."],
        dica="Cheguem cedo ao Fushimi Inari para aproveitar os portões vermelhos antes das multidões! Não é necessário subir a montanha inteira para ter uma experiência linda.",
        importante=["A entrada do teamLab Biovortex está marcada para as 16h30. Cheguem com antecedência e reservem cerca de 2h30 para a visita."]),
))
DATA["p3"].append(dict(
    label="26/10", date=dt(26, 10), title="Bate e volta em Nara",
    sub="Nara, antiga capital do Japão, famosa pelos cervos que circulam livremente pelo parque.",
    origin=None, dest_q="Nara Park, Nara",
    stops=[
        S("8h", "Bate e volta em Nara — Parque, Todai-ji e Kasuga Taisha", "Saiam de Kyoto por volta das 8h e sigam de trem para Nara. Comecem pelo Parque de Nara, onde os cervos circulam livremente (vocês podem comprar os biscoitinhos próprios para alimentá-los). Depois, conheçam o Templo Todai-ji, que abriga uma enorme estátua de Buda, e caminhem pelos jardins da região. Se estiverem dispostos, sigam até o Santuário Kasuga Taisha, conhecido pelos caminhos cercados de lanternas de pedra.", "templo", q="Todai-ji, Nara"),
        ALM("14h", "Almoço e tarde em Nara", "Almocem com calma e explorem as lojinhas e ruas tradicionais. Vale passar na Nakatanidou, famosa pelo mochi preparado na hora, e conhecer a região de Naramachi, com casinhas antigas, cafés e lojas charmosas. No fim da tarde, retornem para Kyoto.", "Naramachi, Nara"),
        JAN("20h", "Jantar tranquilo perto do hotel", "Sugestão: um jantar tranquilo perto do hotel e descanso, porque amanhã vocês seguem para Hiroshima.", "Kyoto Station, Kyoto"),
    ],
    guide=dict(
        locomover=["Hotel → Nara: caminhem até Kyoto Station e peguem o trem JR Miyakoji Rapid, da linha Nara, até JR Nara Station (45–50 min).",
                   "JR Nara → Parque de Nara: caminhada de 20–25 min ou ônibus local.",
                   "Parque → Todai-ji → Kasuga Taisha: a pé, aproveitando os jardins e os cervos.",
                   "Kasuga Taisha → Naramachi: caminhada de 25–30 min ou ônibus, se estiverem cansados.",
                   "Nara → Kyoto: retornem à JR Nara Station e peguem a linha JR Nara até Kyoto Station; depois a pé até o hotel."],
        comer=["Naramachi: ótima região para almoçar, com restaurantes tradicionais e cafés.",
               "Nakatanidou: famoso pelos mochis fresquinhos, uma parada deliciosa!"],
        dica="Os cervos de Nara são lindos, mas são animais selvagens! Se comprarem os biscoitos próprios para alimentá-los, guardem bem o restante e evitem provocá-los.",
        importante=["Amanhã vocês seguem para Hiroshima. Organizem o envio das malas grandes de Kyoto para o Travelodge Honmachi Osaka (onde ficam a partir de 29/10), levando apenas uma mala pequena para as duas noites em Hiroshima. Confirmem na recepção o prazo de entrega e se o hotel de Osaka aceita receber as bagagens antecipadamente."]),
))

# ───────────────────────── p4 · Hiroshima (27–29/10)
DATA["p4"].append(dict(
    label="27/10", date=dt(27, 10), title="Kyoto → Hiroshima e Parque Memorial da Paz",
    sub="Uma cidade marcada pela história e por uma emocionante mensagem de paz.",
    origin="Kyoto Station", dest_q="Hotel Vista, Hiroshima",
    stops=[
        S("9h", "Checkout + Shinkansen para Hiroshima", "Sigam a pé para a estação de Kyoto. Shinkansen às 9h46, com chegada prevista às 11h27 (bilhete já comprado).", "transporte", q="Kyoto Station", st="ok", stl="BILHETE COMPRADO"),
        ALM("11h27", "Chegada em Hiroshima + almoço (Okonomimura)", "Ao chegarem, deixem as malas no hotel e sigam para almoçar. Comecem experimentando o famoso okonomiyaki de Hiroshima, preparado em camadas com repolho, massa e macarrão. Sugestão: o Okonomimura, um prédio com vários pequenos restaurantes especializados nesse prato.", "Okonomimura, Hiroshima"),
        S("15h", "Parque Memorial da Paz", "Conheçam o Parque Memorial da Paz, um dos lugares mais importantes da história do Japão: a Cúpula da Bomba Atômica, o Monumento às Crianças e o Cenotáfio. Depois, entrem no Museu Memorial da Paz, que conta a história do bombardeio de Hiroshima. Reservem cerca de 1h30 a 2h. É um passeio emocionante, que merece ser feito sem pressa.", "passeio", q="Hiroshima Peace Memorial Park"),
        JAN("19h", "Jantar na região de Hondori", "Caminhem pela região de Hondori, cheia de lojas, restaurantes e izakayas. Hiroshima também é famosa pelas ostras, então vale experimentar em algum restaurante local!", "Hondori Shopping Street, Hiroshima"),
    ],
    guide=dict(
        locomover=["Hotel → Kyoto Station: a pé, poucos minutos.",
                   "Kyoto → Hiroshima: Shinkansen às 9h46, chegada às 11h27.",
                   "Hiroshima Station → Hotel Vista: tram (bonde) em direção ao centro, descendo em Hatchobori; depois, cerca de 5 min a pé.",
                   "Hotel → Parque Memorial da Paz: 15–20 min a pé ou tram até Genbaku Dome-mae.",
                   "Parque → Museu da Paz: cerca de 10 min a pé pelos jardins."],
        comer=["Okonomimura: edifício com vários restaurantes de okonomiyaki de Hiroshima.",
               "Centro de Hiroshima: boas opções de restaurantes e izakayas para o jantar."],
        dica="A visita ao Museu Memorial da Paz é intensa e emocionante. Reservem um tempo para conhecer tudo com calma, sem tentar encaixar muitos outros passeios no mesmo dia.",
        importante=["Como as malas grandes já seguiram para Osaka, viajem apenas com a bagagem necessária para as duas noites em Hiroshima. Amanhã é dia de Miyajima!"]),
))
DATA["p4"].append(dict(
    label="28/10", date=dt(28, 10), title="Miyajima",
    sub="Uma das ilhas mais encantadoras do Japão, com o torii vermelho que parece flutuar no mar.",
    origin=None, dest_q="Hiroshima Station",
    stops=[
        S("9h", "Bate e volta em Miyajima", "Após o café, sigam para a estação de Hiroshima e peguem o trem até Miyajimaguchi. De lá, atravessem de ferry até a ilha. Comecem pelo Santuário Itsukushima, construído sobre a água, e caminhem pelas ruas tradicionais, onde também há cervos circulando livremente.", "templo", q="Itsukushima Shrine, Miyajima"),
        S("11h", "Teleférico ao Monte Misen", "Se estiverem dispostos, subam de teleférico ao Monte Misen, com vista linda do Mar Interior de Seto. O teleférico não chega ao cume: ainda há uma caminhada com subidas e degraus. Façam isso mais cedo, pois o teleférico tem horário limitado; não deixem a subida para o fim da tarde.", "natureza", q="Miyajima Ropeway Momijidani Station"),
        ALM("13h30", "Almoço em Miyajima", "Experimentem o anago-meshi (arroz com enguia-do-mar grelhada, especialidade local). Também vale provar as famosas ostras grelhadas e o momiji manju, doce típico em formato de folha. A rua Omotesando é cheia de restaurantes e lojinhas.", "Omotesando Shopping Street, Miyajima"),
        S("15h", "Templo Daisho-in", "Se preferirem algo mais tranquilo, continuem explorando lojinhas, templos e paisagens. Vale conhecer o Templo Daisho-in, com seus jardins e pequenas estátuas. No fim da tarde, retornem para Hiroshima.", "templo", q="Daisho-in Temple, Miyajima"),
    ],
    guide=dict(
        locomover=["Hotel → Hiroshima Station: caminhem até Hatchobori e peguem o tram até Hiroshima Station (20–25 min).",
                   "Hiroshima → Miyajimaguchi: linha JR Sanyo (cerca de 30 min).",
                   "Miyajimaguchi → Miyajima: caminhem até o terminal e embarquem no ferry (cerca de 10 min).",
                   "Porto → Santuário Itsukushima: 10–15 min a pé pelas ruas da ilha.",
                   "Santuário → Monte Misen: a pé até a estação Momijidani do teleférico ou transporte de apoio, se disponível.",
                   "Miyajima → Hotel: façam o trajeto inverso, de ferry e trem JR."],
        comer=["Rua Omotesando: restaurantes e lojinhas para provar as especialidades da ilha.",
               "Ostras de Hiroshima: uma das comidas mais famosas da região.",
               "Momiji manju: doce típico em formato de folha de bordo."],
        importante=["Para subir o Monte Misen, façam isso mais cedo: o teleférico tem horário limitado e ainda há caminhada. Os cervos são animais selvagens, então evitem alimentá-los."]),
))

# ───────────────────────── p5 · Osaka (29/10–02/11)
DATA["p5"].append(dict(
    label="29/10", date=dt(29, 10), title="Hiroshima → Osaka e Dotonbori",
    sub="Chegada em uma das cidades mais animadas do Japão, com a noite em Dotonbori.",
    origin="Hotel Vista, Hiroshima", dest_q="Hiroshima Station",
    stops=[
        S("9h20", "Checkout + estação de Hiroshima", "Saiam do hotel perto das 9h20 e peguem o bonde ou táxi até a estação. Cheguem às catracas do Shinkansen 20 minutos antes. Shinkansen às 10h03, chegada em Shin-Osaka às 11h28 (bilhete já comprado).", "transporte", q="Hiroshima Station", st="ok", stl="BILHETE COMPRADO"),
        S("11h28", "Chegada em Osaka", "Após o check-in no hotel, a tarde é mais tranquila para se instalarem e começarem a explorar Osaka sem pressa. Se estiverem animados, passeiem pelas lojas e cafés da região de Shinsaibashi.", "hotel", q="Travelodge Honmachi Osaka", t="hotel"),
        JAN("19h", "Jantar em Dotonbori", "Dotonbori é a região mais famosa de Osaka, cheia de letreiros gigantes, restaurantes e ruas iluminadas. Não deixem de ver o painel do Glico Running Man e caminhar às margens do canal. Depois, passem pela charmosa Hozenji Yokocho, ruazinha de pedra com lanternas e pequenos restaurantes, e aproveitem para jantar por lá, experimentando especialidades de Osaka.", "Dotonbori, Osaka"),
    ],
    optional=[
        S("Tarde", "Opcional — Castelo de Osaka", "Se estiverem animados depois da viagem, aproveitem a tarde para conhecer o Castelo de Osaka e seus jardins, um dos principais cartões-postais da cidade (vale a visita mesmo só pela área externa). Se quiserem entrar, façam a visita durante a tarde. Se estiverem cansados, podem pular e seguir direto para Shinsaibashi e Dotonbori.", "passeio", q="Osaka Castle", t="city"),
    ],
    guide=dict(
        locomover=["Hotel → Hiroshima Station: caminhem até Hatchobori e peguem o tram até Hiroshima Station (20–25 min). Com malas, podem optar por táxi.",
                   "Hiroshima → Shin-Osaka: Shinkansen às 10h03, chegada às 11h28.",
                   "Shin-Osaka → Hotel: linha Midosuji até Honmachi (10–15 min) e depois a pé até o Travelodge.",
                   "Hotel → Shinsaibashi: linha Midosuji, de Honmachi até Shinsaibashi (1 parada), ou 15–20 min a pé.",
                   "Shinsaibashi → Dotonbori: a pé, 10–15 min.",
                   "Dotonbori → Hotel: linha Midosuji, de Namba até Honmachi, seguida de caminhada. Se preferirem, táxi.",
                   "Opcional · Castelo de Osaka: caminhem até Honmachi e peguem a linha Chuo até Tanimachi 4-chome (2 estações); depois, 15–20 min a pé até o castelo. Volta: linha Chuo até Hommachi, baldeação para Midosuji até Shinsaibashi."],
        comer=["Takoyaki: bolinhos de polvo, uma das especialidades mais famosas de Osaka.",
               "Okonomiyaki: espécie de panqueca japonesa preparada na chapa.",
               "Dotonbori: ótima região para experimentar comidas típicas e escolher um restaurante para jantar."],
        dica="Deixem Dotonbori para o fim da tarde e a noite, quando os letreiros ficam iluminados e a região ganha ainda mais vida!"),
))
DATA["p5"].append(dict(
    label="30/10", date=dt(30, 10), title="Kuromon, Shinsekai e compras",
    sub="Dia para explorar a gastronomia de Osaka, a capital da comida de rua japonesa.",
    origin=None, dest_q="Kuromon Ichiba Market, Osaka",
    stops=[
        S("9h", "Mercado Kuromon", "Um dos mais famosos de Osaka, cheio de barraquinhas com frutos do mar, espetinhos de wagyu, sushi e outras delícias japonesas. Experimentem algumas especialidades locais e passeiem sem pressa.", "passeio", q="Kuromon Ichiba Market, Osaka", website="https://kuromon.com/en/"),
        ALM("13h", "Almoço — Mizuno (okonomiyaki)", "Depois, sigam para Namba e Dotonbori. Sugestão: o Mizuno, um dos restaurantes mais tradicionais de Osaka para provar okonomiyaki. Se a fila estiver muito grande, o Fukutaro é uma ótima alternativa.", "Mizuno Okonomiyaki Dotonbori, Osaka"),
        S("15h", "Shinsekai + compras em Shinsaibashi", "Conheçam Shinsekai, bairro de atmosfera retrô com a famosa Torre Tsutenkaku. Vale experimentar o kushikatsu, os tradicionais espetinhos empanados de Osaka. Depois, sigam para Shinsaibashi, uma das melhores regiões para compras.", "passeio", q="Tsutenkaku Tower, Osaka"),
        JAN("19h", "Jantar na região de Ura-Namba", "Se ainda estiverem animados, jantem em Ura-Namba, conhecida pelos pequenos restaurantes e izakayas. Sugestão: não estender muito a noite, porque amanhã é dia de Universal Studios Japan!", "Ura-Namba, Osaka"),
    ],
    guide=dict(
        locomover=["Hotel → Mercado Kuromon: caminhem até Honmachi e peguem a linha Midosuji até Namba; depois, 10–15 min a pé.",
                   "Kuromon → Namba/Dotonbori: caminhada de 10–15 min.",
                   "Namba → Shinsekai: linha Midosuji, de Namba até Dobutsuen-mae, e cerca de 10 min a pé até a Torre Tsutenkaku.",
                   "Shinsekai → Shinsaibashi: linha Midosuji, de Dobutsuen-mae até Shinsaibashi.",
                   "Shinsaibashi → Ura-Namba: 15–20 min a pé ou metrô até Namba.",
                   "Namba → Hotel: linha Midosuji até Honmachi e caminhada até o Travelodge."],
        comer=["Mercado Kuromon: espetinhos de wagyu, sushi e outras especialidades.",
               "Mizuno (Dotonbori): tradicional okonomiyaki, sugestão para o almoço.",
               "Fukutaro: ótima alternativa caso a fila do Mizuno esteja grande.",
               "Shinsekai: experimentem o kushikatsu, os famosos espetinhos empanados."],
        dica="Osaka é uma cidade para experimentar comidas diferentes! Aproveitem o Mercado Kuromon sem pressa e deixem espaço para provar o okonomiyaki e o kushikatsu ao longo do dia."),
))
DATA["p5"].append(dict(
    label="31/10", date=dt(31, 10), title="Universal Studios Japan — Halloween",
    sub="Dia de diversão: cenários de Harry Potter, Super Nintendo World e a programação especial de Halloween.",
    origin=None, dest_q="Universal Studios Japan, Osaka",
    stops=[
        S("~9h", "Chegada ao parque", "Saiam cedo do hotel e tentem chegar ao parque cerca de 30–45 minutos antes da abertura oficial (confiram o horário no aplicativo da Universal, que é obrigatório no parque). Aproveitem a manhã para conhecer o parque e fazer atrações sem horário marcado no Express Pass. O Express Pass também inclui Harry Potter and the Forbidden Journey e atrações de escolha, como JAWS ou Jurassic Park e The Flying Dinosaur ou Minion Mayhem: confiram horários e condições nos ingressos.", "ingresso", q="Universal Studios Japan, Osaka", st="ok", stl="EXPRESS PASS COMPRADO"),
        S("11h50", "Flight of the Hippogriff", "Horário reservado: 11h50–12h20, na área de Harry Potter.", "ingresso", q="Universal Studios Japan, Osaka", st="ok", stl="HORÁRIO RESERVADO"),
        ALM("~12h30", "Almoço — Three Broomsticks", "Sugestão: aproveitem a área de Harry Potter para conhecer o Three Broomsticks, restaurante temático onde também podem experimentar a famosa cerveja amanteigada. No Super Nintendo World, vale conhecer o Kinopio's Cafe, se houver disponibilidade. Sem horário definido no roteiro.", "Universal Studios Japan, Osaka"),
        S("14h", "Super Nintendo World + Mario Kart", "Horários reservados: 14h–15h entrada no Super Nintendo World; 14h–14h30 Mario Kart: Koopa's Challenge; 14h30–15h Yoshi's Adventure.", "ingresso", q="Super Nintendo World, Universal Studios Japan, Osaka", st="ok", stl="HORÁRIO RESERVADO"),
        S("15h", "Mine Cart Madness (Donkey Kong)", "Horário reservado: 15h–15h30, na área de Donkey Kong.", "ingresso", q="Universal Studios Japan, Osaka", st="ok", stl="HORÁRIO RESERVADO"),
        S("17h", "Illumination's Villain-Con Minion Blast", "Horário reservado: 17h–17h30.", "ingresso", q="Universal Studios Japan, Osaka", st="ok", stl="HORÁRIO RESERVADO"),
        S("~19h", "Noite de Halloween", "Como é Halloween, o parque pode ter programação especial de terror e atrações temáticas. Se estiverem animados, aproveitem a experiência! Caso contrário, podem voltar mais cedo para descansar. Sem horário definido no roteiro.", "passeio", q="Universal Studios Japan, Osaka"),
    ],
    guide=dict(
        locomover=["Hotel → Universal: caminhem até Honmachi e peguem a linha Midosuji até Umeda; sigam as placas para a estação JR Osaka.",
                   "Osaka → Universal City: linha JR Osaka Loop, sentido Nishikujo, e baldeação para a JR Yumesaki Line até Universal City (alguns trens seguem direto).",
                   "Universal City → Parque: cerca de 5 min a pé.",
                   "Retorno: trajeto inverso, via JR Osaka e metrô Midosuji até Honmachi. Reservem 40–50 minutos por trecho."],
        comer=["Three Broomsticks: restaurante temático de Harry Potter, com a famosa cerveja amanteigada.",
               "Kinopio's Cafe: restaurante do Super Nintendo World, sujeito à disponibilidade."],
        dica="Cheguem ao parque antes da abertura e aproveitem a manhã para conhecer as atrações sem horário marcado. Organizem o passeio em torno dos horários do Express Pass, principalmente da entrada no Super Nintendo World!",
        importante=["O Express Pass já está comprado, com horários reservados para Flight of the Hippogriff, Mario Kart, Yoshi, Mine Cart Madness e Minion Blast. Confiram todos os horários no ingresso e deixem os QR Codes salvos no celular. A entrada no Super Nintendo World está marcada para 14h–15h."]),
))
DATA["p5"].append(dict(
    label="01/11", date=dt(1, 11), title="Bate e volta a Kobe + Umeda Sky Building",
    sub="Dia para provar a autêntica carne de Kobe e terminar com uma vista panorâmica de Osaka.",
    origin=None, dest_q="Sannomiya Station, Kobe",
    stops=[
        S("10h", "Bate e volta a Kobe — carne de Kobe no Mouriya Honten", "ANTES de sair: consultem a recepção sobre o envio das malas grandes para o Daiwa Roynet Hotel Tokyo Kyobashi Premier, onde ficam a partir de 02/11. Confirmem o prazo de entrega; se não for possível garantir a chegada em 02/11, levem as malas no Shinkansen. Hoje podem começar um pouco mais tarde! Sigam de trem para Kobe, cidade portuária a cerca de 30 minutos de Osaka. A grande experiência do dia é provar a famosa carne de Kobe, preparada na chapa por um chef. Sugestão: o Mouriya Honten, restaurante tradicional especializado nessa carne. Recomendo reservar antecipadamente. Depois, caminhem pela região do porto e pelo Meriken Park. Se animados, explorem o bairro de Kitano, de casarões históricos, mas priorizem o porto para não deixar o dia corrido.", "almoço", q="Mouriya Honten, Kobe", t="lunch", website="https://www.mouriya.co.jp/", st="warn", stl="RESERVAR"),
        S("15h30", "Retorno a Osaka", "Retornem a Osaka no fim da tarde.", "transporte", q="Osaka Station"),
        S("16h30", "Umeda Sky Building (pôr do sol)", "Observatório com uma vista panorâmica incrível da cidade. Sugestão: subir por volta das 16h30 para acompanhar o pôr do sol, previsto para perto das 17h. Assim vocês veem Osaka de dia e a cidade se iluminando!", "passeio", q="Umeda Sky Building, Osaka"),
        JAN("~18h30", "Jantar em Umeda ou Kitashinchi", "Regiões cheias de restaurantes e bares japoneses, próximas ao observatório.", "Kitashinchi, Osaka"),
    ],
    guide=dict(
        locomover=["Hotel → Kobe: caminhem até Honmachi e peguem a linha Midosuji até Umeda. Na estação JR Osaka, embarquem no JR Special Rapid até Sannomiya (cerca de 25 min).",
                   "Sannomiya → Mouriya Honten: 5–10 min a pé.",
                   "Mouriya → Meriken Park: 20–25 min a pé ou táxi.",
                   "Kobe → Osaka: retornem à estação JR Sannomiya e peguem o JR Special Rapid até Osaka.",
                   "Osaka Station → Umeda Sky Building: 10–15 min a pé.",
                   "Umeda → Hotel: linha Midosuji até Honmachi e caminhada até o Travelodge."],
        comer=["Mouriya Honten: carne de Kobe. Recomendo reservar antecipadamente.",
               "Jantar: restaurantes de Umeda ou Kitashinchi, próximos ao observatório."],
        dica="Tentem chegar ao Umeda Sky Building antes do pôr do sol, previsto para perto das 17h.",
        importante=["Amanhã vocês retornam a Tóquio! Consultem a recepção sobre o envio das malas grandes para o hotel em Tokyo Kyobashi. Confirmem o prazo de entrega; se não houver garantia de chegada no dia 02/11, levem as malas no Shinkansen.",
                    "A partir de 01/11 muda o sistema de Tax Free (veja o Guia): o reembolso passa a ser pedido no aeroporto, na saída do Japão."]),
))

# ───────────────────────── p6 · Tóquio (02–05/11)
DATA["p6"].append(dict(
    label="02/11", date=dt(2, 11), title="Osaka → Tóquio, Marunouchi e Nihonbashi",
    sub="Volta a Tóquio para os últimos dias, com a fachada histórica da Estação de Tóquio e bairros que misturam tradição e modernidade.",
    origin="Travelodge Honmachi Osaka", dest_q="Shin-Osaka Station",
    stops=[
        S("9h", "Checkout + Shinkansen para Tóquio", "Após o café, façam o checkout e sigam para a estação Shin-Osaka. Shinkansen às 10h06, chegada em Tóquio às 12h33 (bilhete comprado). Durante a viagem, se o céu estiver limpo, vocês poderão avistar o Monte Fuji pela janela (no sentido Osaka → Tóquio, a vista costuma ficar do lado esquerdo do trem). Sigam para o hotel (10–15 min a pé da Estação de Tóquio ou táxi com as malas) e deixem as bagagens.", "transporte", q="Shin-Osaka Station", st="ok", stl="BILHETE COMPRADO"),
        ALM("14h", "Almoço — 400°C Pizza", "Prioridade para o almoço, ainda sem reserva confirmada. Como depende de confirmação, mantenham os passeios da tarde flexíveis.", "400°C Pizza Kagurazaka, Tokyo", website="https://400do-pizza.com/", st="warn", stl="RESERVA A CONFIRMAR"),
        S("16h", "Marunouchi + Muromachi e Nihonbashi", "Comecem pela região da Estação de Tóquio, famosa pela fachada histórica de tijolos vermelhos. Vale subir ao terraço do KITTE, com vista linda da estação, e caminhar por Marunouchi, região elegante, cheia de lojas e cafés. Se estiverem dispostos, continuem até Nihonbashi, com lojas tradicionais, a famosa Mitsukoshi e o complexo Coredo Muromachi.", "passeio", q="KITTE Marunouchi, Tokyo"),
        JAN("20h", "Jantar — Ten Yokota Asue", "Sugestão para um jantar especial de tempurá japonês.", "Ten Yokota Asue, Tokyo", ig="tenyokota_asue"),
    ],
    guide=dict(
        locomover=["Hotel → Shin-Osaka: caminhem até Honmachi e peguem a linha Midosuji, sentido Shin-Osaka (cerca de 15 min).",
                   "Shin-Osaka → Tokyo Station: Shinkansen às 10h06, chegada às 12h33.",
                   "Tokyo Station → Hotel: 10–15 min a pé até o Daiwa Roynet Tokyo Kyobashi Premier, ou táxi com as malas.",
                   "Hotel → 400°C Pizza (Kagurazaka): linha Ginza de Kyobashi até Nihombashi e linha Tozai até Kagurazaka (cerca de 20 min).",
                   "400°C Pizza → Marunouchi/KITTE: linha Tozai de Kagurazaka até Otemachi e caminhada de 10 min.",
                   "Marunouchi → Nihonbashi/Muromachi: caminhada de 15–20 min.",
                   "Nihonbashi → Hotel: linha Ginza, de Mitsukoshimae até Kyobashi, seguida de caminhada."],
        comer=["400°C Pizza: prioridade para o almoço, ainda sem reserva confirmada.",
               "Ten Yokota Asue: sugestão para um jantar especial de tempurá japonês."],
        importante=["Confirmem o recebimento das malas no hotel de Tóquio, caso tenham usado o serviço de envio."]),
))
DATA["p6"].append(dict(
    label="03/11", date=dt(3, 11), title="Yanaka, Nezu, Ueno e Yakiniku Ushigoro",
    sub="Hoje é o Dia da Cultura, feriado nacional no Japão. Um lado mais tradicional e tranquilo de Tóquio, com jantar especial reservado em Ginza.",
    origin=None, dest_q="Yanaka Ginza, Tokyo",
    stops=[
        S("9h", "Passeio por Yanaka", "Hoje é feriado nacional (Dia da Cultura): algumas regiões podem estar mais movimentadas. Comecem por Yanaka, um dos bairros mais tradicionais de Tóquio, com ruazinhas antigas, pequenos templos e lojas artesanais. Passeiem pela Yanaka Ginza, rua comercial cheia de lojinhas e comidinhas: experimentem os croquetes de carne e os doces típicos.", "passeio", q="Yanaka Ginza, Tokyo"),
        ALM("13h", "Almoço em Yanaka", "Sugestão: almoçar pela própria região, escolhendo um dos pequenos restaurantes ou aproveitando as comidinhas da Yanaka Ginza.", "Yanaka Ginza, Tokyo"),
        S("15h", "Santuário Nezu + Parque de Ueno", "Sigam para o Santuário Nezu, famoso pelos caminhos de portões vermelhos e jardins tranquilos. Continuem até o Parque de Ueno, um dos mais conhecidos de Tóquio, onde fica o Lago Shinobazu. Deixem um tempinho para descansar antes do jantar.", "templo", q="Nezu Shrine, Tokyo"),
        JAN("19h", "Jantar — Yakiniku Ushigoro Ginza", "Reserva confirmada para 2 pessoas, às 19h, em lugares no balcão. Endereço: Kirarito Ginza, 7º andar, 1-8-19 Ginza, Chuo-ku. A reserva é apenas da mesa, sem menu previamente escolhido, e a ocasião informada foi o casamento de vocês. Cheguem com cerca de 10 minutos de antecedência e tenham a confirmação da reserva salva no celular. Wagyu japonês.", "Yakiniku Ushigoro Ginza, Kirarito Ginza, Tokyo", website="https://ushigoro.com/shop/ginza/", st="ok", stl="RESERVA CONFIRMADA"),
    ],
    optional=[
        S("Tarde", "Opcional — Museu Nacional de Tóquio", "Se tiverem interesse em museus, o Museu Nacional de Tóquio, no Parque de Ueno, é uma boa opção, mas a agência deixaria como passeio opcional.", "passeio", q="Tokyo National Museum, Ueno", t="city"),
    ],
    guide=dict(
        locomover=["Hotel → Yanaka: linha Ginza de Kyobashi até Ueno e JR Yamanote por 2 estações até Nippori.",
                   "Yanaka → Santuário Nezu: caminhada de 20–25 min ou táxi.",
                   "Nezu → Parque de Ueno: caminhada de 15–20 min.",
                   "Ueno → Hotel: linha Ginza, de Ueno até Kyobashi, seguida de caminhada.",
                   "Hotel → Ushigoro Ginza: caminhada de 10–15 min ou táxi."],
        comer=["Yanaka Ginza: croquetes, doces e comidinhas de rua para o almoço.",
               "Yakiniku Ushigoro Ginza: jantar especial com wagyu japonês. Reserva confirmada!"],
        dica="Hoje é o Dia da Cultura, feriado nacional no Japão, então algumas regiões podem estar mais movimentadas. Aproveitem Yanaka sem pressa e deixem um tempinho para descansar antes do jantar!"),
))
DATA["p6"].append(dict(
    label="04/11", date=dt(4, 11), title="Tsukiji, Nakameguro e último jantar",
    sub="Último dia inteiro no Japão: mercado de sushi, um bairro charmoso com canal e as últimas comprinhas em Ginza.",
    origin=None, dest_q="Tsukiji Outer Market, Tokyo",
    stops=[
        S("10h", "Mercado Externo de Tsukiji + Nakameguro", "Comecem pelo Mercado Externo de Tsukiji, famoso pelas barraquinhas de comida japonesa: sushi fresco, tamagoyaki (omelete japonês), frutos do mar e outras especialidades. Depois, sigam para Nakameguro, bairro charmoso com cafés, lojinhas e um canal arborizado, perfeito para caminhar. Atenção: saiam de Nakameguro por volta das 12h50 para chegar com folga ao almoço das 13h30 em Ginza.", "passeio", q="Tsukiji Outer Market, Tokyo", website="https://www.tsukiji.or.jp/english/"),
        ALM("13h30", "Almoço — Rare Tendon Ginza Mitsuyoshi", "Reserva confirmada para 2 pessoas, às 13h30, na unidade principal de Ginza. Tradicional tempurá sobre arroz. Cheguem com cerca de 10 minutos de antecedência e deixem a confirmação da reserva salva no celular (o código está no e-mail de confirmação).", "Rare Tendon Ginza Mitsuyoshi, Tokyo", st="ok", stl="RESERVA CONFIRMADA"),
        S("15h", "Retorno ao hotel", "Retornem ao hotel por volta das 15h para organizar as malas e descansar antes do jantar. Aproveitem para fazer as últimas comprinhas em Ginza.", "hotel", q="Daiwa Roynet Hotel Tokyo Kyobashi Premier", t="hotel"),
        JAN("19h", "Jantar — Ginza Kyubey", "Sugestão para um último jantar especial de sushi.", "Ginza Kyubey, Tokyo", website="https://www.kyubey.jp/"),
    ],
    guide=dict(
        locomover=["Hotel → Tsukiji: caminhem até Takaracho e peguem a linha Toei Asakusa até Higashi-Ginza; depois, cerca de 10 min a pé.",
                   "Tsukiji → Nakameguro: caminhem até Higashi-Ginza, peguem a linha Hibiya até Naka-meguro (25–30 min).",
                   "Nakameguro → Ginza: linha Hibiya direto até Ginza (cerca de 20 min). O Rare Tendon fica a 4 min a pé da estação Ginza.",
                   "Ginza → Hotel: caminhada de 10–15 min."],
        comer=["Mercado de Tsukiji: sushi fresco, tamagoyaki e outras especialidades.",
               "Rare Tendon Ginza Mitsuyoshi: almoço reservado para experimentar o tradicional tempurá sobre arroz.",
               "Ginza Kyubey: sugestão para um último jantar especial de sushi."],
        importante=["Rare Tendon Ginza Mitsuyoshi: reserva confirmada para 2 pessoas, às 13h30. Saiam de Nakameguro por volta das 12h50.",
                    "Compras com tax free a partir de 01/11: o reembolso é pedido no aeroporto, antes do embarque. Guardem as notas e os produtos intactos (veja o Guia)."]),
))
DATA["p6"].append(dict(
    label="05/11", date=dt(5, 11), title="Despedida do Japão — Tóquio → EUA → Brasil",
    sub="Dia de se despedir do Japão: saída do hotel às 7h rumo ao Aeroporto de Haneda.",
    origin="Daiwa Roynet Hotel Tokyo Kyobashi Premier", dest_q="Haneda Airport Terminal 3, Tokyo",
    stops=[
        S("7h", "Checkout + ida ao aeroporto de Haneda", "Sugestão: acordar por volta das 6h30, fazer o checkout e sair do hotel às 7h. Transporte público: caminhem até a estação Takaracho e peguem um trem da linha Toei Asakusa com serviço direto pela Keikyu até Haneda (confiram o destino do trem e o terminal indicado na passagem; 40–50 min, incluindo a caminhada). Táxi: alternativa mais confortável com as malas. Cheguem com cerca de 3 horas de antecedência, por causa do Tax Free, despacho das malas, segurança e imigração. Nas compras feitas a partir de 01/11 será necessário validar a saída dos produtos do Japão para receber o reembolso.", "transporte", q="Haneda Airport Terminal 3, Tokyo"),
        S("11h05", "Voo Tóquio (HND) → Nova York (JFK)", "Japan Airlines. Embarque 05/11 às 11h05, chegada 05/11 às 9h50 (mesmo dia, por causa do fuso).", "transporte", q="Haneda Airport Terminal 3, Tokyo"),
        S("18h35", "Voo Nova York (JFK) → São Paulo (GRU)", "American. Embarque 05/11 às 18h35, chegada 06/11 às 6h05.", "transporte", q="John F. Kennedy International Airport"),
        S(None, "06/11 · 13h05 — Voo São Paulo (GRU) → Recife (REC)", "Azul. Embarque 06/11 às 13h05, chegada às 16h10.", "transporte", q="Guarulhos International Airport"),
    ],
    guide=dict(
        importante=["Pesem as malas antes do voo de volta. Lojas como a Don Quijote vendem balança de mão. Facas japonesas e líquidos vão sempre na mala despachada.",
                    "A volta passa pelos EUA (JFK): reservem tempo para imigração e conexão."]),
))
