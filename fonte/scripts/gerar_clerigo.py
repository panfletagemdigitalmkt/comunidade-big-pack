# Itens do Clérigo: 3 cetros, 3 livros/relíquias 3D (mão secundária), Vestes da Pomba (mitra 3D + textura) e caixa.
import math, random, json
from PIL import Image
from voxel import gerar, icone, cor, mix, lerp, espelhar, R
import armadura as A

P = 'clerigo'
MAT = {
    'w': ([cor('7a5634'), cor('86603a'), cor('6b4a2b')], 2.0, False),   # madeira
    's': ([cor('c9ced4'), cor('dde1e5'), cor('b4bac1')], 2.2, False),   # prata
    'g': ([cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 2.4, False),   # ouro
    'b': ([cor('7b4a2a'), cor('5e3a22')], 1.6, False),                  # contas do terço
    'P': ([cor('ffe3f1'), cor('ffc7e2'), cor('fff4fa')], 1.8, True),    # pétala de cristal
    'p': ([cor('ff8fc7'), cor('ffb3d9')], 2.2, True),                   # miolo
    'L': ([cor('4fa648'), cor('3f8f3a')], 1.4, False),                  # folha
    'W': ([cor('f8f8f6'), cor('ebebe7'), cor('dededa')], 1.6, False),   # asa de pomba
    'Y': ([cor('ffd23f'), cor('fff0a0')], 3.0, True),                   # orbe de luz
    'B': ([cor('7fd8ff'), cor('b5ecff')], 2.8, True),                   # gema celeste
}
def brilho(ch, x, y, f, n, c0):
    if ch == 'Y': return lerp(c0, cor('ffffff'), 0.5 + 0.5 * math.sin(2 * math.pi * f / n - math.hypot(x - 15.5, y - 5) / 2))
    if ch in 'PpB': return mix(c0, 0.85 + 0.2 * (1 + math.sin(2 * math.pi * f / n + y * 0.6)) / 2)
    return None

gerar(P, 'cetro_prece', espelhar([
    "", "",
    "...............s",
    "...............s",
    "..............ss",
    "...............s",
    "............ssss",
    "...........s.sss",
    "...............s",
    "...............s",
    "..............ss",
    "...............w",
    "...............w",
    "..............bw",
    ".............b.w",
    ".............b.w",
    "..............bw",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "...............w",
    "..............ss",
    "...............s",
]), MAT, seed=51)

gerar(P, 'cetro_lirio', espelhar([
    "",
    "...............P",
    "..............PP",
    "...........P..PP",
    "..........PP..PP",
    "..........PPP.PP",
    "...........PPPpp",
    "............PPpp",
    ".............PPP",
    "..............ss",
    "............L.ss",
    "...........LL..s",
    "............L..s",
    "...............s",
    "...............s",
    "..............Bs",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "...............s",
    "..............ss",
    "...............B",
]), MAT, frames=6, anim=brilho, seed=52)

gerar(P, 'cetro_aureo', espelhar([
    "",
    "..............gY",
    "...........g..YY",
    "............gYYY",
    ".....W......YYYY",
    "....WW......YYYY",
    "...WWW.......YYY",
    "...WWWW......gYY",
    "....WWWWW....ggg",
    ".....WWWWWWW.ggg",
    ".......WWWWWgggB",
    "..........WWgggg",
    ".............ggg",
    "..............gg",
    "...............g",
    "...............g",
    "...............g",
    "..............Bg",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "...............g",
    "..............gg",
    "...............Y",
]), MAT, frames=8, anim=brilho, seed=53)

# ------------------------------------------------------------------ livros, relicário, mitra e caixa (blocos)
Modelo, TONS = A.carregar_modelo(P)
TONS.update({'capa': [cor('5a2f1c'), cor('6b3a22'), cor('4e2818')], 'papel': [cor('efe6cf'), cor('e3d8bd'), cor('f5eedc')],
             'ouro': [cor('d9a62e'), cor('f0c75a'), cor('c4952a')], 'fita': [cor('a51d2a'), cor('b8232f')],
             'branco': [cor('f6f6f3'), cor('e8e8e4'), cor('fbfbf9')], 'luz': [cor('fff3b0'), cor('ffe680')],
             'vidro': [cor('cfe9f5'), cor('b9dff0')], 'azul': [cor('1e3a8a'), cor('2547a8')], 'celeste': [cor('7fd8ff'), cor('b5ecff')]})
DISP_LIVRO = {
    'thirdperson_righthand': {'rotation': [0, 90, -10], 'translation': [0, 1.5, 0.5], 'scale': [0.42, 0.42, 0.42]},
    'thirdperson_lefthand': {'rotation': [0, 90, 10], 'translation': [0, 1.5, 0.5], 'scale': [0.42, 0.42, 0.42]},
    'firstperson_righthand': {'rotation': [5, -70, 5], 'translation': [1.5, 3, 0], 'scale': [0.45, 0.45, 0.45]},
    'firstperson_lefthand': {'rotation': [5, -70, 5], 'translation': [1.5, 3, 0], 'scale': [0.45, 0.45, 0.45]},
    'gui': {'rotation': [15, -30, 0], 'translation': [0, 0, 0], 'scale': [0.68, 0.68, 0.68]},
    'ground': {'translation': [0, 2, 0], 'scale': [0.3, 0.3, 0.3]},
    'fixed': {'rotation': [0, 180, 0], 'scale': [0.6, 0.6, 0.6]}}

l = Modelo('livro_salmos', 64)
l.cubo('capa_frente', [2, 1, 6.2], [14, 15, 7], 'capa')
l.cubo('capa_tras', [2, 1, 9], [14, 15, 9.8], 'capa')
l.cubo('lombada', [1.2, 1, 6.2], [2.2, 15, 9.8], 'capa')
l.cubo('paginas', [2.2, 1.5, 7], [13.6, 14.5, 9], 'papel')
l.cubo('cruz_v', [7.3, 4, 5.8], [8.7, 12.5, 6.3], 'ouro')
l.cubo('cruz_h', [5, 9, 5.8], [11, 10.4, 6.3], 'ouro')
for y0 in (1, 13.6):
    l.cubo(f'canto{y0}', [12.6, y0, 5.9], [14.2, y0 + 1.4, 10.1], 'ouro')
l.cubo('fita', [10, -2, 8], [11, 1.5, 8.4], 'fita')
l.salvar(DISP_LIVRO)

r = Modelo('relicario', 64)
r.cubo('base', [3, 0, 4], [13, 2, 12], 'ouro')
r.cubo('vidro', [4, 2, 5], [12, 10, 11], 'vidro')
for x0, z0 in ((3.5, 4.5), (11.5, 4.5), (3.5, 10.5), (11.5, 10.5)):
    r.cubo(f'coluna{x0}{z0}', [x0, 2, z0], [x0 + 1, 10, z0 + 1], 'ouro')
r.cubo('pena', [7.4, 3, 7.5], [8.6, 9, 8.5], 'luz', brilho=True)
r.cubo('pena_ponta', [6.8, 7, 7.6], [9.2, 9.5, 8.4], 'branco', brilho=True)
r.cubo('teto', [3, 10, 4], [13, 11.5, 12], 'ouro')
r.cubo('cupula', [5, 11.5, 6], [11, 13.5, 10], 'ouro')
r.cubo('cruz_v', [7.4, 13.5, 7.4], [8.6, 18, 8.6], 'ouro')
r.cubo('cruz_h', [6, 15.5, 7.4], [10, 16.6, 8.6], 'ouro')
r.cubo('gema', [7.2, 4.5, 3.6], [8.8, 6.1, 4.1], 'celeste', brilho=True)
r.salvar(DISP_LIVRO)

t = Modelo('tomo_luz', 128)
t.cubo('capa_frente', [1, 0, 5.5], [15, 16, 6.5], 'branco')
t.cubo('capa_tras', [1, 0, 10.5], [15, 16, 11.5], 'branco')
t.cubo('lombada', [0, 0, 5.5], [1.2, 16, 11.5], 'ouro')
t.cubo('paginas', [1.2, 0.5, 6.5], [14.6, 15.5, 10.5], 'luz', brilho=True)
t.cubo('moldura_c', [1, 15, 5.2], [15, 16, 5.6], 'ouro'); t.cubo('moldura_b', [1, 0, 5.2], [15, 1, 5.6], 'ouro')
t.cubo('moldura_d', [14, 0, 5.2], [15, 16, 5.6], 'ouro'); t.cubo('moldura_e', [1, 0, 5.2], [2, 16, 5.6], 'ouro')
t.cubo('sol', [5.5, 5.5, 4.8], [10.5, 10.5, 5.5], 'ouro')
t.cubo('sol_meio', [6.8, 6.8, 4.5], [9.2, 9.2, 4.8], 'luz', brilho=True)
for i, y in enumerate((3, 12)):
    t.cubo(f'fecho{i}', [14.6, y, 5], [16, y + 1.5, 12], 'ouro')
for i, (x, y, ang) in enumerate(((3, 17, 0), (12, 17.5, 0), (7.5, 19, 0))):             # letras de luz flutuando
    t.cubo(f'letra{i}', [x, y, 8], [x + 1, y + 1.4, 8.3], 'luz', brilho=True)
t.salvar(DISP_LIVRO)

m = Modelo('pomba_mitra', 128)
m.cubo('faixa', [-0.5, 9.5, -0.5], [16.5, 12.5, 16.5], 'ouro')
m.cubo('topo', [0, 12.5, 0], [16, 16.5, 16], 'branco')
m.cubo('corpo', [0.5, 16.5, 1.5], [15.5, 20, 14.5], 'branco')
m.cubo('meio', [1.5, 20, 2.5], [14.5, 23.5, 13.5], 'branco')
m.cubo('alto', [3.5, 23.5, 4], [12.5, 26.5, 12], 'branco')
m.cubo('pico', [5.5, 26.5, 5.5], [10.5, 28.5, 10.5], 'branco')
m.cubo('ponta', [7, 28.5, 7], [9, 30, 9], 'ouro')
m.cubo('listra_f', [7, 12.5, -0.3], [9, 26, 0.3], 'ouro')
m.cubo('listra_t', [7, 12.5, 15.7], [9, 26, 16.3], 'ouro')
m.cubo('cruz_h', [4.5, 19.5, 0.9], [11.5, 21, 1.6], 'ouro')
m.cubo('cruz_v', [7.2, 16.5, 0.9], [8.8, 24, 1.6], 'ouro')
m.cubo('pomba', [6.6, 10.2, -1], [9.4, 12, -0.5], 'luz', brilho=True)
for x0 in (4, 10.5):
    m.cubo(f'fita{x0}', [x0, 0, 16.2], [x0 + 1.5, 10, 16.8], 'branco')
    m.cubo(f'fita_ponta{x0}', [x0, -1, 16.1], [x0 + 1.5, 0.5, 16.9], 'ouro')
m.salvar(A.DISP_ELMO)

c = Modelo('caixa_clerigo', 128)
c.cubo('base', [0.5, 0, 1.5], [15.5, 1.5, 14.5], 'ouro')
c.cubo('corpo', [1, 1.5, 2], [15, 9.5, 14], 'branco')
for x0 in (1.2, 5.2, 9.2):                                    # arcos dourados na frente
    c.cubo(f'arco{x0}', [x0 + 0.6, 2, 1.6], [x0 + 4.6, 8.5, 2.1], 'ouro')
    c.cubo(f'arco_in{x0}', [x0 + 1.4, 2, 1.4], [x0 + 3.8, 7.5, 1.8], 'azul')
c.cubo('tampa', [0.5, 9.5, 1.5], [15.5, 11.5, 14.5], 'ouro')
c.cubo('cupula', [2, 11.5, 3], [14, 14, 13], 'branco')
c.cubo('cupula2', [4, 14, 5], [12, 15.5, 11], 'branco')
c.cubo('cruz_v', [7.2, 3, 0.9], [8.8, 9, 1.4], 'luz', brilho=True)
c.cubo('cruz_h', [5.5, 6, 0.9], [10.5, 7.4, 1.4], 'luz', brilho=True)
c.cubo('pomba_corpo', [6.5, 15.5, 6.5], [9.5, 17.5, 10.5], 'branco')        # pombinha no topo
c.cubo('pomba_cabeca', [7, 17, 5.2], [9, 19, 7], 'branco')
c.cubo('pomba_bico', [7.6, 17.5, 4.5], [8.4, 18.2, 5.2], 'ouro')
c.cubo('pomba_asa_e', [4, 16.5, 7], [6.5, 18, 10], 'branco', rot={'angle': 22.5, 'axis': 'z', 'origin': [6.5, 16.5, 8]})
c.cubo('pomba_asa_d', [9.5, 16.5, 7], [12, 18, 10], 'branco', rot={'angle': -22.5, 'axis': 'z', 'origin': [9.5, 16.5, 8]})
c.cubo('pomba_cauda', [7, 15.8, 10.5], [9, 17, 12.5], 'branco')
c.salvar(A.DISP_CAIXA)

# ------------------------------------------------------------------ Vestes da Pomba vestidas
random.seed(61)
BRANCO = [cor('f4f4f1'), cor('e9e9e5'), cor('fbfbf9')]
OURO = [cor('d9a62e'), cor('f0c75a'), cor('c4952a')]
AZUL = [cor('2a5fc0'), cor('1f4fa8'), cor('3a6fd0')]
COURO = [cor('7a4e2e'), cor('6b4327')]
cam = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cam, 16, 16, 8, 12, 4, BRANCO)
A.ret(cam, 40, 40, 16, 2, OURO)
for y in range(42, 64):                                       # barra dourada no meio da túnica
    cam.putpixel((47, y), random.choice(OURO)); cam.putpixel((48, y), random.choice(OURO))
A.ret(cam, 44, 45, 8, 2, OURO)                                # cruz no peito
for i in range(16):                                           # faixa azul na diagonal
    for k in range(3): cam.putpixel((40 + i, 50 + i // 2 + k - 4), random.choice(AZUL))
A.ret(cam, 64, 40, 16, 24, BRANCO, 0.95)
for y in range(44, 52): cam.putpixel((71, y), random.choice(OURO)); cam.putpixel((72, y), random.choice(OURO))
A.ret(cam, 68, 46, 8, 2, OURO)
A.box(cam, 40, 16, 4, 12, 4, BRANCO)
for x in range(80, 112):
    for y in (58, 59, 60): cam.putpixel((x, y), random.choice(OURO))
    for y in (40, 41): cam.putpixel((x, y), random.choice(OURO))
A.limpa(cam, 0, 32, 32, 32); A.box(cam, 0, 16, 4, 12, 4, COURO); A.limpa(cam, 0, 40, 32, 16)  # sandálias
for y in (57, 60): A.linha_h(cam, 0, 32, y, [cor('5a3820')])
A.limpa(cam, 0, 0, 64, 32)
cal = Image.new('RGBA', (128, 64), (0, 0, 0, 0))
A.box(cal, 0, 16, 4, 12, 4, BRANCO)
for y in (60, 61): A.linha_h(cal, 0, 32, y, OURO)
A.box(cal, 16, 16, 8, 12, 4, BRANCO); A.limpa(cal, 32, 32, 48, 16)
for y in (48, 49): A.linha_h(cal, 32, 80, y, AZUL)
A.ret(cal, 47, 50, 2, 14, OURO)
A.salvar('set_pomba', cam, cal)

ICO = {'w': BRANCO, 'g': OURO, 'b': AZUL, 'c': COURO}
icone(P, 'set_pomba_peitoral', ["", "..www......www..", ".wwwwg....gwwww.", ".wwwwwggggwwwww.", ".wwwwwwggwwwwww.",
      "..wwwbgggggwww..", "...wwwbbggwww...", "...wwwwwgbbww...", "...wwwwwggwbb...", "...wwwwwggwww...", "...wwwwwggwww...",
      "...wwwwwggwww...", "...gggggggggg..."], ICO)
icone(P, 'set_pomba_calcas', ["", "", "...bbbbbbbbbb...", "...wwwwggwwww...", "...wwwwggwwww...", "...wwwwggwwww...",
      "..wwwwwggwwwww..", "..wwwwwggwwwww..", "..wwwwwggwwwww..", ".wwwwwwggwwwwww.", ".wwwwwwggwwwwww.", ".gggggggggggggg."], ICO)
icone(P, 'set_pomba_botas', ["", "", "", "", "", "", "", "..c.c.....c.c...", "..ccc.....ccc...", "..c.c.....c.c...",
      ".cccc....cccc...", "cccccc..cccccc.."], ICO)
print('clerigo ok')
