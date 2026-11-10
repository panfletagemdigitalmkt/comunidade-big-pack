# Fazenda BIG — expansão (Etapa 1): 8 culturas novas no mesmo estilo das plantas v2.
#   planta_<id>_<0..3> (modelos 3D por cubos), <id> (colheita extrudada) e semente_<id> (saco com etiqueta).
# Reaproveita o montador Mod do gerar_plantas_v2.py e o extrudar do gerar_fazenda_pesca.py sem rodar os geradores deles.
# Rodar da pasta fonte/:  python3 scripts/gerar_fazenda_expansao.py
import json, os, random, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)


def trecho(arquivo, ate, de=None):
    src = open(os.path.join(AQUI, arquivo), encoding='utf-8').read()
    if de: src = src[src.index(de):]
    return src[:src.index(ate)]


ns = {}
exec(trecho('gerar_plantas_v2.py', "def milho(s):"), ns)                       # Mod, rot, CH, VERDES, DIRS
pesca = {}
exec("import json, os, random, math\nfrom PIL import Image\nfrom voxel import cor, mix, R", pesca)
exec(trecho('gerar_fazenda_pesca.py', "DISP_VARA = dict(DISP_ITEM)", de="DISP_ITEM = {"), pesca)        # só o dicionário
exec(trecho('gerar_fazenda_pesca.py', "# ---------------- colheitas", de="def extrudar("), pesca)         # só a função
Mod, rot, CH, DIRS = ns['Mod'], ns['rot'], ns['CH'], ns['DIRS']
extrudar, DISP_ITEM, R = pesca['extrudar'], pesca['DISP_ITEM'], pesca['R']
for d in ('models/item/fazenda', 'textures/item/fazenda', 'items/fazenda'): os.makedirs(f'{R}/{d}', exist_ok=True)


def item_planta(nome):
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/fazenda/{nome}'}},
              open(f'{R}/items/fazenda/{nome}.json', 'w'), indent=1)


def fim(m):
    m.salvar(); item_planta(m.nome)


# ======================================================= tomate: tutor de madeira, pé que sobe e cachos
def tomate(s):
    m = Mod(f'planta_tomate_{s}')
    h = [3, 8, 12, 13][s]
    if s >= 1: m.cubo([9.2, CH, 9.2], [10.0, CH + 15, 10.0], 'a87a4a', topo='c49a62')         # tutor
    m.cubo([7.6, CH, 7.6], [8.4, CH + h, 8.4], '4f8a35')
    for i in range(2 if s == 0 else 3 + s):
        y = CH + 1 + i * (h - 1) / max(1, 2 + s)
        m.folha(8, y, 8, [2.2, 3.4, 4.0, 4.2][s] * (1 - 0.06 * i), 1.8, DIRS[i % 4], ['4c9a3c', '3f8a35', '357a2e'], (22.5, -22.5))
    if s in (1, 2):
        for (x, z, y) in ((6.2, 8, h * 0.7), (9.8, 7.0, h * 0.5)):
            m.cubo([x, CH + y, z], [x + 0.8, CH + y + 0.5, z + 0.8], 'f2d24a')
    if s >= 2:
        c = 'e0262f' if s == 3 else '7cc04a'
        for (x, z, y) in ((5.6, 7.4, h * 0.45), (10.2, 6.2, h * 0.65), (6.6, 10.2, h * 0.3), (9.4, 10.6, h * 0.8)):
            m.cubo([x, CH + y, z], [x + 1.8, CH + y + 1.6, z + 1.8], c, topo='3c7a2a' if s == 3 else None)
            if s == 3: m.cubo([x + 0.3, CH + y + 1.0, z - 0.05], [x + 0.7, CH + y + 1.4, z + 0.05], 'ffb0a0')
    fim(m)


# ======================================================= soja: arbusto baixo de trifólios e vagens
def soja(s):
    m = Mod(f'planta_soja_{s}')
    h = [2, 4, 6, 6.5][s]
    for (x, z) in ([(8, 8)] if s == 0 else [(7, 7.5), (9.4, 8.8)]):
        m.cubo([x - 0.35, CH, z - 0.35], [x + 0.35, CH + h, z + 0.35], '6a8a3a')
        for i, d in enumerate(DIRS if s else 'EW'):
            folha = ['8a9a4a', '7a8a3a'] if s == 3 else ['5aa043', '4c9038', '3f8030']
            fimg = m.seg(x, CH + h * (0.55 + 0.15 * (i % 2)), z, 1.4, 0.3, d, 45, '6a8a3a', 0.3)
            m.folha(fimg[0], fimg[1], fimg[2], [1.6, 2.4, 3.0, 2.8][s], 1.6, d, folha, (22.5, -22.5))
        if s >= 2:
            c = 'b8a060' if s == 3 else '8cc05a'
            for k, d in enumerate('NS'):
                y = CH + h * (0.35 + 0.2 * k)
                dz = 0.5 if d == 'S' else -1.3
                m.cubo([x - 0.4, y - 1.8, z + dz], [x + 0.4, y, z + dz + 0.8], c)
    fim(m)


# ======================================================= arroz: touceiras de folhas finas e cachos curvados
def arroz(s):
    m = Mod(f'planta_arroz_{s}')
    h = [4, 8, 12, 13][s]
    tufos = [(8, 8)] if s == 0 else [(5.6, 6.2), (10.2, 6.6), (6.4, 10.4), (10.6, 10.2)] + ([(8, 8.2)] if s >= 2 else [])
    verde = ['7cbf4a', '6aae3e', '5a9a35'] if s < 3 else ['c8b45a', 'b8a04a', 'a89040']
    for (x, z) in tufos:
        for i, d in enumerate(DIRS):
            m.folha(x, CH, z, h * 0.55, 0.7, d, verde, (45, 45, 22.5))
        m.cubo([x - 0.3, CH, z - 0.3], [x + 0.3, CH + h * 0.8, z + 0.3], verde[0])
        if s >= 2:
            c = 'e8d070' if s == 3 else 'b8d080'
            p = m.seg(x, CH + h * 0.8, z, 2.6, 0.6, 'E' if x < 8 else 'W', 22.5, c, 0.6)
            m.seg(p[0], p[1], p[2], 2.2, 0.5, 'E' if x < 8 else 'W', -22.5, c, 0.5)
    fim(m)


# ======================================================= algodão: arbusto com capulhos (verdes, depois abertos e brancos)
def algodao(s):
    m = Mod(f'planta_algodao_{s}')
    h = [3, 7, 10, 11][s]
    m.cubo([7.5, CH, 7.5], [8.5, CH + h, 8.5], '6a4a2a')
    L = [2.2, 3.4, 4.2, 4.4][s]
    for i, d in enumerate(DIRS if s else 'EW'):
        for f in ((0.55, 0.9) if s >= 2 else (0.9,)):
            p = m.seg(8, CH + h * f, 8, L * 0.5, 0.4, d, 22.5, '6a4a2a', 0.4)
            m.folha(p[0], p[1], p[2], L * 0.7, 2.0, d, ['3f8a35', '357a2e'] if s < 3 else ['6a7a35', '5a6a2e'], (0, -22.5))
            if s >= 2:
                x, y, z = p
                if s == 2:
                    m.cubo([x - 0.7, y + 0.2, z - 0.7], [x + 0.7, y + 1.6, z + 0.7], '7aa845')
                else:
                    m.cubo([x - 1.1, y + 0.2, z - 1.1], [x + 1.1, y + 2.2, z + 1.1], 'f6f4ee', topo='ffffff')
                    m.cubo([x - 0.4, y - 0.1, z - 0.4], [x + 0.4, y + 0.3, z + 0.4], '5a3a22')
    fim(m)


# ======================================================= cana: colmos segmentados altos com folhas longas
def cana(s):
    m = Mod(f'planta_cana_{s}')
    h = [5, 12, 20, 26][s]
    colmos = [(8, 8, 1.0)] if s == 0 else [(6.8, 7.2, 1.0), (9.4, 7.8, 0.9), (7.6, 9.8, 0.8)]
    for k, (x, z, e) in enumerate(colmos):
        hh = h * e
        cor = '8aa848' if s < 3 else 'a06a8a'
        m.cubo([x - 0.7, CH, z - 0.7], [x + 0.7, CH + hh, z + 0.7], cor)
        for j in range(1, int(hh // 3.5) + 1):
            m.cubo([x - 0.8, CH + j * 3.5 - 0.3, z - 0.8], [x + 0.8, CH + j * 3.5, z + 0.8], 'c8c88a')
        for i in range(2 + s):
            d = DIRS[(i + k) % 4]
            m.folha(x, CH + hh * (0.55 + 0.4 * i / (2 + s)), z, [3, 6, 8, 9][s], 1.0, d, ['7cbf4a', '6aae3e', '5a9a35'])
    fim(m)


# ======================================================= rasteiras (abóbora e melancia): ramas no chão e o fruto grande
def rasteira(m, s, folha, flor):
    L = [2.4, 4.4, 6.0, 6.4][s]
    for i, d in enumerate(DIRS if s else 'EN'):
        p = m.seg(8, CH + 0.2, 8, L, 0.5, d, 0, '5a8a35', 0.5)
        m.folha(p[0], p[1], p[2], 2.6, 2.6, 'N' if d in 'EW' else 'E', folha, (22.5, 0))
        m.folha(8, CH + 0.3, 8, L * 0.6, 2.4, d, folha, (45, 0))
    if s in (1, 2):
        m.cubo([10.6, CH + 0.4, 9.6], [11.6, CH + 1.4, 10.6], flor)


def abobora(s):
    m = Mod(f'planta_abobora_{s}')
    rasteira(m, s, ['4c9a3c', '3f8a35'], 'f2c230')
    if s == 2: m.cubo([5.2, CH, 5.6], [8.0, CH + 2.4, 8.4], '6a9a3a')
    if s == 3:
        m.cubo([4.2, CH, 4.6], [10.4, CH + 5.4, 10.8], 'e8751a', topo='d86a14')
        for x in (5.6, 7.3, 9.0):
            m.cubo([x, CH + 0.2, 4.45], [x + 0.4, CH + 5.2, 4.6], 'b8560e')
            m.cubo([x, CH + 0.2, 10.8], [x + 0.4, CH + 5.2, 10.95], 'b8560e')
        m.cubo([7.0, CH + 5.4, 7.4], [7.8, CH + 6.6, 8.2], '5a7a2a')
    fim(m)


def melancia(s):
    m = Mod(f'planta_melancia_{s}')
    rasteira(m, s, ['4f9a3a', '43852f'], 'f2d24a')
    if s == 2: m.cubo([4.8, CH, 5.6], [8.4, CH + 2.6, 8.4], '5a9a3a')
    if s == 3:
        m.cubo([3.6, CH, 5.0], [11.6, CH + 5.0, 10.6], '3f8a35', topo='4f9a3a')
        for z in (5.0, 10.6):
            for x in (4.8, 7.0, 9.2, 11.0):
                m.cubo([x, CH + 0.2, z - 0.08], [x + 0.6, CH + 4.8, z + 0.08], '24622a')
        m.cubo([11.6, CH + 2.0, 7.2], [12.2, CH + 2.8, 8.0], '5a7a2a')
    fim(m)


# ======================================================= uva: parreira em latada com cachos
def uva(s):
    m = Mod(f'planta_uva_{s}')
    m.cubo([7.4, CH, 7.4], [8.6, CH + [4, 10, 14, 14][s], 8.6], '6b4a2b')
    if s >= 1:
        for x in (2.4, 12.6):
            m.cubo([x, CH, 7.4], [x + 1, CH + 16, 8.4], 'a87a4a', topo='c49a62')
        m.cubo([2.4, CH + 16, 7.5], [13.6, CH + 16.8, 8.3], 'a87a4a')
        for d in 'EW':
            p = m.seg(8, CH + [10, 14, 14][s - 1], 8, 4.6, 0.6, d, 22.5, '6b4a2b', 0.6)
            for k in range(1 + s):
                m.folha(p[0] + (-1.2 * k if d == 'E' else 1.2 * k), p[1], p[2], 2.4, 2.2, 'N' if k % 2 else 'S',
                        ['4c9a3c', '3f8a35'], (22.5, -22.5))
    else:
        for d in 'EW': m.folha(8, CH + 4, 8, 2.4, 1.6, d, ['4c9a3c', '3f8a35'], (22.5, 0))
    if s >= 2:
        c = ['6a2a8a', '7a3aa0', '5a1f78'] if s == 3 else ['9fc55a', 'b6cf62']
        rnd = random.Random(7)
        for cx in (4.6, 10.6):
            for k in range(6 if s == 3 else 4):
                x = cx + rnd.uniform(-0.8, 0.8); y = CH + 14.6 - k * 0.9; z = 7.6 + rnd.uniform(-0.6, 0.6)
                w = 1.0 - k * 0.08
                m.cubo([x - w, y - 1, z - w], [x + w, y, z + w], rnd.choice(c))
    fim(m)


for nome, f in {'tomate': tomate, 'soja': soja, 'arroz': arroz, 'algodao': algodao, 'cana': cana, 'abobora': abobora,
                'melancia': melancia, 'uva': uva}.items():
    for s in range(4): f(s)

# ======================================================= colheitas (itens de mão)
COLHEITAS = {
 'tomate': (['.......gg.......', '.....gGGGg......', '....rrgGgrr.....', '...rRRRrRRRr....', '..rRRwRRRRRRr...', '..rRwwRRRRRRr...',
             '..rRRRRRRRRRr...', '..rRRRRRRRRRr...', '..rRRRRRRRRRr...', '...rRRRRRRRr....', '....rrRRRrr.....', '......rrr.......'],
            {'g': ['3c7a2a'], 'G': ['4f9a3a'], 'r': ['b81a14', 'a8160f'], 'R': ['e0261b', 'ea3a28'], 'w': ['ffb0a0']},
            {'g': 1, 'G': 1.6, 'r': 3.4, 'R': 4, 'w': 4.2}),
 'soja': (['..........gg....', '.........gg.....', '.....yyyyg......', '....yYYYYy......', '...yYoYYoYy.....', '..yYoYYoYYy.....',
           '..yYYoYYoYy.....', '...yYYYYYy......', '....yyyyy.......'],
          {'g': ['6a8a3a'], 'y': ['b8a060', 'a89050'], 'Y': ['d9c56b', 'e0cc78'], 'o': ['8a7a3a']}, {'g': 1, 'y': 2.2, 'Y': 2.6, 'o': 2.6}),
 'arroz': (['......s.........', '......s.s.......', '.....sws.s......', '.....wwswsw.....', '....wwswwsww....', '....wswwswws....',
            '...wwswwswws....', '...wswwswws.....', '..wwswwsww......', '..wswwsws.......', '..sswwss........', '..ss............',
            '.ss.............'],
           {'s': ['a89040', '9a8238'], 'w': ['f2e6b0', 'e8dca0', 'fff4c8']}, {'s': 1, 'w': 2.2}),
 'algodao': (['.....wwww.......', '...wwWWWWww.....', '..wWWWWWWWWw....', '..wWWWwWWWWw....', '.wWWWWWWWWWWw...', '.wWWWWWWWwWWw...',
              '..wWWWWWWWWw....', '...wwWWWWWw.....', '....bBwwBb......', '...bBBbbBBb.....', '....bb..bb......'],
             {'w': ['e7e5e4', 'd6d3d1'], 'W': ['ffffff', 'f8f8f6'], 'b': ['5a3a22'], 'B': ['7a5a32']},
             {'w': 3.2, 'W': 3.8, 'b': 1.6, 'B': 1.8}),
 'cana': (['..........gg....', '.........gGg....', '........gGg.....', '.......cCc......', '......cCCc......', '......nnn.......',
           '.....cCCc.......', '....cCCc........', '....nnn.........', '...cCCc.........', '..cCCc..........', '..nnn...........',
           '.cCc............', '.cc.............'],
          {'g': ['4f9a3a'], 'G': ['6aae3e'], 'c': ['7a8a3a', '8a9a48'], 'C': ['a8c060', 'b8cc6a'], 'n': ['c8c88a']},
          {'g': 1, 'G': 1.2, 'c': 2.4, 'C': 2.8, 'n': 3}),
 'abobora': (['.......gg.......', '......gGg.......', '...ooooGoooo....', '..oOOoOOOoOOo...', '.oOOOoOOOoOOOo..', '.oOOOoOOOoOOOo..',
              '.oOOOoOOOoOOOo..', '.oOOOoOOOoOOOo..', '.oOOOoOOOoOOOo..', '..oOOoOOOoOOo...', '...ooooooooo....'],
             {'g': ['3c7a2a'], 'G': ['5a7a2a'], 'o': ['b8560e', 'a84c0a'], 'O': ['e8751a', 'f0862a']}, {'g': 1.4, 'G': 1.8, 'o': 4, 'O': 4.6}),
 'melancia': (['................', '....dddddddd....', '..ddLdLdLdLddd..', '.dLdLdLdLdLdLdd.', '.dddLdLdLdLdLdd.', 'dLdLdLdLdLdLdLdd',
               'dddLdLdLdLdLdLdd', '.dLdLdLdLdLdLdd.', '.dddLdLdLdLdLdd.', '..ddLdLdLdLddd..', '....dddddddd....'],
              {'d': ['24622a', '2a6e2e'], 'L': ['5aa043', '6ab04a']}, {'d': 4, 'L': 4.4}),
 'uva': (['.......gg.......', '......gGb.......', '.....ppppp......', '....pPpPpPp.....', '....PpPpPpP.....', '.....pPpPp......',
          '.....PpPpP......', '......pPp.......', '......PpP.......', '.......p........'],
         {'g': ['4f9a3a'], 'G': ['6aae3e'], 'b': ['6b4a2b'], 'p': ['5a1f78', '6a2a8a'], 'P': ['8a4ab0', '9a5ac0']},
         {'g': 1, 'G': 1.2, 'b': 1, 'p': 3, 'P': 3.4}),
}
for nome, (g, c, e) in COLHEITAS.items():
    extrudar('fazenda', nome, g, c, e, DISP_ITEM, seed=len(nome))

COR_SEMENTE = {'tomate': 'e0261b', 'soja': 'd9c56b', 'arroz': 'f2e6b0', 'algodao': 'ffffff', 'cana': 'a8c060',
               'abobora': 'e8751a', 'melancia': '3f8a35', 'uva': '7a3aa0'}
SACO = ['................', '....pppppppp....', '...pPPPPPPPPp...', '...pppppppppp...', '...p.p.pp.p.p...', '...pppppppppp...',
        '...pLLLLLLLLp...', '...pLccccccLp...', '...pLcCCCCcLp...', '...pLcCCCCcLp...', '...pLccccccLp...', '...pLLLLLLLLp...',
        '...pppppppppp...', '...pppppppppp...', '....pppppppp....']
for nome, c in COR_SEMENTE.items():
    extrudar('fazenda', f'semente_{nome}', SACO,
             {'p': ['b98a5a', 'a87a4a'], 'P': ['8a6a3a'], 'L': ['f2ead2'], 'c': [c], 'C': [c]},
             {'p': 1.6, 'P': 1.8, 'L': 1.8, 'c': 2.0, 'C': 2.3}, DISP_ITEM, seed=3)
print('expansão da fazenda ok')
