# Caixas de skins: 12 espadas de anime (estilo, todas originais) e 11 varas de pesca, + caixas e chaves.
import json, os, math, random
from PIL import Image
from voxel import cor, mix, lerp, R, gerar

# ---------- reaproveita os montadores dos outros geradores
src = open('gerar_fazenda_pesca.py', encoding='utf-8').read()
defs = src.split('# chão da planta')[0]
ext = src.split('# ======================================================= itens extrudados')[1].split('# ---------------- colheitas')[0]
varas = src.split('# ======================================================= varas de pesca (3D, cubo a cubo)')[1].split("montar('vara_bambu'")[0]
g = {}
exec(defs + ext + varas, g)
Mod0, extrudar, DISP_ITEM, rot = g['Mod'], g['extrudar'], g['DISP_ITEM'], g['rot']
g['Mod'] = lambda pasta, nome, tam=64: Mod0('skins', nome, tam)       # varas vão para a pasta skins
Vara, montar = g['Vara'], g['montar']
lb = open('gerar_lootbox.py', encoding='utf-8').read().split("caixa('caixa_comum'")[0]
h = {}
exec(lb, h)
caixa, aro = h['caixa'], h['aro']

# ======================================================= ESPADAS DE ANIME
P = 'skins'
def M(pal, esp=2.0, brilho=False): return ([cor(c) for c in pal], esp, brilho)
BASE = {
    'b': M(['b9c0c8', 'c8ced5', 'a9b1ba'], 1.8), 'e': M(['eef2f5', 'ffffff', 'dfe5ea'], 1.0), 'n': M(['26232b', '1c1a20', '312d38'], 2.2),
    's': M(['c9ced4', 'dde1e5', 'b4bac1'], 2.2), 'g': M(['d9a62e', 'f0c75a', 'c4952a'], 2.6), 'l': M(['3a2a20', '4a3628', '2e221a'], 2.4),
    'L': M(['6b4a2b', '7a5634'], 2.4), 'w': M(['efeae0', 'fbf8f1'], 2.4), 'k': M(['1e2a4a', '26345c'], 2.4),
}
def mat(**over):
    d = dict(BASE)
    for k, v in over.items(): d[k] = v
    return d

def brilho(ch, x, y, f, n, c0):
    if ch.isupper() and ch in ANIM:
        onda = 0.5 + 0.5 * math.sin(2 * math.pi * f / n - y * 0.45)
        return lerp(c0, cor('ffffff'), onda * 0.5)
    return None
ANIM = set()

CX = 15
def centro(s): return '.' * (CX - len(s) // 2) + s
def lamina(L, larg, curva=lambda r: 0, fio='e', corpo='b', costas=None, dois=False, pad=None):
    rows = []
    for r in range(L):
        w = larg(r); c0 = CX - w // 2 + curva(r); s = ''
        for i in range(w):
            ch = corpo
            if dois and (i == 0 or i == w - 1): ch = fio
            elif not dois and i == w - 1: ch = fio
            elif costas and i == 0 and w > 2: ch = costas
            if pad: ch = pad(r, i, w, ch) or ch
            s += ch
        rows.append('.' * c0 + s)
    return rows
def cabo(n, a, b): return [centro(a + b + a if i % 2 == 0 else b + a + b) for i in range(n)]
KAT = lambda r: 2 if r < 3 else 1 if r < 6 else 0 if r < 11 else -1
def kat_larg(r): return 1 if r == 0 else 2 if r == 1 else 3
def montar_espada(nome, linhas, mt, anim_chars='', frames=1):
    ANIM.clear(); ANIM.update(anim_chars)
    gerar(P, nome, linhas, mt, frames=frames if anim_chars else 1, anim=brilho if anim_chars else None, seed=len(nome) * 7)

# 1 Lâmina do Vento Azul
montar_espada('vento_azul', lamina(18, kat_larg, KAT, fio='a', costas='s') + [centro('sss'), centro('kkkkkkk'), centro('kAkkkAk')] + cabo(8, 'k', 'w') + [centro('nnn')],
              mat(a=M(['9ad8ff', 'bde6ff', '7cc8f5'], 1.0), A=M(['5fb8ff', '9ad8ff'], 2.6, True)), 'A', 6)
# 2 Katana Sakura
montar_espada('sakura', lamina(18, kat_larg, KAT, pad=lambda r, i, w, ch: 'p' if (r % 4 == 1 and i == 1 and r > 2) else None)
              + [centro('sss'), centro('.ppp.'), centro('ppYpp'), centro('.ppp.')] + cabo(8, 'q', 'n') + [centro('ppp')],
              mat(p=M(['f9a8d4', 'fbcfe8', 'f472b6'], 2.4), Y=M(['fde047'], 2.8), q=M(['db2777', 'be185d'], 2.4)))
# 3 Odachi da Lua Pálida
montar_espada('lua_palida', lamina(20, lambda r: 1 if r == 0 else 2 if r < 3 else 3, lambda r: 1 if r < 5 else 0, fio='e', corpo='s')
              + [centro('m.....m'), centro('.mmmmm.'), centro('..mMm..')] + cabo(7, 'w', 'h') + [centro('.M.')],
              mat(m=M(['dfe6f0', 'f4f7fb'], 2.4), M=M(['bfe3ff', 'e0f3ff'], 2.6, True), h=M(['9aa4b4', '8a94a4'], 2.4)), 'M', 6)
# 4 Cutelo Colossal
def cutelo_pad(r, i, w, ch):
    if i == w // 2 and r in (5, 8, 11, 14): return 'O'
    if (i == 1 or i == w - 2) and r % 4 == 2: return 'g'
    return None
montar_espada('cutelo_colossal', lamina(17, lambda r: [3, 5, 7][min(r, 2)], lambda r: 1 if r == 0 else 0, fio='e', corpo='i', dois=True, pad=cutelo_pad)
              + [centro('nnnnnnnnn'), centro('nnnnnnnnn')] + cabo(8, 'l', 'L') + [centro('nnn')],
              mat(i=M(['5a5e66', '666a72', '4e5258'], 2.6), O=M(['ff8a2a', 'ffb066'], 2.8, True)), 'O', 6)
# 5 Lâmina do Trovão
ZZ = [0, 1, 2, 1, 0, -1, -2, -1]
montar_espada('trovao', lamina(18, kat_larg, lambda r: ZZ[(r // 2) % 8], fio='W', corpo='Y')
              + [centro('.y.y.'), centro('yyyyyyy'), centro('y.yyy.y')] + cabo(8, 'n', 'y') + [centro('YYY')],
              mat(Y=M(['fde047', 'facc15', 'fef08a'], 2.0, True), W=M(['ffffff', 'fefce8'], 1.2, True), y=M(['ca8a04', 'a16207'], 2.4)), 'YW', 8)
# 6 Katana Carmesim Sombria
montar_espada('carmesim', lamina(18, kat_larg, KAT, fio='R', corpo='n')
              + [centro('rrr'), centro('nnrrrnn'), centro('nrnnnrn')] + cabo(8, 'r', 'n') + [centro('RRR')],
              mat(R=M(['ff3b3b', 'ff7070'], 1.4, True), r=M(['8b1a1a', 'a51d1d', '701414'], 2.4)), 'R', 8)
# 7 Espada Gélida
def gelo_larg(r): return [1, 3, 3, 5, 5][min(r, 4)]
montar_espada('gelida', lamina(18, gelo_larg, fio='C', corpo='c', dois=True, pad=lambda r, i, w, ch: 'C' if (r % 5 == 3 and i == w // 2) else None)
              + [centro('.c.c.c.'), centro('ccccccc'), centro('..cCc..')] + cabo(8, 'w', 'k') + [centro('.C.')],
              mat(c=M(['a5f3fc', 'cffafe', '7dd3fc'], 2.0), C=M(['5ff2ff', 'b8fbff', 'e6feff'], 1.6, True)), 'C', 6)
# 8 Lâmina Fênix
def fenix_pad(r, i, w, ch):
    if r < 6: return 'Y' if i != w - 1 else 'W'
    if r < 12: return 'O' if i != w - 1 else 'Y'
    return 'F' if i != w - 1 else 'O'
montar_espada('fenix', lamina(18, lambda r: 1 if r == 0 else 2 if r < 2 else 3 + (1 if r % 4 in (1, 2) else 0), lambda r: (1 if r % 6 < 3 else 0), pad=fenix_pad)
              + [centro('o.....o'), centro('oo...oo'), centro('.ooooo.')] + cabo(8, 'r', 'g') + [centro('.F.')],
              mat(Y=M(['fde047', 'fef08a'], 2.0, True), O=M(['fb923c', 'f97316'], 2.0, True), F=M(['ef4444', 'f87171'], 2.0, True),
                  W=M(['fffbeb'], 1.2, True), o=M(['f97316', 'ea580c'], 2.4), r=M(['7f1d1d', '991b1b'], 2.4)), 'YOFW', 8)
# 9 Katana do Vazio
estrelas = {(4, 1), (8, 0), (11, 1), (15, 0), (6, 1)}
montar_espada('vazio', lamina(18, kat_larg, KAT, fio='P', corpo='v', pad=lambda r, i, w, ch: 'S' if (r, i) in estrelas else None)
              + [centro('.vvv.'), centro('vPvvvPv'), centro('.vvvvv.')] + cabo(8, 'v', 'n') + [centro('PPP')],
              mat(v=M(['2e1065', '3b0f7a', '1e0a45'], 2.0), P=M(['c084fc', 'e9d5ff', 'a855f7'], 1.4, True), S=M(['ffffff', 'fde68a'], 2.2, True)), 'PS', 8)
# 10 Espada Celestial
montar_espada('celestial', lamina(18, lambda r: 1 if r == 0 else 3 if r < 2 else 5, fio='e', corpo='W', dois=True,
              pad=lambda r, i, w, ch: 'g' if (i == w // 2 and r > 2) else None)
              + [centro('ww.ggg.ww'), centro('.wwwgwww.'), centro('...gGg...')] + cabo(8, 'w', 'g') + [centro('.G.')],
              mat(W=M(['f8fafc', 'ffffff', 'eef2f6'], 2.0), G=M(['fde68a', 'fff7c2'], 2.8, True)), 'G', 6)
# 11 Lâmina do Dragão Esmeralda
def dragao_larg(r): return 1 if r == 0 else 3 if r < 2 else 4 + (1 if r % 2 == 0 else 0)
montar_espada('dragao_esmeralda', lamina(18, dragao_larg, fio='V', corpo='d', pad=lambda r, i, w, ch: 'D' if ((r + i) % 3 == 0 and i < w - 1) else None)
              + [centro('..ggg..'), centro('gddgddg'), centro('.ggggg.')] + cabo(8, 'd', 'g') + [centro('.R.')],
              mat(d=M(['15803d', '166534', '1a7a3a'], 2.2), D=M(['0f5a2b', '14532d'], 2.4), V=M(['7dff6b', 'b5ff9e'], 1.6, True),
                  R=M(['ff3b3b', 'ff7070'], 2.8, True)), 'VR', 8)
# 12 Katana do Eclipse Solar
montar_espada('eclipse', lamina(18, kat_larg, KAT, fio='G', corpo='n', pad=lambda r, i, w, ch: 'G' if (r % 6 == 4 and i == 1) else None)
              + [centro('..GGG..'), centro('.GnnnG.'), centro('..GGG..')] + cabo(8, 'n', 'g') + [centro('GGG')],
              mat(G=M(['fbbf24', 'fde68a', 'f59e0b'], 1.6, True)), 'G', 8)
ESPADAS = ['vento_azul', 'sakura', 'lua_palida', 'cutelo_colossal', 'trovao', 'carmesim', 'gelida', 'fenix', 'vazio', 'celestial', 'dragao_esmeralda', 'eclipse']

# ======================================================= VARAS DE PESCA
def vara_skin(v, c):
    v.eixo(-3.4, -2.5, 1.15, c['ponteira'])
    v.eixo(-2.5, 3.2, 1.0, c['cabo'])
    for y in (-1.6, 0.2, 2.0): v.anel(y, 1.08, 0.3, c['aneis'])
    v.eixo(3.2, 4.4, 0.85, c['aneis'])
    v.eixo(4.4, 12.6, 0.55, c['eixo1'])
    v.eixo(12.6, 19.8, 0.4, c['eixo2'])
    for y in (7.4, 11.6, 15.2, 18.0):
        if c.get('amarra'): v.anel(y - 0.4, 0.62 if y < 12.6 else 0.48, 1.0, c['amarra'])
        v.passador(y, c['passador'], 1.0 if y < 10 else 0.8)
    m1, m2, m3 = c['mol']
    v.c([8.85, 0.6, 7.55], [9.8, 1.4, 8.45], m3)
    if c['molinete'] == 'carretel':
        v.c([9.8, -0.6, 6.4], [12.0, -0.1, 9.6], m1); v.c([9.8, 2.1, 6.4], [12.0, 2.6, 9.6], m1)
        v.c([10.2, -0.1, 6.9], [11.6, 2.1, 9.1], m2)
    elif c['molinete'] == 'concha':
        v.c([9.8, -0.8, 6.6], [12.2, 2.6, 9.4], m1, topo=m2)
        for y in (-0.4, 0.6, 1.6): v.c([9.7, y, 6.5], [12.3, y + 0.3, 9.5], m3)
    else:
        v.c([9.8, -0.4, 6.9], [12.3, 2.6, 9.1], m1); v.c([12.3, -0.1, 7.2], [12.9, 2.3, 8.8], m2)
    v.c([10.6, 0.6, 9.1], [11.2, 1.2, 10.9], m3); v.c([10.4, 0.4, 10.9], [11.4, 1.4, 11.8], c['manivela'], brilho=c.get('mbrilho', False))
    for f in c.get('extras', ()): f(v)
    if c.get('lanterna'):
        v.eixo(19.8, 20.4, 0.25, c['eixo2']); v.c([8.9, 20.0, 7.7], [9.6, 21.4, 8.3], c['eixo2'])
        v.c([9.2, 21.4, 7.4], [10.6, 22.8, 8.6], c['ponta'], brilho=True)
        return 22.8
    v.c([7.4, 19.8, 7.4], [8.6, 20.9, 8.6], c['ponta'], brilho=c.get('pbrilho', False))
    return 20.9

def tentaculos(v):
    for (y, s) in ((5.5, 1), (8.5, -1), (13.5, 1), (16.5, -1)):
        v.c([8.5 if s > 0 else 6.9, y, 7.6], [9.1 if s > 0 else 7.5, y + 1.4, 8.4], '7e22ce')
        v.c([9.1 if s > 0 else 6.5, y + 1.2, 7.7], [9.5 if s > 0 else 6.9, y + 2.2, 8.3], 'a855f7')
def barbatanas(v):
    v.c([7.4, 1.2, 5.8], [8.6, 4.0, 6.9], '5ae0d8'); v.c([7.4, 1.2, 9.1], [8.6, 4.0, 10.2], '5ae0d8')
def gemas(v):
    for y in (-1.0, 0.9): v.c([6.85, y, 7.6], [7.1, y + 0.8, 8.4], 'ef4444', brilho=True)
    v.c([8.9, 0.9, 7.6], [9.15, 1.7, 8.4], '22d3ee', brilho=True)
def lava(v):
    for y in (5.0, 6.8, 8.6, 10.4, 14.0, 16.4): v.c([7.42, y, 7.42], [8.58, y + 0.35, 8.58], 'ff7a1a', brilho=True)

VARAS = {
    'vara_classica': dict(ponteira='1a1a1a', cabo='c0262a', aneis='f0f0f0', eixo1='e33b3b', eixo2='f0f0f0', amarra='1a1a1a', passador='c8ccd0',
                          molinete='metal', mol=('d0d4d8', 'e33b3b', '8a8e92'), manivela='1a1a1a', ponta='e33b3b', linha=('f0f0f0', 'b0b4b8', ('e33b3b', 'f0f0f0'))),
    'vara_caipira': dict(ponteira='5a3a1e', cabo='b08a5a', aneis='7a5634', eixo1='9a7a4a', eixo2='b09060', amarra=None, passador='8a8e92',
                         molinete='carretel', mol=('7a5634', 'e8e2d0', '5a3a1e'), manivela='c8a060', ponta='6a4a2a', linha=('e8e2d0', '9a9a9a', ('f2a65a', 'f0f0f0'))),
    'vara_tropical': dict(ponteira='166534', cabo='22c55e', aneis='facc15', eixo1='16a34a', eixo2='facc15', amarra='1d4ed8', passador='facc15',
                          molinete='metal', mol=('1d4ed8', 'facc15', '166534'), manivela='ffffff', ponta='1d4ed8', linha=('fef08a', 'facc15', ('22c55e', 'facc15'))),
    'vara_coral': dict(ponteira='f472b6', cabo='fbcfe8', aneis='fb7185', eixo1='fda4af', eixo2='fecdd3', amarra='f43f5e', passador='fff1f2',
                       molinete='concha', mol=('ffe4e6', 'fff1f2', 'fb7185'), manivela='fb7185', ponta='fb7185', linha=('ffe4e6', 'fb7185', ('fb7185', 'ffffff'))),
    'vara_abismo': dict(ponteira='0b1020', cabo='111a33', aneis='22d3ee', eixo1='172554', eixo2='1e3a8a', amarra='22d3ee', passador='67e8f9',
                        molinete='metal', mol=('172554', '22d3ee', '0b1020'), manivela='22d3ee', mbrilho=True, ponta='a5f3fc', lanterna=True,
                        linha=('67e8f9', '22d3ee', ('a5f3fc', 'a5f3fc'))),
    'vara_pirata': dict(ponteira='e8c040', cabo='4a2c17', aneis='e8c040', eixo1='5a3a1e', eixo2='6b4a2b', amarra='1a1a1a', passador='e8c040',
                        molinete='carretel', mol=('4a2c17', 'f0e6d0', 'e8c040'), manivela='e8c040', ponta='e8c040', extras=(gemas,),
                        linha=('f0e6d0', 'e8c040', ('e33b3b', 'f0f0f0'))),
    'vara_gelo': dict(ponteira='bae6fd', cabo='e0f2fe', aneis='7dd3fc', eixo1='a5f3fc', eixo2='cffafe', amarra='38bdf8', passador='e0f2fe',
                      molinete='metal', mol=('cffafe', '7dd3fc', 'bae6fd'), manivela='5ff2ff', mbrilho=True, ponta='5ff2ff', pbrilho=True,
                      linha=('e0f2fe', '7dd3fc', ('5ff2ff', 'ffffff'))),
    'vara_vulcanica': dict(ponteira='1a1414', cabo='2b1d1d', aneis='ff7a1a', eixo1='1f1a1a', eixo2='2a2222', amarra='b91c1c', passador='3a3030',
                           molinete='metal', mol=('2a2222', 'ff7a1a', '1a1414'), manivela='ff7a1a', mbrilho=True, ponta='ff7a1a', pbrilho=True,
                           extras=(lava,), linha=('fca5a5', 'ff7a1a', ('ff7a1a', 'fde047'))),
    'vara_neon': dict(ponteira='18181b', cabo='27272a', aneis='f0abfc', eixo1='1e1b4b', eixo2='312e81', amarra='22d3ee', passador='f0abfc',
                      molinete='metal', mol=('18181b', 'f0abfc', '22d3ee'), manivela='22d3ee', mbrilho=True, ponta='f0abfc', pbrilho=True,
                      linha=('f0abfc', '22d3ee', ('22d3ee', 'f0abfc'))),
    'vara_kraken': dict(ponteira='3b0764', cabo='581c87', aneis='22d3ee', eixo1='4c1d95', eixo2='6d28d9', amarra=None, passador='a855f7',
                        molinete='concha', mol=('6d28d9', 'a855f7', '3b0764'), manivela='22d3ee', mbrilho=True, ponta='fde047', pbrilho=True,
                        extras=(tentaculos, barbatanas), linha=('c4b5fd', 'a855f7', ('fde047', 'fde047'))),
    'vara_rei': dict(ponteira='fbbf24', cabo='d97706', aneis='fde68a', eixo1='f59e0b', eixo2='fbbf24', amarra='b91c1c', passador='fde68a',
                     molinete='metal', mol=('fbbf24', 'fde68a', 'd97706'), manivela='ef4444', mbrilho=True, ponta='fff7c2', pbrilho=True,
                     extras=(gemas,), linha=('fde68a', 'fbbf24', ('ef4444', 'fde68a'))),
}
for nome, c in VARAS.items():
    montar(nome, lambda v, c=c: vara_skin(v, c), lambda v, t, c=c: v.linha(t, c['linha'][0], c['linha'][1], c['linha'][2]))
    json.dump({'model': {'type': 'minecraft:condition', 'property': 'minecraft:fishing_rod/cast',
                         'on_false': {'type': 'minecraft:model', 'model': f'big:item/skins/{nome}'},
                         'on_true': {'type': 'minecraft:model', 'model': f'big:item/skins/{nome}_lancada'}}},
              open(f'{R}/items/skins/{nome}.json', 'w'), indent=1)
    lan = f'{R}/items/skins/{nome}_lancada.json'
    if os.path.exists(lan):
        try: os.remove(lan)
        except OSError: pass

# ======================================================= CAIXAS E CHAVES
def anime(m, p):
    if p == 'base':
        m.cubo([1, 0, 2], [15, 9, 14], 'b91c1c', topo='1a0a0a')
        aro(m, 0.8, 8.2, 1.8, 15.2, 9.1, 14.2, '1a1a1a')
        m.cubo([0.8, 0, 1.8], [15.2, 0.9, 14.2], '1a1a1a')
        for x in (0.6, 14.4):
            for z in (1.6, 13.4): m.cubo([x, 0, z], [x + 1, 9.2, z + 1], 'd4a83a')
        m.cubo([5.6, 3.0, 1.75], [10.4, 7.8, 2], '1a1a1a')                    # placa preta com flor de cerejeira
        for (x, y) in ((7.4, 6.3), (5.9, 5.2), (8.9, 5.2), (6.4, 3.5), (8.4, 3.5)): m.cubo([x, y, 1.5], [x + 1.2, y + 1.2, 1.75], 'f9a8d4')
        m.cubo([7.6, 4.8, 1.4], [8.4, 5.6, 1.5], 'fde047')
        for (x, y) in ((2.5, 6.5), (12, 2.5), (4, 2)): m.cubo([x, y, 1.75], [x + 1, y + 1, 1.95], 'f9a8d4')
    else:
        m.cubo([0.4, 9, 1.4], [15.6, 11, 14.6], '1a1a1a')                     # telhado em dois níveis
        m.cubo([1.5, 11, 2.5], [14.5, 12.4, 13.5], 'b91c1c', topo='c62828')
        m.cubo([-0.2, 11, 7.4], [16.2, 12, 8.6], '1a1a1a')
        m.cubo([6.5, 12.4, 6.5], [9.5, 14.2, 9.5], 'd4a83a')
        m.cubo([7.3, 14.2, 7.3], [8.7, 15.6, 8.7], '5ff2ff', brilho=True)
        for (x, z) in ((3, 4), (11, 10), (5, 11)): m.cubo([x, 12.4, z], [x + 1, 12.6, z + 1], 'f9a8d4')
        m.cubo([7.2, 7.8, 1.0], [8.8, 10.2, 1.4], 'd4a83a')

def varas_caixa(m, p):
    if p == 'base':
        m.cubo([1, 0, 2], [15, 9, 14], '0f766e', topo='2a1a10')
        for y in (2.5, 6): m.cubo([0.8, y, 1.8], [15.2, y + 0.7, 14.2], 'c8a060')    # cordas
        m.cubo([0.8, 0, 1.8], [15.2, 0.8, 14.2], '5a3a1e')
        m.cubo([5, 3.6, 1.6], [11, 5.8, 2], 'f59e0b')                                 # peixe dourado
        m.cubo([11, 3.2, 1.6], [12.6, 6.2, 2], 'f59e0b'); m.cubo([5.8, 4.8, 1.5], [6.6, 5.4, 1.6], '1a1a1a')
        for x in (0.6, 14.4):
            for z in (1.6, 13.4): m.cubo([x, 0, z], [x + 1, 9.2, z + 1], '5a3a1e')
    else:
        m.cubo([1, 9, 2], [15, 12.5, 14], '14b8a6', topo='2dd4bf')
        aro(m, 0.8, 9, 1.8, 15.2, 9.6, 14.2, '5a3a1e')
        m.cubo([4, 12.5, 7.4], [12, 13.4, 8.6], 'c8a060')                             # alça de corda
        m.cubo([4, 12.5, 7.4], [4.8, 14.2, 8.6], 'c8a060'); m.cubo([11.2, 12.5, 7.4], [12, 14.2, 8.6], 'c8a060')
        m.cubo([5.5, 12.5, 3.5], [7.5, 13.2, 5.5], 'fbcfe8'); m.cubo([10, 12.5, 10], [11.6, 13.0, 11.6], 'fef3c7')   # conchas
        m.cubo([7.2, 7.8, 1.4], [8.8, 10, 2], 'c8a060')

caixa('caixa_anime', anime)
caixa('caixa_varas', varas_caixa)
CHAVE = ['................'] * 3 + ['................', '................', '..BBBB..........', '.BBBBBB.........', 'BBHHHHBB........', 'BBHHHHBBSSSSSSSS',
         'BBHHHHBBSSSSSSSS', 'BBHHHHBB....T.TT', '.BBBBBB.....T.TT', '..BBBB.......T..', '................'] + ['................'] * 2
extrudar('lootbox', 'chave_anime', CHAVE, {'B': ['1a1a1a', 'b91c1c'], 'H': ['f9a8d4', 'fbcfe8'], 'S': ['c9ced4'], 'T': ['d4a83a']},
         {'B': 2.4, 'H': 2.8, 'S': 1.4, 'T': 1.2}, DISP_ITEM, seed=11, brilho='H')
extrudar('lootbox', 'chave_varas', CHAVE, {'B': ['0f766e', '14b8a6'], 'H': ['f59e0b', 'fbbf24'], 'S': ['c8a060', 'b8904a'], 'T': ['5a3a1e']},
         {'B': 2.4, 'H': 2.6, 'S': 1.4, 'T': 1.2}, DISP_ITEM, seed=12)
print('skins prontas:', len(ESPADAS), 'espadas,', len(VARAS), 'varas')
