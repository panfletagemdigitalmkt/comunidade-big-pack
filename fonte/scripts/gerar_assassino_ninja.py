# Itens do Assassino e do Ninja: armas 3D, capuz/máscara 3D, roupas vestidas, ícones e caixas.
import math, random
from PIL import Image
from voxel import gerar, icone, cor, mix, lerp, espelhar, R
import armadura as A

MAT = {
    'b': ([cor('b9c0c8'), cor('c8ced5'), cor('a9b1ba')], 1.8, False),   # aço
    'e': ([cor('eef2f5'), cor('ffffff'), cor('dfe5ea')], 1.0, False),   # fio
    'n': ([cor('26232b'), cor('1c1a20'), cor('312d38')], 2.2, False),   # aço negro
    'p': ([cor('5b21b6'), cor('6d28d9'), cor('4c1d95')], 2.4, False),   # faixa roxa
    'P': ([cor('c084fc'), cor('e9d5ff'), cor('a855f7')], 1.4, True),    # brilho roxo
    'l': ([cor('1a1614'), cor('241e1b'), cor('2e2622')], 2.4, False),   # couro negro
    's': ([cor('c9ced4'), cor('dde1e5'), cor('b4bac1')], 2.2, False),   # prata
    'o': ([cor('ece6d6'), cor('d8cfba')], 2.2, False),                  # osso
    'r': ([cor('8b1a1a'), cor('a51d1d'), cor('701414')], 2.4, False),   # vermelho escuro
    'R': ([cor('ff3b3b'), cor('ff7070')], 2.0, True),                   # vermelho brilhante
    'V': ([cor('7dff6b'), cor('b5ff9e')], 2.0, True),                   # veneno
    'C': ([cor('5ff2ff'), cor('b8fbff'), cor('e6feff')], 1.6, True),    # brilho ciano
    'f': ([cor('15131a'), cor('211d29'), cor('2d2838')], 1.2, False),   # penas de corvo
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 2.6, False),   # ouro
    'k': ([cor('141414'), cor('1e1e1e')], 2.6, False),                  # cabo preto
    'K': ([cor('e9e4d8'), cor('d8d2c3')], 2.7, False),                  # trama branca
    'u': ([cor('1e3a8a'), cor('1d4ed8')], 2.6, False),                  # azul
    'w': ([cor('6b4a2b'), cor('7a5634'), cor('5c3d22')], 2.2, False),   # madeira
}

def brilho(ch, x, y, f, n, c0):
    if ch in 'PCRV':
        onda = 0.5 + 0.5 * math.sin(2 * math.pi * f / n - y * 0.45)
        return lerp(c0, cor('ffffff'), onda * 0.55)
    return None

# ======================================================= ASSASSINO
P = 'assassino'
gerar(P, 'adaga_presa', [""] * 8 + [
    "..................e",
    ".................be",
    "................nbe",
    "................nbe",
    "...............nbbe",
    "...............nbbe",
    "..............nnbbe",
    "..............nbbbe",
    "..............nbbe",
    "..............nbbe",
    "..............nbbe",
    "............ppnnnnpp",
    "...............ll",
    "...............pp",
    "...............ll",
    "...............pp",
    "...............ll",
    "...............pp",
    "..............nnnn",
    "...............PP",
], MAT, frames=6, anim=brilho, seed=101)

gerar(P, 'adaga_eclipse', [""] * 6 + [
    "...............P",
    "..............nP",
    "..............nnP",
    ".............nnnP",
    ".............nnnP",
    ".............nnnP",
    "............nnnnP",
    "............nnnnP",
    "............nnnP",
    "............nnnP",
    "............nnnP",
    "..........P.nnnn.P",
    "...........PPnnPP",
    "..............ss",
    "...............ll",
    "...............ss",
    "...............ll",
    "...............ss",
    "...............ll",
    "..............ssss",
    "...............PP",
], MAT, frames=8, anim=brilho, seed=102)

gerar(P, 'adaga_viuva', [""] * 5 + [
    "...............e",
    "..............eb",
    "..............bVe",
    ".............ebVb",
    "..............bVbe",
    ".............ebVb",
    "..............bVbe",
    ".............ebVb",
    "..............bVbe",
    ".............ebVb",
    "..............bVb",
    "..........r..rrrrr..r",
    "...........r.rRRr.r",
    "............rrrrr",
    "...............ll",
    "...............rr",
    "...............ll",
    "...............rr",
    "...............ll",
    "..............rrrr",
    "...............VV",
], MAT, frames=8, anim=brilho, seed=103)

gerar(P, 'estilete', [""] * 7 + ["...............e"] + ["...............s"] * 11 + [
    "..............ssss",
    "...............oo",
    "...............oo",
    "...............oo",
    "...............oo",
    "...............oo",
    "..............oooo",
], MAT, seed=104)

gerar(P, 'garra_corvo', [""] * 8 + [
    "..........ee",
    ".........ebb",
    "........ebb",
    "........eb",
    "........eb",
    ".........eb",
    "..........ebb",
    "...........ebbn",
    "............nnnn",
    "..............ll",
    "..............ll",
    ".............nnnn",
    ".............n..n",
    ".............nnnn",
    "............f....f",
    "...........ff....ff",
    "...........f......f",
], MAT, seed=105)

gerar(P, 'lamina_fantasma', [""] * 5 + [
    "...............C",
    "..............CC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    ".............CCCC",
    "...........ssssssss",
    "...............ll",
    "...............ss",
    "...............ll",
    "...............ss",
    "...............ll",
    "..............ssss",
    "...............CC",
], MAT, frames=8, anim=brilho, seed=106)

# ======================================================= NINJA
P = 'ninja'
def katana(lamina, fio, tsuba, cabo1, cabo2, extra=None):
    l = ["..................e".replace('e', fio)]
    for i in range(1, 18):
        col = 17 if i < 3 else 16 if i < 6 else 15 if i < 11 else 14
        l.append('.' * col + lamina * 2 + fio)
    l.append("..............ggg")
    l.append("............" + tsuba * 7)
    l.append("............" + tsuba * 7)
    for i in range(8):
        l.append("..............kKk".replace('k', cabo1).replace('K', cabo2) if i % 2 == 0 else "..............KkK".replace('k', cabo1).replace('K', cabo2))
    l.append("..............nnn")
    if extra:
        for (x, y, ch) in extra:
            row = l[y].ljust(32, '.')
            l[y] = row[:x] + ch + row[x + 1:]
    return l

gerar(P, 'katana_aprendiz', katana('b', 'e', 'n', 'k', 'K'), MAT, seed=201)
gerar(P, 'katana_tempestade', katana('b', 'C', 'u', 'k', 'u',
      extra=[(14, 3, 'C'), (13, 4, 'C'), (19, 7, 'C'), (20, 8, 'C'), (12, 12, 'C'), (11, 13, 'C'), (18, 15, 'C')]),
      MAT, frames=8, anim=brilho, seed=202)
gerar(P, 'kusanagi', katana('R', 'e', 'g', 'r', 'k', extra=[(11, 19, 'g'), (19, 20, 'g')]), MAT, frames=8, anim=brilho, seed=203)

gerar(P, 'kunai', [""] * 8 + [
    "...............e",
    "..............bbb",
    ".............bbbbb",
    ".............bbnbb",
    "..............bnb",
    "..............bnb",
    "...............n",
    "..............nnn",
    "...............l",
    "...............n",
    "...............l",
    "...............n",
    "...............l",
    "...............n",
    "...............l",
    "..............nnn",
    ".............n...n",
    ".............n...n",
    "..............nnn",
], MAT, seed=204)

def shuriken_grade():
    g = []
    for y in range(32):
        row = ''
        for x in range(32):
            dx, dy = x - 15.5, y - 13.5
            d = math.hypot(dx, dy)
            a = math.atan2(dy, dx)
            ponta = max(abs(math.cos(2 * a)) ** 6, 0)
            lim = 2.2 + 7.0 * ponta
            if d < 1.3: row += '.'
            elif d < 2.4: row += 'n'
            elif d < lim:
                row += 'e' if d > lim - 1.0 else ('C' if 3.0 < d < 3.8 else 'b')
            else: row += '.'
        g.append(row)
    return g
gerar(P, 'shuriken_aco', shuriken_grade(), MAT, frames=6, anim=brilho, seed=205)

gerar(P, 'kama_sombria', [""] * 5 + [
    "...........eeee",
    "..........ebbbbnn",
    ".........ebb...nn",
    "........ebb....ww",
    "........eb.....ww",
    ".......eb......ww",
    ".......e.......ww",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............ll",
    "...............ww",
    "...............nn",
    "................s",
    ".................s",
    "................s",
    ".................s",
    "................ss",
], MAT, seed=206)

# ======================================================= capuz, máscara e caixas (blocos)
Modelo, TONS = A.carregar_modelo('assassino')
TONS.update({'capuz': [cor('16131c'), cor('1f1a28'), cor('120f17')], 'roxo': [cor('5b21b6'), cor('6d28d9')],
             'bico': [cor('2b2724'), cor('38322d')], 'lente': [cor('ff1a1a'), cor('ff5050')], 'pena': [cor('121015'), cor('1d1a22'), cor('2a2531')],
             'prata': [cor('c9ced4'), cor('dde1e5')], 'osso': [cor('ece6d6'), cor('d8cfba')], 'brilho': [cor('c084fc'), cor('e9d5ff')],
             'madeira_negra': [cor('1c1410'), cor('261b15'), cor('140e0b')]})
h = Modelo('corvo_capuz', 128)
h.cubo('topo', [-0.5, 8, -0.5], [16.5, 17, 16.5], 'capuz')
h.cubo('ponta', [5, 16.5, 9], [11, 19, 15], 'capuz', rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 17, 12]})
h.cubo('lado_e', [-0.8, 0, 0.5], [1.5, 8, 16], 'capuz')
h.cubo('lado_d', [14.5, 0, 0.5], [16.8, 8, 16], 'capuz')
h.cubo('nuca', [-0.5, -1, 14], [16.5, 8, 16.8], 'capuz')
h.cubo('borda', [-0.8, 11, -1], [16.8, 12.5, 0.5], 'roxo')
h.cubo('mascara', [2, 6, -1.2], [14, 11.5, 0], 'bico')
h.cubo('bico1', [5, 6.5, -5], [11, 10, -1.2], 'bico')
h.cubo('bico2', [6, 5.5, -9], [10, 8.5, -5], 'bico', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 8, -5]})
h.cubo('bico3', [7, 4.5, -12], [9, 6.5, -8.5], 'bico', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 8, -5]})
h.cubo('lente_e', [2.8, 8.4, -1.6], [6, 10.8, -1.2], 'lente', brilho=True)
h.cubo('lente_d', [10, 8.4, -1.6], [13.2, 10.8, -1.2], 'lente', brilho=True)
h.cubo('aro_e', [2.5, 8, -1.4], [6.3, 11.2, -1.1], 'prata')
h.cubo('aro_d', [9.7, 8, -1.4], [13.5, 11.2, -1.1], 'prata')
for i, x in enumerate((1, 5, 9, 13)):
    h.cubo(f'pena{i}', [x - 1, 0, 15.5], [x + 2, 10, 17.5], 'pena', rot={'angle': [-22.5, 0, 0, 22.5][i], 'axis': 'z', 'origin': [x, 10, 16]})
h.salvar(A.DISP_ELMO)

c = Modelo('caixa_assassino', 128)
c.cubo('corpo', [2, 0, 1], [14, 9, 15], 'madeira_negra')
c.cubo('pes', [1.5, 0, 0.5], [14.5, 1.2, 15.5], 'prata')
c.cubo('tampa', [1.5, 9, 0.5], [14.5, 11.5, 15.5], 'madeira_negra')
c.cubo('tampa2', [3, 11.5, 2], [13, 12.5, 14], 'roxo')
for x0 in (1.4, 13.6):
    c.cubo(f'friso{x0}', [x0, 0, 0.4], [x0 + 1, 11.6, 15.6], 'prata')
c.cubo('cranio', [6, 3, 0.3], [10, 7.5, 1.2], 'osso')
c.cubo('olho_e', [6.6, 5.2, 0.1], [7.6, 6.2, 0.3], 'brilho', brilho=True)
c.cubo('olho_d', [8.4, 5.2, 0.1], [9.4, 6.2, 0.3], 'brilho', brilho=True)
c.cubo('dentes', [6.8, 3.3, 0.1], [9.2, 3.9, 0.3], 'capuz')
for i, ang in enumerate((-45, 45)):                     # adagas cruzadas na tampa
    rot = {'angle': ang, 'axis': 'y', 'origin': [8, 12.5, 8]}
    c.cubo(f'lamina{i}', [7.5, 12.5, 1.5], [8.5, 13.2, 10.5], 'prata', rot=rot)
    c.cubo(f'guarda{i}', [6, 12.5, 10.5], [10, 13.4, 11.2], 'roxo', rot=rot)
    c.cubo(f'cabo{i}', [7.5, 12.5, 11.2], [8.5, 13.3, 14], 'capuz', rot=rot)
for i, (x, y) in enumerate(((3, 6), (12, 6), (3, 2.5), (12, 2.5))):
    c.cubo(f'runa{i}', [x, y, 0.6], [x + 1, y + 2, 0.9], 'brilho', brilho=True)
c.salvar(A.DISP_CAIXA)

Modelo, TONS = A.carregar_modelo('ninja')
TONS.update({'capuz': [cor('111827'), cor('1a2333'), cor('0b1220')], 'faixa': [cor('b91c1c'), cor('dc2626'), cor('991b1b')],
             'placa': [cor('9ca3af'), cor('d1d5db')], 'olho_ciano': [cor('5ff2ff'), cor('b8fbff')], 'pele': [cor('c8a27c'), cor('b8916c')],
             'laca': [cor('9b1c1c'), cor('b91c1c'), cor('7f1d1d')], 'preto': [cor('111111'), cor('1c1c1c')],
             'ouro': [cor('d9a62e'), cor('f0c75a')], 'aco': [cor('c8ced5'), cor('e6eaee')], 'sakura': [cor('fbcfe8'), cor('f9a8d4'), cor('fce7f3')],
             'papel': [cor('fff7e0'), cor('ffefc2')]})
h = Modelo('nevoa_mascara', 128)
h.cubo('topo', [-0.5, 8.5, -0.5], [16.5, 16.8, 16.5], 'capuz')
h.cubo('lado_e', [-0.8, 0, 0.5], [1.5, 9, 16], 'capuz')
h.cubo('lado_d', [14.5, 0, 0.5], [16.8, 9, 16], 'capuz')
h.cubo('nuca', [-0.5, -1, 14], [16.5, 9, 16.8], 'capuz')
h.cubo('mascara', [-0.6, 0, -0.9], [16.6, 6.5, 0.4], 'capuz')
h.cubo('nariz', [6.5, 4, -1.6], [9.5, 6.5, -0.9], 'capuz')
h.cubo('fenda', [1, 6.5, -0.4], [15, 9, -0.2], 'pele')
h.cubo('olho_e', [3, 7.1, -0.6], [6, 8.3, -0.4], 'olho_ciano', brilho=True)
h.cubo('olho_d', [10, 7.1, -0.6], [13, 8.3, -0.4], 'olho_ciano', brilho=True)
h.cubo('faixa', [-1, 9, -1.2], [17, 11.5, 17], 'faixa')
h.cubo('placa', [4.5, 8.7, -1.6], [11.5, 11.8, -1.1], 'placa')
h.cubo('simbolo', [7.4, 9.5, -1.8], [8.6, 11, -1.6], 'preto')
h.cubo('ponta_faixa1', [6, 4, 17], [8, 10.5, 18], 'faixa', rot={'angle': 22.5, 'axis': 'z', 'origin': [7, 10, 17.5]})
h.cubo('ponta_faixa2', [8.5, 3, 17], [10.5, 10.5, 18], 'faixa', rot={'angle': -22.5, 'axis': 'z', 'origin': [9.5, 10, 17.5]})
h.salvar(A.DISP_ELMO)

c = Modelo('caixa_ninja', 128)
c.cubo('corpo', [1.5, 0, 2], [14.5, 9, 14], 'laca')
c.cubo('base', [1, 0, 1.5], [15, 1.2, 14.5], 'preto')
c.cubo('tampa', [1, 9, 1.5], [15, 11, 14.5], 'preto')
for x0, z0 in ((0.8, 1.3), (13.2, 1.3), (0.8, 12.7), (13.2, 12.7)):
    c.cubo(f'canto{x0}{z0}', [x0, 0, z0], [x0 + 2, 11.2, z0 + 2], 'ouro')
c.cubo('selo', [6, 3.5, 1.7], [10, 7.5, 2.1], 'ouro')
c.cubo('selo_meio', [7, 4.5, 1.5], [9, 6.5, 1.8], 'preto')
c.cubo('suporte_e', [3, 11, 7], [4.5, 13.5, 9], 'preto')
c.cubo('suporte_d', [11.5, 11, 7], [13, 13.5, 9], 'preto')
c.cubo('bainha', [1, 12.5, 7.4], [12, 13.6, 8.6], 'preto')
c.cubo('tsuba', [12, 12, 7], [12.6, 14.1, 9], 'ouro')
c.cubo('cabo', [12.6, 12.6, 7.5], [16, 13.5, 8.5], 'papel')
for i, (x, z) in enumerate(((3, 4), (10, 11), (6, 12), (12, 3.5))):
    c.cubo(f'petala{i}', [x, 11, z], [x + 1.5, 11.4, z + 1.5], 'sakura')
c.cubo('lanterna', [5.5, 11, 10.5], [8, 14, 13], 'papel', brilho=True)
c.salvar(A.DISP_CAIXA)

# ======================================================= roupas vestidas
random.seed(301)
NEG = [cor('16131c'), cor('1f1a28'), cor('120f17'), cor('1a1622')]
ROXO = [cor('5b21b6'), cor('6d28d9'), cor('4c1d95')]
COURO = [cor('2b211c'), cor('3a2c24')]
PRATA = [cor('c9ced4'), cor('dde1e5')]
cam = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cam, 16, 16, 8, 12, 4, NEG)
A.ret(cam, 40, 40, 16, 2, ROXO)
for i in range(20):                                       # bandoleira com facas
    for k in range(2): cam.putpixel((40 + i * 15 // 20 + k, 42 + i), random.choice(COURO))
for (x, y) in ((43, 46), (46, 50), (49, 54)):
    for k in range(3): cam.putpixel((x + 1, y + k - 2), random.choice(PRATA))
A.ret(cam, 40, 56, 16, 2, ROXO, 1.1)
A.ret(cam, 64, 40, 16, 24, NEG, 0.9)                      # capa
for y in range(40, 64, 3): A.linha_h(cam, 64, 80, y, [mix(NEG[0], 1.3)])
A.box(cam, 40, 16, 4, 12, 4, NEG)
for x in range(80, 112):
    for y in range(54, 62): cam.putpixel((x, y), random.choice(COURO))
    cam.putpixel((x, 58), random.choice(PRATA))
A.limpa(cam, 0, 32, 32, 32); A.box(cam, 0, 16, 4, 12, 4, COURO); A.limpa(cam, 0, 40, 32, 10)
for x in range(32): cam.putpixel((x, 50), random.choice(ROXO))
A.limpa(cam, 0, 0, 64, 32)
cal = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cal, 0, 16, 4, 12, 4, NEG)
for y in (44, 50): A.linha_h(cal, 0, 32, y, COURO)
A.box(cal, 16, 16, 8, 12, 4, NEG); A.limpa(cal, 32, 32, 48, 16)
for y in (48, 49): A.linha_h(cal, 32, 80, y, ROXO)
A.salvar('set_corvo', cam, cal)
ICO = {'n': NEG, 'p': ROXO, 'c': COURO, 's': PRATA}
icone('assassino', 'set_corvo_peitoral', ["", "..nnn......nnn..", ".nnnnn....nnnnn.", ".nnnnnppppnnnnn.", ".nnnncnnnnnnnnn.", "..nnnnccnnnnnn..",
      "...nnnnscnnnnn..", "...nnnnnsccnnn..", "...nnnnnnnscnn..", "...pppppppppppp.", "...nnnnnnnnnnn..", "...nnnnnnnnnnn..", "...nnnnnnnnnnn.."], ICO)
icone('assassino', 'set_corvo_calcas', ["", "", "...pppppppppp...", "...nnnnccnnnn...", "...nnnnccnnnn...", "...nnnn..nnnn...", "...cccc..cccc...",
      "...nnnn..nnnn...", "...nnnn..nnnn...", "...cccc..cccc...", "...nnnn..nnnn...", "...nnnn..nnnn..."], ICO)
icone('assassino', 'set_corvo_botas', ["", "", "", "", "", "..pppp....pppp..", "..cccc....cccc..", "..cccc....cccc..", "..cccc....cccc..",
      ".ccccc....ccccc.", "cccccc....cccccc", "cccccc....cccccc"], ICO)

random.seed(302)
AZUL = [cor('111827'), cor('172033'), cor('0d1526'), cor('1b2740')]
BRANCO = [cor('e5e7eb'), cor('d1d5db')]
FAIXA = [cor('b91c1c'), cor('dc2626')]
ATAD = [cor('9ca3af'), cor('b5bcc6'), cor('8b929c')]
cam = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cam, 16, 16, 8, 12, 4, AZUL)
for i in range(10):                                       # gola cruzada
    for k in range(2):
        cam.putpixel((40 + i, 40 + i + k), random.choice(BRANCO))
        cam.putpixel((55 - i, 40 + i + k), random.choice(BRANCO))
A.ret(cam, 40, 54, 16, 3, FAIXA)                          # obi vermelho
A.ret(cam, 46, 54, 3, 6, FAIXA, 0.8)
A.ret(cam, 64, 54, 16, 3, FAIXA)
A.box(cam, 40, 16, 4, 12, 4, AZUL)
for x in range(80, 112):                                   # ataduras nos antebraços
    for y in range(52, 64): cam.putpixel((x, y), random.choice(ATAD) if (y + x // 3) % 3 else mix(ATAD[0], 0.8))
A.limpa(cam, 0, 32, 32, 32); A.box(cam, 0, 16, 4, 12, 4, [cor('0b0f19'), cor('111827')]); A.limpa(cam, 0, 40, 32, 12)
for x in range(32): cam.putpixel((x, 52), random.choice(ATAD))
A.limpa(cam, 0, 0, 64, 32)
cal = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cal, 0, 16, 4, 12, 4, AZUL)
for y in range(52, 62): A.linha_h(cal, 0, 32, y, ATAD if y % 2 else [mix(ATAD[0], 0.8)])
A.box(cal, 16, 16, 8, 12, 4, AZUL); A.limpa(cal, 32, 32, 48, 16)
for y in (48, 49, 50): A.linha_h(cal, 32, 80, y, FAIXA)
A.salvar('set_nevoa', cam, cal)
ICO = {'a': AZUL, 'b': BRANCO, 'f': FAIXA, 't': ATAD}
icone('ninja', 'set_nevoa_peitoral', ["", "..aaa......aaa..", ".aaaab....baaaa.", ".aaaaab..baaaaa.", ".aaaaaabbaaaaaa.", "..aaaaaabaaaaa..",
      "...aaaaabaaaaa..", "...aaaaaaaaaaa..", "...ffffffffffff.", "...aaaaffaaaaa..", "...aaaaaaaaaaa..", "...aaaaaaaaaaa.."], ICO)
icone('ninja', 'set_nevoa_calcas', ["", "", "...ffffffffff...", "...aaaaaaaaaa...", "...aaaaaaaaaa...", "...aaaa..aaaa...", "...aaaa..aaaa...",
      "...aaaa..aaaa...", "...tttt..tttt...", "...tttt..tttt...", "...tttt..tttt...", "...tttt..tttt..."], ICO)
icone('ninja', 'set_nevoa_botas', ["", "", "", "", "", "..tttt....tttt..", "..tttt....tttt..", "..aaaa....aaaa..", "..aaaa....aaaa..",
      ".aaaaa....aaaaa.", "aaaaaa....aaaaaa", "aaaaaa....aaaaaa"], ICO)
print('assassino e ninja ok')
