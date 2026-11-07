# Emojis do chat em pixel art (fonte big:emoji, 9x9). Rostos são montados sobre uma carinha base;
# os ícones são desenhados à mão. Gera também a lista para o plugin (emojis.json).
import json, os
from PIL import Image
from voxel import cor, mix, R

PASTA = f'{R}/textures/font/emoji'
os.makedirs(PASTA, exist_ok=True); os.makedirs(f'{R}/font', exist_ok=True)

ROSTO = ['..YYYYY..', '.YYYYYYY.', 'YYYYYYYYY', 'YYYYYYYYY', 'YYYYYYYYY', 'YYYYYYYYY', 'YYYYYYYYY', '.YYYYYYY.', '..YYYYY..']

def rosto(base, feicao):
    g = [list(l) for l in ROSTO]
    for y, l in enumerate(feicao):
        for x, ch in enumerate(l):
            if ch != '.' and g[y][x] != '.': g[y][x] = ch
            elif ch not in '.' and ch in 'hHAtT': g[y][x] = ch      # chifres, auréola, lágrimas fora do rosto
    return [''.join(l) for l in g]

CORES = {'Y': 'ffd23f', 'y': 'e0a800', 'o': '3a2410', 'w': 'ffffff', 'r': 'e2342c', 'R': 'ff6a8a', 'p': 'f472b6', 'b': '4aa8ff',
         'B': '1a1a1a', 'g': '7ac74f', 'G': '3c8a2a', 'P': '9b5de5', 'h': '7c1d1d', 'A': 'ffe680', 'T': '4aa8ff', 't': 'a8dcff',
         'k': '2a2a2a', 's': 'c8ccd4', 'S': '8a8f98', 'd': '5ee0e0', 'D': '1e9a9a', 'm': '6b3a1f', 'M': 'b98a4a', 'O': 'ff9b3d',
         'u': 'fff3b0', 'v': '5ab552', 'x': 'f0f0f0', 'c': 'c48a1a', 'n': '2563eb', 'e': 'e8eef4', 'q': '7a7a7a'}

FACES = {
    'sorriso':    ['.........', '.........', '..o...o..', '..o...o..', '.........', '.o.....o.', '..ooooo..', '.........', '.........'],
    'feliz':      ['.........', '.........', '..o...o..', '..o...o..', '.........', '.ooooooo.', '.owwwwwo.', '..ooooo..', '.........'],
    'risada':     ['.........', '.........', '.o.o.o.o.', '..o...o..', '.o.o.o.o.', '.ooooooo.', '.oRRRRRo.', '..ooooo..', '.........'],
    'piscada':    ['.........', '.........', '..o......', '..o..ooo.', '.........', '.o.....o.', '..ooooo..', '.........', '.........'],
    'apaixonado': ['.........', '.........', '.r.r.r.r.', '.rrr.rrr.', '..r...r..', '.o.....o.', '..ooooo..', '.........', '.........'],
    'legal':      ['.........', '.........', '.BBBBBBB.', '.BBB.BBB.', '..B...B..', '.........', '..o...o..', '...ooo...', '.........'],
    'lingua':     ['.........', '.........', '..o...o..', '..o...o..', '.........', '.ooooooo.', '....RR...', '....RR...', '.........'],
    'triste':     ['.........', '.........', '..o...o..', '..o...o..', '.........', '..ooooo..', '.o.....o.', '.........', '.........'],
    'chorando':   ['.........', '.........', '.oo...oo.', '..T...T..', '..T...T..', '..TooooT.', '.oT....o.', '..t......', '.........'],
    'bravo':      ['.........', '.o.....o.', '..o...o..', '..o...o..', '.........', '..ooooo..', '.o.....o.', '.........', '.........'],
    'surpreso':   ['.........', '.........', '..o...o..', '..o...o..', '.........', '....o....', '...o.o...', '....o....', '.........'],
    'dormindo':   ['.........', '......wB.', '.........', '.oo...oo.', '.........', '.........', '...ooo...', '.........', '.........'],
    'enjoado':    ['.........', '.........', '..o...o..', '.ooo.ooo.', '.........', '.ooooooo.', '.GGGGGGG.', '..GGGGG..', '.........'],
    'morto':      ['.........', '.........', '.o.o.o.o.', '..o...o..', '.o.o.o.o.', '.........', '..ooooo..', '.........', '.........'],
    'vergonha':   ['.........', '.........', '..o...o..', '..o...o..', '.pp...pp.', '.pp.o.pp.', '...o.o...', '.........', '.........'],
    'nerd':       ['.........', '.........', '.sss.sss.', '.sos.sos.', '.sssssss.', '.........', '..ooooo..', '...www...', '.........'],
    'pensativo':  ['.........', '..oo.....', '.....o...', '..o..o...', '.........', '...oooo..', '.........', '......YY.', '.....yy..'],
    'chocado':    ['.........', '..oo.oo..', '.owo.owo.', '..oo.oo..', '.........', '...ooo...', '...oBo...', '...ooo...', '.........'],
}
ESPECIAIS = {   # base de outra cor
    'anjo':    ('AAAAAAAAA', ['.........', '.........', '..o...o..', '..o...o..', '.........', '.o.....o.', '..ooooo..', '.........', '.........']),
    'diabinho': ('P', ['h.......h', 'hh.....hh', '..o...o..', '..oo.oo..', '.........', '.o.....o.', '..ooooo..', '.........', '.........']),
    'palhaco': ('x', ['.........', '.........', '..b...b..', '..b...b..', '....r....', '.r..r..r.', '..rrrrr..', '.........', '.........']),
}

ICONES = {
    'coracao':   ['.........', '.rr...rr.', 'rRrr.rrrr', 'rRrrrrrrr', 'rrrrrrrrr', '.rrrrrrr.', '..rrrrr..', '...rrr...', '....r....'],
    'coracao_partido': ['.........', '.rr...rr.', 'rRrr.rrrr', 'rRr.rrrrr', 'rrrr.rrrr', '.rr.rrrr.', '..rr.rr..', '...r.r...', '....r....'],
    'fogo':      ['....O....', '...OO....', '...OOO.O.', '..OOrOOO.', '.OOrrrOO.', '.OrrYrrO.', '.OrYYYrO.', '..rYYYr..', '...rrr...'],
    'estrela':   ['....Y....', '....Y....', '...YYY...', 'YYYYuYYYY', '.YYYuYYY.', '..YYYYY..', '..YY.YY..', '.YY...YY.', '.Y.....Y.'],
    'joinha':    ['....M....', '...MM....', '...MM....', '.MMMMMMM.', 'nMMMMMMM.', 'nMMMMMMM.', 'nMMMMMMM.', 'nMMMMMM..', '.........'],
    'coroa':     ['.........', 'Y...Y...Y', 'YY.YYY.YY', 'YYYYYYYYY', 'YrYYbYYrY', 'YYYYYYYYY', 'ccccccccc', '.........', '.........'],
    'diamante':  ['.........', '..ddddd..', '.dDdddDd.', 'dDddddddD', '.dDdddDd.', '..dDddD..', '...dDd...', '....d....', '.........'],
    'espada':    ['.......ee', '......ese', '.....ese.', '....ese..', '.c.ese...', '..cse....', '..mc.....', '.mm.c....', 'mm.......'],
    'dinheiro':  ['...ccc...', '....c....', '..MMMMM..', '.MMMYMMM.', '.MMYYYMM.', '.MMMYYMM.', '.MMYYYMM.', '.MMMYMMM.', '..MMMMM..'],
    'peixe':     ['.........', '.....bbb.', 'b...bbbbb', 'bb.bbbbwb', '.bbbbbbbb', 'bb.bbbbbb', 'b...bbbb.', '.....bb..', '.........'],
    'caveira':   ['..xxxxx..', '.xxxxxxx.', 'xxxxxxxxx', 'xBBxxxBBx', 'xBBxxxBBx', 'xxxxBxxxx', '.xxxxxxx.', '..xBxBx..', '..xxxxx..'],
    'trofeu':    ['YYYYYYYYY', 'YuYYYYYYY', '.YYYYYYY.', 'Y.YYYYY.Y', '..YYYYY..', '...YYY...', '....Y....', '...YYY...', '..ccccc..'],
    'raio':      ['.....YY..', '....YY...', '...YY....', '..YYYYY..', '....YY...', '...YY....', '..YY.....', '.YY......', '.Y.......'],
    'check':     ['.........', '........v', '.......vv', '......vv.', 'v....vv..', 'vv..vv...', '.vvvv....', '..vv.....', '.........'],
    'xis':       ['.........', '.rr...rr.', '..rr.rr..', '...rrr...', '...rrr...', '..rr.rr..', '.rr...rr.', '.........', '.........'],
    'musica':    ['.........', '...PPPPP.', '...PPPPP.', '...P...P.', '...P...P.', '.PPP.PPP.', 'PPPPPPPP.', '.PP..PP..', '.........'],
    'creeper':   ['vvvvvvvvv', 'vGvvvvvGv', 'vBBvvvBBv', 'vBBvvvBBv', 'vvvBBBvvv', 'vvBBBBBvv', 'vvBBBBBvv', 'vvBvvvBvv', 'vvvvvvvvv'],
    'presente':  ['..r...r..', '...r.r...', 'PPPPrPPPP', 'PPPPrPPPP', 'rrrrrrrrr', 'PPPPrPPPP', 'PPPPrPPPP', 'PPPPrPPPP', 'PPPPrPPPP'],
    'gg':        ['.........', '.ggg.ggg.', 'g...g....', 'g.gGg.gg.', 'g..gg..g.', '.ggg.ggg.', '.........', '.........', '.........'],
    'picareta':  ['.dddddd..', 'dd....dd.', 'd...mm.d.', '....mm...', '...mm....', '..mm.....', '.mm......', 'mm.......', '.........'],
}

prov = []; lista = []
cod = 0xE100
def salvar(nome, grade, sub=None):
    global cod
    im = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    for y, l in enumerate(grade):
        for x, ch in enumerate(l):
            if ch == '.': continue
            c = cor(CORES[sub if (sub and ch == 'Y') else ch]) if not (sub and ch == 'Y') else cor(sub)
            if ch in 'Y' and not sub:
                c = mix(c, 1.12 if y < 3 else 0.9 if y > 6 else 1.0)
            im.putpixel((x, y), c)
    # contorno escuro de 1 px para destacar no chat
    out = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    out.paste(im, (0, 0))
    im.save(f'{PASTA}/{nome}.png')
    ch = chr(cod); cod += 1
    prov.append({'type': 'bitmap', 'file': f'big:font/emoji/{nome}.png', 'ascent': 8, 'height': 9, 'chars': [ch]})
    lista.append([nome, ch])

for n, f in FACES.items(): salvar(n, rosto('Y', f))
salvar('anjo', ['.wwwwwww.'] + rosto('Y', ESPECIAIS['anjo'][1])[1:])
salvar('diabinho', rosto('Y', ESPECIAIS['diabinho'][1]), sub='9b5de5')
salvar('palhaco', rosto('Y', ESPECIAIS['palhaco'][1]), sub='f4f4f4')
for n, g in ICONES.items(): salvar(n, g)
json.dump({'providers': prov}, open(f'{R}/font/emoji.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump(lista, open(os.path.expanduser('~/mnt/Bigserver/chat-emojis/emojis.json'), 'w', encoding='utf-8'), ensure_ascii=False)
# folha de prévia
S = 10; fol = Image.new('RGBA', (len(lista) * 11 * S, 11 * S), (54, 57, 63, 255))
for i, (n, ch) in enumerate(lista):
    g = Image.open(f'{PASTA}/{n}.png').resize((9 * S, 9 * S), Image.NEAREST)
    fol.alpha_composite(g, (i * 11 * S + S, S))
fol.save(os.path.expanduser('~/mnt/Bigserver/chat-emojis/preview_emojis.png'))
print(len(lista), 'emojis')
