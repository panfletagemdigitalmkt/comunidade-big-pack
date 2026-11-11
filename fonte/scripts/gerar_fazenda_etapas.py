# Fazenda BIG — Etapas 2 a 6: tudo que o pack precisa além das telas.
#   maquina_<tipo>        modelos 3D (cubos) de 20 máquinas/equipamentos, com display de bloco
#   produto_<id>          24 ícones de produtos (extrudados)
#   insumo_<id>           12 ícones de insumos
#   planta_<id>_<0..3>, <id>, semente_<id>   5 culturas especiais (mesmo montador das plantas v2)
#   <mutação>, semente_<mutação>             7 mutações (colheita recolorida da base + saco de semente)
# Não usa o MCP do Blockbench: os modelos são montados por código, como as plantas.
# Rodar da pasta fonte/:  python3 scripts/gerar_fazenda_etapas.py   (depois rodar o gerar_fazenda_gui.py)
import json, os, random, sys, colorsys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)


def trecho(arquivo, ate, de=None):
    src = open(os.path.join(AQUI, arquivo), encoding='utf-8').read()
    if de: src = src[src.index(de):]
    return src[:src.index(ate)]


ns = {}
exec(trecho('gerar_plantas_v2.py', "def milho(s):"), ns)
pesca = {}
exec("import json, os, random, math\nfrom PIL import Image\nfrom voxel import cor, mix, R", pesca)
exec(trecho('gerar_fazenda_pesca.py', "DISP_VARA = dict(DISP_ITEM)", de="DISP_ITEM = {"), pesca)
exec(trecho('gerar_fazenda_pesca.py', "# ---------------- colheitas", de="def extrudar("), pesca)
Mod, rot, CH, DIRS = ns['Mod'], ns['rot'], ns['CH'], ns['DIRS']
extrudar, DISP_ITEM, R = pesca['extrudar'], pesca['DISP_ITEM'], pesca['R']
from PIL import Image
for d in ('models/item/fazenda', 'textures/item/fazenda', 'items/fazenda'): os.makedirs(f'{R}/{d}', exist_ok=True)


def item_def(nome):
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/fazenda/{nome}'}}, open(f'{R}/items/fazenda/{nome}.json', 'w'), indent=1)


# ================================================================== máquinas (blocos de 16x16x16)
DISP_BLOCO = {'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.625, 0.625, 0.625]},
              'ground': {'translation': [0, 3, 0], 'scale': [0.25, 0.25, 0.25]},
              'fixed': {'scale': [0.5, 0.5, 0.5]},
              'thirdperson_righthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
              'thirdperson_lefthand': {'rotation': [75, 45, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
              'firstperson_righthand': {'rotation': [0, 45, 0], 'scale': [0.4, 0.4, 0.4]},
              'firstperson_lefthand': {'rotation': [0, 225, 0], 'scale': [0.4, 0.4, 0.4]},
              'head': {'translation': [0, -2, 0], 'scale': [0.9, 0.9, 0.9]}}


class Maq(Mod):
    """Mod com o chão em y=0 e display de bloco."""
    def c(s, de, ate, cor, topo=None, brilho=False):
        s.cubo([de[0], de[1] - 0.0001 + 0.0001, de[2]], ate, cor, topo=topo, brilho=brilho)

    def salvar(s):
        tex = f'big:item/fazenda/{s.nome}'
        json.dump({'texture_size': [s.tam, s.tam], 'textures': {'0': tex, 'particle': tex}, 'elements': s.el, 'display': DISP_BLOCO},
                  open(f'{R}/models/item/fazenda/{s.nome}.json', 'w'))
        s.img.save(f'{R}/textures/item/fazenda/{s.nome}.png')
        item_def(s.nome)


MAD, MAD2, MAD3, PEDRA, PEDRA2, FERRO, FERRO2, COBRE = 'a87a4a', '8a5a32', 'c49a62', '8a8a86', '6e6e6a', 'a8acb0', '6a7078', 'c87533'


def base_madeira(m, h=2):
    m.c([1, 0, 1], [15, h, 15], MAD2, topo=MAD)


def composteira():
    m = Maq('maquina_composteira')
    for z in (1, 14): m.c([1, 0, z], [15, 11, z + 1], MAD, topo=MAD3)
    for x in (1, 14): m.c([x, 0, 2], [x + 1, 11, 14], MAD2, topo=MAD3)
    for y in (3, 7): m.c([0.6, y, 0.6], [15.4, y + 1, 1.2], MAD3)
    m.c([2, 0, 2], [14, 9.5, 14], '4a3220', topo='3a2818')
    m.c([5, 9.5, 6], [8, 10.5, 9], '6a8a35', topo='7aa845')
    m.c([9, 9.5, 8], [11, 10.2, 11], 'b8560e')
    m.salvar()


def moinho():
    m = Maq('maquina_moinho')
    m.c([1, 0, 1], [15, 4, 15], PEDRA2, topo=PEDRA)
    m.c([2, 4, 2], [14, 7, 14], PEDRA, topo='9a9a96')
    m.c([2.5, 7, 2.5], [13.5, 9, 13.5], '7a7a76', topo='8a8a86')
    m.c([7.4, 9, 7.4], [8.6, 14, 8.6], MAD2)
    m.c([4, 12, 4], [12, 15, 12], MAD, topo='e7d6ae')
    m.c([5, 15, 5], [11, 16, 11], MAD3, topo='f2e6b0')
    m.c([14, 3, 7], [16, 4, 9], MAD3)
    m.salvar()


def prensa():
    m = Maq('maquina_prensa')
    base_madeira(m)
    for x in (2, 13): m.c([x, 2, 6], [x + 1, 15, 10], MAD, topo=MAD3)
    m.c([2, 14, 6], [14, 16, 10], MAD2, topo=MAD)
    m.c([7.3, 8, 7.3], [8.7, 14, 8.7], FERRO, topo='d0d4d8')
    m.c([4, 7, 5], [12, 8, 11], FERRO2)
    m.c([4, 2, 4], [12, 4, 12], 'b98a4a', topo='e0c060')
    m.c([5, 15.6, 7.5], [11, 16.4, 8.5], FERRO)
    m.salvar()


def tacho():
    m = Maq('maquina_tacho')
    m.c([1, 0, 1], [15, 6, 15], 'a04a2a', topo='8a3a20')
    m.c([5, 1, 0.8], [11, 4, 1.2], 'ff8a2a', brilho=True)
    m.c([2, 6, 2], [14, 11, 14], COBRE, topo='a85a20')
    m.c([3, 10.5, 3], [13, 11, 13], 'c81e3a', topo='e0263b')
    m.c([1.5, 10, 7.4], [2.2, 12, 8.6], FERRO2)
    m.c([7.5, 10.5, 7.5], [8.5, 15, 8.5], MAD)
    m.salvar()


def espremedor():
    m = Maq('maquina_espremedor')
    m.c([2, 0, 2], [14, 9, 14], 'd6d3d1', topo='e7e5e4')
    m.c([3, 9, 3], [13, 11, 13], FERRO, topo='c0c4c8')
    m.c([5, 11, 5], [11, 14, 11], 'f0b030', topo='ffd060')
    m.c([6, 14, 6], [10, 16, 10], '4f9a3a')
    m.c([11, 2, 6], [15, 6, 10], 'cfe8f0', topo='e0f4ff')
    m.c([12, 2.4, 7], [14, 5, 9], 'f2c230')
    m.salvar()


def moenda():
    m = Maq('maquina_moenda')
    base_madeira(m)
    for z in (3, 12): m.c([2, 2, z], [14, 12, z + 1], MAD, topo=MAD3)
    for y, cor in ((4.5, '6a8a35'), (8, '6a8a35')):
        m.c([3, y, 4], [13, y + 3, 12], FERRO2, topo=FERRO)
    m.c([13, 9, 7.5], [16, 10, 8.5], MAD3)
    m.c([15, 9, 7.5], [16, 14, 8.5], MAD3)
    m.c([0, 2, 6], [3, 3, 10], 'a8c060')
    m.salvar()


def torrefador():
    m = Maq('maquina_torrefador')
    for (x, z) in ((2, 2), (13, 2), (2, 13), (13, 13)): m.c([x, 0, z], [x + 1, 5, z + 1], FERRO2)
    m.c([1, 5, 3], [15, 13, 13], '3a3a3a', topo='4a4a4a')
    m.c([1.4, 6, 2.6], [14.6, 12, 3], '5a3a22')
    m.c([5, 13, 5], [11, 15, 11], FERRO, topo='6b3a1f')
    m.c([3, 1, 6], [13, 3, 10], 'ff7a1a', brilho=True)
    m.c([14, 8, 7], [16, 9, 9], COBRE)
    m.salvar()


def descarocador():
    m = Maq('maquina_descarocador')
    m.c([1, 0, 1], [15, 10, 15], MAD, topo=MAD3)
    m.c([0.8, 3, 3], [1.2, 9, 13], MAD2)
    for x in (4, 8, 12): m.c([x - 1, 10, 2], [x + 1, 12, 14], FERRO2, topo=FERRO)
    m.c([3, 12, 4], [9, 15, 10], 'f6f4ee', topo='ffffff')
    m.c([9, 12, 7], [13, 14, 12], 'ece8e0', topo='f8f6f2')
    m.salvar()


def desidratador():
    m = Maq('maquina_desidratador')
    m.c([2, 0, 2], [14, 15, 14], 'e8e0d0', topo='f0ead8')
    for y in (3, 6, 9, 12): m.c([2.6, y, 1.6], [13.4, y + 1.2, 2.2], '7a3aa0' if y % 2 else 'b05a2a')
    m.c([5, 15, 5], [11, 16, 11], FERRO2)
    m.c([3, 13.6, 1.6], [6, 14.6, 2.0], 'ff8a2a', brilho=True)
    m.salvar()


def secador():
    m = Maq('maquina_secador')
    for (x, z) in ((1, 1), (14, 1), (1, 14), (14, 14)): m.c([x, 0, z], [x + 1, 12, z + 1], MAD2)
    for y in (3, 7, 11):
        m.c([1, y, 1], [15, y + 1, 15], MAD, topo=MAD3)
        random.seed(y)
        for k in range(6):
            x, z = random.uniform(2, 13), random.uniform(2, 13)
            m.c([x, y + 1, z], [x + 1.6, y + 1.8, z + 1.2], 'a0522d')
    m.salvar()


def refinador():
    m = Maq('maquina_refinador')
    m.c([1, 0, 1], [15, 2, 15], FERRO2, topo=FERRO)
    m.c([3, 2, 3], [13, 14, 13], 'c0c4c8', topo='d8dce0')
    m.c([5, 14, 5], [11, 16, 11], FERRO)
    m.c([13, 8, 7], [16, 9.5, 8.5], COBRE)
    m.c([0, 4, 7], [3, 5.5, 8.5], COBRE)
    m.c([6, 9, 2.6], [10, 12, 3], 'f8f8f0')
    m.c([7.6, 10, 2.4], [8.4, 11.4, 2.6], 'e0263b')
    m.salvar()


def tear():
    m = Maq('maquina_tear')
    base_madeira(m)
    for x in (1, 14): m.c([x, 2, 2], [x + 1, 15, 3], MAD, topo=MAD3); m.c([x, 2, 13], [x + 1, 15, 14], MAD, topo=MAD3)
    m.c([1, 14, 2], [15, 15, 14], MAD2)
    m.c([2, 6, 4], [14, 7, 12], MAD3)
    for i in range(10): m.c([2.5 + i * 1.1, 7, 4], [2.9 + i * 1.1, 14, 4.4], 'f6f4ee')
    m.c([2, 6.5, 6], [14, 7.2, 12], '0e7490', topo='22a0b8')
    m.salvar()


def deposito(nome, cor1, cor2, metal):
    m = Maq(nome)
    m.c([1, 0, 1], [15, 13, 15], cor1, topo=cor2)
    for y in (0.5, 6, 11.5): m.c([0.7, y, 0.7], [15.3, y + 1, 15.3], metal)
    m.c([6, 7, 0.5], [10, 10, 0.9], 'f2c230')
    m.c([1, 13, 1], [15, 14, 15], cor2, topo=cor1)
    m.salvar()


def caixa_dagua():
    m = Maq('maquina_caixa_dagua')
    for (x, z) in ((2, 2), (13, 2), (2, 13), (13, 13)): m.c([x, 0, z], [x + 1, 6, z + 1], FERRO2)
    m.c([1, 6, 1], [15, 15, 15], '2a7ab8', topo='38a0d8')
    m.c([1.4, 15, 1.4], [14.6, 16, 14.6], '1e5a8a', topo='5ab8e8')
    m.c([5, 9, 0.6], [11, 12, 1.0], 'e0f4ff')
    m.salvar()


def bomba():
    m = Maq('maquina_bomba')
    m.c([2, 0, 2], [14, 3, 14], FERRO2, topo=FERRO)
    m.c([4, 3, 4], [12, 10, 12], '3a6ab0', topo='4a7ac0')
    m.c([7, 10, 7], [9, 14, 9], FERRO)
    m.c([9, 13, 7.5], [15, 14, 8.5], FERRO2)
    m.c([0, 1, 7], [4, 3, 9], '6a7078')
    m.c([12, 5, 7], [16, 7, 9], '6a7078')
    m.salvar()


def aspersor():
    m = Maq('maquina_aspersor')
    m.c([5, 0, 5], [11, 2, 11], FERRO2, topo=FERRO)
    m.c([7.3, 2, 7.3], [8.7, 11, 8.7], '6a7078')
    m.c([6, 11, 6], [10, 12.5, 10], FERRO, topo='c0c4c8')
    m.c([2, 12, 7.5], [14, 13, 8.5], '0ea5e9')
    m.c([7.5, 12, 2], [8.5, 13, 14], '0ea5e9')
    m.c([1.4, 12.6, 7.2], [2.4, 13.6, 8.8], '7dd3fc', brilho=True)
    m.c([13.6, 12.6, 7.2], [14.6, 13.6, 8.8], '7dd3fc', brilho=True)
    m.salvar()


def filtro():
    m = Maq('maquina_filtro')
    m.c([3, 0, 3], [13, 2, 13], FERRO2)
    for i, c in enumerate(('d8c08a', '3a3a3a', 'e8dcb0', '6a7a8a')): m.c([3.5, 2 + i * 3, 3.5], [12.5, 5 + i * 3, 12.5], c, topo=c)
    m.c([3, 14, 3], [13, 15, 13], '0891b2', topo='22b8d8')
    m.c([12.5, 6, 7], [16, 7.5, 8.5], FERRO)
    m.salvar()


def estufa(nome, borda):
    m = Maq(nome)
    m.c([1, 0, 1], [15, 3, 15], '3a3a3a', topo=borda)
    m.c([3, 3, 3], [13, 11, 13], 'cfe8f0', topo='e0f4ff')
    m.c([4, 3, 4], [12, 7, 12], '3f8a35', topo='5aa043')
    m.c([7, 7, 7], [9, 9.5, 9], 'e0263b')
    m.c([2.6, 11, 2.6], [13.4, 12, 13.4], borda)
    m.c([5, 1, 0.8], [11, 2.4, 1.2], '84cc16', brilho=True)
    m.salvar()


for f in (composteira, moinho, prensa, tacho, espremedor, moenda, torrefador, descarocador, desidratador, secador, refinador, tear,
          caixa_dagua, bomba, aspersor, filtro):
    f()
deposito('maquina_deposito', MAD, MAD3, '5a5a5a')
deposito('maquina_armazem', '8a6a2a', 'b8902a', 'a8acb0')
estufa('maquina_estufa', '4d7c0f')
estufa('maquina_estufa_avancada', 'd4a017')

# ================================================================== ícones de produtos e insumos (16x16)
SACO = ['................', '.....tttttt.....', '....tTTTTTTt....', '.....tttttt.....', '....pppppppp....', '...pPPPPPPPPp...',
        '..pPPPPPPPPPPp..', '..pPPLLLLLLPPp..', '..pPPLccccLPPp..', '..pPPLcCCcLPPp..', '..pPPLccccLPPp..', '..pPPLLLLLLPPp..',
        '..pPPPPPPPPPPp..', '..pPPPPPPPPPPp..', '...pppppppppp...']
POTE = ['................', '....dddddddd....', '....dDDDDDDd....', '.....dddddd.....', '....gggggggg....', '...gGffffffGg...',
        '...gfFFFFFFfg...', '...gfFLLLLFfg...', '...gfFLccLFfg...', '...gfFLLLLFfg...', '...gfFFFFFFfg...', '...gfFFFFFFfg...',
        '...gGffffffGg...', '....gggggggg....']
GARRAFA = ['.......dd.......', '.......dd.......', '......gDDg......', '......gffg......', '.....gfffFg.....', '....gfFFFFfg....',
           '....gfFLLFfg....', '....gfLccLfg....', '....gfFLLFfg....', '....gfFFFFfg....', '....gfFFFFfg....', '....gfFFFFfg....',
           '....ggggggggg...']
COPO = ['................', '...........s....', '..........s.....', '...gggggggsgg...', '...gffffffffg...', '...gfFFFFFFfg...',
        '....gFFFFFFg....', '....gfFFFFfg....', '....gfFFFFfg....', '.....gFFFFg.....', '.....gfFFfg.....', '.....gggggg.....']
BARRA = ['................', '................', '..pppppppppppp..', '..pCCcCCcCCcCp..', '..pCCcCCcCCcCp..', '..pcccccccccCp..',
         '..pCCcCCcCCcCp..', '..pCCcCCcCCcCp..', '..pcccccccccCp..', '..LLLLLLLLLLLL..', '..LllllllllllL..', '..LLLLLLLLLLLL..']
GRAOS = ['................', '.......cC.......', '.....cCccCc.....', '....cCcCCcCc....', '...cCcCcCcCcC...', '..cCcCcCcCcCcC..',
         '..CcCcCcCcCcCc..', '...cCcCcCcCcC...', '....cCcCcCcC....']
NOVELO = ['................', '.....wwwwww.....', '...wWwWWwWWw....', '..wWWwWWWwWWw...', '..wWwWWwWWWwW...', '.wWWWwWWwWWWw...',
          '.wWwWWWwWWwWw...', '..wWWwWWwWWw....', '..wwWWwWWWw.....', '....wwwwww......']
PANO = ['................', '..ffffffffffff..', '..fFFFFFFFFFFf..', '..fFdFFdFFdFFf..', '..ffffffffffff..', '..fFFFFFFFFFFf..',
        '..fFdFFdFFdFFf..', '..ffffffffffff..', '..fFFFFFFFFFFf..', '..fFdFFdFFdFFf..', '..ffffffffffff..']
CUBOS = ['................', '.....wwwww......', '....wWWWWw......', '....wWWWWwwwww..', '....wwwwwwWWWw..', '..wwwww..wWWWw..',
         '..wWWWw..wwwww..', '..wWWWw.wwwww...', '..wwwww.wWWWw...', '........wwwww...']
SPRAY = ['....dd..........', '....dDdddd......', '....dd...d......', '....gg..........', '...gffg.........', '..gfFFfg........',
         '..gfLLfg........', '..gLccLg........', '..gfLLfg........', '..gfFFfg........', '..gfFFfg........', '..gggggg........']
ENGRENAGEM = ['......dd........', '...d.dDDd.d.....', '..dDdDDDDdDd....', '...dDDddDDd.....', '.ddDDd..dDDdd...', '.dDDd....dDDd...',
              '.ddDDd..dDDdd...', '...dDDddDDd.....', '..dDdDDDDdDd....', '...d.dDDd.d.....', '......dd........']

ESP = {'.': 0, 't': 1.6, 'T': 1.8, 'p': 2.6, 'P': 3, 'L': 3.2, 'c': 3.3, 'C': 3.5, 'd': 2.2, 'D': 2.6, 'g': 2.8, 'G': 3, 'f': 3.1,
       'F': 3.3, 'l': 3.0, 's': 0.8, 'w': 2.6, 'W': 3.0}


def icone(nome, grade, cores):
    usados = {ch for l in grade for ch in l if ch != '.'}
    cs = {k: v if isinstance(v, list) else [v] for k, v in cores.items()}
    for ch in usados:
        if ch not in cs: cs[ch] = ['808080']
    extrudar('fazenda', nome, grade, cs, {k: ESP.get(k, 2) for k in usados}, DISP_ITEM, seed=len(nome))


def saco(nome, corpo, rotulo, marca):
    icone(nome, SACO, {'t': 'b98a5a', 'T': 'd6b38a', 'p': corpo[0], 'P': corpo[1], 'L': 'f2ead2', 'c': rotulo, 'C': marca})


def pote(nome, fruta, tampa='c81e3a'):
    icone(nome, POTE, {'d': tampa, 'D': tampa, 'g': 'cfe8f0', 'G': 'e0f4ff', 'f': fruta[0], 'F': fruta[1], 'L': 'f2ead2', 'c': fruta[1]})


def garrafa(nome, liquido, tampa='5a3a22'):
    icone(nome, GARRAFA, {'d': tampa, 'D': tampa, 'g': 'cfe8f0', 'f': liquido[0], 'F': liquido[1], 'L': 'f2ead2', 'c': liquido[0]})


def copo(nome, liquido):
    icone(nome, COPO, {'g': 'dff2f8', 'f': liquido[0], 'F': liquido[1], 's': 'f43f5e'})


for nome, c, l, mk in (('farinha_milho', ('e8dcb0', 'f2e6c4'), 'f2c230', 'd99a0b'), ('farinha_mandioca', ('e8dcb0', 'f2e6c4'), 'e8d6ae', 'a8743a'),
                       ('farinha_arroz', ('e8dcb0', 'f2e6c4'), 'fefce8', 'a3a07a')):
    saco('produto_' + nome, c, l, mk)
garrafa('produto_oleo_soja', ('e0b020', 'f2c840'), 'e0c060')
pote('produto_geleia_morango', ('a8142a', 'd81e3a'))
garrafa('produto_molho_tomate', ('a8160f', 'd8261b'), 'c81e3a')
garrafa('produto_molho_picante', ('8a0f08', 'c81a10'), '3f8a35')
pote('produto_doce_abobora', ('c8600e', 'e8751a'), 'a8743a')
pote('produto_geleia_maracuja', ('c89a10', 'e8c020'), '6a2a8a')
copo('produto_suco_abacaxi', ('e8c020', 'f2d850'))
copo('produto_suco_uva', ('5a1f78', '7a3aa0'))
copo('produto_suco_melancia', ('e0263b', 'f45a6a'))
copo('produto_suco_maracuja', ('d8a810', 'f0c830'))
copo('produto_caldo_cana', ('a8c060', 'c8d880'))
icone('produto_acucar', CUBOS, {'w': ['e7e5e4'], 'W': ['ffffff']})
icone('produto_cafe_torrado', GRAOS, {'c': ['3b1d0e'], 'C': ['6b3a1f']})
icone('produto_cacau_seco', GRAOS, {'c': ['7c4a2a'], 'C': ['a8743a']})
icone('produto_cacau_torrado', GRAOS, {'c': ['4a2511'], 'C': ['7c3a1a']})
icone('produto_chocolate', BARRA, {'p': '3b1d0e', 'C': '6b3a1f', 'c': '4a2511', 'L': 'c81e3a', 'l': 'e0263b'})
icone('produto_chocolate_fino', BARRA, {'p': '3b1d0e', 'C': '6b3a1f', 'c': '4a2511', 'L': 'd4a017', 'l': 'f2c230'})
icone('produto_fibra_algodao', NOVELO, {'w': ['e7e5e4'], 'W': ['ffffff']})
icone('produto_tecido', PANO, {'f': ['0e7490'], 'F': ['22a0b8'], 'd': ['ecfeff']})
icone('produto_passas', GRAOS, {'c': ['3b0f5a'], 'C': ['5a1f78']})
icone('produto_pitaya_desidratada', GRAOS, {'c': ['be185d'], 'C': ['f0f0e8']})

saco('insumo_composto', ('6b4423', '8a5a32'), '4a3220', '7aa845')
saco('insumo_adubo_n', ('2a7a3a', '3a9a4a'), 'f2ead2', '16a34a')
saco('insumo_adubo_p', ('b8560e', 'd86a14'), 'f2ead2', 'ea580c')
saco('insumo_adubo_k', ('6a2a8a', '8a3ab0'), 'f2ead2', '9333ea')
garrafa('insumo_biofertilizante', ('4d7c0f', '65a30d'), '3a2818')
garrafa('insumo_fertilizante_liquido', ('0369a1', '0ea5e9'), 'e0f4ff')
saco('insumo_fertilizante_especial', ('a16207', 'd4a017'), 'c084fc', 'fef08a')
icone('insumo_defensivo', SPRAY, {'d': '3a3a3a', 'D': '6a6a6a', 'g': 'e0f4ff', 'f': '65a30d', 'F': '84cc16', 'L': 'f2ead2', 'c': 'f2c230'})
icone('insumo_antifungico', SPRAY, {'d': '3a3a3a', 'D': '6a6a6a', 'g': 'e0f4ff', 'f': '0284c7', 'F': '38bdf8', 'L': 'f2ead2', 'c': 'ffffff'})
saco('insumo_recuperador_solo', ('92400e', 'b45309'), 'fde68a', '4a3220')
pote('insumo_controle_biologico', ('3f8a35', '5aa043'), '15803d')
icone('insumo_engrenagem', ENGRENAGEM, {'d': ['6a7078'], 'D': ['a8acb0']})

# ================================================================== culturas especiais (planta 3D em 4 estágios + colheita + semente)


def fim(m):
    m.salvar(); item_def(m.nome)


def tutor(m, h=16):
    m.cubo([7.4, CH, 7.4], [8.6, CH + h, 8.6], 'a87a4a', topo='c49a62')


def baunilha(s):
    m = Mod(f'planta_baunilha_{s}')
    tutor(m, [6, 14, 18, 18][s])
    h = [5, 12, 16, 16][s]
    for i in range(2 + s * 2):
        d = DIRS[i % 4]
        m.folha(8, CH + 1.5 + i * h / (3 + 2 * s), 8, 2.6, 1.6, d, ['3f8a35', '357a2e'], (22.5, 0))
    if s == 2:
        for (x, z, y) in ((6.2, 8, 10), (9.4, 7.2, 13)): m.cubo([x, CH + y, z], [x + 1.2, CH + y + 1.2, z + 1.2], 'f6f0c8')
    if s == 3:
        for (x, z, y) in ((6.0, 7.6, 9), (9.6, 8.0, 11), (6.6, 9.4, 13), (9.0, 6.6, 14)):
            m.cubo([x, CH + y - 3.6, z], [x + 0.6, CH + y, z + 0.6], '4a6a1a' if y < 12 else '6b4423')
    fim(m)


def cacau(s):
    m = Mod(f'planta_cacau_{s}')
    h = [5, 10, 14, 15][s]
    m.cubo([7.2, CH, 7.2], [8.8, CH + h, 8.8], '6b4423')
    L = [2.4, 3.6, 4.4, 4.6][s]
    for i, d in enumerate(DIRS if s else 'EW'):
        p = m.seg(8, CH + h * 0.75, 8, L * 0.5, 0.5, d, 22.5, '6b4423', 0.5)
        m.folha(p[0], p[1], p[2], L, 2.4, d, ['2f6a28', '24582a'], (0, -22.5))
    if s >= 2:
        for (x, z, y, d) in ((5.6, 7.6, 0.45, 'W'), (9.0, 7.4, 0.55, 'E'), (7.4, 5.6, 0.35, 'N'), (7.6, 9.0, 0.6, 'S')):
            c = ('d86a14' if s == 3 else '8ab050')
            m.cubo([x, CH + h * y - 2.6, z], [x + 1.4, CH + h * y, z + 1.4], c, topo='b8560e' if s == 3 else None)
    fim(m)


def maracuja(s):
    m = Mod(f'planta_maracuja_{s}')
    if s >= 1:
        for x in (2.4, 12.6): m.cubo([x, CH, 7.4], [x + 1, CH + 15, 8.4], 'a87a4a', topo='c49a62')
        m.cubo([2.4, CH + 15, 7.5], [13.6, CH + 15.8, 8.3], 'a87a4a')
    m.cubo([7.5, CH, 7.5], [8.5, CH + [4, 15, 15, 15][s], 8.5], '4a7a2a')
    for k in range(1 + 2 * s):
        x = 3.5 + k * (9.0 / max(1, 2 * s))
        m.folha(x, CH + (15 if s else 3), 8, 2.2, 2.2, 'N' if k % 2 else 'S', ['3f8a35', '357a2e'], (0, -45))
    if s == 2:
        for x in (5, 10): m.cubo([x, CH + 13.4, 7.6], [x + 1.4, CH + 14.4, 9.0], 'b48ad0', topo='f6f0ff')
    if s == 3:
        for x in (4.6, 7.6, 10.6): m.cubo([x, CH + 11.6, 7.4], [x + 1.8, CH + 13.8, 9.2], 'e0b820', topo='c8a018')
    fim(m)


def pitaya(s):
    m = Mod(f'planta_pitaya_{s}')
    h = [4, 8, 11, 11][s]
    m.cubo([6.8, CH, 6.8], [9.2, CH + h, 9.2], '4a8a3a', topo='5a9a45')
    if s >= 1:
        for (d, x0, z0) in (('E', 9.2, 7.4), ('W', 4.4, 7.4)):
            m.cubo([x0, CH + h * 0.5, z0], [x0 + 2.4, CH + h * 0.5 + 1.6, z0 + 1.2], '4a8a3a')
            xx = x0 + (1.2 if d == 'E' else 0)
            m.cubo([xx, CH + h * 0.5 + 1.6, z0], [xx + 1.2, CH + h * 0.5 + 5, z0 + 1.2], '4a8a3a', topo='5a9a45')
    if s == 2: m.cubo([7.2, CH + h, 7.2], [8.8, CH + h + 2.4, 8.8], 'f6f0e8', topo='fff8f0')
    if s == 3:
        for (x, y, z) in ((7.0, h, 7.0), (10.0, h * 0.5 + 5, 7.0), (4.0, h * 0.5 + 5, 7.0)):
            m.cubo([x, CH + y, z], [x + 2.2, CH + y + 2.6, z + 2.2], 'e8338a', topo='a8d05a')
    fim(m)


def biquinho(s):
    m = Mod(f'planta_biquinho_{s}')
    h = [3, 6, 8, 8.5][s]
    m.cubo([7.6, CH, 7.6], [8.4, CH + h, 8.4], '4a7a2a')
    for i, d in enumerate(DIRS if s else 'EW'):
        m.folha(8, CH + h * 0.6, 8, [1.8, 3.0, 3.6, 3.6][s], 1.6, d, ['4c9a3c', '3f8a35'], (22.5, 0))
        m.folha(8, CH + h * 0.95, 8, [1.2, 2.2, 2.8, 2.8][s], 1.4, DIRS[(i + 1) % 4], ['5aa043', '4c9a3c'], (45, 22.5))
    if s >= 2:
        random.seed(5)
        for k in range(8 if s == 3 else 4):
            x, z, y = random.uniform(5, 10.4), random.uniform(5, 10.4), random.uniform(h * 0.4, h * 0.95)
            c = random.choice(['e0261b', 'f2c230']) if s == 3 else '7cc04a'
            m.cubo([x, CH + y - 1.0, z], [x + 0.8, CH + y, z + 0.8], c)
    fim(m)


for f in (baunilha, cacau, maracuja, pitaya, biquinho):
    for s in range(4): f(s)

COLHEITAS = {
 'baunilha': (['..........gg....', '.........g......', '........bb......', '.......bBb......', '......bBb.......', '.....bBb........',
               '....bBb.........', '...bBb..........', '..bBb...........', '.bb.............'],
              {'g': ['4a7a2a'], 'b': ['3b1d0e', '4a2511'], 'B': ['6b3a1f', '7c4a2a']}, {'g': 1, 'b': 1.6, 'B': 1.8}),
 'cacau': (['......gg........', '.....gG.........', '....oooooo......', '...oOoOOoOo.....', '..oOOoOOoOOo....', '..oOOoOOoOOo....',
            '..oOOoOOoOOo....', '..oOOoOOoOOo....', '...oOoOOoOo.....', '....oooooo......'],
           {'g': ['5a7a2a'], 'G': ['6a8a35'], 'o': ['a84c0a', 'b8560e'], 'O': ['d86a14', 'e8751a']}, {'g': 1, 'G': 1.2, 'o': 3.6, 'O': 4}),
 'maracuja': (['.......gg.......', '......gG........', '....yyyyyy......', '...yYYYYYYy.....', '..yYYwYYYYYy....', '..yYwYYYYYYy....',
               '..yYYYYYYYYy....', '..yYYYYYYYYy....', '...yYYYYYYy.....', '....yyyyyy......'],
              {'g': ['4f9a3a'], 'G': ['6aae3e'], 'y': ['c89a10', 'b88a08'], 'Y': ['e8c020', 'f0cc30'], 'w': ['fff4c0']},
              {'g': 1, 'G': 1.2, 'y': 3.6, 'Y': 4, 'w': 4.2}),
 'pitaya': (['......g..g......', '.....gpppg......', '....pPPPPPp.....', '...gPPpPPPPg....', '...pPPPPPpPp....', '..gPpPPPPPPPg...',
             '...pPPPPpPPp....', '...gPPPPPPPg....', '....pPPpPPp.....', '.....gpppg......'],
            {'g': ['8ac04a'], 'p': ['c81e6a', 'b81a5a'], 'P': ['e8338a', 'f04a98']}, {'g': 2.8, 'p': 3.6, 'P': 4}),
 'biquinho': (['......g.........', '.....gG.........', '....rRr.........', '...rRRRr........', '...rRRRr........', '....rRRr........',
               '.....rRr........', '......rr........', '.......r........'],
              {'g': ['4f9a3a'], 'G': ['6aae3e'], 'r': ['b81a14'], 'R': ['e0261b', 'f03a28']}, {'g': 1, 'G': 1.2, 'r': 2.6, 'R': 3}),
}
for nome, (g, c, e) in COLHEITAS.items():
    extrudar('fazenda', nome, g, c, e, DISP_ITEM, seed=len(nome))

SACO_S = ['................', '....pppppppp....', '...pPPPPPPPPp...', '...pppppppppp...', '...p.p.pp.p.p...', '...pppppppppp...',
          '...pLLLLLLLLp...', '...pLccccccLp...', '...pLcCCCCcLp...', '...pLcCCCCcLp...', '...pLccccccLp...', '...pLLLLLLLLp...',
          '...pppppppppp...', '...pppppppppp...', '....pppppppp....']


def semente(nome, c, c2=None):
    extrudar('fazenda', f'semente_{nome}', SACO_S, {'p': ['b98a5a', 'a87a4a'], 'P': ['8a6a3a'], 'L': ['f2ead2'], 'c': [c], 'C': [c2 or c]},
             {'p': 1.6, 'P': 1.8, 'L': 1.8, 'c': 2.0, 'C': 2.3}, DISP_ITEM, seed=3)


for nome, c in (('baunilha', '6b3a1f'), ('cacau', 'd86a14'), ('maracuja', 'e8c020'), ('pitaya', 'e8338a'), ('biquinho', 'e0261b')):
    semente(nome, c)

# ================================================================== mutações: colheita recolorida da base
MUT = {'morango_gigante': ('morango', 'ff2e4d', 1.25), 'milho_azul': ('milho', '3b82f6', 1.0), 'abacaxi_dourado': ('abacaxi', 'facc15', 1.0),
       'cafe_ancestral': ('cafe', 'a16207', 1.0), 'tomate_carmesim': ('tomate', '7f1d3a', 1.0), 'uva_cristalina': ('uva', '67e8f9', 1.0),
       'pitaya_radiante': ('pitaya', 'f472b6', 1.0)}


def recolorir(img, alvo, preservar_verde=True):
    """troca o matiz dos pixels coloridos para o da cor alvo (folhas verdes ficam)"""
    tr, tg, tb = (int(alvo[i:i + 2], 16) / 255 for i in (0, 2, 4))
    th, ts, tv = colorsys.rgb_to_hsv(tr, tg, tb)
    out = img.copy()
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a == 0: continue
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if preservar_verde and 0.2 < h < 0.45 and s > 0.25: continue
            if s < 0.12: continue
            nr, ng, nb = colorsys.hsv_to_rgb(th, min(1, s * 0.6 + ts * 0.4), min(1, v * (0.75 + tv * 0.35)))
            px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), a)
    return out


for mid, (base, cor, escala) in MUT.items():
    modelo = json.load(open(f'{R}/models/item/fazenda/{base}.json'))
    img = Image.open(f'{R}/textures/item/fazenda/{base}.png').convert('RGBA')
    recolorir(img, cor).save(f'{R}/textures/item/fazenda/{mid}.png')
    tex = f'big:item/fazenda/{mid}'
    modelo['textures'] = {'0': tex, 'particle': tex}
    if escala != 1.0:
        d = json.loads(json.dumps(modelo.get('display', {})))
        for k in d:
            if 'scale' in d[k]: d[k]['scale'] = [v * escala for v in d[k]['scale']]
        modelo['display'] = d
    json.dump(modelo, open(f'{R}/models/item/fazenda/{mid}.json', 'w'))
    item_def(mid)
    semente(mid, cor, 'fef08a')

print('etapas da fazenda ok')
