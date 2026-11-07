# Machados vikings do Berserker (3D "voxel": cada linha do desenho vira um bloquinho com espessura)
# e a Caixa do Berserker (baú viking 3D). Rodar dentro de resourcepack/.
import json, os, random, math
from PIL import Image
random.seed(77)
R = 'assets/big'

def cor(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
def mix(c, f):
    return tuple(max(0, min(255, int(x * f))) for x in c[:3]) + (255,)
def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)

# char -> (paleta, espessura, brilha)
MAT = {
    'h': ([cor('6b4a2b'), cor('7a5634'), cor('5c3d22'), cor('86603a')], 2.0, False),   # cabo de madeira
    'k': ([cor('2a211b'), cor('3a2d24'), cor('231b16')], 2.0, False),                  # madeira negra
    'l': ([cor('3e2a1e'), cor('4f3626'), cor('5c4030')], 2.7, False),                  # couro enrolado
    'r': ([cor('c9ced4'), cor('aeb4bb')], 2.9, False),                                 # rebite
    'b': ([cor('8d949c'), cor('9fa6ad'), cor('7d848c'), cor('a9b0b7')], 2.0, False),   # aço
    'e': ([cor('e6ebef'), cor('f5f8fa'), cor('d5dbe0')], 1.0, False),                  # fio da lâmina
    'd': ([cor('4a4f57'), cor('3b3f46'), cor('555b64')], 2.4, False),                  # aço escuro
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('b8861f')], 2.6, False),                  # ouro
    'o': ([cor('e8e1d0'), cor('d4cab3'), cor('f2ece0')], 2.4, False),                  # osso
    'R': ([cor('ff3b30'), cor('ff6a4d'), cor('e0201a')], 2.3, True),                   # runa vermelha
    'Y': ([cor('ffd23f')], 2.8, True),                                                 # olho
    'f': ([cor('5d544b'), cor('6c6258'), cor('7b7065'), cor('8a7e72')], 3.4, False),   # pelo
    'c': ([cor('9e1b1b'), cor('b52424'), cor('7f1414')], 1.0, False),                  # pano vermelho
    'M': ([cor('d8dde6'), cor('c6ccd6'), cor('e9edf2')], 2.0, True),                   # lâmina da lua
}

def espelhar(meia):
    return [l.ljust(16, '.')[:16] + l.ljust(16, '.')[:16][::-1] for l in meia]

def gerar(nome, linhas, frames_lua=0):
    linhas = [l.ljust(32, '.')[:32] for l in linhas] + ['.' * 32] * (32 - len(linhas))
    nf = max(1, frames_lua)
    img = Image.new('RGBA', (32, 32 * nf), (0, 0, 0, 0))
    vazio = lambda x, y: not (0 <= x < 32 and 0 <= y < 32) or linhas[y][x] == '.'
    for y in range(32):
        for x in range(32):
            ch = linhas[y][x]
            if ch == '.': continue
            pal = MAT[ch][0]
            base = pal[(x * 7 + y * 3 + random.randrange(2)) % len(pal)] if ch in 'hk' else random.choice(pal)
            if ch in 'hk' and (y % 3 == 0): base = mix(base, 0.85)                    # veio da madeira
            luz = 1.0
            if vazio(x - 1, y) or vazio(x, y - 1): luz *= 1.18                        # luz vindo de cima/esquerda
            if vazio(x + 1, y) or vazio(x, y + 1): luz *= 0.78
            if ch == 'b' and (x + y) % 5 == 0: luz *= 1.08                            # reflexo do aço
            c0 = mix(base, luz)
            for f in range(nf):
                c = c0
                if ch == 'M' and nf > 1:                                              # lua vai ficando vermelha
                    t = (math.sin(f / nf * 2 * math.pi - math.pi / 2) + 1) / 2
                    c = lerp(c0, mix(cor('c81e1e'), luz), t * (0.55 + 0.45 * (x / 16)))
                img.putpixel((x, y + 32 * f), c)
    k = 16 / 32
    els = []
    for y in range(32):
        x = 0
        while x < 32:
            ch = linhas[y][x]
            if ch == '.': x += 1; continue
            x1 = x
            while x1 + 1 < 32 and linhas[y][x1 + 1] == ch: x1 += 1
            t = MAT[ch][1]
            px = lambda a, b, c_, d: [a * k, b * k, c_ * k, d * k]
            e = {'from': [x - 8, 24 - y - 1, 8 - t / 2], 'to': [x1 + 1 - 8, 24 - y, 8 + t / 2],
                 'rotation': {'angle': -45, 'axis': 'z', 'origin': [8, 8, 8]},
                 'faces': {'south': {'uv': px(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'north': {'uv': px(x1 + 1, y, x, y + 1), 'texture': '#0'},
                           'up': {'uv': px(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'down': {'uv': px(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'east': {'uv': px(x1, y, x1 + 1, y + 1), 'texture': '#0'},
                           'west': {'uv': px(x, y, x + 1, y + 1), 'texture': '#0'}}}
            if MAT[ch][2]: e['light_emission'] = 15
            els.append(e)
            x = x1 + 1
    tex = f'big:item/berserker/{nome}'
    disp = {
        'thirdperson_righthand': {'rotation': [0, -90, 55], 'translation': [0, 4, 0.5], 'scale': [0.6, 0.6, 0.6]},
        'thirdperson_lefthand': {'rotation': [0, 90, -55], 'translation': [0, 4, 0.5], 'scale': [0.6, 0.6, 0.6]},
        'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.48, 0.48, 0.48]},
        'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.48, 0.48, 0.48]},
        'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.5, 0.5, 0.5]},
        'ground': {'translation': [0, 2, 0], 'scale': [0.3, 0.3, 0.3]},
        'fixed': {'rotation': [0, 180, 0], 'scale': [0.55, 0.55, 0.55]},
        'head': {'rotation': [0, 180, 0], 'translation': [0, 13, 7], 'scale': [0.6, 0.6, 0.6]}}
    m = {'texture_size': [32, 32], 'textures': {'0': tex, 'particle': tex}, 'elements': els, 'display': disp}
    for d in ('models/item/berserker', 'textures/item/berserker', 'items/berserker'):
        os.makedirs(f'{R}/{d}', exist_ok=True)
    json.dump(m, open(f'{R}/models/item/berserker/{nome}.json', 'w'))
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/berserker/{nome}'}},
              open(f'{R}/items/berserker/{nome}.json', 'w'), indent=1)
    img.save(f'{R}/textures/item/berserker/{nome}.png')
    mc = f'{R}/textures/item/berserker/{nome}.png.mcmeta'
    if nf > 1:
        json.dump({'animation': {'frametime': 8, 'interpolate': True}}, open(mc, 'w'))
    print(nome, len(els), 'elementos')

# ---------------------------------------------------------------- Presa de Ferro (comum): machado barbado
gerar('machado_presa', [
    "................rr",
    "...............dddd",
    "......eebbbbbbbdhhd",
    ".....ebbbbbbbbbdhhd",
    "....ebbbbbbbbbbdhhd",
    "....ebbbbbbbbbbrhhd",
    "....ebbbbbbbbbbdhhd",
    "....ebbbbbbbbbbdddd",
    "....ebbbbbbbbd..hh",
    "....ebbbbbbbd...hh",
    "....ebbbbbbd....hh",
    "....ebbbbbd.....hhc",
    ".....ebbbd......hh.c",
    "......eed.......hh.o",
    "................hh.o",
    "................ll",
    "................hh",
    "................ll",
    "................hh",
    "................ll",
    "................hh",
    "................ll",
    "................hh",
    "................hh",
    "................hh",
    "................ll",
    "................ll",
    "................hh",
    "................hh",
    "...............dddd",
    "................dd",
])

# ---------------------------------------------------------------- Uivo Rubro (raro): machado dinamarquês com runas
gerar('machado_uivo', [
    "....e...........dd",
    "...eb...........dd",
    "...ebb.........dhhd",
    "..ebbbb.......ddhhdoo",
    "..ebbbbbb....dddhhdooo",
    "..ebbRbbbbbbbbddhhdoooo",
    ".ebbbRRbbbbbbbddhhdooo",
    ".ebbbbRbbbRbbbddhhdoo",
    ".ebbbRRbbRRbbbddhhd",
    ".ebbbbRbbbRbbbddhhd",
    ".ebbbRRbbRbbbbddhhd",
    "..ebbbbbbbbbbbddhhd",
    "..ebbbbbb....dddhhd",
    "..ebbbb.......ddhhd",
    "...ebb.........dhhd",
    "...eb...........hh",
    "....e...........hhc",
    "................hhcc",
    "................llccc",
    "................hh.cc",
    "................ll..c",
    "................hh",
    "................ll",
    "................hh",
    "................hh",
    "................ll",
    "................hh",
    "................hh",
    "................ll",
    "................hh",
    "...............dhhd",
    "................RR",
])

# ---------------------------------------------------------------- Machado do Alfa (épico): duas lâminas e caveira de lobo
gerar('machado_alfa', espelhar([
    "...............e",
    "..............ge",
    ".ee...........gd",
    "eddee........ggd",
    "edddddgg....gooo",
    "eddddddgggggoYoo",
    "edddddddddgooooo",
    "edddddddddggoooo",
    "eddddddgggg.oo.o",
    "edddddg.....o.oo",
    "eddde.......ffff",
    "edde.......fffff",
    ".ee.........ffff",
    "...............h",
    "...............l",
    "...............h",
    "...............l",
    "...............h",
    "...............g",
    "...............h",
    "...............h",
    "...............h",
    "...............l",
    "...............h",
    "...............l",
    "...............h",
    "...............h",
    "...............g",
    "..............gg",
    "...............d",
    "...............e",
]))

# ---------------------------------------------------------------- Garra (comum): machadinha de garras de osso
gerar('machadinha_garra', [
    "", "", "", "", "", "",
    "...............dd",
    "..dd..........dhhd",
    "...ooo........dhhd",
    "....ooooo.....dhhd",
    ".dd..ooooooooodhhd",
    "...oooo..ooooodhhd",
    ".....ooooooooodhhd",
    "..dd....oooooodhhd",
    "....ooo..ooooodhhd",
    "......oooooo..dhhd",
    "..........oooodhhd",
    "..............dhhd",
    "...............hh",
    "...............ll",
    "...............hh",
    "...............ll",
    "...............hh",
    "...............ll",
    "...............hh",
    "...............hh",
    "...............ll",
    "...............hh",
    "..............oddo",
    "...............oo",
])

# ---------------------------------------------------------------- Rasgadora (raro): lâmina-gancho serrilhada
gerar('machadinha_rasgo', [
    "", "", "", "", "",
    "...............ee",
    "..............dddd",
    ".......ebbbbbbdkkd",
    ".....eebbbbbbbdkkd",
    "....ebbbbbbbbbdkkd",
    "...ebbbbdddbbbdkkd",
    "..ebbbdd...bbbdkkd",
    "..ebbd......bbdkkd",
    ".e.bbd.......bdkkd",
    "e..bbd........dkkd",
    ".e.bbd.........kk",
    "..ebbd.........kk",
    ".e.bd..........kk",
    "..ed...........kk",
    "...............ll",
    "...............kk",
    "...............ll",
    "...............kk",
    "...............ll",
    "...............kk",
    "...............kk",
    "...............ll",
    "...............kk",
    "..............rkkr",
    "...............rr",
])

# ---------------------------------------------------------------- Lua Sangrenta (épico): lâmina de lua que fica vermelha
gerar('machadinha_lua', [
    "", "", "",
    "........MM",
    "......MMM",
    ".....MMM",
    "....MMM.......dd",
    "...MMMM.......dood",
    "..MMMMM.......dood",
    "..MMMMM.......dood",
    "..MMMMMggggggggood",
    "..MMMMMgggggggdRRd",
    "..MMMMMggggggggood",
    "..MMMMM.......dood",
    "..MMMMM.......dood",
    "...MMMM.......dood",
    "...MMMM........oo",
    "....MMM........oo",
    ".....MMM.......ll",
    "......MMM......oo",
    "........MM.....ll",
    "...............oo",
    "...............ll",
    "...............oo",
    "...............ll",
    "...............oo",
    "...............RR",
    "..............c..c",
    "..............c..c",
], frames_lua=6)

# ---------------------------------------------------------------- Caixa do Berserker: baú viking 3D
exec(open('gerar_lobo_3d.py').read().split('# ---------------- cabeça de lobo')[0])
TONS['madeira'] = [cor('3b2a1d'), cor('47331f'), cor('523b25'), cor('2f2217')]
TONS['runa'] = [cor('ff3b30'), cor('ff5a3d')]
c = Modelo('caixa_berserker', 128)
c.cubo('corpo', [1, 0, 2], [15, 10, 14], 'madeira')
c.cubo('tampa', [0.5, 10, 1.5], [15.5, 14, 14.5], 'madeira')
for x0 in (2.8, 11.4):                                  # cintas de ferro
    c.cubo(f'cinta_{x0}', [x0, -0.1, 1.3], [x0 + 1.8, 14.3, 14.7], 'ferro')
for x0, z0 in ((0.6, 1.6), (13.4, 1.6), (0.6, 12.4), (13.4, 12.4)):  # cantoneiras
    c.cubo(f'canto_{x0}_{z0}', [x0, 0, z0], [x0 + 2, 2, z0 + 2], 'ferro')
c.cubo('fechadura', [6.5, 8, 1.1], [9.5, 11.5, 1.6], 'ferro')
c.cubo('cranio', [5.5, 2.5, 0.8], [10.5, 7, 2], 'osso')
c.cubo('focinho', [6.6, 1.8, -0.6], [9.4, 4.2, 0.8], 'osso')
c.cubo('nariz', [7.4, 3.6, -0.8], [8.6, 4.4, -0.6], 'nariz')
c.cubo('olho_e', [6.1, 5, 0.6], [7.3, 6, 0.8], 'runa', brilho=True)
c.cubo('olho_d', [8.7, 5, 0.6], [9.9, 6, 0.8], 'runa', brilho=True)
for i, x in enumerate((6.8, 8.6)):
    c.cubo(f'presa{i}', [x, 0.8, -0.2], [x + 0.6, 2, 0.4], 'dente')
for nome, xa, xb, s in (('e', -1.5, 0.5, -1), ('d', 15.5, 17.5, 1)):   # chifres nos lados
    c.cubo('chifre_base_' + nome, [xa, 10.5, 6.5], [xb, 12.5, 9.5], 'osso')
    xm = xa - 0.5 if s < 0 else xb - 1.5
    c.cubo('chifre_meio_' + nome, [xm, 12.5, 7], [xm + 2, 15, 9], 'osso')
    xp = xm - 0.3 if s < 0 else xm + 0.8
    c.cubo('chifre_ponta_' + nome, [xp, 15, 7.5], [xp + 1.5, 17, 8.5], 'escuro')
c.cubo('pele_topo', [2, 14, 4], [14, 15, 12.5], 'pelo')
c.cubo('pele_caida', [2.5, 11, 12.5], [13.5, 15, 15.2], 'pelo')
c.cubo('pele_gola', [2, 14.6, 5], [14, 15.3, 7], 'claro')
for i, (x, y) in enumerate(((1.6, 11.5), (13.2, 11.5), (1.6, 4.5), (13.2, 4.5))):  # runas que brilham
    c.cubo(f'runa{i}', [x, y, 1.2], [x + 1.2, y + 2.2, 1.45], 'runa', brilho=True)
c.salvar({'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.58, 0.58, 0.58]},
          'ground': {'translation': [0, 3, 0], 'scale': [0.25, 0.25, 0.25]},
          'fixed': {'rotation': [0, 180, 0], 'scale': [0.5, 0.5, 0.5]},
          'head': {'rotation': [0, 180, 0], 'translation': [0, 14, 0], 'scale': [0.9, 0.9, 0.9]},
          'thirdperson_righthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
          'thirdperson_lefthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
          'firstperson_righthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]},
          'firstperson_lefthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]}})
print('caixa ok')
