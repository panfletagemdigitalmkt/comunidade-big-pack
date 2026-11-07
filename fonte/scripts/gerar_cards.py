# Cards de descrição (tooltip_style) dos itens: fundo + moldura em 9-slice, com joias nos cantos.
# O item usa tooltip_style "big:<estilo>" e o jogo procura big:tooltip/<estilo>_background e _frame.
import json, os
from PIL import Image
from voxel import cor, mix, R

P = f'{R}/textures/gui/sprites/tooltip'
os.makedirs(P, exist_ok=True)
META = {'gui': {'scaling': {'type': 'nine_slice', 'width': 100, 'height': 100, 'border': 9}}}
N = 100

ESTILOS = {   # linha clara, linha de baixo, fundo, joia, enfeite extra
    'comum':    ('a1a1aa', '71717a', '131317', 'e4e4e7', None),
    'incomum':  ('4ade80', '15803d', '0d1710', '86efac', None),
    'raro':     ('60a5fa', '1d4ed8', '0b1222', 'bfdbfe', None),
    'epico':    ('c084fc', '7e22ce', '150b22', 'f5d0fe', 'c084fc'),
    'lendario': ('fbbf24', 'c2410c', '1b1206', 'fff3b0', 'fbbf24'),
    'caixa':    ('f0abfc', '7c3aed', '160b20', 'fae8ff', 'f0abfc'),
    'fazenda':  ('a3e635', '4d7c0f', '17110a', 'fde047', None),
    'pesca':    ('38bdf8', '0369a1', '06141d', 'a5f3fc', None),
}

def d_borda(x, y):
    return min(x, y, N - 1 - x, N - 1 - y)

def canto(x, y):
    """distância ao canto mais próximo, em coordenadas do canto (0..)"""
    cx = x if x < N / 2 else N - 1 - x
    cy = y if y < N / 2 else N - 1 - y
    return cx, cy

for nome, (a, a2, fundo, joia, extra) in ESTILOS.items():
    bg = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    fr = Image.new('RGBA', (N, N), (0, 0, 0, 0))
    A, A2, F, J = cor(a), cor(a2), cor(fundo), cor(joia)
    for y in range(N):
        for x in range(N):
            d = d_borda(x, y)
            cx, cy = canto(x, y)
            # fundo: painel a partir de d=5, quinas cortadas
            if d >= 5 and not (cx == 5 and cy == 5):
                c = F
                if y < N / 2 and 6 <= y <= 8 and d >= 6: c = mix(F, 1.35 if y == 6 else 1.15)   # brilho no topo
                bg.putpixel((x, y), c[:3] + (246,))
            # moldura
            if cx >= 5 and cy >= 5 and (cx == 5 or cy == 5) and not (cx == 5 and cy == 5):
                fr.putpixel((x, y), cor('05060a'))                      # contorno escuro
            elif cx >= 6 and cy >= 6 and (cx == 6 or cy == 6):
                if y < N / 2 and cy == 6: c = A                          # linha de cima clara
                elif y >= N / 2 and cy == 6: c = A2                      # linha de baixo escura
                else: c = tuple(int((A[i] + A2[i]) / 2) for i in range(3)) + (255,)
                fr.putpixel((x, y), c)
            elif cx >= 7 and cy >= 7 and (cx == 7 or cy == 7):
                fr.putpixel((x, y), mix(A2, 0.55)[:3] + (200,))          # linha interna
    # joia em losango em cada canto (centro 4,4 do canto)
    for (ox, oy) in ((0, 0), (N - 9, 0), (0, N - 9), (N - 9, N - 9)):
        for y in range(9):
            for x in range(9):
                dd = abs(x - 4) + abs(y - 4)
                px, py = ox + x, oy + y
                if dd == 4: fr.putpixel((px, py), cor('05060a'))
                elif dd <= 3:
                    c = J if (x - 4) + (y - 4) < -1 else mix(J, 0.8) if dd <= 1 else mix(A2, 1.05) if (x - 4) + (y - 4) > 1 else A
                    if x == 3 and y == 3: c = cor('ffffff')
                    fr.putpixel((px, py), c)
    bg.save(f'{P}/{nome}_background.png'); fr.save(f'{P}/{nome}_frame.png')
    for s in ('background', 'frame'):
        json.dump(META, open(f'{P}/{nome}_{s}.png.mcmeta', 'w'))
print('cards:', ', '.join(ESTILOS))
