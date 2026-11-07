# Fazenda e pescaria: plantas em 4 estágios, colheitas, sacos de semente, 16 peixes e 3 varas.
# Plantas: cubos e folhas inclinadas (como no Blockbench), mostradas no chão por ItemDisplay.
# Itens de mão: desenho em pixels extrudado com espessura por material (peixes ficam "gordinhos" no meio).
import json, os, random, math, zlib
from PIL import Image
from voxel import cor, mix, R

def rot(ang, eixo, origem):
    assert ang in (-45, -22.5, 0, 22.5, 45), ang
    return {'angle': ang, 'axis': eixo, 'origin': [round(v, 3) for v in origem]}

# ======================================================= montador por cubos
class Mod:
    def __init__(s, pasta, nome, tam=64):
        s.pasta, s.nome, s.tam = pasta, nome, tam
        s.img = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); s.el = []; s.sw = {}; s.n = 0
    def amostra(s, hexc, luz):
        k = (hexc, luz)
        if k in s.sw: return s.sw[k]
        i = s.n; s.n += 1; por = s.tam // 4
        x, y = (i % por) * 4, (i // por) * 4
        assert y + 4 <= s.tam, s.nome
        base = cor(hexc); rnd = random.Random(zlib.crc32(f'{hexc}{luz}{s.nome}'.encode()))
        for xx in range(4):
            for yy in range(4):
                s.img.putpixel((x + xx, y + yy), mix(base, luz * rnd.uniform(0.88, 1.08)))
        k2 = 16 / s.tam
        s.sw[k] = [(x + 0.5) * k2, (y + 0.5) * k2, (x + 3.5) * k2, (y + 3.5) * k2]
        return s.sw[k]
    def cubo(s, de, ate, c, r=None, brilho=False, topo=None):
        faces = {}
        for f, l in (('up', 1.12), ('down', 0.72), ('north', 0.96), ('south', 0.96), ('east', 0.86), ('west', 0.86)):
            faces[f] = {'uv': s.amostra(topo if (f == 'up' and topo) else c, l), 'texture': '#0'}
        for v in de + ate: assert -16 <= v <= 32, (s.nome, de, ate)
        e = {'from': [round(v, 3) for v in de], 'to': [round(v, 3) for v in ate], 'faces': faces}
        if r: e['rotation'] = r
        if brilho: e['light_emission'] = 10
        s.el.append(e)
    def folha(s, x, y, z, L, W, dir, incl, c, esp=0.3):
        """Folha saindo de (x,y,z) para E/W/N/S, inclinada para cima `incl` graus (ou diagonal NE/NW/SE/SW reta)."""
        if dir in ('E', 'NE', 'SE'): de, ate = [x, y, z - W / 2], [x + L, y + esp, z + W / 2]
        elif dir in ('W', 'NW', 'SW'): de, ate = [x - L, y, z - W / 2], [x, y + esp, z + W / 2]
        elif dir == 'S': de, ate = [x - W / 2, y, z], [x + W / 2, y + esp, z + L]
        else: de, ate = [x - W / 2, y, z - L], [x + W / 2, y + esp, z]
        if dir == 'E': r = rot(incl, 'z', [x, y, z])
        elif dir == 'W': r = rot(-incl, 'z', [x, y, z])
        elif dir == 'S': r = rot(-incl, 'x', [x, y, z])
        elif dir == 'N': r = rot(incl, 'x', [x, y, z])
        elif dir in ('NE', 'SW'): r = rot(45, 'y', [x, y, z])
        else: r = rot(-45, 'y', [x, y, z])
        s.cubo(de, ate, c, r)
    def salvar(s, display):
        tex = f'big:item/{s.pasta}/{s.nome}'
        for d in ('models/item', 'textures/item', 'items'): os.makedirs(f'{R}/{d}/{s.pasta}', exist_ok=True)
        json.dump({'texture_size': [s.tam, s.tam], 'textures': {'0': tex, 'particle': tex}, 'elements': s.el, 'display': display},
                  open(f'{R}/models/item/{s.pasta}/{s.nome}.json', 'w'))
        json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/{s.pasta}/{s.nome}'}},
                  open(f'{R}/items/{s.pasta}/{s.nome}.json', 'w'), indent=1)
        s.img.save(f'{R}/textures/item/{s.pasta}/{s.nome}.png')
        print(s.nome, len(s.el), 'cubos')

DISP_PLANTA = {'gui': {'rotation': [25, 45, 0], 'translation': [0, -3, 0], 'scale': [0.5, 0.5, 0.5]},
               'fixed': {'scale': [0.6, 0.6, 0.6]}, 'ground': {'scale': [0.3, 0.3, 0.3]}}

# chão da planta: o ItemDisplay fica no centro do bloco de cima da terra arada (que tem 15/16 de altura)
CH = -1.0

# ======================================================= plantas (4 estágios)
def milho(s):
    m = Mod('fazenda', f'planta_milho_{s}')
    h = [6, 13, 21, 28][s]
    m.cubo([7.4, CH, 7.4], [8.6, CH + h, 8.6], '6f9b3c')
    n = [2, 3, 5, 6][s]; L = [3, 5, 7, 8][s]
    for i in range(n):
        y = CH + (i + 1) * h / (n + 1.3)
        d = 'EWSN'[i % 4]
        m.folha(8, y, 8, L - i * 0.4, 1.7, d, 22.5 if i % 2 else 45, '7fb24a' if i % 2 else '64983a')
    if s >= 2:
        for (y, d) in ((CH + h * 0.42, 1), (CH + h * 0.6, -1)):
            x0 = 8.6 if d > 0 else 5.6
            m.cubo([x0, y, 7.2], [x0 + 1.8, y + 5, 8.8], '9cc25c', rot(-22.5 * d, 'z', [8, y, 8]))
            if s == 3:
                m.cubo([x0 + 0.3, y + 3.2, 7.45], [x0 + 1.5, y + 5.8, 8.55], 'f2c230', rot(-22.5 * d, 'z', [8, y, 8]))
                m.cubo([x0 + 0.6, y + 5.8, 7.8], [x0 + 1.2, y + 7, 8.2], 'b07a3a', rot(-22.5 * d, 'z', [8, y, 8]))
    if s == 3:
        top = CH + h
        m.cubo([7.6, top, 7.6], [8.4, top + 3, 8.4], 'd8b56a')
        for d in 'EWNS': m.folha(8, top + 1.5, 8, 2.5, 0.6, d, 45, 'cfa457')
    m.salvar(DISP_PLANTA)

def mandioca(s):
    m = Mod('fazenda', f'planta_mandioca_{s}')
    hs = [4, 8, 12, 15][s]; L = [2, 3.2, 4.2, 5][s]
    for i, (x, z, dh) in enumerate(((6.2, 7.0, 0), (9.6, 6.6, -1.5), (8.0, 9.8, -0.8))):
        if s == 0 and i: continue
        h = hs + dh * (s / 3)
        m.cubo([x - 0.45, CH, z - 0.45], [x + 0.45, CH + h, z + 0.45], '9b4a3c')
        for j, d in enumerate(('E', 'W', 'N', 'S', 'NE' if i % 2 else 'SE')):
            m.folha(x, CH + h, z, L, 1.1, d, 22.5 if j % 2 else 45, '4e9238' if j % 2 else '3f7f2e', 0.25)
        if s >= 2:
            for d in ('SW', 'NW'):
                m.folha(x, CH + h * 0.6, z, L * 0.7, 1, d, 0, '57983f', 0.25)
    if s == 3:
        for (x, z) in ((5, 5.5), (10.5, 9.5), (6.5, 10.5)):
            m.cubo([x, CH - 0.2, z], [x + 2.2, CH + 0.9, z + 1.4], '8b5a33', topo='a06a3c')
    m.salvar(DISP_PLANTA)

def cafe(s):
    m = Mod('fazenda', f'planta_cafe_{s}')
    hT = [3, 6, 9, 11][s]
    m.cubo([7.3, CH, 7.3], [8.7, CH + hT, 8.7], '6b4a2b')
    if s == 0:
        for d in 'EW': m.folha(8, CH + hT, 8, 2.5, 1.6, d, 22.5, '2f7a2c')
        m.salvar(DISP_PLANTA); return
    tufos = [((8, 6.5, 8), 2.5)] if s == 1 else [((8, CH + hT - 1, 8), 3.2), ((5.5, CH + hT * 0.55, 8), 2.4), ((10.5, CH + hT * 0.6, 8.5), 2.4), ((8, CH + hT * 0.5, 5.5), 2.2), ((8, CH + hT * 0.45, 10.6), 2.2)]
    if s == 3: tufos.append(((8, CH + hT + 1.4, 8), 2.4))
    rnd = random.Random(7 + s)
    for (cx, cy, cz), r in tufos:
        m.cubo([cx - r, cy - r * 0.8, cz - r], [cx + r, cy + r * 0.8, cz + r], '2e6a2a', topo='3b7f33')
        if s >= 2:
            for k in range(5 if s == 3 else 3):
                lado = rnd.choice('EWNS'); a = rnd.uniform(-r + 0.5, r - 1.2); b = rnd.uniform(-r * 0.6, r * 0.5)
                c = rnd.choice(['c2262e', '9e1c24', 'd8402e']) if s == 3 else rnd.choice(['9fc55a', 'b6cf62'])
                if lado == 'E': de = [cx + r, cy + b, cz + a]
                elif lado == 'W': de = [cx - r - 0.9, cy + b, cz + a]
                elif lado == 'S': de = [cx + a, cy + b, cz + r]
                else: de = [cx + a, cy + b, cz - r - 0.9]
                m.cubo(de, [de[0] + 0.9, de[1] + 0.9, de[2] + 0.9], c)
    m.salvar(DISP_PLANTA)

def pimenta(s):
    m = Mod('fazenda', f'planta_pimenta_{s}')
    h = [3, 6, 8.5, 9.5][s]; L = [2, 3, 3.8, 4.2][s]
    m.cubo([7.5, CH, 7.5], [8.5, CH + h, 8.5], '4f7f2f')
    for i, (y, d) in enumerate(((CH + h, 'E'), (CH + h, 'W'), (CH + h * 0.7, 'N'), (CH + h * 0.7, 'S'), (CH + h * 0.45, 'NE'), (CH + h * 0.45, 'SW'), (CH + h * 0.85, 'NW'), (CH + h * 0.85, 'SE'))):
        if s == 0 and i > 1: break
        if s == 1 and i > 3: break
        m.folha(8, y, 8, L, 2.0, d, 22.5 if i % 2 else 45 if len(d) == 1 else 0, '3f8a35' if i % 2 else '4c9a3c')
    if s == 2:
        for (x, z) in ((10, 8), (6, 9), (8.5, 5.8)):
            m.cubo([x, CH + h - 0.4, z], [x + 1, CH + h + 0.5, z + 1], 'f4f4ee', topo='f2d24a')
    if s == 3:
        for (x, z, y) in ((10.6, 7.6, 5.5), (5.0, 8.6, 4.8), (8.2, 4.6, 6.2), (8.0, 11.0, 5.0), (11.2, 10.2, 3.8)):
            m.cubo([x, CH + y - 3, z], [x + 1, CH + y, z + 1], 'd8261b')
            m.cubo([x + 0.2, CH + y, z + 0.2], [x + 0.8, CH + y + 0.6, z + 0.8], '3c7a2a')
    m.salvar(DISP_PLANTA)

def abacaxi(s):
    m = Mod('fazenda', f'planta_abacaxi_{s}')
    L = [3, 5, 6.5, 7.5][s]
    for i, d in enumerate('EWNS'):
        m.folha(8, CH + 0.3, 8, L, 1.3, d, 45, '4f7d4a')
        if s >= 1: m.folha(8, CH + 0.1, 8, L * 0.9, 1.2, ('NE', 'SW', 'NW', 'SE')[i], 0, '5d8c56')
        if s >= 2: m.folha(8, CH + 0.6, 8, L * 0.8, 1.1, d, 22.5, '6a965a')
    if s == 2:
        m.cubo([7, CH + 1, 7], [9, CH + 4, 9], '8a9a3a', topo='5f8a3a')
        for d in 'EWNS': m.folha(8, CH + 4, 8, 1.5, 0.7, d, 45, '3f7a3a')
    if s == 3:
        m.cubo([5.6, CH + 1.5, 5.6], [10.4, CH + 8.5, 10.4], 'e0a020', topo='c48a1a')
        for y in (CH + 2.5, CH + 4.7, CH + 6.9):            # losangos escuros da casca
            for (a, b) in ((5.4, 7), (5.4, 9), (10.4, 8)):
                m.cubo([a, y, b], [a + 0.2, y + 0.7, b + 0.7], '9a6012')
            for (a, b) in ((7.5, 5.4), (9, 10.4), (6.5, 10.4)):
                m.cubo([a, y + 1, b], [a + 0.7, y + 1.7, b + 0.2], '9a6012')
        m.cubo([7.4, CH + 8.5, 7.4], [8.6, CH + 10, 8.6], '3f7a3a')
        for d in 'EWNS': m.folha(8, CH + 9, 8, 2.6, 0.9, d, 45, '3f7a3a')
    m.salvar(DISP_PLANTA)

def morango(s):
    m = Mod('fazenda', f'planta_morango_{s}')
    L = [1.6, 2.6, 3.4, 3.8][s]; y = CH + [0.4, 0.8, 1.2, 1.5][s]
    for i, d in enumerate(('E', 'W', 'N', 'S', 'NE', 'SW', 'NW', 'SE')):
        if s == 0 and i > 2: break
        if s == 1 and i > 4: break
        incl = 22.5 if len(d) == 1 else 0
        m.cubo([7.8, CH, 7.8], [8.2, y, 8.2], '5a8f3a')
        m.folha(8, y + (i % 2) * 0.4, 8, L, 2.4, d, incl, '3f8a35' if i % 2 else '358030')
    if s == 2:
        for (x, z) in ((10, 9), (5.5, 7), (8, 4.8)):
            m.cubo([x, y + 0.5, z], [x + 1.2, y + 1.1, z + 1.2], 'f4f4f0', topo='f2d24a')
    if s == 3:
        for (x, z) in ((10.8, 8.5), (4.5, 7.5), (7.6, 4.2), (8.8, 11.3), (11.4, 5.6)):
            m.cubo([x, CH - 0.1, z], [x + 1.5, CH + 1.6, z + 1.5], 'e0262f', topo='3c8a2a')
    m.salvar(DISP_PLANTA)

PLANTAS = {'milho': milho, 'mandioca': mandioca, 'cafe': cafe, 'pimenta': pimenta, 'abacaxi': abacaxi, 'morango': morango}
for nome, f in PLANTAS.items():
    for s in range(4): f(s)

# ======================================================= itens extrudados
DISP_ITEM = {'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 3, 1], 'scale': [0.55, 0.55, 0.55]},
             'thirdperson_lefthand': {'rotation': [0, 0, 0], 'translation': [0, 3, 1], 'scale': [0.55, 0.55, 0.55]},
             'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
             'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
             'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
             'head': {'rotation': [0, 180, 0], 'translation': [0, 13, 7], 'scale': [1, 1, 1]},
             'fixed': {'rotation': [0, 180, 0], 'scale': [1, 1, 1]},
             'gui': {'rotation': [0, 0, 0], 'scale': [1, 1, 1]}}
DISP_VARA = dict(DISP_ITEM)
DISP_VARA.update({'thirdperson_righthand': {'rotation': [0, 90, 55], 'translation': [0, 4, 2.5], 'scale': [0.85, 0.85, 0.85]},
                  'thirdperson_lefthand': {'rotation': [0, -90, -55], 'translation': [0, 4, 2.5], 'scale': [0.85, 0.85, 0.85]},
                  'firstperson_righthand': {'rotation': [0, 90, 25], 'translation': [0, 1.6, 0.8], 'scale': [0.68, 0.68, 0.68]},
                  'firstperson_lefthand': {'rotation': [0, -90, -25], 'translation': [0, 1.6, 0.8], 'scale': [0.68, 0.68, 0.68]}})

def extrudar(pasta, nome, grade, cores, esp, display, perfil=None, brilho='', item=True, seed=1):
    """grade: lista de strings (ou de listas de char); cores: char -> lista de hex; esp: char -> espessura em pixels."""
    rnd = random.Random(seed)
    H = len(grade); W = max(len(l) for l in grade)
    grade = [list(''.join(l).ljust(W, '.')) for l in grade]
    T = 16 if max(W, H) <= 16 else 32
    k = 16 / max(W, H); ox = (16 - W * k) / 2; oy = (16 - H * k) / 2
    img = Image.new('RGBA', (T, T), (0, 0, 0, 0))
    vazio = lambda x, y: not (0 <= x < W and 0 <= y < H) or grade[y][x] == '.'
    for y in range(H):
        for x in range(W):
            ch = grade[y][x]
            if ch == '.': continue
            luz = 1.0
            if vazio(x, y - 1) or vazio(x - 1, y): luz *= 1.12
            if vazio(x, y + 1) or vazio(x + 1, y): luz *= 0.8
            img.putpixel((x, y), mix(cor(rnd.choice(cores[ch])), luz * rnd.uniform(0.94, 1.04)))
    u = 16 / T
    els = []
    for y in range(H):
        f = perfil(y) if perfil else 1
        x = 0
        while x < W:
            ch = grade[y][x]
            if ch == '.': x += 1; continue
            x1 = x
            while x1 + 1 < W and grade[y][x1 + 1] == ch: x1 += 1
            t = max(0.5, esp[ch] * (f if ch.islower() else 1)) * k
            de = [ox + x * k, oy + (H - 1 - y) * k, 8 - t / 2]
            ate = [ox + (x1 + 1) * k, oy + (H - y) * k, 8 + t / 2]
            frente = [x * u, y * u, (x1 + 1) * u, (y + 1) * u]
            e = {'from': [round(v, 3) for v in de], 'to': [round(v, 3) for v in ate],
                 'faces': {'south': {'uv': frente, 'texture': '#0'},
                           'north': {'uv': [(x1 + 1) * u, y * u, x * u, (y + 1) * u], 'texture': '#0'},
                           'up': {'uv': frente, 'texture': '#0'}, 'down': {'uv': frente, 'texture': '#0'},
                           'east': {'uv': [x1 * u, y * u, (x1 + 1) * u, (y + 1) * u], 'texture': '#0'},
                           'west': {'uv': [x * u, y * u, (x + 1) * u, (y + 1) * u], 'texture': '#0'}}}
            if ch in brilho: e['light_emission'] = 12
            els.append(e)
            x = x1 + 1
    tex = f'big:item/{pasta}/{nome}'
    for d in ('models/item', 'textures/item', 'items'): os.makedirs(f'{R}/{d}/{pasta}', exist_ok=True)
    json.dump({'texture_size': [T, T], 'textures': {'0': tex, 'particle': tex}, 'elements': els, 'display': display},
              open(f'{R}/models/item/{pasta}/{nome}.json', 'w'))
    if item:
        json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/{pasta}/{nome}'}},
                  open(f'{R}/items/{pasta}/{nome}.json', 'w'), indent=1)
    img.save(f'{R}/textures/item/{pasta}/{nome}.png')
    print(nome, len(els), 'elementos')

# ---------------- colheitas
COLHEITAS = {
 'milho': (['......gg........', '.....gGGg.......', '....gGyyGg......', '....gyyyyG......', '...gGyyyyyg.....', '...gyyyyyyG.....',
            '..gGyyyyyyg.....', '..gyyyyyyyG.....', '..gGyyyyyg......', '...gyyyyyG......', '...gGyyyg.......', '....gGGg........',
            '.....ggs........', '......ss........', '.......s........'],
           {'g': ['7fb04a', '6a9a3a'], 'G': ['9bc25c', '8ab650'], 'y': ['f2c230', 'e8b420', 'f7d250'], 's': ['b98a4a', 'a87a3a']},
           {'g': 2.2, 'G': 2.6, 'y': 3.2, 's': 1}),
 'mandioca': (['..........gg.g..', '.........g.gg...', '..........bb....', '.........bBBb...', '........bBBBb...', '.......bBwwBb...',
               '......bBwwwBb...', '.....bBwwwBb....', '....bBwwwBb.....', '...bBwwwBb......', '..bBwwBBb.......', '..bBBBbb........',
               '...bbb..........'],
              {'g': ['4e9238'], 'b': ['6b3f22', '7a4a2a'], 'B': ['8b5a33', '9a6a3c'], 'w': ['f0e2c0', 'e8d6ae']},
              {'g': 0.8, 'b': 2.6, 'B': 3, 'w': 3.2}),
 'cafe': (['................', '.....rr.........', '....rRRr..rr....', '....rRRr.rRRr...', '.....rr..rRRr...', '..rr......rr....',
           '.rRRr..rr.......', '.rRRr.rRRr..rr..', '..rr..rRRr.rRRr.', '.......rr..rRRr.', '...rr.......rr..', '..rRRr...rr.....',
           '..rRRr..rRRr....', '...rr...rRRr....', '.........rr.....'],
          {'r': ['6b3a1f', '5a2f18'], 'R': ['8a4e2a', '9a5a32']}, {'r': 2.2, 'R': 2.8}),
 'pimenta': (['........gg......', '.......gG.......', '.......G........', '......rRr.......', '......rRRr......', '.....rRRRr......',
              '.....rRRRr......', '....rRRRr.......', '....rRRRr.......', '...rRRRr........', '...rRRr.........', '..rRRr..........',
              '..rRr...........', '..rr............'],
             {'g': ['3c7a2a'], 'G': ['4f8f35'], 'r': ['b81a14', 'a8160f'], 'R': ['e0261b', 'ee3a28']}, {'g': 1, 'G': 1.4, 'r': 2.4, 'R': 2.8}),
 'abacaxi': (['......g..g......', '...g..gg.g..g...', '....g.gGgg.g....', '.....gGGGgg.....', '......gGGg......', '.....oyyyyo.....',
              '....oyYyyYyo....', '....yyoyyoyy....', '....yYyyyyYy....', '....oyyoyyyo....', '....yyYyyYyy....', '....yoyyoyyy....',
              '....oyyYyyYo....', '.....yyyoyy.....', '......oyyo......'],
             {'g': ['3f7a3a', '4f8a45'], 'G': ['5d9a50'], 'y': ['e0a020', 'd89818', 'e8b030'], 'Y': ['f2c84a'], 'o': ['9a6012', '8a5410']},
             {'g': 1.2, 'G': 2, 'y': 4, 'Y': 4, 'o': 3.8}),
 'morango': (['................', '.....g.gg.g.....', '....gGGGGGg.....', '.....rGGGr......', '....rRRRRRr.....', '...rRRwRRwRr....',
              '...rRRRRRRRr....', '...rRwRRRwRr....', '....rRRRRRr.....', '....rRRwRRr.....', '.....rRRRr......', '......rRr.......',
              '.......r........'],
             {'g': ['3c8a2a'], 'G': ['4f9a3a'], 'r': ['b8142a', 'c01a30'], 'R': ['e0262f', 'ea3a40'], 'w': ['f4e8a0']},
             {'g': 1, 'G': 1.6, 'r': 3, 'R': 3.6, 'w': 3.8}),
}
for nome, (g, c, e) in COLHEITAS.items():
    extrudar('fazenda', nome, g, c, e, DISP_ITEM, seed=len(nome))

# ---------------- sacos de semente (cor da etiqueta = cor da planta)
COR_SEMENTE = {'milho': 'f2c230', 'mandioca': 'f0e2c0', 'cafe': '8a4e2a', 'pimenta': 'e0261b', 'abacaxi': 'e0a020', 'morango': 'e0262f'}
SACO = ['................', '....pppppppp....', '...pPPPPPPPPp...', '...pppppppppp...', '...p.p.pp.p.p...', '...pppppppppp...',
        '...pLLLLLLLLp...', '...pLccccccLp...', '...pLcCCCCcLp...', '...pLcCCCCcLp...', '...pLccccccLp...', '...pLLLLLLLLp...',
        '...pppppppppp...', '...pppppppppp...', '....pppppppp....']
for nome, c in COR_SEMENTE.items():
    extrudar('fazenda', f'semente_{nome}', SACO,
             {'p': ['b98a5a', 'a87a4a'], 'P': ['8a6a3a'], 'L': ['f2ead2'], 'c': [c], 'C': [c, mix and c]},
             {'p': 1.6, 'P': 1.8, 'L': 1.8, 'c': 2.0, 'C': 2.3}, DISP_ITEM, seed=3)

# ======================================================= peixes
def peixe(nome, comp, alt, dorso, ventre, barb, cauda='forquilha', padrao=None, extras=(), cor_padrao='202020', olho='101010', esp=3.0):
    W, H = 24, 12
    g = [['.'] * W for _ in range(H)]
    cy = 5.5; x0 = (W - comp) // 2 + 2; x1 = x0 + comp - 1
    cx = (x0 + x1) / 2; a = comp / 2; b = alt / 2
    for y in range(H):
        for x in range(x0, x1 + 1):
            dx = (x - cx) / a
            topo = b * (1.02 - dx * dx) ** 0.5 if abs(dx) < 1.01 else 0
            if dx > 0.3: topo *= 1 - (dx - 0.3) * 0.35           # cabeça afina
            if abs(y + 0.5 - cy) <= topo: g[y][x] = 'b' if y + 0.5 < cy + 0.3 else 'v'
    # cauda à esquerda
    for y in range(H):
        d = abs(y + 0.5 - cy)
        for x in range(x0 - 5, x0 + 1):
            k = x0 - x
            if cauda == 'forquilha': ok = d <= 0.8 + k * 0.9 and (k < 2 or d > k * 0.45)
            elif cauda == 'lua': ok = d <= 1 + k * 1.2 and (k < 2 or d > k * 0.75)
            else: ok = d <= 1.2 + k * 0.7
            if ok and 0 <= x < W and g[y][x] == '.': g[y][x] = 'f'
    # nadadeiras dorsal e ventral
    meio = int(cx); top = min(y for y in range(H) if any(g[y][x] in 'bv' for x in range(W)))
    bot = max(y for y in range(H) if any(g[y][x] in 'bv' for x in range(W)))
    dorsal = 'vela' in extras
    for i in range(-2 if not dorsal else -6, 3 if not dorsal else 4):
        x = meio + i
        for j in range(1, (2 if not dorsal else 4) + 1):
            yy = top - j + (1 if j > 1 and i > 1 else 0)
            if 0 <= yy < H and g[yy][x] == '.' and (dorsal or abs(i) + j < 4): g[yy][x] = 'f'
    for i in range(-1, 2):
        yy = bot + 1
        if yy < H and g[yy][meio + i - 1] == '.': g[yy][meio + i - 1] = 'f'
    # padrão
    for y in range(H):
        for x in range(W):
            if g[y][x] not in 'bv': continue
            r = (x * 7 + y * 13) % 5
            if padrao == 'listras' and (x - x0) % 4 == 0 and x < x1 - 2: g[y][x] = 'p'
            elif padrao == 'pintas' and r == 0 and x < x1 - 2: g[y][x] = 'p'
            elif padrao == 'linha' and y == int(cy) and x < x1 - 1: g[y][x] = 'p'
            elif padrao == 'escamas' and x < x0 + comp * 0.45 and (x + y) % 2 == 0 and g[y][x] == 'v': g[y][x] = 'p'
            elif padrao == 'manchas' and ((x // 2 + y // 2) % 3 == 0) and x < x1 - 2: g[y][x] = 'p'
    if padrao == 'ocelo': g[int(cy)][x0 + 1] = 'p'; g[int(cy) - 1][x0 + 1] = 'p'
    # olho e extras
    ey = int(cy) - (1 if alt > 4 else 0); ex = x1 - 2
    g[ey][ex] = 'o'
    if 'dentes' in extras:
        for x in (x1 - 1, x1): g[int(cy) + 1][x] = 'd'
    if 'bigode' in extras:
        for i in range(1, 4):
            if x1 + i < W: g[int(cy) + i // 2][x1 + i] = 'x'
    if 'bico' in extras:
        for i in range(1, 5):
            if x1 + i < W: g[int(cy)][x1 + i] = 'x'
    if 'boca' in extras: g[int(cy) + 1][x1] = 'd'
    cores = {'b': dorso, 'v': ventre, 'f': barb, 'p': [cor_padrao], 'o': [olho], 'd': ['f2f2ea'], 'x': [barb[0]]}
    espessura = {'b': esp, 'v': esp, 'p': esp + 0.1, 'o': esp + 0.3, 'd': esp, 'F': 0.6, 'f': 0.6, 'x': 0.5}
    cyi = cy
    perfil = lambda y: max(0.35, 1 - ((y + 0.5 - cyi) / (b + 0.5)) ** 2 * 0.8)
    # fins não variam com o perfil: troca para maiúscula (espessura fixa)
    g = [[('F' if c == 'f' else c) for c in l] for l in g]
    cores['F'] = barb
    extrudar('pesca', nome, g, cores, espessura, DISP_ITEM, perfil=perfil, seed=len(nome) * 3)

PEIXES = [
 ('lambari', 9, 4, ['b8c4cc', 'a8b6c0'], ['e6ecef'], ['f0c040', 'e05030'], 'forquilha', 'linha', (), '6a7a88'),
 ('tilapia', 13, 7, ['6f7f7a', '7d8c86'], ['c6ccc4'], ['8a6a6a'], 'redonda', 'listras', (), '55625e'),
 ('sardinha', 11, 4, ['3a6fa8', '4a7fb8'], ['dfe8ee'], ['9ab0c4'], 'forquilha', 'pintas', (), '203a5a'),
 ('bagre', 15, 5, ['6b6052', '7a6e5e'], ['c9bea8'], ['5a5046'], 'forquilha', None, ('bigode',), '403830'),
 ('traira', 15, 5, ['4a5230', '565e38'], ['a0a070'], ['3e4428'], 'redonda', 'manchas', ('boca', 'dentes'), '2a2e1a'),
 ('piranha', 10, 8, ['7a8a92', '8a9aa2'], ['d8402e', 'c8301e'], ['5a6a72'], 'lua', 'pintas', ('dentes',), '4a5a62'),
 ('pacu', 12, 9, ['505a60', '5e686e'], ['a8a090'], ['3a4248'], 'redonda', None, (), '303030'),
 ('robalo', 16, 6, ['8a9aa4', '98a8b2'], ['eef2f4'], ['7a8a94'], 'forquilha', 'linha', (), '1a1a1a'),
 ('tucunare', 15, 6, ['8aa040', '9ab04a'], ['e8d860'], ['c86a20'], 'redonda', 'listras', ('boca',), '1a2010'),
 ('tambaqui', 13, 9, ['2e3a30', '3a463a'], ['c8b860'], ['202820'], 'redonda', None, (), '101010'),
 ('garoupa', 16, 8, ['8a4a30', '9a5a3a'], ['c08a60'], ['6a3a24'], 'redonda', 'manchas', ('boca',), '4a2416'),
 ('dourado', 16, 7, ['e8b020', 'f0c030'], ['f8e070'], ['e09010', 'd07a10'], 'forquilha', 'pintas', ('dentes',), 'b07a10'),
 ('pintado', 18, 5, ['8a9096', '9aa0a6'], ['e6e6e0'], ['70767c'], 'forquilha', 'pintas', ('bigode',), '1a1a1a'),
 ('marlim', 16, 6, ['1e4a9a', '2a5ab0'], ['d8e4f0'], ['1a3a80'], 'lua', 'listras', ('bico', 'vela'), '7ab0f0'),
 ('pirarucu', 20, 6, ['4a5a48', '566656'], ['c86048', 'b04a38'], ['8a2a20', 'a03424'], 'redonda', 'escamas', (), 'e04a30'),
 ('mero', 17, 9, ['6a5a3a', '7a6a48'], ['a89a70'], ['4a3e28'], 'redonda', 'manchas', ('boca',), '3a3020'),
]
for p in PEIXES:
    nome, comp, alt, dorso, ventre, barb, cauda, padrao, extras, cp = p
    peixe(nome, comp, alt, dorso, ventre, barb, cauda, padrao, extras, cp, esp=2.2 + alt * 0.25)

# ======================================================= varas de pesca (normal e lançada)
def vara(nome, cores, brilho=''):
    def desenho(lancada):
        g = [['.'] * 16 for _ in range(16)]
        for i in range(14):                       # cabo embaixo à esquerda, ponta em cima à direita
            x, y = 1 + i, 14 - i
            g[y][x] = 'h' if i < 4 else ('n' if i in (6, 9, 12) else 's')
            if i < 3: g[y - 1][x] = 'h'
        g[12][4] = 'm'; g[11][4] = 'm'; g[12][5] = 'm'        # molinete
        g[1][14] = 't'
        if not lancada:
            for y in range(2, 10): g[y][14] = 'l'
            g[10][14] = 'k'; g[10][13] = 'k'; g[9][13] = 'k'
        return [''.join(l) for l in g]
    esp = {'h': 1.8, 's': 1.1, 'n': 1.4, 'm': 2.6, 't': 1.4, 'l': 0.3, 'k': 0.6}
    extrudar('pesca', nome, desenho(False), cores, esp, DISP_VARA, item=False, brilho=brilho, seed=9)
    extrudar('pesca', nome + '_lancada', desenho(True), cores, esp, DISP_VARA, item=False, brilho=brilho, seed=9)
    json.dump({'model': {'type': 'minecraft:condition', 'property': 'minecraft:fishing_rod/cast',
                         'on_false': {'type': 'minecraft:model', 'model': f'big:item/pesca/{nome}'},
                         'on_true': {'type': 'minecraft:model', 'model': f'big:item/pesca/{nome}_lancada'}}},
              open(f'{R}/items/pesca/{nome}.json', 'w'), indent=1)

vara('vara_bambu', {'h': ['7a5a2a', '6a4a22'], 's': ['b8b060', 'c8c070'], 'n': ['6a7a2a'], 'm': ['8a8a8a'], 't': ['6a7a2a'], 'l': ['e8e8e8'], 'k': ['9a9a9a']})
vara('vara_carbono', {'h': ['2a2a2a', '1e1e1e'], 's': ['303036', '26262c'], 'n': ['c0262a'], 'm': ['c8ccd0', 'aab0b4'], 't': ['c0262a'], 'l': ['f0f0f0'], 'k': ['b0b4b8']})
vara('vara_iara', {'h': ['b8862a', 'c8962e'], 's': ['1e9a9a', '2ab0aa'], 'n': ['e8c040'], 'm': ['e8c040', 'f2d060'], 't': ['e8f8ff'], 'l': ['a8f0ff'], 'k': ['e8c040']}, brilho='t')
print('pronto')
