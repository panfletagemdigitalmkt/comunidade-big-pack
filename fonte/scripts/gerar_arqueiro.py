# Itens do Arqueiro: 3 arcos 3D (com animação de puxar), 3 adagas, Manto do Falcão (capuz 3D + textura) e caixa.
import math, random, json
from PIL import Image
from voxel import gerar, icone, cor, mix, lerp, R
import armadura as A

P = 'arqueiro'
MAT = {
    'w': ([cor('7a4a26'), cor('8a5630'), cor('6a3f20')], 2.2, False),   # teixo
    'v': ([cor('dfe6ea'), cor('cdd6dc'), cor('eef2f4')], 2.2, False),   # madeira-prata do vento
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 2.4, False),   # ouro
    'l': ([cor('4a2e1a'), cor('5a3820'), cor('3e2616')], 2.8, False),   # couro do punho
    's': ([cor('ece8dc'), cor('ddd8ca')], 0.6, False),                  # corda
    'a': ([cor('8a6a44'), cor('9b7a50')], 1.0, False),                  # haste da flecha
    'p': ([cor('9aa1a8'), cor('c3c8cd')], 1.4, False),                  # ponta da flecha
    'q': ([cor('e9e9e9'), cor('c94b3a')], 1.0, False),                  # pena da flecha
    'C': ([cor('5ff2ff'), cor('a8f8ff')], 2.5, True),                   # runa do vento
    'c': ([cor('3fb7d6'), cor('59cbe6')], 0.8, False),                  # fita
    'F': ([cor('6b4a2b'), cor('7d5835'), cor('f1ece2')], 1.4, False),   # penas de falcão
    'H': ([cor('5b3b22'), cor('6e4a2c')], 3.0, False),                  # cabeça do falcão
    'k': ([cor('e8b23a'), cor('d29a22')], 3.2, False),                  # bico
    'Y': ([cor('ffd23f')], 3.3, True),                                  # olho/gema
    'o': ([cor('ede6d4'), cor('ddd3bd')], 2.6, False),                  # ponta de chifre
    # adagas
    'x': ([cor('3d4250'), cor('4a5060'), cor('2f3440'), cor('5a6172')], 1.8, False),  # sílex
    'b': ([cor('c3c9d0'), cor('d6dbe0'), cor('aab2ba')], 1.4, False),   # aço fino
    'e': ([cor('f2f5f7'), cor('ffffff')], 0.9, False),                  # fio
    'n': ([cor('1b1b1b'), cor('262626')], 2.4, False),                  # preto
    'y': ([cor('f2c230'), cor('e0ad1c')], 2.4, False),                  # amarelo
    'V': ([cor('7dff6b'), cor('b5ff9e')], 1.6, True),                   # veneno
    'G': ([cor('1f4d2b'), cor('2a6338'), cor('173d21')], 1.8, True),    # lâmina sombra verde
    'L': ([cor('3f8f3a'), cor('4fa648'), cor('357a31')], 1.6, False),   # folha
    'E': ([cor('3dff8c'), cor('9effc4')], 2.8, True),                   # esmeralda
}

DISP_ARCO = {
    'thirdperson_righthand': {'rotation': [-80, 260, -40], 'translation': [-1, -2, 2.5], 'scale': [0.5, 0.5, 0.5]},
    'thirdperson_lefthand': {'rotation': [-80, -280, 40], 'translation': [-1, -2, 2.5], 'scale': [0.5, 0.5, 0.5]},
    'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.4, 0.4, 0.4]},
    'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.4, 0.4, 0.4]},
    'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.5, 0.5, 0.5]},
    'ground': {'translation': [0, 2, 0], 'scale': [0.3, 0.3, 0.3]},
    'fixed': {'rotation': [0, 180, 0], 'scale': [0.55, 0.55, 0.55]}}

def reta(g, x0, y0, x1, y1, ch, so_vazio=True):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        if 0 <= x < 32 and 0 <= y < 32 and (not so_vazio or g[y][x] == '.'): g[y][x] = ch

def arco(estilo, puxada):
    g = [['.'] * 32 for _ in range(32)]
    cy, L = 15.5, 13.5
    madeira = {'caca': 'w', 'vento': 'v', 'falcao': 'g'}[estilo]
    ant = None
    for y in range(2, 30):
        t = (y - cy) / L
        x = round(15 - 7 * (1 - t * t))
        xs = range(min(x, ant), max(x, ant) + 1) if ant is not None else [x]
        for xx in xs:
            g[y][xx] = madeira; g[y][xx + 1] = madeira
        ant = x
    for y, dx in ((2, 2), (3, 2), (28, 2), (29, 2)):              # pontas recurvas
        x = round(15 - 7 * (1 - ((y - cy) / L) ** 2))
        g[y][x + dx] = 'o' if estilo == 'caca' else madeira
    for y in range(13, 19):                                        # punho
        for x in range(7, 11): g[y][x] = 'l'
    if estilo == 'vento':
        for y in (6, 10, 21, 25):
            x = round(15 - 7 * (1 - ((y - cy) / L) ** 2)); g[y][x] = 'C'
        for y in range(19, 25): g[y][9 - (y - 19) // 3] = 'c'       # fita pendurada
        for (x, y) in ((17, 1), (18, 0), (17, 30), (18, 31)): g[y][x] = 'C'
    if estilo == 'falcao':
        for y in list(range(4, 12)) + list(range(20, 28)):           # asas de penas ao longo dos braços
            x = round(15 - 7 * (1 - ((y - cy) / L) ** 2))
            comp = 3 if y % 2 == 0 else 2
            for k in range(1, comp + 1):
                if 0 <= x - k: g[y][x - k] = 'F'
        for y in range(13, 18):                                    # cabeça de falcão no punho
            for x in range(5, 8): g[y][x] = 'H'
        g[14][6] = 'Y'; g[16][4] = 'k'; g[15][4] = 'k'; g[16][3] = 'k'
        g[15][10] = 'Y'
    # corda
    xn = 17 + puxada * 3
    reta(g, 17, 2, xn, 15, 's'); reta(g, 17, 29, xn, 16, 's')
    if puxada == 0:
        for y in range(2, 30):
            if g[y][17] == '.': g[y][17] = 's'
    else:                                                          # flecha encaixada
        ponta = xn - 17
        for x in range(ponta + 2, xn):
            g[15][x] = 'a'
        g[15][ponta] = 'p'; g[15][ponta + 1] = 'p'; g[14][ponta + 1] = 'p'; g[16][ponta + 1] = 'p'
        for x in (xn - 3, xn - 2):
            g[14][x] = 'q'; g[16][x] = 'q'
    return [''.join(r) for r in g]

def fazer_arco(nome, estilo, seed):
    for i in range(4):
        sufixo = '' if i == 0 else f'_puxando_{i - 1}'
        gerar(P, nome + sufixo, arco(estilo, i), MAT, disp=DISP_ARCO, sem_item=True, seed=seed)
    m = lambda s: {'type': 'minecraft:model', 'model': f'big:item/{P}/{nome}{s}'}
    item = {'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item', 'on_false': m(''),
                      'on_true': {'type': 'minecraft:range_dispatch', 'property': 'minecraft:use_duration', 'scale': 0.05,
                                  'entries': [{'threshold': 0.65, 'model': m('_puxando_1')}, {'threshold': 0.9, 'model': m('_puxando_2')}],
                                  'fallback': m('_puxando_0')}}}
    json.dump(item, open(f'{R}/items/{P}/{nome}.json', 'w'), indent=1)

fazer_arco('arco_caca', 'caca', 11)
fazer_arco('arco_vento', 'vento', 12)
fazer_arco('arco_falcao', 'falcao', 13)

def pisca(ch, x, y, f, n, c0):
    if ch in 'VE': return mix(c0, 0.75 + 0.35 * (1 + math.sin(2 * math.pi * f / n + x)) / 2)
    if ch == 'G':
        faixa = 22 - (f / n) * 16
        return mix(c0, 1.5) if abs(y - faixa) < 1.2 else c0
    return None

gerar(P, 'adaga_silex', [
    "", "", "", "", "", "", "", "", "",
    "...............x",
    "..............xxx",
    "..............xxx",
    ".............xxxxx",
    ".............xxxxx",
    ".............xxxxx",
    "..............xxx",
    "..............xxx",
    "...............x",
    "..............llll",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............ll",
    "...............ww",
    "..............llll",
    "...............ll.l",
    "................l..l",
], MAT, seed=21)

gerar(P, 'adaga_vespa', [
    "", "", "", "", "", "",
    "...............V",
    "...............V",
    "...............e",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............eb",
    "..............ebb",
    "............nnnnnn",
    "...........n.yyyy.n",
    "..............nn",
    "..............yy",
    "..............nn",
    "..............yy",
    "..............nn",
    "..............yy",
    ".............nnnn",
    "..............VV",
], MAT, frames=6, anim=pisca, seed=22)

gerar(P, 'adaga_sombra', [
    "", "", "", "", "",
    "..................G",
    ".................GG",
    "................GGe",
    "...............GGGe",
    "...............GGGe",
    "..............GGGe",
    "..............GGGe",
    "..............GGGe",
    "..............GGGe",
    "..............GGGe",
    "...............GGe",
    "...............GGe",
    "...........LL..GG..LL",
    "............LLLEELLL",
    "..............LEEL",
    "...............nn",
    "...............nL",
    "...............nn",
    "...............Ln",
    "...............nn",
    "..............nnnn",
    "...............EE",
], MAT, frames=6, anim=pisca, seed=23)

# ------------------------------------------------------------------ capuz 3D e caixa
Modelo, TONS = A.carregar_modelo(P)
TONS.update({'verde': [cor('2f5e2b'), cor('3a6e34'), cor('284f25')], 'pena': [cor('6b4a2b'), cor('7d5835'), cor('5b3d22')],
             'creme': [cor('efe7d6'), cor('e2d8c2')], 'bico': [cor('e8b23a'), cor('d29a22')], 'bico_esc': [cor('3a2a1a')],
             'madeira': [cor('5b3b22'), cor('6b4428'), cor('4e321d')], 'folha': [cor('3f8f3a'), cor('4fa648'), cor('357a31')],
             'ouro': [cor('d9a62e'), cor('f0c75a')], 'haste': [cor('8a6a44'), cor('9b7a50')], 'ferro': [cor('9aa1a8'), cor('c3c8cd')]})

h = Modelo('falcao_capuz', 128)
h.cubo('topo', [-0.5, 8, -0.5], [16.5, 16.8, 16.5], 'verde')
h.cubo('lado_e', [-0.8, 0.5, 0.5], [1.5, 8, 16], 'verde')
h.cubo('lado_d', [14.5, 0.5, 0.5], [16.8, 8, 16], 'verde')
h.cubo('nuca', [-0.5, -1, 14], [16.5, 8, 16.8], 'verde')
h.cubo('mascara', [2, 11.5, -1.6], [14, 16.2, 0], 'pena')
h.cubo('sobrancelha', [1.5, 14.5, -2], [14.5, 15.6, -1.2], 'creme')
h.cubo('olho_e', [3.5, 12.4, -1.8], [6, 13.8, -1.5], 'olho', brilho=True)
h.cubo('olho_d', [10, 12.4, -1.8], [12.5, 13.8, -1.5], 'olho', brilho=True)
h.cubo('bico', [6.5, 10, -4], [9.5, 13.5, -1.4], 'bico')
h.cubo('bico_ponta', [7, 8.8, -4.6], [9, 10.5, -3], 'bico_esc')
for i, (ang, cor_) in enumerate(((-22.5, 'pena'), (0, 'creme'), (22.5, 'pena'))):    # crista de penas
    h.cubo(f'crista{i}', [7, 16.5, 5 + i * 3], [9, 22, 7 + i * 3], cor_, rot={'angle': ang, 'axis': 'x', 'origin': [8, 16.5, 8]})
for nome, xa in (('e', -2.5), ('d', 16.5)):                                       # penas nas têmporas
    h.cubo('pena1_' + nome, [xa, 9, 3], [xa + 2, 15, 10], 'pena')
    h.cubo('pena2_' + nome, [xa, 12, 9], [xa + 2, 17, 14], 'creme')
h.cubo('cauda_pena', [5, 4, 16.5], [11, 12, 18.5], 'pena')
h.salvar(A.DISP_ELMO)

c = Modelo('caixa_arqueiro', 128)
c.cubo('corpo', [1, 0, 2], [15, 9.5, 14], 'madeira')
c.cubo('tampa', [0.5, 9.5, 1.5], [15.5, 13, 14.5], 'madeira')
c.cubo('pano', [0.3, 9.3, 5.5], [15.7, 13.3, 10.5], 'verde')
for x0 in (2.5, 12):
    c.cubo(f'tira{x0}', [x0, -0.1, 1.3], [x0 + 1.5, 13.2, 14.7], 'couro')
c.cubo('fivela', [6.8, 7, 1.0], [9.2, 10.5, 1.6], 'ouro')
c.cubo('folha1', [1, 13, 2], [5, 13.6, 6], 'folha'); c.cubo('folha2', [11, 13, 10], [15, 13.6, 14], 'folha')
for i, (x, z, ang) in enumerate(((5, 7, 22.5), (8, 9, -22.5), (10.5, 6, 0))):         # flechas cravadas na tampa
    rot = {'angle': ang, 'axis': 'z', 'origin': [x + 0.5, 13, z + 0.5]}
    c.cubo(f'haste{i}', [x, 13, z], [x + 1, 21, z + 1], 'haste', rot=rot)
    c.cubo(f'pena{i}', [x - 0.6, 19, z + 0.3], [x + 1.6, 22, z + 0.7], 'creme', rot=rot)
c.cubo('alvo', [5.5, 2.5, 1.0], [10.5, 6.5, 1.6], 'creme')
c.cubo('alvo_meio', [7.2, 3.7, 0.8], [8.8, 5.3, 1.0], 'olho', brilho=True)
c.salvar(A.DISP_CAIXA)

# ------------------------------------------------------------------ Manto do Falcão vestido
random.seed(41)
VERDE = [cor('2f5e2b'), cor('3a6e34'), cor('284f25'), cor('356630')]
COURO = [cor('5a3820'), cor('6b4428'), cor('4a2e1a')]
PENA = [cor('6b4a2b'), cor('7d5835'), cor('5b3d22')]
CREME = [cor('efe7d6'), cor('e2d8c2')]
OURO = [cor('d9a62e'), cor('f0c75a')]
cam = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cam, 16, 16, 8, 12, 4, VERDE)
A.ret(cam, 40, 40, 16, 3, PENA)                                     # gola de penas
for x in range(40, 56, 2): cam.putpixel((x, 43), random.choice(CREME))
for i in range(18):                                                 # alça da aljava no peito
    for k in range(2): cam.putpixel((41 + i * 14 // 18 + k, 42 + i), random.choice(COURO))
A.ret(cam, 40, 56, 16, 2, COURO); cam.putpixel((47, 56), OURO[0]); cam.putpixel((48, 56), OURO[1])
A.ret(cam, 64, 40, 16, 24, VERDE, 0.9)                              # aljava nas costas
for x in range(67, 74):
    for y in range(42, 62): cam.putpixel((x, y), random.choice(COURO))
for x in (68, 70, 72):
    for y in (40, 41): cam.putpixel((x, y), random.choice(CREME))
    cam.putpixel((x, 42), cor('c94b3a'))
for y in (46, 56): A.linha_h(cam, 67, 74, y, OURO)
A.box(cam, 40, 16, 4, 12, 4, VERDE)                                 # braços
for x in range(80, 112):
    for y in range(40, 46): cam.putpixel((x, y), random.choice(PENA if (x + y) % 3 else CREME))
    for y in range(56, 63): cam.putpixel((x, y), random.choice(COURO))
for x in range(88, 96):
    for y in range(32, 40): cam.putpixel((x, y), random.choice(PENA))
A.limpa(cam, 0, 32, 32, 32); A.box(cam, 0, 16, 4, 12, 4, COURO); A.limpa(cam, 0, 40, 32, 12)
for x in range(32): cam.putpixel((x, 52), random.choice(PENA)); cam.putpixel((x, 53), random.choice(CREME))
A.limpa(cam, 0, 0, 64, 32)
cal = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cal, 0, 16, 4, 12, 4, [cor('4a3a28'), cor('564430'), cor('3f3122')])
for y in (46, 47): A.linha_h(cal, 0, 32, y, COURO)
A.box(cal, 16, 16, 8, 12, 4, VERDE); A.limpa(cal, 32, 32, 48, 16)
for y in (48, 49, 50): A.linha_h(cal, 32, 80, y, COURO)
A.ret(cal, 49, 51, 4, 5, COURO, 1.2)                                # bolsinha
A.salvar('set_falcao', cam, cal)

ICO = {'v': VERDE, 'c': COURO, 'p': PENA, 'w': CREME, 'g': OURO}
icone(P, 'set_falcao_peitoral', ["", "..ppp......ppp..", ".pvvvp....pvvvp.", ".pvvvvccccvvvvp.", ".pvvvvvcvvvvvvp.",
      "..pvvvvvcvvvvp..", "...pvvvvvcvvp...", "...pvvvvvvcvp...", "...pvvvvvvvcp...", "...pccccgccccp..", "...pvvvvvvvvp...",
      "...pvvvvvvvvp...", "...pppppppppp..."], ICO)
icone(P, 'set_falcao_calcas', ["", "", "...cccccccccc...", "...cvvvccvvvc...", "...cvvvccvvvc...", "...cvvc..cvvc...",
      "...cvvc..cvvc...", "...cccc..cccc...", "...cvvc..cvvc...", "...cvvc..cvvc...", "...cvvc..cvvc...", "...cccc..cccc..."], ICO)
icone(P, 'set_falcao_botas', ["", "", "", "", "", "..pwpw....pwpw..", "..cccc....cccc..", "..cccc....cccc..",
      "..cccc....cccc..", ".ccccc....ccccc.", "cccccc....cccccc", "cccccc....cccccc"], ICO)
print('arqueiro ok')
