# -*- coding: utf-8 -*-
import html

IG = "https://www.instagram.com/%s/"


def a(label, url):
    return '<a href="%s">%s</a>' % (html.escape(url, quote=True), html.escape(label))


def ul(items):
    return "<ul>" + "".join("<li>%s</li>" % i for i in items) + "</ul>"


def sec(title, body, open_=False):
    return '<details class="dsec"%s><summary>%s</summary>%s</details>' % (" open" if open_ else "", title, body)


def rest_list(groups):
    out = ""
    for title, items in groups:
        out += "<p><b>%s</b></p>" % html.escape(title)
        li = []
        for name, desc, url in items:
            nm = a(name, url) if url else html.escape(name)
            li.append(nm + (" — " + html.escape(desc) if desc else ""))
        out += ul(li)
    return out


TOQUIO = [
    ("Sugestões", [
        ("Sushi no Midori", "sushi tradicional", "https://www.sushinomidori.co.jp/"),
        ("Ichiran", "ramen tonkotsu", "https://en.ichiran.com/shop/area-tokyo.html"),
        ("Sushi Zanmai", "sushi casual", "https://tabelog.com/en/tokyo/A1313/A131301/13002302/"),
        ("Omoide Yokocho", "vielas de izakayas em Shinjuku", "https://en.shinjuku-omoide.com/"),
        ("Tempura Tsunahachi", "", "https://www.tunahachi.co.jp/en/"),
        ("Yakitori Kufuraku", "", "https://kuuraku-ginza.jp/"),
        ("Ten Yokota Asue", "tempurá", IG % "tenyokota_asue"),
        ("Daikokuya", "tendon clássico de Asakusa", None),
        ("Hikiniku to Come", "hambúrguer japonês", "https://hikinikutocome.com/"),
        ("Tonkatsu Maisen", "porco empanado", "https://mai-sen.com/"),
        ("Gyukatsu Motomura", "bife empanado", None),
        ("Marion Crepes", "", "https://www.marion.co.jp/store/tokyo/"),
        ("Afuri", "ramen com yuzu", "https://www.afuriramen.com/"),
        ("Udon Shin", "", IG % "udon_shin.official"),
        ("Mercado Externo de Tsukiji", "", "https://www.tsukiji.or.jp/english/"),
    ]),
    ("Premiados e clássicos", [
        ("Konjiki Hototogisu", "", IG % "konjikihototogisu"),
        ("Nakiryu", "", IG % "nakiryusg"),
        ("Tonkatsu Hasegawa", "", "https://tabelog.com/en/tokyo/A1312/A131201/13019126/"),
        ("Tsuta", "", "https://www.tsuta.com/"),
        ("Ginza Kagari", "ramen cremoso de frango", IG % "kagari_honten"),
        ("Yakiniku Ushigoro Ginza", "wagyu japonês", "https://ushigoro.com/shop/ginza/"),
    ]),
    ("Omakase em Tóquio", [
        ("Sushi Han", "", "https://www.tablecheck.com/en/sushi-han"),
        ("Sushi Tokyo Ten", "", "https://sushitokyo-ten.com/"),
        ("Otaru Masazushi Ginza", "", "https://en.masazushi.co.jp/shop-ginza/"),
        ("Ebisu Kicho (Ebisu)", "", "https://tabelog.com/en/tokyo/A1303/A130302/13207465/"),
        ("Sushi Kusumi", "", "https://ginza-kusumi.jp/en/"),
        ("Ginza Kyubey", "", "https://kyubey.jp/"),
        ("Ginza Sushi Aoki", "", "https://www.sushiaoki.jp/en/oshinagaki.html"),
    ]),
]
KYOTO = [
    ("Experiência com reserva", [
        ("Gion Karyo", "", "http://www.karyo-kyoto.jp/gion/"),
        ("Mishima-tei (Teramachi)", "sukiyaki de wagyu", "https://kyoto-mishimatei.com/"),
        ("Mouriya Gion", "", "https://www.mouriya.co.jp/"),
        ("Sukiyaki Iroha", "", "https://www.sukiyaki-iroha.com/"),
        ("Shoraian", "tofu japonês, em Arashiyama", "https://www.shoraian.jp/"),
    ]),
    ("Sugestões", [
        ("Menya Inoichi", "ramen", "https://menyainoichi.net/"),
        ("Katsukura", "tonkatsu de Kyoto", "https://www.katsukura.jp/shops/sanjo/"),
        ("Kyoto Ramen Koji", "", "https://www.kyoto-station-building.co.jp/ramen_koji/"),
        ("Okutan Kiyomizu", "", "https://www.tofuokutan.info/"),
        ("Izuu", "", "https://www.izuu.jp/english/"),
        ("Shinpuku Saikan Honten", "", "https://tabelog.com/en/kyoto/A2601/A260101/26000791/"),
        ("Honke Daiichi Asahi", "", "https://www.honke-daiichiasahi.com/"),
        ("Yudofu Sagano", "", "https://kyoto-sagano.jp/"),
    ]),
    ("Doces e cafés", [
        ("Kagizen Yoshifusa", "", "https://www.kagizen.co.jp/"),
        ("Gion Tokuya", "", "https://gion-tokuya.jp/"),
        ("Tsujiri Gion", "", "https://www.giontsujiri.co.jp/en/"),
        ("% Arabica Arashiyama", "", "https://arabica.com/en/location/arabica-kyoto-arashiyama/"),
    ]),
]
OSAKA = [
    ("Experiência com reserva", [
        ("Matsusaka Gyu Yakiniku M", "", "https://matsusaka-projects.com/english/"),
        ("Sushi Nobutaka", "", IG % "sushi.nobutaka"),
        ("Mouriya Honten (Kobe)", "", "https://www.mouriya.co.jp/"),
        ("Hozenji Sushidokoro Nakatani", "", "https://tabelog.com/en/osaka/A2701/A270202/27084853/"),
    ]),
    ("Premiados", [
        ("Mizuno", "okonomiyaki desde 1945", None),
        ("Fukutaro", "negiyaki", "https://2951.jp/en/"),
        ("Kiji", "okonomiyaki em Umeda", "https://tabelog.com/en/osaka/A2701/A270101/27000322/"),
    ]),
    ("Sugestões", [
        ("Kushikatsu Daruma", "espetinhos empanados", None),
        ("Wanaka", "takoyaki", "https://takoyaki-wanaka.com/en/index.html"),
        ("Dotonbori Imai", "udon clássico", "https://tabelog.com/en/osaka/A2701/A270202/27001289/"),
        ("Harukoma", "sushi popular (só dinheiro)", None),
        ("Hokkyokusei", "omurice", "https://www.hokkyokusei.online/shinsaibashi"),
        ("Gyukatsu Motomura Namba", "bife empanado", "https://tabelog.com/en/osaka/A2701/A270202/27087004/"),
        ("Endo Sushi", "sushi de mercado", "https://www.endo-sushi.com/"),
        ("Mercado Kuromon", "comida de rua", "https://kuromon.com/en/"),
        ("Kinryu Ramen", "ramen do dragão", "https://kinryuramen.com/"),
        ("Kani Doraku", "caranguejo, o do letreiro gigante", "https://douraku.co.jp/en/"),
    ]),
    ("Doces e cafés", [
        ("551 Horai", "pãozinho de porco no vapor", "https://www.551horai.co.jp/"),
        ("Rikuro Ojisan", "cheesecake fofinho", "https://www.rikuro.co.jp/en/"),
    ]),
]


def build(H):
    parts = []
    parts.append(sec("✅ Checklist pré-viagem", ul([
        "<b>Passaporte com chip</b>, válido durante toda a viagem. Brasileiros não precisam de visto para turismo no Japão por até 90 dias (isenção prorrogada até setembro de 2029, vale para passaporte com chip).",
        "<b>Visto americano válido.</b> As conexões em Dallas e Nova York exigem passar pela imigração dos Estados Unidos, retirar as malas e despachar de novo.",
        "<b>Seguro viagem:</b> não é exigido para entrar no Japão, mas é essencial (atendimento médico no Japão e nos EUA é caro). Levem a apólice salva no celular.",
        "<b>Internet:</b> o eSIM é a opção mais prática. Comprem e instalem no Brasil, para ativar quando pousarem.",
        "<b>Visit Japan Web</b> (site oficial do governo japonês): preencham antes do embarque os dados do passaporte, do voo e do primeiro hotel, e a declaração da alfândega. Vocês recebem dois QR Codes (imigração e alfândega): salvem os dois em print.",
    ]), True))
    hot = ""
    for k in ["p1", "p2", "p3", "p4", "p5", "p6"]:
        h = H[k]
        extra = "".join(" · " + x for x in [a("Site", h["website"]) if h.get("website") else "", html.escape(h["phone"]) if h.get("phone") else ""] if x)
        hot += "<li><b>%s</b><br>%s<br>Check-in %s · Check-out %s%s</li>" % (html.escape(h["name"]), html.escape(h["addr"]), h["din"], h["dout"], extra)
    parts.append(sec("🏨 Hotéis", "<ul>" + hot + "</ul>"))
    parts.append(sec("✈️ Voos", ul([
        "<b>Ida:</b> São Paulo (GRU) → Dallas (DFW), American: embarque 16/10 às 22h, chegada 17/10 às 6h20. Dallas (DFW) → Tóquio Haneda (HND), American: embarque 17/10 às 10h30, chegada 18/10 às 14h20.",
        "<b>Volta:</b> Tóquio (HND) → Nova York (JFK), Japan Airlines: embarque 05/11 às 11h05, chegada 05/11 às 9h50. Nova York (JFK) → São Paulo (GRU), American: embarque 05/11 às 18h35, chegada 06/11 às 6h05. São Paulo (GRU) → Recife (REC), Azul: embarque 06/11 às 13h05, chegada às 16h10.",
    ])))
    parts.append(sec("🛬 Chegada e imigração", "<p>Ao chegar, não é mais necessário apresentar comprovantes como antigamente. No avião, os comissários costumam distribuir dois formulários (imigração e alfândega), mas é mais prático preencher tudo online antes da viagem no Visit Japan Web.</p>" + ul([
        "Os atendentes encaminham vocês para filas diferentes: quem tem formulário em papel e quem já fez o cadastro online (QR Codes).",
        "<b>Inspeção inicial:</b> pode haver uma rápida verificação de saúde, e os agentes orientam se necessário.",
        "<b>Controle de imigração:</b> apresentem o passaporte e o QR Code do Visit Japan Web. Após a validação é concedida a Landing Permission.",
        "<b>Bagagens:</b> sigam para a área de Baggage Claim para retirar as malas despachadas.",
        "<b>Alfândega:</b> normalmente basta apresentar o QR Code da declaração; em alguns casos os agentes podem pedir a abertura da mala.",
        "Por fim, sigam para a área de desembarque. Tenham os documentos de entrada e o endereço do hotel à mão.",
    ])))
    parts.append(sec("💴 Dinheiro e Tax Free", "<p>A moeda é o iene (¥). Como referência, <b>¥1.000 equivalem a cerca de R$ 31</b>.</p>" + ul([
        "Cartões são aceitos na maioria das lojas, hotéis, estações e restaurantes. Wise e Nomad funcionam bem.",
        "Restaurantes pequenos, barraquinhas de mercado e templos muitas vezes só aceitam dinheiro. Comecem com uns ¥30.000 em espécie e reponham conforme o uso.",
        "<b>Onde sacar:</b> nos caixas da 7-Eleven (Seven Bank) e dos correios (Japan Post), que aceitam cartões estrangeiros. Há 7-Eleven em praticamente toda esquina!",
        "<b>Tax Free, atenção à mudança:</b> até 31/10, em lojas Tax Free, compras acima de ¥5.000 por loja, no mesmo dia, têm o imposto de 10% descontado direto no caixa (apresentem o passaporte físico). A partir de 01/11, vocês pagam o preço cheio e pedem o reembolso na alfândega, no aeroporto, antes do check-in do voo de volta. No sistema novo, os produtos precisam estar intactos e sem uso; se faltar algum item de uma nota, a isenção cai para a nota inteira. Por isso, vale concentrar as compras maiores até 31/10.",
        "Dinheiro e cartões devem ser entregues com as duas mãos ou colocados na bandejinha do caixa.",
    ])))
    parts.append(sec("🚆 Transporte público", "<p>Os apps Google Maps e Japan Travel (Navitime) ajudam muito a planejar rotas e horários.</p>" + ul([
        "<b>Metrô</b> (rápido e muito usado em Tóquio e Osaka), <b>trens urbanos</b> (JR e privados), <b>ônibus</b> (muito usados em Kyoto, principalmente para chegar aos templos) e <b>táxis</b> (seguros e confortáveis, mas mais caros).",
        "<b>Suica / Pasmo / Icoca:</b> cartões recarregáveis que funcionam em metrô, trens, ônibus e lojas de conveniência. No iPhone, o Suica pode ser adicionado direto na carteira; basta encostar o celular na catraca ao entrar e ao sair. Sempre passem o cartão ao entrar e sair das estações para validar o trajeto.",
        "<b>Google Maps:</b> mostra linha, plataforma, horário e até a saída certa da estação. Estações grandes têm dezenas de saídas, então confiram sempre o número (exit).",
        "<b>Shinkansen (trem-bala):</b> os trechos de vocês já estão comprados pelo SmartEX. O Shinkansen tem catracas próprias, sinalizadas em azul, dentro das estações. O bilhete indica o número do carro e do assento; na plataforma, o chão mostra onde cada carro para. Cheguem 15 a 20 minutos antes, porque o trem para por pouco tempo.",
        "<b>Etiqueta:</b> silêncio no trem e nada de ligações; mochila na frente do corpo quando estiver cheio; esperem nas marcações do chão e deixem as pessoas saírem primeiro; na escada rolante, fiquem parados à esquerda em Tóquio e à direita em Osaka.",
        "<b>Dica:</b> no metrô não se come. No Shinkansen pode, e o ekiben (a marmita de trem) faz parte da experiência!",
    ])))
    parts.append(sec("📱 Aplicativos essenciais", ul([
        "Google Maps: rotas, horários e plataformas",
        "Google Tradutor: use a câmera para ler cardápios",
        "Carteira do iPhone (Suica): transporte e pagamentos",
        "SmartEX: bilhetes do Shinkansen",
        "App oficial da Universal Studios Japan: obrigatório no parque",
        "Klook: ingressos e atrações",
        "GO: para chamar táxi",
    ]) + "<p>Baixem tudo, criem as contas e testem antes de embarcar. Levem também uma bateria portátil, porque o celular será usado o dia inteiro!</p>"))
    parts.append(sec("🍂 Clima no Japão", "<p><b>Outono japonês: dias agradáveis, noites fresquinhas e paisagens lindas!</b></p>" + ul([
        "<b>Temperaturas:</b> em média, 10°C a 23°C nas cidades. Na região do Monte Fuji, pode fazer menos de 5°C à noite.",
        "<b>Chuvas:</b> podem ocorrer chuvas leves ou passageiras, embora outubro e novembro sejam geralmente menos chuvosos que o verão.",
        "<b>Dicas:</b> levem roupas em camadas, casaco de meia-estação e tênis confortáveis. Para o Monte Fuji e os passeios noturnos, incluam um casaco mais quente. Um guarda-chuva compacto também é útil.",
    ])))
    parts.append(sec("🙇 Etiqueta no Japão", ul([
        "Tirem os sapatos ao entrar em casas, alguns restaurantes e templos.",
        "Evitem falar alto em transporte público.",
        "Não comam andando na rua (prefiram parar para comer).",
        "Formem filas sempre que necessário.",
        "Dinheiro e cartões devem ser entregues com as duas mãos ou colocados na bandejinha do caixa.",
    ])))
    parts.append(sec("ℹ️ Informações úteis", ul([
        "<b>Vacinas:</b> não é exigido nenhum tipo de vacina para entrada no país.",
        "<b>Tomadas:</b> voltagem de 100V e tomadas tipo A (pino achatado), semelhantes às dos Estados Unidos.",
        "<b>Segurança:</b> o Japão é um país extremamente seguro, com baixos índices de criminalidade.",
        "<b>Água:</b> a água da torneira é potável.",
        "<b>Banheiros:</b> os famosos banheiros japoneses têm várias funções no assento (jato de água, aquecimento etc.).",
        "<b>Bagagem:</b> pesem as malas antes do voo de volta (lojas como a Don Quijote vendem balança de mão). Facas japonesas e líquidos vão sempre na mala despachada.",
    ])))
    parts.append(sec("🍜 Culinária local", "<p>Muitos restaurantes exibem réplicas dos pratos nas vitrines: basta apontar o prato ou mostrar uma foto ao atendente. Em alguns lugares o pedido é feito em máquinas na entrada (escolhe o prato, paga e entrega o ticket ao atendente). Nos mercados e lojas de conveniência há refeições prontas chamadas bento. Há também máquinas automáticas espalhadas pelas cidades, que vendem desde bebidas e café até pequenos lanches.</p><p><b>Comidas para provar em Tóquio:</b></p>" + ul([
        "Ramen: sopa de macarrão com caldo rico e aromático.",
        "Sushi e sashimi: peixes extremamente frescos.",
        "Tempura: frutos do mar e vegetais empanados com massa leve e crocante.",
        "Tonkatsu: carne de porco empanada e frita.",
        "Gyoza: pequenos dumplings grelhados ou cozidos.",
        "Okonomiyaki: espécie de panqueca japonesa com repolho, carne ou frutos do mar.",
        "Matcha e sobremesas japonesas: doces de chá verde, mochis e outras sobremesas tradicionais.",
    ])))
    parts.append(sec("🍣 Restaurantes sugeridos — Tóquio", rest_list(TOQUIO)))
    parts.append(sec("🍵 Restaurantes sugeridos — Kyoto", rest_list(KYOTO)))
    parts.append(sec("🐙 Restaurantes sugeridos — Osaka", rest_list(OSAKA)))
    return "".join(parts)
