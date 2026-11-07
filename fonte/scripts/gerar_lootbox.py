# Lootboxes do Santuário: Caixa Comum (madeira), Caixa dos Ovos (cesta com tampa de ovo) e Caixa Ultra (netherite e diamante).
# Cada caixa tem base e tampa separadas (a tampa abre girando na dobradiça) e um modelo inteiro para o menu.
# Chaves: desenho em pixels extrudado em 3D.
import json, os, random, math, zlib
from PIL import Image
from voxel import cor, mix, R

src = open('gerar_fazenda_pesca.py', encoding='utf-8').read()
defs = src.split('# chão da planta')[0]                                   # rot, Mod, DISP_PLANTA
ext = src.split('# ======================================================= itens extrudados')[1].split('# ---------------- colheitas')[0]
g = {}
exec(defs + ext, g)
Mod, rot, extrudar, DISP_ITEM = g['Mod'], g['rot'], g['extrudar'], g['DISP_ITEM']
DISP_CAIXA = {'gui': {'rotation': [30, 225, 0], 'translation': [0, -1, 0], 'scale': [0.62, 0.62, 0.62]},
              'ground': {'translation': [0, 3, 0], 'scale': [0.3, 0.3, 0.3]},
              'fixed': {'rotation': [0, 180, 0], 'scale': [0.6, 0.6, 0.6]},
              'thirdperson_righthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
              'firstperson_righthand': {'rotation': [0, 225, 0], 'scale': [0.4, 0.4, 0.4]}}

def aro(m, x0, y0, z0, x1, y1, z1, c, w=0.8, brilho=False):
    """moldura (4 barras) em volta de um retângulo, sem cobrir o meio"""
    m.cubo([x0, y0, z0], [x1, y1, z0 + w], c, brilho=brilho)
    m.cubo([x0, y0, z1 - w], [x1, y1, z1], c, brilho=brilho)
    m.cubo([x0, y0, z0 + w], [x0 + w, y1, z1 - w], c, brilho=brilho)
    m.cubo([x1 - w, y0, z0 + w], [x1, y1, z1 - w], c, brilho=brilho)

def caixa(nome, desenho):
    for parte in ('base', 'tampa', 'inteira'):
        m = Mod('lootbox', f'{nome}_{parte}', 64)
        if parte in ('base', 'inteira'): desenho(m, 'base')
        if parte in ('tampa', 'inteira'): desenho(m, 'tampa')
        m.salvar(DISP_CAIXA)

# ---------------- Caixa Comum: baú de madeira com cintas de ferro
def comum(m, p):
    if p == 'base':
        m.cubo([1, 0, 2], [15, 9, 14], 'a0703a', topo='3a2614')
        for x in (3.4, 11.4): m.cubo([x, 0, 1.8], [x + 1.2, 9.1, 14.2], '6b6f76')
        m.cubo([0.8, 0, 1.8], [15.2, 0.8, 14.2], '5a5e64')
        for x in (0.7, 14.3):
            for z in (1.7, 13.3): m.cubo([x, 0, z], [x + 1, 9.1, z + 1], '8a8e94')
        m.cubo([7, 4.6, 1.6], [9, 7.6, 2], 'd4a83a')
        m.cubo([7.7, 5.3, 1.5], [8.3, 6.5, 1.6], '1a1410')
    else:
        m.cubo([1, 9, 2], [15, 13, 14], 'b07a40', topo='b88448')
        for x in (3.4, 11.4): m.cubo([x, 8.9, 1.8], [x + 1.2, 13.2, 14.2], '6b6f76')
        for x in (0.7, 14.3):
            for z in (1.7, 13.3): m.cubo([x, 9, z], [x + 1, 13.2, z + 1], '8a8e94')
        m.cubo([7.2, 7.8, 1.5], [8.8, 10.2, 2], 'c09030')

# ---------------- Caixa dos Ovos: cesta trançada com tampa de ovo pintado
def ovos(m, p):
    if p == 'base':
        m.cubo([1.5, 0, 2.5], [14.5, 8, 13.5], 'c8a060', topo='a3c24a')
        for y in (1.2, 3.7, 6.2): m.cubo([1.3, y, 2.3], [14.7, y + 0.9, 13.7], 'a07a3a')
        aro(m, 1.1, 7.4, 2.1, 14.9, 8.6, 13.9, 'b8904a', 1.0)
        for x in (4, 8, 12): m.cubo([x - 0.4, 0, 2.2], [x + 0.4, 7.4, 2.4], '8a6430')
        m.cubo([6.8, 3.4, 2.0], [9.2, 5.6, 2.3], 'f2a0c0')                 # laço
        m.cubo([5.6, 3.9, 2.05], [6.8, 5.1, 2.3], 'e888b0'); m.cubo([9.2, 3.9, 2.05], [10.4, 5.1, 2.3], 'e888b0')
    else:
        camadas = [([1.6, 8.5, 2.6], [14.4, 10.5, 13.4]), ([2.6, 10.5, 3.6], [13.4, 12.5, 12.4]),
                   ([4, 12.5, 5], [12, 14, 11]), ([5.6, 14, 6.6], [10.4, 15, 9.4])]
        for de, ate in camadas: m.cubo(de, ate, 'f4ecd8', topo='fbf6ea')
        for (de, ate, c) in [([3, 9.2, 2.4], [5, 10.4, 2.6], '7ac8e8'), ([9, 9.4, 2.4], [10.6, 10.4, 2.6], '9fd36a'),
                             ([6, 11, 3.4], [7.6, 12, 3.6], 'f2a0c0'), ([11, 11, 3.4], [12.4, 12.2, 3.6], '7ac8e8'),
                             ([14.4, 9, 6], [14.6, 10.2, 8], 'f2a0c0'), ([1.4, 9.2, 8], [1.6, 10.2, 10], '9fd36a'),
                             ([7, 15, 7.4], [9, 15.2, 8.6], '7ac8e8'), ([12, 12.6, 7], [12.2, 13.6, 9], '9fd36a'),
                             ([4.4, 12.6, 7.4], [4.6, 13.6, 9], 'f2a0c0'), ([6, 9.6, 13.4], [8, 10.6, 13.6], '7ac8e8')]:
            m.cubo(de, ate, c)

# ---------------- Caixa Ultra: netherite, ouro, diamantes e cristais
def ultra(m, p):
    if p == 'base':
        m.cubo([1, 0, 2], [15, 9, 14], '3a3438', topo='c084fc')
        aro(m, 0.8, 8.2, 1.8, 15.2, 9.1, 14.2, 'e8c040')
        m.cubo([0.8, 0, 1.8], [15.2, 0.9, 14.2], 'b8902a')
        for x in (0.4, 13.8):
            for z in (1.4, 12.8):
                m.cubo([x, 0, z], [x + 1.8, 10.5, z + 1.8], 'a855f7', brilho=True)
                m.cubo([x + 0.4, 10.5, z + 0.4], [x + 1.4, 11.8, z + 1.4], 'e9d5ff', brilho=True)
        m.cubo([6.6, 3.6, 1.5], [9.4, 7.4, 2], 'e8c040')
        m.cubo([7.4, 4.4, 1.3], [8.6, 6.6, 1.5], '5ee0e0', brilho=True)
        for x in (3.5, 12.5): m.cubo([x - 0.6, 4.2, 1.7], [x + 0.6, 5.4, 2], '5ee0e0', brilho=True)
    else:
        m.cubo([1, 9, 2], [15, 13, 14], '2e2a2e', topo='3a3438')
        aro(m, 0.8, 12.2, 1.8, 15.2, 13.1, 14.2, 'e8c040')
        aro(m, 0.8, 9, 1.8, 15.2, 9.6, 14.2, 'b8902a')
        m.cubo([6.2, 13, 6.2], [9.8, 14.2, 9.8], 'e8c040')
        m.cubo([6.8, 14.2, 6.8], [9.2, 16.4, 9.2], '5ee0e0', brilho=True)
        m.cubo([7.4, 16.4, 7.4], [8.6, 17.4, 8.6], 'cffafe', brilho=True)
        m.cubo([7, 8.2, 1.4], [9, 10.2, 2], 'e8c040')

caixa('caixa_comum', comum)
caixa('caixa_ovos', ovos)
caixa('caixa_ultra', ultra)

# ---------------- chaves
CHAVE = ['................', '................', '..BBBB..........', '.BBBBBB.........', 'BBHHHHBB........', 'BBHHHHBBSSSSSSSS',
         'BBHHHHBBSSSSSSSS', 'BBHHHHBB....T.TT', '.BBBBBB.....T.TT', '..BBBB.......T..', '................']
CHAVE = ['................'] * 3 + CHAVE + ['................'] * 2
extrudar('lootbox', 'chave_comum', CHAVE, {'B': ['b08a4a', '9a7838'], 'H': ['5a3a1e'], 'S': ['c0c4c8', 'b0b4b8'], 'T': ['a0a4a8']},
         {'B': 2.2, 'H': 1.2, 'S': 1.4, 'T': 1.2}, DISP_ITEM, seed=1)
extrudar('lootbox', 'chave_ovos', CHAVE, {'B': ['f4ecd8', 'fbf6ea', '7ac8e8', 'f2a0c0'], 'H': ['9fd36a'], 'S': ['e8c060', 'd8b050'], 'T': ['d8b050']},
         {'B': 2.4, 'H': 2.8, 'S': 1.4, 'T': 1.2}, DISP_ITEM, seed=2)
extrudar('lootbox', 'chave_ultra', CHAVE, {'B': ['3a3438', '2e2a2e', 'e8c040'], 'H': ['5ee0e0', '8af0f0'], 'S': ['4a4448'], 'T': ['e8c040']},
         {'B': 2.4, 'H': 3.0, 'S': 1.5, 'T': 1.3}, DISP_ITEM, seed=3, brilho='H')
print('lootbox pronto')
