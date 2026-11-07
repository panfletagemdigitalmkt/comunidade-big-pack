# Itens do Paladino: 3 espadas, 3 escudos 3D (com pose de bloqueio), Armadura do Sol Nascente
# (elmo 3D + textura vestida) e a Caixa do Paladino. Rodar dentro de resourcepack/.
import math, random, json, os
from PIL import Image
from voxel import gerar, icone, cor, mix, lerp, espelhar, R

P = 'paladino'
AUR_INI, AUR_FIM = cor('ff9b3d'), cor('fff3c4')
NAVY = [cor('101a3d'), cor('16224d'), cor('0c1430')]

MAT = {
    'b': ([cor('b9c0c8'), cor('c8ced5'), cor('a9b1ba')], 2.0, False),   # aço
    'e': ([cor('eef2f5'), cor('ffffff'), cor('dfe5ea')], 1.0, False),   # fio
    'f': ([cor('8b939c'), cor('7d858e')], 1.4, False),                  # sulco da lâmina
    'd': ([cor('5d646d'), cor('4b525a'), cor('6b737c')], 2.6, False),   # ferro da guarda
    'l': ([cor('5a3820'), cor('6b4428'), cor('4a2e1a')], 2.4, False),   # couro do cabo
    'c': ([cor('1f4fa8'), cor('2a5fc0'), cor('183f88')], 0.8, False),   # fita azul
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 2.6, False),   # ouro
    'Y': ([cor('ffd23f'), cor('ffe27a')], 3.0, True),                   # gema-sol
    'o': ([cor('efe9dc'), cor('e2dac8')], 2.4, False),                  # marfim
    'A': ([cor('ffd18a')], 2.0, True),                                  # lâmina da aurora
    'S': (NAVY, 2.0, True),                                             # metal estelar
    'E': ([cor('bff3ff'), cor('e6fbff')], 1.2, True),                   # fio celeste
    'W': ([cor('f4f4f2'), cor('e6e6e2'), cor('d9d9d4')], 1.6, False),   # asas
    'B': ([cor('4fc3ff'), cor('8fdcff')], 3.0, True),                   # gema azul
}

def pulso(c0, f, n, a=0.25):
    return mix(c0, 1 - a + a * (1 + math.sin(2 * math.pi * f / n)))

def anim(ch, x, y, f, n, c0):
    if ch == 'A':
        t = 1 - y / 21
        c = lerp(AUR_INI, AUR_FIM, t)
        faixa = 21 - (f / n) * 26
        if abs(y - faixa) < 2.2: c = mix(c, 1.25)
        return mix(c, 1.1 if (x % 2 == 0) else 0.97)
    if ch == 'S':
        h = (x * 73 + y * 151) % 11
        if h == 0:
            b = 0.5 + 0.5 * math.sin(2 * math.pi * (f / n) + x * 1.7 + y)
            return lerp(c0, cor('ffffff'), b)
        if h == 5: return lerp(c0, cor('6a5acd'), 0.35)
        return c0
    if ch in 'YBE': return pulso(c0, f, n)
    return None

# ------------------------------------------------------------------ espadas
gerar(P, 'espada_juramento', [
    "...............ee",
    "..............ebbe",
    "..............ebbe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............effe",
    "..............ebbe",
    "..............ebbe",
    "..............ebbe",
    "..............ebbe",
    "............ddebbedd",
    "..........dddddddddddd",
    "..........d..dddddd..d",
    "...............ll.cc",
    "...............ll.c.c",
    "...............ll..cc",
    "...............ll...c",
    "...............ll",
    "...............ll",
    "..............dddd",
    "...............dd",
], MAT, seed=3)

gerar(P, 'espada_aurora', [
    "...............AA",
    "..............eAAe",
    "..............eAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    ".............eAAAAe",
    "...........g.eAAAAe.g",
    "............g.gAAg.g",
    "..........g..gggggg..g",
    "...........gggggggggg",
    "..........ggggggYYgggggg"[:22],
    "...........gggggYYgggg",
    "............gggggggg",
    "...............oo",
    "...............gg",
    "...............oo",
    "...............oo",
    "...............gg",
    "..............gYYg",
    "...............gg",
], MAT, frames=8, anim=anim, seed=4)

gerar(P, 'espada_justica', espelhar([
    "...............E",
    "..............ES",
    "..............ES",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".............ESS",
    ".W...........ESS",
    ".WW..........ESS",
    "..WW.........ESS",
    "..WWW........ESS",
    "...WWWW......ESS",
    "....WWWWW....ESS",
    ".....WWWWWWggggg",
    "......WWWWgggggB",
    "........WWgggggB",
    "..........gggggg",
    "..............go",
    "...............o",
    "...............g",
    "...............o",
    "...............o",
    "...............g",
    "..............gg",
    "...............B",
]), MAT, frames=8, anim=anim, seed=5)

# ------------------------------------------------------------------ escudos (desenhados por fórmula, 16x24)
MATE = {
    'w': ([cor('ece6d6'), cor('e2dbc9'), cor('f3eee2')], 1.0, False),   # madeira pintada de branco
    'R': ([cor('b3201f'), cor('c42a26'), cor('9e1b1b')], 1.6, False),   # cruz vermelha
    'i': ([cor('8e959d'), cor('a3a9b0'), cor('7a8189')], 1.8, False),   # aro de ferro
    'r': ([cor('d7dbe0')], 2.1, False),                                 # rebite
    'u': ([cor('3e5f8a'), cor('486a96'), cor('35537a')], 1.0, False),   # aço azulado
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 1.7, False),   # ouro
    'G': ([cor('e8b93a'), cor('ffd76a'), cor('d4a12c')], 2.3, False),   # ouro em relevo
    'Y': ([cor('ffd23f'), cor('fff0a0')], 2.9, True),                   # sol
    'p': ([cor('f7f3ea'), cor('ffffff'), cor('ece7db')], 1.0, False),   # esmalte branco
}

def grade(fn):
    return [''.join(fn(x, y) for x in range(16)) for y in range(24)]

TEMPLARIO = [
    "iiiiiiiiiiiiiiii",
    "iwwwwwwRRwwwwwwi",
    "iwrwwwwRRwwwwrwi",
    "iwwwwwwRRwwwwwwi",
    "iwwwwwwRRwwwwwwi",
    "iwwwwwwRRwwwwwwi",
    "iRRRRRRRRRRRRRRi",
    "iRRRRRRRRRRRRRRi",
    "iwwwwwwRRwwwwwwi",
    "iwwwwwwRRwwwwwwi",
    "iwwwwwwRRwwwwwwi",
    "iwwwwwwRRwwwwwwi",
    "iwrwwwwRRwwwwrwi",
    ".iwwwwwRRwwwwwi.",
    ".iwwwwwRRwwwwwi.",
    ".iwwwwwRRwwwwwi.",
    "..iwwwwRRwwwwi..",
    "..iwwwwRRwwwwi..",
    "...iwwwRRwwwi...",
    "...iwwwRRwwwi...",
    "....iwwRRwwi....",
    ".....iwRRwi.....",
    "......iRRi......",
    ".......ii.......",
]
gerar(P, 'escudo_templario', TEMPLARIO, MATE, modo='escudo', seed=6)

def bastiao(x, y):
    dentro = lambda a, b: 0 <= a < 16 and 0 <= b < 24 and (b >= 3 or ((a - 7.5) / 8) ** 2 + ((b - 3) / 3.4) ** 2 <= 1) \
        and not (b >= 22 and (a < 23 - b or a > b - 8))
    if not dentro(x, y): return '.'
    if not all(dentro(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))): return 'g'
    d = math.hypot(x - 7.5, y - 13.5)
    if d < 1.6: return 'Y'
    if d < 2.9: return 'G'
    ang = math.degrees(math.atan2(y - 13.5, x - 7.5)) % 45
    if 2.9 <= d < 5 and (ang < 9 or ang > 36): return 'G'
    if y in (6, 21): return 'g'
    if x in (1, 14) and y % 4 == 1: return 'r'
    return 'u'
gerar(P, 'escudo_bastiao', grade(bastiao), MATE, modo='escudo', seed=7)

def egide(x, y):
    d = math.hypot(x - 7.5, y - 11.5)
    pont = (abs(x - 7.5) <= 1 and (y <= 3 or y >= 20) and (abs(x - 7.5) < 0.6 or y in (2, 3, 20, 21)))
    if d > 7.7 and not pont: return '.'
    if pont and d > 7.7: return 'G'
    if d > 6.7: return 'G'
    if d < 2.3: return 'Y'
    if d < 3.3: return 'g'
    ang = math.degrees(math.atan2(y - 11.5, x - 7.5)) % 45
    if ang < 8 or ang > 37: return 'g'
    return 'p'
gerar(P, 'escudo_egide', grade(egide), MATE, modo='escudo', frames=6,
      anim=lambda ch, x, y, f, n, c0: (lambda b: lerp(c0, cor('fffbe6'), b))(0.5 + 0.5 * math.sin(2 * math.pi * f / n - math.hypot(x - 7.5, y - 11.5) / 2)) if ch == 'Y' else None,
      verso=[cor('d6d2c8'), cor('c9c4b8')], seed=8)

# ------------------------------------------------------------------ elmo 3D e caixa (blocos com pintura)
src = open('gerar_lobo_3d.py', encoding='utf-8').read().split('# ---------------- cabeça de lobo')[0].replace('berserker', P)
exec(src)
TONS.update({'aco': [cor('d8dde4'), cor('c9cfd7'), cor('e6eaee')], 'ouro': [cor('d9a62e'), cor('f0c75a'), cor('c4952a')],
             'sol': [cor('ffd23f'), cor('ffe680')], 'azul': [cor('1e3a8a'), cor('2547a8'), cor('1a3170')],
             'marmore': [cor('ece9e3'), cor('ded9d0'), cor('f5f3ee')], 'branco': [cor('f6f6f3'), cor('e8e8e4')],
             'fenda': [cor('121212'), cor('1c1c1c')]})

h = Modelo('sol_elmo', 128)
h.cubo('topo', [-0.5, 12, -0.5], [16.5, 16.8, 16.5], 'aco')
h.cubo('parede_e', [-1, 0, -0.5], [0, 12, 16.5], 'aco')
h.cubo('parede_d', [16, 0, -0.5], [17, 12, 16.5], 'aco')
h.cubo('nuca', [-0.5, 0, 16], [16.5, 12, 17], 'aco')
h.cubo('frente_baixo', [-0.5, 0, -1], [16.5, 7.5, 0], 'aco')
h.cubo('frente_cima', [-0.5, 9, -1], [16.5, 12, 0], 'aco')
h.cubo('fenda', [0, 7.5, -0.4], [16, 9, -0.2], 'fenda')
h.cubo('cruz_v', [7, 0.5, -1.5], [9, 12.5, -1], 'ouro')
h.cubo('cruz_h', [3, 9.2, -1.4], [13, 10.6, -0.9], 'ouro')
h.cubo('aro_testa', [-1.2, 11.6, -1.3], [17.2, 13, 17.3], 'ouro')
for i, z in enumerate((2, 6, 10)):                       # furos de respiro (rebites)
    h.cubo(f'respiro_e{i}', [-1.3, 3, z], [-1, 4, z + 1], 'fenda')
    h.cubo(f'respiro_d{i}', [17, 3, z], [17.3, 4, z + 1], 'fenda')
h.cubo('sol', [6, 16.5, 7], [10, 20.5, 9], 'sol', brilho=True)
for ang in (-45, -22.5, 0, 22.5, 45):                    # coroa de raios de sol
    h.cubo(f'raio{ang}', [7.3, 16.5, 7.4], [8.7, 25 if ang == 0 else 23.5, 8.6], 'ouro',
           rot={'angle': ang, 'axis': 'z', 'origin': [8, 16.5, 8]} if ang else None)
for nome, xa, s in (('e', -3.2, -1), ('d', 17.0, 1)):    # asinhas
    h.cubo('asa1_' + nome, [xa, 8, 8], [xa + 2.2, 14, 14], 'branco')
    h.cubo('asa2_' + nome, [xa + (-0.8 if s < 0 else 0.8), 11, 10], [xa + (1.4 if s < 0 else 3.0), 17, 14.5], 'branco')
    h.cubo('asa3_' + nome, [xa + (-1.4 if s < 0 else 1.4), 14, 11.5], [xa + (0.8 if s < 0 else 3.6), 19, 15], 'branco')
h.salvar({'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.02, 1.02, 1.02]},
          'gui': {'rotation': [25, -145, 0], 'translation': [0, -1.5, 0], 'scale': [0.55, 0.55, 0.55]},
          'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
          'fixed': {'rotation': [0, 180, 0], 'scale': [0.75, 0.75, 0.75]},
          'thirdperson_righthand': {'rotation': [75, 180, 0], 'translation': [0, 1, -2], 'scale': [0.4, 0.4, 0.4]},
          'firstperson_righthand': {'rotation': [0, 225, 0], 'scale': [0.4, 0.4, 0.4]}})

c = Modelo('caixa_paladino', 128)
c.cubo('corpo', [1, 0, 2], [15, 9.5, 14], 'marmore')
c.cubo('base', [0.5, 0, 1.5], [15.5, 1.5, 14.5], 'ouro')
c.cubo('tampa', [0.5, 9.5, 1.5], [15.5, 13, 14.5], 'marmore')
c.cubo('aro_tampa', [0.3, 9.3, 1.3], [15.7, 10.2, 14.7], 'ouro')
c.cubo('topo', [3, 13, 4], [13, 14, 12], 'marmore')
c.cubo('pano', [6, 13.9, 1.2], [10, 14.4, 14.8], 'azul')
c.cubo('pano_frente', [6, 9, 0.9], [10, 14.2, 1.4], 'azul')
c.cubo('pano_tras', [6, 9, 14.6], [10, 14.2, 15.1], 'azul')
for x0, z0 in ((0.4, 1.4), (13.6, 1.4), (0.4, 12.6), (13.6, 12.6)):
    c.cubo(f'pilar_{x0}_{z0}', [x0, 1.5, z0], [x0 + 2, 9.5, z0 + 2], 'ouro')
c.cubo('sol', [6.2, 3.2, 1.0], [9.8, 6.8, 1.6], 'sol', brilho=True)
c.cubo('sol_aro', [5.5, 2.5, 1.4], [10.5, 7.5, 2], 'ouro')
for ang in (-45, -22.5, 22.5, 45):
    c.cubo(f'raio{ang}', [7.5, 7.5, 1.3], [8.5, 9.4, 1.8], 'ouro', rot={'angle': ang, 'axis': 'z', 'origin': [8, 5, 1.5]})
for nome, xa, s in (('e', -2.5, -1), ('d', 15.5, 1)):
    c.cubo('asa1_' + nome, [xa, 5, 5], [xa + 2, 11, 11], 'branco')
    c.cubo('asa2_' + nome, [xa + (-1 if s < 0 else 1), 8, 6.5], [xa + (1 if s < 0 else 3), 14, 11], 'branco')
c.cubo('gema', [7.2, 14.3, 7.2], [8.8, 15.5, 8.8], 'sol', brilho=True)
c.salvar({'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.58, 0.58, 0.58]},
          'ground': {'translation': [0, 3, 0], 'scale': [0.25, 0.25, 0.25]},
          'fixed': {'rotation': [0, 180, 0], 'scale': [0.5, 0.5, 0.5]},
          'head': {'rotation': [0, 180, 0], 'translation': [0, 14, 0], 'scale': [0.9, 0.9, 0.9]},
          'thirdperson_righthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
          'thirdperson_lefthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
          'firstperson_righthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]},
          'firstperson_lefthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]}})

# ------------------------------------------------------------------ armadura vestida (128x64)
random.seed(31)
S = 2
ACO = [cor('cfd5dc'), cor('dde2e7'), cor('c2c9d1'), cor('e8ecef')]
OURO = [cor('d9a62e'), cor('f0c75a'), cor('c4952a')]
AZUL = [cor('1e3a8a'), cor('2547a8'), cor('1a3170')]
SOL = [cor('ffd23f'), cor('ffe680')]
def face(img, x0, y0, w, h, pal, luz=1.0):
    for x in range(w):
        for y in range(h):
            c = mix(random.choice(pal), luz * (1.08 - 0.22 * y / max(1, h - 1)))
            if (x + y) % 7 == 0: c = mix(c, 1.08)
            img.putpixel((x0 + x, y0 + y), c)
        for y in (0, h - 1): img.putpixel((x0 + x, y0 + y), mix(img.getpixel((x0 + x, y0 + y)), 0.8))
def box(img, u, v, w, h, d, pal):
    u, v, w, h, d = u * S, v * S, w * S, h * S, d * S
    face(img, u + d, v, w, d, pal, 1.15); face(img, u + d + w, v, w, d, pal, 0.75)
    face(img, u, v + d, d, h, pal, 0.9); face(img, u + d, v + d, w, h, pal, 1.0)
    face(img, u + d + w, v + d, d, h, pal, 0.9); face(img, u + 2 * d + w, v + d, w, h, pal, 0.85)
def ret(img, x, y, w, h, pal, luz=1.0):
    for xx in range(x, x + w):
        for yy in range(y, y + h): img.putpixel((xx, yy), mix(random.choice(pal), luz))
def limpa(img, x, y, w, h):
    for xx in range(x, x + w):
        for yy in range(y, y + h): img.putpixel((xx, yy), (0, 0, 0, 0))

cam = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
box(cam, 16, 16, 8, 12, 4, ACO)
ret(cam, 40, 40, 16, 2, OURO, 1.1)                    # gola dourada
for y in range(40, 64):                                # bordas douradas laterais no peito
    for x in (40, 55): cam.putpixel((x, y), random.choice(OURO))
for x in range(41, 55):                                # sol no peito
    for y in range(42, 54):
        d = math.hypot(x - 47.5, y - 47.5)
        a = math.degrees(math.atan2(y - 47.5, x - 47.5)) % 45
        if d < 2.2: cam.putpixel((x, y), random.choice(SOL))
        elif d < 3.2: cam.putpixel((x, y), random.choice(OURO))
        elif d < 5.8 and (a < 7 or a > 38): cam.putpixel((x, y), mix(random.choice(OURO), 1.05))
ret(cam, 44, 54, 8, 10, AZUL)                          # tabardo azul
for y in range(54, 64): cam.putpixel((44, y), random.choice(OURO)); cam.putpixel((51, y), random.choice(OURO))
ret(cam, 64, 40, 16, 24, AZUL, 0.95)                   # capa azul nas costas
for x in range(64, 80): cam.putpixel((x, 40), random.choice(OURO)); cam.putpixel((x, 63), random.choice(OURO))
for x in range(69, 75):
    for y in range(46, 52):
        if math.hypot(x - 71.5, y - 48.5) < 2.8: cam.putpixel((x, y), random.choice(OURO))
box(cam, 40, 16, 4, 12, 4, ACO)                        # braços
for x in range(80, 112):
    for y in range(40, 46): cam.putpixel((x, y), mix(random.choice(ACO), 1.1))
    cam.putpixel((x, 46), random.choice(OURO)); cam.putpixel((x, 47), random.choice(OURO))
    for y in (54, 55): cam.putpixel((x, y), random.choice(OURO))
    for y in (61, 62, 63): cam.putpixel((x, y), random.choice(OURO))
for x in range(88, 96):
    for y in range(32, 40): cam.putpixel((x, y), random.choice(OURO) if x in (88, 95) or y in (32, 39) else mix(random.choice(ACO), 1.15))
limpa(cam, 0, 32, 32, 32); box(cam, 0, 16, 4, 12, 4, ACO); limpa(cam, 0, 40, 32, 14)   # botas
for x in range(0, 32):
    for y in (54, 55): cam.putpixel((x, y), random.choice(OURO))
    cam.putpixel((x, 63), mix(cam.getpixel((x, 63)), 0.7))
limpa(cam, 0, 0, 64, 32)                               # cabeça: o elmo é 3D

cal = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
box(cal, 0, 16, 4, 12, 4, ACO)
for x in range(0, 32):
    for y in (44, 45): cal.putpixel((x, y), random.choice(OURO))
for x in range(8, 16):                                 # joelheira com sol pequeno
    for y in range(46, 52):
        if math.hypot(x - 11.5, y - 48.5) < 2.6: cal.putpixel((x, y), random.choice(OURO))
box(cal, 16, 16, 8, 12, 4, ACO); limpa(cal, 32, 32, 48, 18)
for x in range(32, 80):
    for y in (50, 51, 52): cal.putpixel((x, y), random.choice(OURO))
ret(cal, 44, 53, 8, 11, AZUL)
for d in ('humanoid', 'humanoid_leggings'): os.makedirs(f'{R}/textures/entity/equipment/{d}', exist_ok=True)
cam.save(f'{R}/textures/entity/equipment/humanoid/set_sol.png')
cal.save(f'{R}/textures/entity/equipment/humanoid_leggings/set_sol.png')
os.makedirs(f'{R}/equipment', exist_ok=True)
json.dump({'layers': {'humanoid': [{'texture': 'big:set_sol'}], 'humanoid_leggings': [{'texture': 'big:set_sol'}]}},
          open(f'{R}/equipment/set_sol.json', 'w'), indent=2)

ICO = {'w': ACO, 'g': OURO, 'y': SOL, 'b': AZUL}
icone(P, 'set_sol_peitoral', [
    "", "..ggg......ggg..", ".gwwwg....gwwwg.", ".gwwwwggggwwwwg.", ".gwwwwwwwwwwwwg.", "..gwwwwyywwwwg..",
    "...gwwyyyywwg...", "...gwwwyywwwg...", "...gwwwwwwwwg...", "...gwwbbbbwwg...", "...gwwbbbbwwg...",
    "...gwwbbbbwwg...", "...gggbbbbggg...", "......bbbb......"], ICO)
icone(P, 'set_sol_calcas', [
    "", "", "...gggggggggg...", "...gwwwbbwwwg...", "...gwwwbbwwwg...", "...gwwwggwwwg...", "...gwwg..gwwg...",
    "...gwwg..gwwg...", "...gggg..gggg...", "...gwwg..gwwg...", "...gwwg..gwwg...", "...gwwg..gwwg...", "...gggg..gggg..."], ICO)
icone(P, 'set_sol_botas', [
    "", "", "", "", "", "..gggg....gggg..", "..gwwg....gwwg..", "..gwwg....gwwg..", "..gggg....gggg..",
    "..gwwg....gwwg..", ".gwwwg....gwwwg.", "gwwwwg....gwwwwg", "gggggg....gggggg"], ICO)
print('paladino ok')
