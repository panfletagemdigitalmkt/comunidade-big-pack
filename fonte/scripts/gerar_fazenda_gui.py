# Fazenda BIG — telas personalizadas (técnica "fundo por fonte").
# Cada tela é um baú de 6 linhas (176x222). O fundo inteiro é um glyph da fonte big:gui colocado no título;
# os botões são itens com item_model big:gui/* em cima dos slots. Textos que mudam vão no título e nos tooltips.
#   font/gui.json           -> glyphs dos fundos (U+E100..) e espaços negativos (U+E000..)
#   textures/font/gui/*.png -> fundos 176x222
#   items|models|textures   -> big:gui/<ícone> (16x16) e big:gui/grande_<cultura> (colheita ampliada)
# Rodar da pasta fonte/:  python3 scripts/gerar_fazenda_gui.py
import json, os
from PIL import Image, ImageDraw

R = 'assets/big'
for d in ('font', 'textures/font/gui', 'textures/item/gui', 'models/item/gui', 'items/gui'):
    os.makedirs(f'{R}/{d}', exist_ok=True)


def hx(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


# paleta das maquetes aprovadas
PAINEL, FUNDO, MOLDURA, ESCURO, CANTO = hx('2a1d14'), hx('1f150e'), hx('84cc16'), hx('1a120b'), hx('eab308')
BORDA, ROTULO, POCO, POCO_BORDA, TRILHO = hx('3d2b1d'), hx('fde68a'), hx('1a120b'), hx('5b4532'), hx('120c08')
W, H = 176, 222


# ------------------------------------------------------------------ fonte 5x7 para rótulos fixos (maiúsculas)
F = {
 'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'], 'B': ['11110', '10001', '11110', '10001', '10001', '10001', '11110'],
 'C': ['01111', '10000', '10000', '10000', '10000', '10000', '01111'], 'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
 'E': ['11111', '10000', '11110', '10000', '10000', '10000', '11111'], 'F': ['11111', '10000', '11110', '10000', '10000', '10000', '10000'],
 'G': ['01111', '10000', '10000', '10011', '10001', '10001', '01111'], 'H': ['10001', '10001', '11111', '10001', '10001', '10001', '10001'],
 'I': ['111', '010', '010', '010', '010', '010', '111'], 'J': ['00111', '00001', '00001', '00001', '10001', '10001', '01110'],
 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'], 'M': ['10001', '11011', '10101', '10001', '10001', '10001', '10001'],
 'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'], 'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'],
 'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'], 'Q': ['01110', '10001', '10001', '10001', '10101', '10010', '01101'],
 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'], 'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'],
 'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'], 'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'],
 'V': ['10001', '10001', '10001', '10001', '01010', '01010', '00100'], 'X': ['10001', '01010', '00100', '00100', '00100', '01010', '10001'],
 'Z': ['11111', '00010', '00100', '00100', '01000', '10000', '11111'], 'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'],
 ' ': ['000', '000', '000', '000', '000', '000', '000'], '·': ['0', '0', '0', '1', '0', '0', '0'],
}
ACENTO = {'Á': ('A', 'acute'), 'Ó': ('O', 'acute'), 'Ã': ('A', 'tilde'), 'Õ': ('O', 'tilde'), 'Ê': ('E', 'circ'), 'É': ('E', 'acute'),
          'Í': ('I', 'acute'), 'Ç': ('C', 'cedilha'), 'Ú': ('U', 'acute')}


def texto(img, x, y, s, cor=ROTULO, sombra=ESCURO):
    """Escreve em maiúsculas 5x7 (acentos ficam 2 px acima). Devolve a largura."""
    x0 = x
    for ch in s.upper():
        base, marca = ACENTO.get(ch, (ch, None))
        g = F[base]
        for dy, linha in enumerate(g):
            for dx, b in enumerate(linha):
                if b == '1':
                    if sombra: img.putpixel((x + dx + 1, y + dy + 1), sombra)
                    img.putpixel((x + dx, y + dy), cor)
        w = len(g[0])
        meio = x + w // 2
        if marca == 'acute':
            img.putpixel((meio + 1, y - 2), cor); img.putpixel((meio, y - 1), cor)
        elif marca == 'tilde':
            for px, py in ((meio - 2, y - 1), (meio - 1, y - 2), (meio, y - 1), (meio + 1, y - 2)): img.putpixel((px, py), cor)
        elif marca == 'circ':
            img.putpixel((meio - 1, y - 1), cor); img.putpixel((meio, y - 2), cor); img.putpixel((meio + 1, y - 1), cor)
        elif marca == 'cedilha':
            img.putpixel((meio, y + 7), cor); img.putpixel((meio - 1, y + 8), cor)
        x += w + 1
    return x - x0


def largura(s):
    return sum(len(F[ACENTO.get(c, (c, 0))[0]][0]) + 1 for c in s.upper()) - 1


# ------------------------------------------------------------------ peças do fundo
def slot_xy(c, r):
    """canto de cima/esquerda da célula de 18x18 do slot (c 0..8, r 0..5 do baú; r 6..9 = inventário do jogador)"""
    if r <= 5: return 7 + 18 * c, 17 + 18 * r
    return 7 + 18 * c, (139 + 18 * (r - 6)) if r < 9 else 197


def poco(d, c, r, borda=POCO_BORDA, fundo=POCO):
    x, y = slot_xy(c, r)
    d.rectangle([x, y, x + 17, y + 17], fill=borda)
    d.rectangle([x + 1, y + 1, x + 16, y + 16], fill=fundo)


def trilho(d, c0, c1, r, cor=TRILHO):
    """faixa contínua atrás dos segmentos de barra (do slot c0 ao c1)"""
    x0, y = slot_xy(c0, r); x1, _ = slot_xy(c1, r)
    d.rectangle([x0, y + 3, x1 + 17, y + 14], fill=BORDA)
    d.rectangle([x0 + 1, y + 4, x1 + 16, y + 13], fill=cor)


def rotulo_linha(img, d, r, s, cor=ROTULO):
    x, y = slot_xy(0, r)
    d.rectangle([7, y + 1, 168, y + 16], fill=FUNDO)
    d.line([7, y + 17, 168, y + 17], fill=BORDA)
    texto(img, 10, y + 6, s, cor)


def base(abas, ativa):
    img = Image.new('RGBA', (W, H), PAINEL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=ESCURO)
    d.rectangle([1, 1, W - 2, H - 2], outline=MOLDURA)
    d.rectangle([2, 2, W - 3, H - 3], outline=MOLDURA)
    d.rectangle([3, 3, W - 4, H - 4], outline=ESCURO)
    for (x, y) in ((0, 0), (W - 4, 0), (0, H - 4), (W - 4, H - 4)):
        d.rectangle([x, y, x + 3, y + 3], fill=CANTO)
    d.line([6, 15, W - 7, 15], fill=BORDA)                         # separa o título
    # abas (linha 0): poços, a ativa em verde
    for c in abas:
        if c == ativa: poco(d, c, 0, hx('a3e635'), hx('3f5d12'))
        else: poco(d, c, 0)
    # inventário do jogador: área mais escura com os slots marcados
    d.rectangle([6, 128, W - 7, H - 7], fill=hx('22170f'))
    for r in (6, 7, 8, 9):
        for c in range(9): poco(d, c, r, hx('2e2116'), hx('1a120b'))
    return img, d


def salvar_fundo(nome, img):
    img.save(f'{R}/textures/font/gui/{nome}.png')


ABAS = (0, 1, 2, 3, 8)

# ------------------------------------------------ 1) início
img, d = base(ABAS, 0)
for c in (0, 1, 2): poco(d, c, 1)
trilho(d, 4, 7, 1, hx('2b2306')); poco(d, 8, 1, hx('a16207'), ESCURO)
rotulo_linha(img, d, 2, 'PRÓXIMAS COLHEITAS')
for r in (3, 4, 5):
    poco(d, 0, r); trilho(d, 1, 7, r); poco(d, 8, r)
salvar_fundo('inicio', img)

# ------------------------------------------------ 2) culturas
img, d = base(ABAS, 1)
for r in (1, 2):
    for c in range(1, 8): poco(d, c, r)
rotulo_linha(img, d, 3, 'ESPECIAIS · EM BREVE', hx('c9b89e'))
for c in range(2, 7): poco(d, c, 4, hx('3d2b1d'), hx('17100a'))
salvar_fundo('culturas', img)

# ------------------------------------------------ 3) cultura (painel)
img, d = base(ABAS, 1)
poco(d, 0, 0, hx('a3e635'), hx('3f5d12'))                          # voltar ocupa a aba 0 nesta tela
x0, y0 = slot_xy(0, 1); x1, y1 = slot_xy(2, 3)
d.rectangle([x0, y0, x1 + 17, y1 + 17], fill=hx('5b4532'))         # vitrine 3x3 da colheita ampliada
d.rectangle([x0 + 1, y0 + 1, x1 + 16, y1 + 16], fill=FUNDO)
for c in range(4, 9): poco(d, c, 1)
for c in range(4, 8): poco(d, c, 2)
trilho(d, 4, 7, 3); poco(d, 8, 3, hx('a16207'), hx('2b2306'))
for c in range(0, 4): poco(d, c, 4)
poco(d, 5, 4); poco(d, 7, 4, hx('d9f99d'), hx('3f5d12')); poco(d, 8, 4)
salvar_fundo('cultura', img)

# ------------------------------------------------ 4) perfil
img, d = base(ABAS, 2)
poco(d, 0, 1, hx('a16207'), ESCURO); trilho(d, 1, 7, 1, hx('2b2306')); poco(d, 8, 1, hx('a16207'), ESCURO)
rotulo_linha(img, d, 2, 'TRILHA DE DESBLOQUEIOS')
for c in range(9): poco(d, c, 3)
for c in range(8): poco(d, c, 4)
for c in range(4): poco(d, c, 5)
for c in (6, 7, 8): poco(d, c, 5, hx('5b4532'), hx('17100a'))
salvar_fundo('perfil', img)

# ------------------------------------------------ fonte
FUNDOS = ['inicio', 'culturas', 'cultura', 'perfil']
prov = [{'type': 'space', 'advances': {chr(0xE000 + i): -(1 << i) for i in range(9)}}]   # E000=-1, E001=-2 ... E008=-256
for i, n in enumerate(FUNDOS):
    prov.append({'type': 'bitmap', 'file': f'big:font/gui/{n}.png', 'ascent': 13, 'height': H, 'chars': [chr(0xE100 + i)]})
json.dump({'providers': prov}, open(f'{R}/font/gui.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


# ------------------------------------------------------------------ ícones 16x16
def icone(nome, linhas, pal):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, ch in enumerate(l.ljust(16, '.')[:16]):
            if ch != '.': im.putpixel((x, y), hx(pal[ch]))
    im.save(f'{R}/textures/item/gui/{nome}.png')
    json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'big:item/gui/{nome}'}},
              open(f'{R}/models/item/gui/{nome}.json', 'w'))
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/gui/{nome}'}}, open(f'{R}/items/gui/{nome}.json', 'w'), indent=1)


K = '1a120b'
ICONES = {
 'aba_inicio': (['................', '.......kk.......', '......kRRk......', '.....kRRRRk.....', '....kRRRRRRk....', '...kRRRRRRRRk...',
                 '..kkkkkkkkkkkk..', '...kWWWWWWWWk...', '...kWWWWWkkWk...', '...kWkkWWkdkWk..', '...kWkkWWkdkWk..', '...kWWWWWkdkWk..',
                 '...kkkkkkkkkkk..'], {'k': K, 'R': 'c2410c', 'W': 'e7d6ae', 'd': '6b4a2b'}),
 'aba_culturas': (['......gg........', '.....gGGg..gg...', '....gGGGg.gGGg..', '.....ggg.gGGGg..', '.......s..ggg...', '.......s..s.....',
                   '...gg..s.s......', '..gGGg.ss.......', '..gGGGgs........', '...ggg.s........', '.......s........', '..bbbbbbbbbbb...',
                   '..bBBBBBBBBBb...', '..bbbbbbbbbbb...'], {'g': '4d7c0f', 'G': '84cc16', 's': '65a30d', 'b': '6b4a2b', 'B': '8b5a33'}),
 'aba_perfil': (['......yyyy......', '.....yYYYYy.....', '.....yYYYYy.....', '.....yYYYYy.....', '......yyyy......', '...gggggggggg...',
                 '..gGGGGGGGGGGg..', '..gGGGGGGGGGGg..', '..gGGgGGGGgGGg..', '..gGGgGGGGgGGg..', '..gggggggggggg..'],
                {'y': 'b45309', 'Y': 'fcd34d', 'g': '3f6212', 'G': '84cc16'}),
 'aba_loja': (['................', '..cccccccccccc..', '.cRWRWRWRWRWRWc.', '.cRWRWRWRWRWRWc.', '..cccccccccccc..', '..bBBBBBBBBBBb..',
               '..bBkkBBBBkkBb..', '..bBkkBBBBkkBb..', '..bBBBBBBBBBBb..', '..bBBBkkkkBBBb..', '..bBBBkWWkBBBb..', '..bbbbbbbbbbbb..'],
              {'c': K, 'R': 'dc2626', 'W': 'f5f5f4', 'b': '6b4a2b', 'B': 'a87a4a', 'k': '3a2a1d'}),
 'fechar': (['................', '..rr........rr..', '..rRr......rRr..', '...rRr....rRr...', '....rRr..rRr....', '.....rRrrRr.....',
             '......rRRr......', '......rRRr......', '.....rRrrRr.....', '....rRr..rRr....', '...rRr....rRr...', '..rRr......rRr..',
             '..rr........rr..'], {'r': '7f1d1d', 'R': 'ef4444'}),
 'voltar': (['................', '.......gg.......', '......gGg.......', '.....gGGg.......', '....gGGGggggggg.', '...gGGGGGGGGGGg.',
             '..gGGGGGGGGGGGg.', '...gGGGGGGGGGGg.', '....gGGGggggggg.', '.....gGGg.......', '......gGg.......', '.......gg.......'],
            {'g': '3f6212', 'G': 'a3e635'}),
 'plantas': (['.......g........', '......gGg.......', '..gg..gGg..gg...', '.gGGg.gGg.gGGg..', '.gGGGggGggGGGg..', '..ggGGgGgGGgg...',
              '....ggGGGgg.....', '......gGg.......', '......gGg.......', '..bbbbbbbbbbb...', '..bBBBBBBBBBb...', '...bBBBBBBBb....',
              '....bbbbbbb.....'], {'g': '3f6212', 'G': '84cc16', 'b': '4a3220', 'B': '8b5a33'}),
 'prontas': (['....bbbbbbbb....', '...b........b...', '..b..........b..', '.rrRrrOooYyyGgg.', '.rRRrOOooYYyGGg.', 'bbbbbbbbbbbbbbbb',
              'bBwBwBwBwBwBwBwb', 'bwBwBwBwBwBwBwBb', 'bBwBwBwBwBwBwBwb', '.bwBwBwBwBwBwBb.', '..bbbbbbbbbbbb..'],
             {'b': '6b4a2b', 'B': 'a87a4a', 'w': '8b5a33', 'r': 'b91c1c', 'R': 'ef4444', 'O': 'f97316', 'o': 'c2410c', 'Y': 'facc15',
              'y': 'ca8a04', 'G': '84cc16', 'g': '4d7c0f'}),
 'sol': (['.......y........', '..y....y....y...', '...y...y...y....', '.....yyyyy......', '....yYYYYYy.....', '...yYYYYYYYy....',
          'yyyyYYYYYYYyyyy.', '...yYYYYYYYy....', '....yYYYYYy.....', '.....yyyyy......', '...y...y...y....', '..y....y....y...',
          '.......y........'], {'y': 'ca8a04', 'Y': 'fde047'}),
 'chuva': (['....wwwwww......', '...wWWWWWWww....', '..wWWWWWWWWWw...', '.wWWWWWWWWWWWw..', '.wwwwwwwwwwwwww.', '................',
            '..b...b...b...b.', '.b...b...b...b..', '................', '...b...b...b....', '..b...b...b.....'],
           {'w': '64748b', 'W': 'cbd5e1', 'b': '38bdf8'}),
 'noite': (['.....mmmm.......', '...mmMMm........', '..mMMm..........', '.mMMm...........', '.mMMm.........s.', '.mMMm...........',
            '.mMMMm.......m..', '..mMMMm....mm...', '...mmMMMMMMm....', '.....mmmmmm.....'], {'m': '6366f1', 'M': 'c7d2fe', 's': 'fef08a'}),
 'relogio': (['.....kkkkkk.....', '...kkWWWWWWkk...', '..kWWWWkWWWWWk..', '.kWWWWWkWWWWWWk.', '.kWWWWWkWWWWWWk.', 'kWWWWWWkWWWWWWWk',
              'kWWWWWWkkkkkWWWk', 'kWWWWWWWWWWWWWWk', 'kWWWWWWWWWWWWWWk', '.kWWWWWWWWWWWWk.', '.kWWWWWWWWWWWWk.', '..kWWWWWWWWWWk..',
              '...kkWWWWWWkk...', '.....kkkkkk.....'], {'k': '3a2a1d', 'W': 'f5efe3'}),
 'pronto': (['................', '.............gg.', '............gGg.', '...........gGg..', '..gg......gGg...', '.gGGg....gGg....',
             '..gGGg..gGg.....', '...gGGggGg......', '....gGGGg.......', '.....gGg........', '......g.........'],
            {'g': '3f6212', 'G': 'a3e635'}),
 'moeda': (['.....yyyyyy.....', '...yyYYYYYYyy...', '..yYYYYyyYYYYy..', '.yYYYYyYYyYYYYy.', '.yYYYYyYYYYYYYy.', 'yYYYYYYyyYYYYYYy',
            'yYYYYYYYYyYYYYYy', 'yYYYYYyYYyYYYYYy', '.yYYYYYyyYYYYYy.', '.yYYYYYYYYYYYYy.', '..yYYYYYYYYYYy..', '...yyYYYYYYyy...',
            '.....yyyyyy.....'], {'y': 'a16207', 'Y': 'facc15'}),
 'dourada': (['.......y........', '......yYy.......', '......yYy.......', '.....yYYYy......', 'yyyyyYYWYYyyyyy.', '.yYYYYYYYYYYYy..',
              '..yYYYYYYYYYy...', '...yYYYYYYYy....', '...yYYYyYYYy....', '..yYYYy.yYYYy...', '..yYYy...yYYy...', '.yYy.......yYy..',
              '.yy.........yy..'], {'y': 'a16207', 'Y': 'fde047', 'W': 'ffffff'}),
 'perene': (['......ggg.......', '....ggGGGgg.....', '...gGGGGGGGg....', '..gGGGrGGGrGg...', '..gGGGGGGGGGg...', '..gGrGGGGrGGg...',
             '...gGGGGGGGg....', '....ggGGGgg.....', '......bbb.......', '......bBb.......', '......bBb.......', '.....bbBbb......',
             '....bbbbbbb.....'], {'g': '3f6212', 'G': '65a30d', 'r': 'ef4444', 'b': '4a3220', 'B': '8b5a33'}),
 'anual': (['.......g........', '......gGg.......', '.....gGGGg......', '.......g........', '.......g........', '......sss.......',
            '.....sSSSs......', '....sSSSSSs.....', '....sSSSSSs.....', '.....sSSSs......', '......sss.......'],
           {'g': '3f6212', 'G': '84cc16', 's': '8b5a33', 'S': 'e8d6ae'}),
 'gota': (['.......b........', '.......b........', '......bBb.......', '......bBb.......', '.....bBBBb......', '....bBBWBBb.....',
           '...bBBWBBBBb....', '...bBWBBBBBb....', '...bBBBBBBBb....', '...bBBBBBBBb....', '....bBBBBBb.....', '.....bbbbb......'],
          {'b': '0369a1', 'B': '38bdf8', 'W': 'e0f2fe'}),
 'adubo': (['................', '..ww........ww..', '.wWWw......wWWw.', '.wWWWwwwwwwWWWw.', '..wwWWWWWWWWww..', '.wWWWwwwwwwWWWw.',
            '.wWWw......wWWw.', '..ww........ww..'], {'w': 'a8a29e', 'W': 'f5f5f4'}),
 'cadeado': (['.....kkkkkk.....', '....k......k....', '...k........k...', '...k........k...', '..yyyyyyyyyyyy..', '..yYYYYYYYYYYy..',
              '..yYYYYkkYYYYy..', '..yYYYYkkYYYYy..', '..yYYYYYkYYYYy..', '..yYYYYYYYYYYy..', '..yyyyyyyyyyyy..'],
             {'k': '78716c', 'y': '854d0e', 'Y': 'ca8a04'}),
 'livro': (['..bbbbbbbbbbbb..', '..bGGGGGGGGGGb..', '..bGGGGyyGGGGbw.', '..bGGGyGGyGGGbw.', '..bGGGGyyGGGGbw.', '..bGGGGGGGGGGbw.',
            '..bGGGGGGGGGGbw.', '..bGGGGGGGGGGbw.', '..bGGGGGGGGGGbw.', '..bbbbbbbbbbbbw.', '...wwwwwwwwwwww.'],
           {'b': '1a2e05', 'G': '4d7c0f', 'y': 'facc15', 'w': 'e7e5e4'}),
 'sacola': (['.....kkkkkk.....', '....k......k....', '....k......k....', '..bbbbbbbbbbbb..', '..bBBBBBBBBBBb..', '..bBBBBBBBBBBb..',
             '..bBBBgggBBBBb..', '..bBBgGGGgBBBb..', '..bBBBgggBBBBb..', '..bBBBBBBBBBBb..', '..bbbbbbbbbbbb..'],
            {'k': '6b4a2b', 'b': '6b4a2b', 'B': 'c49a62', 'g': '3f6212', 'G': '84cc16'}),
 'mutacao': (['......pppp......', '....ppPPPPpp....', '...pPPPWPPPPp...', '..pPPPWWPPPPPp..', '..pPPPPPPPPPPp..', '..pPPPPPPPPPPp..',
              '...pPPPPPPPPp...', '....ppPPPPpp....', '......pppp......'], {'p': '7e22ce', 'P': 'c084fc', 'W': 'f5d0fe'}),
}
for (n, (l, p)) in ICONES.items(): icone(n, l, p)


# barras: segmento de 16x16 com 0, 1 ou 2 metades cheias (o trilho contínuo fica no fundo)
def barra(nome, cheio, escuro):
    for k in range(3):
        im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
        w = (0, 8, 16)[k]
        for x in range(w):
            for y in range(4, 12):
                im.putpixel((x, y), hx(escuro) if y >= 10 else hx(cheio))
        n = f'{nome}_{k}'
        im.save(f'{R}/textures/item/gui/{n}.png')
        json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'big:item/gui/{n}'}}, open(f'{R}/models/item/gui/{n}.json', 'w'))
        json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/gui/{n}'}}, open(f'{R}/items/gui/{n}.json', 'w'), indent=1)


barra('barra_verde', '84cc16', '4d7c0f')
barra('barra_ouro', 'facc15', 'ca8a04')


# fichas de qualidade e marcos da trilha
def ficha(nome, cor, borda, marca=None):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for x in range(2, 14):
        for y in range(2, 14):
            b = x in (2, 13) or y in (2, 13)
            im.putpixel((x, y), hx(borda) if b else hx(cor))
    if marca == 'check':
        for (x, y) in ((5, 8), (6, 9), (7, 10), (8, 9), (9, 8), (10, 7), (11, 6)): im.putpixel((x, y), hx('f7fee7'))
    if marca == 'seta':
        for (x, y) in ((6, 5), (7, 6), (8, 7), (9, 8), (8, 9), (7, 10), (6, 11)): im.putpixel((x, y), hx('fde047'))
    im.save(f'{R}/textures/item/gui/{nome}.png')
    json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'big:item/gui/{nome}'}}, open(f'{R}/models/item/gui/{nome}.json', 'w'))
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/gui/{nome}'}}, open(f'{R}/items/gui/{nome}.json', 'w'), indent=1)


for n, c, b in (('q_comum', 'a8a29e', '57534e'), ('q_boa', '84cc16', '3f6212'), ('q_excelente', '38bdf8', '0369a1'), ('q_perfeita', 'c084fc', '7e22ce')):
    ficha(n, c, b)
ficha('marco_feito', '3f5d12', 'a3e635', 'check')
ficha('marco_proximo', '2b2306', 'facc15', 'seta')
ficha('marco_bloqueado', '1a120b', '3d2b1d')
for n, c in (('ramo_cultivador', 'bef264'), ('ramo_botanico', '7dd3fc'), ('ramo_produtor', 'e7d6ae')):
    ficha(n, '17100a', c)

# colheita ampliada para a vitrine 3x3 do painel de cultura
CULTURAS = ['morango', 'milho', 'pimenta', 'mandioca', 'cafe', 'abacaxi', 'tomate', 'soja', 'arroz', 'algodao', 'cana', 'abobora',
            'melancia', 'uva']
for c in CULTURAS:
    json.dump({'parent': f'big:item/fazenda/{c}',
               'display': {'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [2.6, 2.6, 2.6]}}},
              open(f'{R}/models/item/gui/grande_{c}.json', 'w'))
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/gui/grande_{c}'}},
              open(f'{R}/items/gui/grande_{c}.json', 'w'), indent=1)
print('gui da fazenda ok:', len(FUNDOS), 'fundos,', len(os.listdir(f'{R}/items/gui')), 'itens')
