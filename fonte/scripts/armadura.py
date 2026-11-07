# Ajudantes para pintar armaduras vestidas 128x64 (o dobro da resolução padrão) e o modelo-bloco (Modelo).
import random, math, os, json
from PIL import Image
from voxel import cor, mix, R

S = 2
def face(img, x0, y0, w, h, pal, luz=1.0, borda=True):
    for x in range(w):
        for y in range(h):
            c = mix(random.choice(pal), luz * (1.08 - 0.22 * y / max(1, h - 1)))
            img.putpixel((x0 + x, y0 + y), c)
        if borda:
            for y in (0, h - 1): img.putpixel((x0 + x, y0 + y), mix(img.getpixel((x0 + x, y0 + y)), 0.8))
def box(img, u, v, w, h, d, pal):
    u, v, w, h, d = u * S, v * S, w * S, h * S, d * S
    face(img, u + d, v, w, d, pal, 1.15); face(img, u + d + w, v, w, d, pal, 0.75)
    face(img, u, v + d, d, h, pal, 0.9); face(img, u + d, v + d, w, h, pal, 1.0)
    face(img, u + d + w, v + d, d, h, pal, 0.9); face(img, u + 2 * d + w, v + d, w, h, pal, 0.85)
def ret(img, x, y, w, h, pal, luz=1.0):
    for xx in range(x, x + w):
        for yy in range(y, y + h): img.putpixel((xx, yy), mix(random.choice(pal), luz))
def limpa(img, x, y, w, h):
    for xx in range(x, x + w):
        for yy in range(y, y + h): img.putpixel((xx, yy), (0, 0, 0, 0))
def linha_h(img, x0, x1, y, pal):
    for x in range(x0, x1): img.putpixel((x, y), random.choice(pal))
def circulo(img, cx, cy, r, pal):
    for x in range(int(cx - r - 1), int(cx + r + 2)):
        for y in range(int(cy - r - 1), int(cy + r + 2)):
            if math.hypot(x - cx, y - cy) < r: img.putpixel((x, y), random.choice(pal))

# regiões (já no 128x64)
PEITO = (40, 40, 16, 24)      # frente do corpo
COSTAS = (64, 40, 16, 24)
BRACOS = (80, 32, 32, 32)     # caixa dos braços (topo em 88..96 x 32..40, laterais em y 40..64)
def salvar(nome, cam, cal):
    for d in ('humanoid', 'humanoid_leggings'): os.makedirs(f'{R}/textures/entity/equipment/{d}', exist_ok=True)
    cam.save(f'{R}/textures/entity/equipment/humanoid/{nome}.png')
    cal.save(f'{R}/textures/entity/equipment/humanoid_leggings/{nome}.png')
    os.makedirs(f'{R}/equipment', exist_ok=True)
    json.dump({'layers': {'humanoid': [{'texture': f'big:{nome}'}], 'humanoid_leggings': [{'texture': f'big:{nome}'}]}},
              open(f'{R}/equipment/{nome}.json', 'w'), indent=2)

def carregar_modelo(pasta):
    """Traz a classe Modelo (cubos com pintura) do gerador do lobo, apontando para a pasta da classe."""
    src = open('gerar_lobo_3d.py', encoding='utf-8').read().split('# ---------------- cabeça de lobo')[0].replace('berserker', pasta)
    g = {}
    exec(src, g)
    return g['Modelo'], g['TONS']

DISP_ELMO = {'head': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1.02, 1.02, 1.02]},
             'gui': {'rotation': [25, -145, 0], 'translation': [0, -1.5, 0], 'scale': [0.55, 0.55, 0.55]},
             'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
             'fixed': {'rotation': [0, 180, 0], 'scale': [0.75, 0.75, 0.75]},
             'thirdperson_righthand': {'rotation': [75, 180, 0], 'translation': [0, 1, -2], 'scale': [0.4, 0.4, 0.4]},
             'firstperson_righthand': {'rotation': [0, 225, 0], 'scale': [0.4, 0.4, 0.4]}}
DISP_CAIXA = {'gui': {'rotation': [30, 225, 0], 'translation': [0, 0, 0], 'scale': [0.58, 0.58, 0.58]},
              'ground': {'translation': [0, 3, 0], 'scale': [0.25, 0.25, 0.25]},
              'fixed': {'rotation': [0, 180, 0], 'scale': [0.5, 0.5, 0.5]},
              'head': {'rotation': [0, 180, 0], 'translation': [0, 14, 0], 'scale': [0.9, 0.9, 0.9]},
              'thirdperson_righthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
              'thirdperson_lefthand': {'rotation': [75, 225, 0], 'translation': [0, 2.5, 0], 'scale': [0.375, 0.375, 0.375]},
              'firstperson_righthand': {'rotation': [0, 225, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]},
              'firstperson_lefthand': {'rotation': [0, 45, 0], 'translation': [0, 0, 0], 'scale': [0.4, 0.4, 0.4]}}
