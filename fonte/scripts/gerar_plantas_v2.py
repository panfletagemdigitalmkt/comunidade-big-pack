# Plantações v2: modelos mais cheios e detalhados das 6 safras (4 estágios cada), substituindo os da v1
# (mesmos nomes: big:fazenda/planta_<safra>_<estagio>). Folhas em arco (segmentos), vários tons, frutos com brilho.
# Rodar DEPOIS do gerar_fazenda_pesca.py.
import json, os, random, math, zlib
from PIL import Image
from voxel import cor, mix, R

ANG = (-45, -22.5, 0, 22.5, 45)


def rot(ang, eixo, origem):
    assert ang in ANG, ang
    return {'angle': ang, 'axis': eixo, 'origin': [round(v, 3) for v in origem]}


class Mod:
    def __init__(s, nome, tam=128):
        s.nome, s.tam = nome, tam
        s.img = Image.new('RGBA', (tam, tam), (0, 0, 0, 0)); s.el = []; s.sw = {}; s.n = 0

    def amostra(s, hexc, luz, veio=False):
        k = (hexc, luz, veio)
        if k in s.sw: return s.sw[k]
        i = s.n; s.n += 1; por = s.tam // 8
        x, y = (i % por) * 8, (i // por) * 8
        assert y + 8 <= s.tam, s.nome
        base = cor(hexc); rnd = random.Random(zlib.crc32(f'{hexc}{luz}{s.nome}{veio}'.encode()))
        for xx in range(8):
            for yy in range(8):
                f = luz * rnd.uniform(0.9, 1.07) * (1.06 - 0.12 * yy / 7)
                if veio and xx in (3, 4): f *= 1.13
                s.img.putpixel((x + xx, y + yy), mix(base, f))
        k2 = 16 / s.tam
        s.sw[k] = [(x + 0.5) * k2, (y + 0.5) * k2, (x + 7.5) * k2, (y + 7.5) * k2]
        return s.sw[k]

    def cubo(s, de, ate, c, r=None, brilho=False, topo=None, veio=False):
        faces = {}
        for f, l in (('up', 1.12), ('down', 0.72), ('north', 0.96), ('south', 0.96), ('east', 0.86), ('west', 0.86)):
            faces[f] = {'uv': s.amostra(topo if (f == 'up' and topo) else c, l, veio and f in ('up', 'down')), 'texture': '#0'}
        for v in de + ate: assert -16 <= v <= 32, (s.nome, de, ate)
        e = {'from': [round(v, 3) for v in de], 'to': [round(v, 3) for v in ate], 'faces': faces}
        if r: e['rotation'] = r
        if brilho: e['light_emission'] = 8
        s.el.append(e)

    def seg(s, x, y, z, L, W, dir, ang, c, esp=0.28):
        """Um segmento de folha a partir de (x,y,z) na direção dir (E/W/N/S), inclinado `ang` graus para cima.
        Devolve a ponta (x, y, z) para encadear o próximo segmento."""
        a = math.radians(ang)
        dx, dy = L * math.cos(a), L * math.sin(a)
        if dir == 'E': de, ate, r, fim = [x, y, z - W / 2], [x + L, y + esp, z + W / 2], rot(ang, 'z', [x, y, z]), (x + dx, y + dy, z)
        elif dir == 'W': de, ate, r, fim = [x - L, y, z - W / 2], [x, y + esp, z + W / 2], rot(-ang, 'z', [x, y, z]), (x - dx, y + dy, z)
        elif dir == 'S': de, ate, r, fim = [x - W / 2, y, z], [x + W / 2, y + esp, z + L], rot(-ang, 'x', [x, y, z]), (x, y + dy, z + dx)
        else: de, ate, r, fim = [x - W / 2, y, z - L], [x + W / 2, y + esp, z], rot(ang, 'x', [x, y, z]), (x, y + dy, z - dx)
        s.cubo(de, ate, c, r if ang else None, veio=True)
        return fim

    def folha(s, x, y, z, L, W, dir, cores, angs=(45, 22.5, -22.5)):
        """Folha em arco: vários segmentos encadeados, afinando e mudando de tom."""
        n = len(angs)
        p = (x, y, z)
        for i, a in enumerate(angs):
            p = s.seg(p[0], p[1], p[2], L / n * (1.05 if i == 0 else 1.0), W * (1 - 0.22 * i), dir, a, cores[min(i, len(cores) - 1)])
        return p

    def salvar(s):
        tex = f'big:item/fazenda/{s.nome}'
        disp = {'gui': {'rotation': [25, 45, 0], 'translation': [0, -3, 0], 'scale': [0.5, 0.5, 0.5]},
                'fixed': {'scale': [0.6, 0.6, 0.6]}, 'ground': {'scale': [0.3, 0.3, 0.3]}}
        json.dump({'texture_size': [s.tam, s.tam], 'textures': {'0': tex, 'particle': tex}, 'elements': s.el, 'display': disp},
                  open(f'{R}/models/item/fazenda/{s.nome}.json', 'w'))
        s.img.save(f'{R}/textures/item/fazenda/{s.nome}.png')
        print(s.nome, len(s.el), 'cubos')


CH = -1.0
VERDES = ['6aa84f', '5b9a43', '4c8a38', '3d7a2e']
DIRS = 'EWNS'


# ======================================================= milho: touceira de 3 pés, folhas em arco, espigas
def milho(s):
    m = Mod(f'planta_milho_{s}')
    pes = [(8, 8, 1.0)] if s == 0 else [(7.2, 7.4, 1.0), (10.2, 9.4, 0.82), (6.2, 10.4, 0.7)]
    for k, (px, pz, esc) in enumerate(pes):
        h = [6, 13, 21, 28][s] * esc
        m.cubo([px - 0.6, CH, pz - 0.6], [px + 0.6, CH + h, pz + 0.6], '7aa845')
        for j in range(1, int(h // 5) + 1):                      # nós do colmo
            m.cubo([px - 0.7, CH + j * 5 - 0.4, pz - 0.7], [px + 0.7, CH + j * 5, pz + 0.7], '5f8f34')
        n = [2, 3, 5, 6][s]
        for i in range(n):
            y = CH + (i + 0.8) * h / (n + 1)
            d = DIRS[(i + k) % 4]
            L = [3.5, 5.5, 8, 9][s] * (1 - i * 0.08)
            m.folha(px, y, pz, L, 1.6, d, ['86b84e', '74a843', '5f9437'])
        if s >= 2:
            for (fy, d) in ((0.45, 'E' if k % 2 == 0 else 'W'), (0.62, 'S' if k % 2 == 0 else 'N')):
                y = CH + h * fy
                ox = {'E': 0.6, 'W': -2.6, 'S': -1, 'N': -1}[d]; oz = {'S': 0.6, 'N': -2.6, 'E': -1, 'W': -1}[d]
                x0, z0 = px + ox, pz + oz
                eixo = 'z' if d in 'EW' else 'x'
                ang = -22.5 if d in 'ES' else 22.5
                if eixo == 'x': ang = -ang
                r = rot(ang, eixo, [px, y, pz])
                m.cubo([x0, y, z0], [x0 + 2, y + 5.5, z0 + 2], 'a8c86a', r)      # palha
                if s == 3:
                    m.cubo([x0 + 0.25, y + 2.6, z0 + 0.25], [x0 + 1.75, y + 6.2, z0 + 1.75], 'f2c230', r, topo='ffd84a')
                    m.cubo([x0 + 0.7, y + 6.2, z0 + 0.7], [x0 + 1.3, y + 7.6, z0 + 1.3], 'b0703a', r)   # cabelo
        if s == 3:
            top = CH + h
            m.cubo([px - 0.3, top, pz - 0.3], [px + 0.3, top + 3.2, pz + 0.3], 'd8b56a')
            for d in DIRS: m.folha(px, top + 1.8, pz, 2.6, 0.5, d, ['e0c070', 'cfa457'], (45, 0))
    m.salvar()


# ======================================================= mandioca: hastes avermelhadas, folhas em leque (palmadas)
def leque(m, x, y, z, L, cores, n=5):
    dirs = ['E', 'W', 'N', 'S']
    for i in range(n):
        d = dirs[i % 4]
        m.folha(x, y, z, L * (1 - 0.1 * (i // 4)), 1.0, d, cores, (45, 22.5) if i < 4 else (22.5, 0))


def mandioca(s):
    m = Mod(f'planta_mandioca_{s}')
    hs = [4, 9, 13, 16][s]; L = [2.2, 3.4, 4.4, 5.2][s]
    hastes = [(8, 8, 0)] if s == 0 else [(6.4, 7.0, 0), (9.6, 6.8, -1.5), (8.2, 9.8, -0.8)] + ([(10.4, 10.2, -3)] if s >= 2 else [])
    for i, (x, z, dh) in enumerate(hastes):
        h = hs + dh * (s / 3)
        m.cubo([x - 0.45, CH, z - 0.45], [x + 0.45, CH + h, z + 0.45], 'a0483a')
        for j in range(1, int(h // 3)):
            m.cubo([x - 0.55, CH + j * 3, z - 0.55], [x + 0.55, CH + j * 3 + 0.35, z + 0.55], '7a3a2e')
        leque(m, x, CH + h, z, L, ['4e9238', '43832f', '3b7a2a'], 5 if s < 2 else 7)
        if s >= 2: leque(m, x, CH + h * 0.62, z, L * 0.75, ['5aa043', '4c9038'], 4)
    if s == 3:
        for (x, z, w) in ((4.6, 5.4, 2.6), (10.4, 9.6, 2.4), (6.2, 10.8, 2.2), (11.2, 5.2, 2.0)):
            m.cubo([x, CH - 0.3, z], [x + w, CH + 1.0, z + 1.3], '8b5a33', topo='a06a3c')
            m.cubo([x + w - 0.4, CH + 0.2, z + 0.2], [x + w, CH + 0.8, z + 1.1], 'efe2c4')     # ponta descascada
    m.salvar()


# ======================================================= café: arbusto em camadas com galhos e cachos de grãos
def cafe(s):
    m = Mod(f'planta_cafe_{s}')
    hT = [3, 7, 10, 12][s]
    m.cubo([7.2, CH, 7.2], [8.8, CH + hT, 8.8], '6b4a2b')
    if s == 0:
        for d in 'EW': m.folha(8, CH + hT, 8, 3, 1.8, d, ['3b8a34', '2f7a2c'], (22.5, 0))
        m.salvar(); return
    rnd = random.Random(31 + s)
    camadas = [0.35, 0.6, 0.85] if s >= 2 else [0.7]
    for ci, f in enumerate(camadas):
        y = CH + hT * f
        L = (4.6 - ci * 1.0) * (0.75 if s == 1 else 1)
        for d in DIRS:
            fim = m.seg(8, y, 8, L * 0.55, 0.5, d, 22.5, '5a3c22', 0.5)               # galho
            m.folha(fim[0], fim[1] - 0.2, fim[2], L * 0.7, 2.2, d, ['2f7a2c', '2a6e28', '24622a'], (0, -22.5))
            for d2 in ('N', 'S') if d in 'EW' else ('E', 'W'):
                m.folha(fim[0], fim[1], fim[2], 2.2, 1.6, d2, ['3b8a34', '2f7a2c'], (22.5, 0))
            if s >= 2:
                for k in range(3 if s == 3 else 2):                                  # cacho de grãos no galho
                    t = 0.35 + 0.25 * k
                    gx = 8 + (fim[0] - 8) * t + rnd.uniform(-0.4, 0.4); gz = 8 + (fim[2] - 8) * t + rnd.uniform(-0.4, 0.4)
                    gy = y + (fim[1] - y) * t - 0.9
                    c = rnd.choice(['c2262e', '9e1c24', 'd8402e']) if s == 3 else rnd.choice(['9fc55a', 'b6cf62', 'c8d86a'])
                    m.cubo([gx - 0.5, gy, gz - 0.5], [gx + 0.5, gy + 1.0, gz + 0.5], c)
                    m.cubo([gx - 0.2, gy + 0.65, gz - 0.55], [gx + 0.2, gy + 0.95, gz - 0.45], 'ffffff' if s == 3 else 'd8e8a0')
    m.folha(8, CH + hT, 8, 2.4, 1.6, 'N', ['3b8a34', '2f7a2c'], (45, 22.5))
    m.folha(8, CH + hT, 8, 2.4, 1.6, 'S', ['3b8a34', '2f7a2c'], (45, 22.5))
    m.salvar()


# ======================================================= pimenta: arbusto cheio com pimentas de cores variadas
def pimenta(s):
    m = Mod(f'planta_pimenta_{s}')
    h = [3, 6.5, 9, 10.5][s]
    m.cubo([7.5, CH, 7.5], [8.5, CH + h, 8.5], '4f7f2f')
    galhos = [(h, 'E'), (h, 'W')] + ([(h * 0.7, 'N'), (h * 0.7, 'S')] if s >= 1 else []) + \
             ([(h * 0.5, 'E'), (h * 0.55, 'W'), (h * 0.85, 'N'), (h * 0.85, 'S')] if s >= 2 else [])
    L = [2.2, 3.4, 4.2, 4.6][s]
    for i, (gy, d) in enumerate(galhos):
        fim = m.seg(8, CH + gy, 8, L * 0.5, 0.45, d, 22.5, '4f7f2f', 0.45)
        m.folha(fim[0], fim[1], fim[2], L * 0.8, 1.9, d, ['4c9a3c', '3f8a35', '357a2e'], (22.5, -22.5))
        for d2 in ('N', 'S') if d in 'EW' else ('E', 'W'):
            m.folha(fim[0], fim[1] - 0.1, fim[2], 1.8, 1.4, d2, ['4c9a3c', '3f8a35'], (22.5, 0))
    if s == 2:
        for (x, z, y) in ((10, 8, h - 0.6), (6, 9, h - 1.4), (8.5, 5.8, h - 0.8), (9.6, 10.4, h - 2)):
            m.cubo([x, CH + y, z], [x + 0.9, CH + y + 0.7, z + 0.9], 'f4f4ee', topo='f2d24a')
    if s == 3:
        rnd = random.Random(5)
        cores = ['d8261b', 'e8461b', 'f2a81b', 'c81b2a', 'd8261b', '6ab03a']
        for i, (x, z, y) in enumerate(((10.8, 7.6, 6.5), (4.8, 8.6, 5.6), (8.2, 4.4, 7.2), (8.0, 11.2, 5.8), (11.4, 10.4, 4.6),
                                       (5.2, 5.2, 4.2), (11.0, 5.0, 3.6), (5.6, 11.0, 3.4))):
            c = cores[i % len(cores)]
            m.cubo([x, CH + y - 3.2, z], [x + 1.1, CH + y, z + 1.1], c)
            m.cubo([x + 0.25, CH + y - 3.8, z + 0.25], [x + 0.85, CH + y - 3.2, z + 0.85], c)
            m.cubo([x + 0.15, CH + y - 2.6, z - 0.05], [x + 0.4, CH + y - 0.6, z + 0.05], 'ffb0a0')      # brilho
            m.cubo([x + 0.25, CH + y, z + 0.25], [x + 0.85, CH + y + 0.7, z + 0.85], '3c7a2a')
    m.salvar()


# ======================================================= abacaxi: roseta de folhas espinhosas e fruto com casca em losangos
def abacaxi(s):
    m = Mod(f'planta_abacaxi_{s}')
    L = [3.2, 5.2, 6.8, 7.8][s]
    folhas = ['5d8c56', '4f7d4a', '6a965a', '42703f']
    for i, d in enumerate(DIRS):
        m.folha(8, CH + 0.3, 8, L, 1.4, d, [folhas[i % 4], folhas[(i + 1) % 4]], (45, 22.5))
        if s >= 1: m.folha(8, CH + 0.1, 8, L * 0.95, 1.2, d, [folhas[(i + 2) % 4], '42703f'], (22.5, 0, -22.5))
        if s >= 2: m.folha(8, CH + 0.6, 8, L * 0.75, 1.0, d, ['6a965a', '5d8c56'], (45, 45, 22.5))
    if s >= 1:   # folhas nas diagonais (feitas com dois segmentos girados)
        for (dx, dz) in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
            x, z = 8 + dx * 0.6, 8 + dz * 0.6
            m.cubo([x - 0.5, CH + 0.2, z - 0.5], [x + 0.5, CH + 0.5 + L * 0.35, z + 0.5], '4f7d4a', rot(22.5 * dx, 'z', [x, CH, z]))
    if s == 2:
        m.cubo([6.8, CH + 1, 6.8], [9.2, CH + 4.4, 9.2], '8a9a3a', topo='5f8a3a')
        for d in DIRS: m.folha(8, CH + 4.4, 8, 1.8, 0.7, d, ['3f7a3a'], (45,))
    if s == 3:
        m.cubo([5.5, CH + 1.5, 5.5], [10.5, CH + 8.6, 10.5], 'e0a020', topo='c48a1a')
        m.cubo([5.9, CH + 1.0, 5.9], [10.1, CH + 1.5, 10.1], 'b8801a')
        for row, y in enumerate((CH + 2.2, CH + 3.6, CH + 5.0, CH + 6.4, CH + 7.8)):
            off = 0.7 if row % 2 else 0
            for k in range(3):
                a = 6.2 + off + k * 1.5
                m.cubo([a, y, 5.35], [a + 0.6, y + 0.6, 5.5], '8a5a12')
                m.cubo([a, y, 10.5], [a + 0.6, y + 0.6, 10.65], '8a5a12')
                m.cubo([5.35, y, a], [5.5, y + 0.6, a + 0.6], '8a5a12')
                m.cubo([10.5, y, a], [10.65, y + 0.6, a + 0.6], '8a5a12')
        m.cubo([7.4, CH + 8.6, 7.4], [8.6, CH + 10.2, 8.6], '3f7a3a')
        for d in DIRS:
            m.folha(8, CH + 9.4, 8, 3.2, 0.9, d, ['4f8a44', '3f7a3a'], (45, 45))
            m.folha(8, CH + 9.0, 8, 2.4, 0.8, d, ['5d9452'], (22.5, 0))
    m.salvar()


# ======================================================= morango: folhas trifoliadas, flores e morangos com sementinhas
def trifolio(m, x, y, z, L, d, cores):
    fim = m.seg(x, y, z, L * 0.6, 0.35, d, 45, '5a8f3a', 0.35)                     # pecíolo
    m.folha(fim[0], fim[1], fim[2], L * 0.55, 1.5, d, cores, (22.5, -22.5))
    for d2 in ('N', 'S') if d in 'EW' else ('E', 'W'):
        m.folha(fim[0], fim[1], fim[2], L * 0.45, 1.3, d2, cores, (22.5, 0))


def morango(s):
    m = Mod(f'planta_morango_{s}')
    L = [2.2, 3.4, 4.4, 4.8][s]
    m.cubo([7.6, CH, 7.6], [8.4, CH + 0.8, 8.4], '5a8f3a')
    for i, d in enumerate(DIRS):
        if s == 0 and i > 1: break
        trifolio(m, 8, CH + 0.4 + (i % 2) * 0.4, 8, L, d, ['3f8a35', '358030', '2f7529'])
    if s >= 2:
        for i, (x, z) in enumerate(((10.2, 9.2), (5.4, 6.8), (8.2, 4.6), (6.2, 10.6))):
            if s == 2:   # flores brancas
                m.cubo([x - 0.8, CH + 1.6, z - 0.8], [x + 0.8, CH + 1.9, z + 0.8], 'f8f8f2')
                m.cubo([x - 0.3, CH + 1.9, z - 0.3], [x + 0.3, CH + 2.1, z + 0.3], 'f2d24a')
    if s == 3:
        for (x, z) in ((10.8, 8.4), (4.4, 7.4), (7.6, 4.0), (8.8, 11.4), (11.6, 5.4), (5.0, 11.0)):
            m.cubo([x, CH - 0.1, z], [x + 1.6, CH + 1.5, z + 1.6], 'e0262f')
            m.cubo([x + 0.25, CH - 0.5, z + 0.25], [x + 1.35, CH - 0.1, z + 1.35], 'c81b28')
            for (a, b) in ((0.3, -0.05), (1.0, -0.05)):                              # sementinhas
                m.cubo([x + a, CH + 0.5, z + b], [x + a + 0.3, CH + 0.8, z + b + 0.1], 'f2d24a')
            m.cubo([x + 0.2, CH + 1.5, z + 0.2], [x + 1.4, CH + 1.8, z + 1.4], '3c8a2a')  # sépala
    m.salvar()


for nome, f in {'milho': milho, 'mandioca': mandioca, 'cafe': cafe, 'pimenta': pimenta, 'abacaxi': abacaxi, 'morango': morango}.items():
    for s in range(4): f(s)
print('plantas v2 ok')
