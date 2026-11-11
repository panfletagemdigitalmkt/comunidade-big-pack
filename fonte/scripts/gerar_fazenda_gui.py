# Fazenda BIG — telas personalizadas v2 (mais perto das maquetes aprovadas).
# Cada tela é um baú de 6 linhas. O fundo é um glyph de 256x222 da fonte big:gui, 40 px mais largo de cada lado
# do baú (176 px), colocado no título. Os textos que mudam (números, nomes, tempos, barras) também vão no título,
# escritos com a fonte de pixel da BIG em "linhas": cada linha é um bloco de caracteres com outro deslocamento
# vertical, então dá para escrever em qualquer altura. Botões continuam sendo itens nos slots.
#   font/gui.json              -> recuos (+/-), fundos (U+E100..) e as linhas de texto (U+F0000..)
#   textures/font/gui/*.png    -> fundos 256x222 e letras.png
#   items|models|textures/gui  -> ícones big:gui/*
#   ../../plugins-separados/.../Letras.java (impresso com --java) -> tabela de larguras e códigos para o plugin
# Rodar da pasta fonte/:  python3 scripts/gerar_fazenda_gui.py [--java caminho/Letras.java]
import json, os, sys
from PIL import Image, ImageDraw

R = 'assets/big'
for d in ('font', 'textures/font/gui', 'textures/item/gui', 'models/item/gui', 'items/gui'):
    os.makedirs(f'{R}/{d}', exist_ok=True)


def hx(h, a=255):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a)


PAINEL, FUNDO, MOLDURA, ESCURO, CANTO = hx('2a1d14'), hx('1f150e'), hx('84cc16'), hx('1a120b'), hx('eab308')
BORDA, ROTULO, POCO, POCO_BORDA, TRILHO = hx('3d2b1d'), hx('fde68a'), hx('1a120b'), hx('5b4532'), hx('120c08')
MUTED, CLARO, VERDE_F, VERDE_B = hx('c9b89e'), hx('f5efe3'), hx('3f5d12'), hx('a3e635')
W, H, OX = 256, 222, 40                       # fundo; OX = quanto o fundo passa do baú para a esquerda

# ================================================================== fonte de pixel (maiúsculas 5x7 + acentos)
F = {
 'A': ['01110', '10001', '10001', '11111', '10001', '10001', '10001'], 'B': ['11110', '10001', '11110', '10001', '10001', '10001', '11110'],
 'C': ['01111', '10000', '10000', '10000', '10000', '10000', '01111'], 'D': ['11110', '10001', '10001', '10001', '10001', '10001', '11110'],
 'E': ['11111', '10000', '11110', '10000', '10000', '10000', '11111'], 'F': ['11111', '10000', '11110', '10000', '10000', '10000', '10000'],
 'G': ['01111', '10000', '10000', '10011', '10001', '10001', '01111'], 'H': ['10001', '10001', '11111', '10001', '10001', '10001', '10001'],
 'I': ['111', '010', '010', '010', '010', '010', '111'], 'J': ['00111', '00001', '00001', '00001', '10001', '10001', '01110'],
 'K': ['10001', '10010', '10100', '11000', '10100', '10010', '10001'], 'L': ['10000', '10000', '10000', '10000', '10000', '10000', '11111'],
 'M': ['10001', '11011', '10101', '10001', '10001', '10001', '10001'], 'N': ['10001', '11001', '10101', '10011', '10001', '10001', '10001'],
 'O': ['01110', '10001', '10001', '10001', '10001', '10001', '01110'], 'P': ['11110', '10001', '10001', '11110', '10000', '10000', '10000'],
 'Q': ['01110', '10001', '10001', '10001', '10101', '10010', '01101'], 'R': ['11110', '10001', '10001', '11110', '10100', '10010', '10001'],
 'S': ['01111', '10000', '10000', '01110', '00001', '00001', '11110'], 'T': ['11111', '00100', '00100', '00100', '00100', '00100', '00100'],
 'U': ['10001', '10001', '10001', '10001', '10001', '10001', '01110'], 'V': ['10001', '10001', '10001', '10001', '01010', '01010', '00100'],
 'W': ['10001', '10001', '10001', '10101', '10101', '11011', '10001'], 'X': ['10001', '01010', '00100', '00100', '00100', '01010', '10001'],
 'Y': ['10001', '10001', '01010', '00100', '00100', '00100', '00100'], 'Z': ['11111', '00010', '00100', '00100', '01000', '10000', '11111'],
 '0': ['01110', '10011', '10101', '10101', '10101', '11001', '01110'], '1': ['010', '110', '010', '010', '010', '010', '111'],
 '2': ['01110', '10001', '00001', '00110', '01000', '10000', '11111'], '3': ['11110', '00001', '00001', '01110', '00001', '00001', '11110'],
 '4': ['00010', '00110', '01010', '10010', '11111', '00010', '00010'], '5': ['11111', '10000', '11110', '00001', '00001', '10001', '01110'],
 '6': ['01110', '10000', '10000', '11110', '10001', '10001', '01110'], '7': ['11111', '00001', '00010', '00100', '01000', '01000', '01000'],
 '8': ['01110', '10001', '10001', '01110', '10001', '10001', '01110'], '9': ['01110', '10001', '10001', '01111', '00001', '00001', '01110'],
 '.': ['0', '0', '0', '0', '0', '0', '1'], ',': ['00', '00', '00', '00', '00', '01', '10'], ':': ['0', '1', '0', '0', '0', '1', '0'],
 '!': ['1', '1', '1', '1', '1', '0', '1'], '?': ['01110', '10001', '00001', '00110', '00100', '00000', '00100'],
 '%': ['11001', '11010', '00010', '00100', '01000', '01011', '10011'], '/': ['00001', '00010', '00010', '00100', '01000', '01000', '10000'],
 '-': ['000', '000', '000', '111', '000', '000', '000'], '+': ['000', '000', '010', '111', '010', '000', '000'],
 '·': ['0', '0', '0', '1', '0', '0', '0'], '~': ['0000', '0000', '0101', '1010', '0000', '0000', '0000'],
 '(': ['01', '10', '10', '10', '10', '10', '01'], ')': ['10', '01', '01', '01', '01', '01', '10'],
 '=': ['000', '000', '111', '000', '111', '000', '000'], '\'': ['1', '1', '0', '0', '0', '0', '0'],
 '‹': ['001', '010', '100', '100', '100', '010', '001'], '›': ['100', '010', '001', '001', '001', '010', '100'],
 '■': ['0000', '1111', '1111', '1111', '1111', '0000', '0000'], '#': ['01010', '11111', '01010', '01010', '01010', '11111', '01010'],
}
ACENTO = {'Á': ('A', 'acute'), 'Ó': ('O', 'acute'), 'Ã': ('A', 'tilde'), 'Õ': ('O', 'tilde'), 'Ê': ('E', 'circ'), 'É': ('E', 'acute'),
          'Í': ('I', 'acute'), 'Ç': ('C', 'cedilha'), 'Ú': ('U', 'acute'), 'Â': ('A', 'circ'), 'Ô': ('O', 'circ'), 'À': ('A', 'grave')}
CW, CH, TOPO = 8, 11, 2                       # célula da folha de letras; TOPO = linhas reservadas para acento
# blocos de barra (altura 4, ficam nas linhas 0..3 da letra) e o caractere de espaço não entra na folha
BLOCOS = {'█1': 1, '█2': 2, '█4': 4, '█8': 8}
GLIFOS = list(F.keys()) + list(ACENTO.keys()) + list(BLOCOS.keys())
assert len(GLIFOS) <= 128


def glifo_pixels(ch):
    """lista de (x, y) dentro da célula 8x11 (y=TOPO é o topo da maiúscula)"""
    if ch in BLOCOS:
        return [(x, TOPO + y) for x in range(BLOCOS[ch]) for y in range(4)]
    base, marca = ACENTO.get(ch, (ch, None))
    g = F[base]; w = len(g[0]); m = w // 2
    px = [(x, TOPO + y) for y, l in enumerate(g) for x, b in enumerate(l) if b == '1']
    if marca == 'acute': px += [(m + 1, 0), (m, 1)]
    elif marca == 'grave': px += [(m - 1, 0), (m, 1)]
    elif marca == 'tilde': px += [(m - 2, 1), (m - 1, 0), (m, 1), (m + 1, 0)]
    elif marca == 'circ': px += [(m - 1, 1), (m, 0), (m + 1, 1)]
    elif marca == 'cedilha': px += [(m, TOPO + 7), (m - 1, TOPO + 8)]
    return px


def largura(ch):
    return max(x for x, _ in glifo_pixels(ch)) + 1


folha = Image.new('RGBA', (16 * CW, ((len(GLIFOS) + 15) // 16) * CH), (0, 0, 0, 0))
for i, ch in enumerate(GLIFOS):
    ox, oy = (i % 16) * CW, (i // 16) * CH
    for x, y in glifo_pixels(ch): folha.putpixel((ox + x, oy + y), (255, 255, 255, 255))
folha.save(f'{R}/textures/font/gui/letras.png')


def texto(img, x, y, s, cor=ROTULO, sombra=ESCURO):
    """escreve no fundo em coordenadas do baú (x pode ser negativo); y = topo da maiúscula. Devolve a largura."""
    cx = x
    for ch in s.upper():
        if ch == ' ': cx += 4; continue
        if ch not in GLIFOS: ch = '?'
        for px, py in glifo_pixels(ch):
            X, Y = cx + OX + px, y + py - TOPO
            if sombra: img.putpixel((X + 1, Y + 1), sombra)
        for px, py in glifo_pixels(ch):
            img.putpixel((cx + OX + px, y + py - TOPO), cor)
        cx += largura(ch) + 1
    return cx - x


def larg_txt(s):
    return sum(4 if c == ' ' else largura(c if c in GLIFOS else '?') + 1 for c in s.upper())


# ================================================================== peças do fundo (coordenadas do baú)
def ret(d, x0, y0, x1, y1, fill=None, outline=None):
    d.rectangle([x0 + OX, y0, x1 + OX, y1], fill=fill, outline=outline)


def slot_xy(c, r):
    if r <= 5: return 7 + 18 * c, 17 + 18 * r
    return 7 + 18 * c, (139 + 18 * (r - 6)) if r < 9 else 197


def poco(d, c, r, borda=POCO_BORDA, fundo=POCO):
    x, y = slot_xy(c, r)
    ret(d, x, y, x + 17, y + 17, fill=borda); ret(d, x + 1, y + 1, x + 16, y + 16, fill=fundo)


def cartao(d, x0, y0, x1, y1, borda=BORDA, fundo=FUNDO):
    ret(d, x0, y0, x1, y1, fill=borda); ret(d, x0 + 1, y0 + 1, x1 - 1, y1 - 1, fill=fundo)


def trilho(d, x0, y, x1, alt=4):
    ret(d, x0 - 1, y - 1, x1 + 1, y + alt, fill=BORDA); ret(d, x0, y, x1, y + alt - 1, fill=TRILHO)


def base():
    img = Image.new('RGBA', (W, H), PAINEL)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=ESCURO)
    d.rectangle([1, 1, W - 2, H - 2], outline=MOLDURA)
    d.rectangle([2, 2, W - 3, H - 3], outline=MOLDURA)
    d.rectangle([3, 3, W - 4, H - 4], outline=ESCURO)
    for (x, y) in ((0, 0), (W - 4, 0), (0, H - 4), (W - 4, H - 4)): d.rectangle([x, y, x + 3, y + 3], fill=CANTO)
    ret(d, -36, 17, 211, 17, fill=BORDA)                          # linha sob o cabeçalho
    ret(d, -36, 126, 211, H - 6, fill=hx('22170f'))                # área do inventário do jogador
    for r in (6, 7, 8, 9):
        for c in range(9): poco(d, c, r, hx('2e2116'), hx('1a120b'))
    return img, d


TRILHO_ITENS = ['INÍCIO', 'CULTURAS', 'AGRICULTOR', 'LOJA', 'AJUDA', 'FECHAR']


def trilho_lateral(img, d, ativo):
    """menu à esquerda, um item por linha de slots (clicável nos slots 0 e 1 daquela linha)"""
    for r, nome in enumerate(TRILHO_ITENS):
        y = 17 + 18 * r
        on = r == ativo
        cartao(d, -36, y + 1, 41, y + 17, VERDE_B if on else BORDA, VERDE_F if on else FUNDO)
        ret(d, -32, y + 7, -29, y + 10, fill=CANTO if on else hx('5b4532'))
        texto(img, -25, y + 6, nome, hx('f7fee7') if on else hx('d6c7ad'))


# ================================================================== telas (só o que é fixo; o resto o plugin escreve)
def salvar_fundo(nome, img):
    img.save(f'{R}/textures/font/gui/{nome}.png')


# ---- início
img, d = base(); trilho_lateral(img, d, 0)
for (x0, x1, b) in ((44, 97, BORDA), (101, 154, hx('65a30d')), (158, 211, BORDA)): cartao(d, x0, 18, x1, 51, b)
for (x0, s) in ((48, 'PLANTAS'), (105, 'PRONTAS'), (162, 'CLIMA')): texto(img, x0, 22, s, MUTED)
cartao(d, 44, 53, 211, 124)
texto(img, 48, 57, 'PRÓXIMAS COLHEITAS', ROTULO)
for r in (3, 4, 5):
    poco(d, 2, r)
    ry = 17 + 18 * r
    trilho(d, 66, ry + 12, 208)
salvar_fundo('inicio', img)

# ---- culturas
img, d = base(); trilho_lateral(img, d, 1)
for r in (0, 1):
    for c in range(2, 9): poco(d, c, r)
cartao(d, 44, 53, 211, 70); texto(img, 48, 58, 'ESPECIAIS · EM BREVE', MUTED)
for c in range(2, 7): poco(d, c, 3, hx('3d2b1d'), hx('17100a'))
cartao(d, 44, 89, 211, 124)
for i, s in enumerate(('CLIQUE NUMA CULTURA PARA', 'VER OS DETALHES. O NÍVEL 5', 'LIBERA AS CULTURAS NOVAS.')):
    texto(img, 48, 93 + 10 * i, s, MUTED)
salvar_fundo('culturas', img)

# ---- painel da cultura
img, d = base()
cartao(d, -32, 18, 64, 69, hx('5b4532'))
texto(img, -34, 77, 'FASES', MUTED)
for c in range(4): poco(d, c, 3)
cartao(d, -36, 90, 77, 105, hx('d9f99d'), VERDE_F); texto(img, -30, 94, 'COMPRAR SEMENTES', hx('f7fee7'))
cartao(d, -36, 108, 77, 123, hx('5b4532'), hx('3a2a1d')); texto(img, -30, 112, '‹ VOLTAR', hx('e7dcc8'))
cartao(d, 82, 18, 211, 51)
for i, s in enumerate(('PRONTA EM', 'COLHEITA', 'VENDA', 'DOURADA')): texto(img, 86, 20 + 8 * i, s, MUTED)
cartao(d, 82, 53, 211, 87); texto(img, 86, 56, 'O QUE ELA PRECISA', ROTULO)
for i, (s, c) in enumerate((('TERRA SECA: MEIA VEL.', '38bdf8'), ('POUCA LUZ: MEIA VEL.', 'fde047'), ('CHUVA: +25% VELOC.', '7dd3fc'))):
    texto(img, 86, 64 + 8 * i, '■', hx(c)); texto(img, 93, 64 + 8 * i, s, CLARO)
cartao(d, 82, 89, 211, 124); texto(img, 86, 92, 'QUALIDADE PROVÁVEL', ROTULO)
trilho(d, 86, 101, 207, 5)
cartao(d, 170, 3, 211, 14, hx('65a30d'), hx('1a2e05'))
salvar_fundo('cultura', img)

# ---- perfil de Agricultor
img, d = base(); trilho_lateral(img, d, 2)
trilho(d, 46, 29, 209, 4)
for c in range(2, 9): poco(d, c, 1); poco(d, c, 2)
for c in range(2, 5): poco(d, c, 3)
cartao(d, 99, 71, 211, 88, hx('a16207'), hx('2b2306'))
cartao(d, 44, 89, 125, 124); texto(img, 48, 92, 'SEUS NÚMEROS', ROTULO)
cartao(d, 129, 89, 211, 124); texto(img, 133, 92, 'RAMOS · NV 50', ROTULO)
for i, (s, c) in enumerate((('CULTIVADOR', 'bef264'), ('BOTÂNICO', '7dd3fc'), ('PRODUTOR', 'e7d6ae'))):
    texto(img, 133, 101 + 8 * i, s, hx(c))
salvar_fundo('perfil', img)

# ================================================================== fonte big:gui
FUNDOS = ['inicio', 'culturas', 'cultura', 'perfil']
BASE, POR_LINHA = 0xF0000, 128
Y1 = (4, 127)        # alturas possíveis do texto normal (topo da maiúscula, coordenadas do baú)
Y2 = (-4, 60)        # alturas possíveis do texto grande (2x)
prov = [{'type': 'space', 'advances': {**{chr(0xE000 + i): -(1 << i) for i in range(9)},
                                       **{chr(0xE010 + i): (1 << i) for i in range(9)}}}]
for i, n in enumerate(FUNDOS):
    prov.append({'type': 'bitmap', 'file': f'big:font/gui/{n}.png', 'ascent': 13, 'height': H, 'chars': [chr(0xE100 + i)]})


def linhas_chars(L):
    linhas = []
    for row in range((len(GLIFOS) + 15) // 16):
        cps = []
        for col in range(16):
            g = row * 16 + col
            cps.append(chr(BASE + L * POR_LINHA + g) if g < len(GLIFOS) else '\u0000')
        linhas.append(''.join(cps))
    return linhas


L = 0
for y in range(Y1[0], Y1[1] + 1):
    prov.append({'type': 'bitmap', 'file': 'big:font/gui/letras.png', 'ascent': 15 - y, 'height': CH, 'chars': linhas_chars(L)}); L += 1
for y in range(Y2[0], Y2[1] + 1):
    prov.append({'type': 'bitmap', 'file': 'big:font/gui/letras.png', 'ascent': 17 - y, 'height': CH * 2, 'chars': linhas_chars(L)}); L += 1
json.dump({'providers': prov}, open(f'{R}/font/gui.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))


# ================================================================== tabela para o plugin
def java_char(ch):
    if ch in BLOCOS: return chr(0x2581 + list(BLOCOS).index(ch))
    return ch


if '--java' in sys.argv:
    destino = sys.argv[sys.argv.index('--java') + 1]
    glifos = ''.join(java_char(c) for c in GLIFOS)
    larg = ', '.join(str(largura(c)) for c in GLIFOS)
    esc = glifos.replace('\\', '\\\\').replace('"', '\\"')
    open(destino, 'w', encoding='utf-8').write(f'''package br.com.comunidadebig.rpg.fazenda;

/** Gerado por fonte/scripts/gerar_fazenda_gui.py (pack comunidade-big-pack). Não editar à mão. */
final class Letras {{
    private Letras() {{ }}

    /** glifos na ordem da folha letras.png (▁▂▃▄ = blocos de barra de 1, 2, 4 e 8 px) */
    static final String GLIFOS = "{esc}";
    static final int[] LARGURA = {{{larg}}};
    static final int BASE = 0x{BASE:X}, POR_LINHA = {POR_LINHA};
    static final int Y1_MIN = {Y1[0]}, Y1_MAX = {Y1[1]}, Y2_MIN = {Y2[0]}, Y2_MAX = {Y2[1]};
    static final int LINHAS_Y1 = Y1_MAX - Y1_MIN + 1;
    static final int FUNDO_LARGURA = {W}, FUNDO_OX = {OX};
}}
''')
    print('tabela java ->', destino)

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
# ícone vazio: deixa o slot clicável sem desenhar nada (o desenho fica no fundo)
im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); im.save(f'{R}/textures/item/gui/vazio.png')
json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': 'big:item/gui/vazio'}}, open(f'{R}/models/item/gui/vazio.json', 'w'))
json.dump({'model': {'type': 'minecraft:model', 'model': 'big:item/gui/vazio'}}, open(f'{R}/items/gui/vazio.json', 'w'), indent=1)
print('gui da fazenda v2 ok:', len(FUNDOS), 'fundos,', len(GLIFOS), 'glifos,', L, 'linhas de texto')
