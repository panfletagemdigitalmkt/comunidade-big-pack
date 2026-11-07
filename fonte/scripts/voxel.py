# Gerador de itens 3D "voxel": cada linha de um desenho em pixels vira bloquinhos com espessura própria.
# Usado pelos machados do Berserker e pelas espadas/escudos do Paladino.
import json, os, random, math
from PIL import Image

R = 'assets/big'

def cor(h):
    h = h.lstrip('#'); return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
def mix(c, f):
    return tuple(max(0, min(255, int(x * f))) for x in c[:3]) + (255,)
def lerp(a, b, t):
    t = max(0, min(1, t)); return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,)

def espelhar(meia, w=16):
    return [l.ljust(w, '.')[:w] + l.ljust(w, '.')[:w][::-1] for l in meia]

DISP_ARMA = {
    'thirdperson_righthand': {'rotation': [0, -90, 55], 'translation': [0, 4, 0.5], 'scale': [0.6, 0.6, 0.6]},
    'thirdperson_lefthand': {'rotation': [0, 90, -55], 'translation': [0, 4, 0.5], 'scale': [0.6, 0.6, 0.6]},
    'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.48, 0.48, 0.48]},
    'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.48, 0.48, 0.48]},
    'gui': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [0.5, 0.5, 0.5]},
    'ground': {'translation': [0, 2, 0], 'scale': [0.3, 0.3, 0.3]},
    'fixed': {'rotation': [0, 180, 0], 'scale': [0.55, 0.55, 0.55]},
    'head': {'rotation': [0, 180, 0], 'translation': [0, 13, 7], 'scale': [0.6, 0.6, 0.6]}}

# mesmo enquadramento do escudo do Minecraft (o desenho fica de frente para +z, a alça para -z)
DISP_ESCUDO = {
    'thirdperson_righthand': {'rotation': [0, 90, 0], 'translation': [10, 6, -4], 'scale': [1, 1, 1]},
    'thirdperson_lefthand': {'rotation': [0, 90, 0], 'translation': [10, 6, 12], 'scale': [1, 1, 1]},
    'firstperson_righthand': {'rotation': [0, 180, 5], 'translation': [-10, 2, -10], 'scale': [1.25, 1.25, 1.25]},
    'firstperson_lefthand': {'rotation': [0, 180, 5], 'translation': [10, 0, -10], 'scale': [1.25, 1.25, 1.25]},
    'gui': {'rotation': [15, -25, -5], 'translation': [2, 3, 0], 'scale': [0.65, 0.65, 0.65]},
    'fixed': {'rotation': [0, 180, 0], 'translation': [-4.5, 4.5, -5], 'scale': [0.55, 0.55, 0.55]},
    'ground': {'translation': [2, 4, 2], 'scale': [0.25, 0.25, 0.25]},
    'head': {'rotation': [0, 180, 0], 'translation': [-8, 18, 12], 'scale': [1, 1, 1]}}
DISP_ESCUDO_BLOQ = {
    'thirdperson_righthand': {'rotation': [45, 135, 0], 'translation': [3.51, 11, -2], 'scale': [1, 1, 1]},
    'thirdperson_lefthand': {'rotation': [45, 135, 0], 'translation': [13.51, 3, 5], 'scale': [1, 1, 1]},
    'firstperson_righthand': {'rotation': [0, 180, -5], 'translation': [-15, 5, -11], 'scale': [1.25, 1.25, 1.25]},
    'firstperson_lefthand': {'rotation': [0, 180, -5], 'translation': [5, 5, -11], 'scale': [1.25, 1.25, 1.25]}}


def gerar(pasta, nome, linhas, MAT, modo='arma', frames=1, anim=None, verso=None, extras=None, seed=1, disp=None, sem_item=False, textura=None):
    """modo 'arma': grade 32x32, girada 45° como as armas do jogo.
       modo 'escudo': grade 16x24 no espaço do escudo do jogo, com alça atrás."""
    random.seed(seed)
    W, H = (32, 32) if modo == 'arma' else (16, 24)
    linhas = [l.ljust(W, '.')[:W] for l in linhas] + ['.' * W] * (H - len(linhas))
    TW, TH = 64, 32
    img = Image.new('RGBA', (TW, TH * frames), (0, 0, 0, 0))
    vazio = lambda x, y: not (0 <= x < W and 0 <= y < H) or linhas[y][x] == '.'
    for y in range(H):
        for x in range(W):
            ch = linhas[y][x]
            if ch == '.': continue
            pal = MAT[ch][0]
            base = random.choice(pal)
            luz = 1.0
            if vazio(x - 1, y) or vazio(x, y - 1): luz *= 1.12
            if vazio(x + 1, y) or vazio(x, y + 1): luz *= 0.8
            c0 = mix(base, luz)
            for f in range(frames):
                c = anim(ch, x, y, f, frames, c0) if anim else None
                img.putpixel((x, y + TH * f), c or c0)
    # retalho do verso (escudo) e do couro da alça em x 32..48
    for f in range(frames):
        for x in range(32, 48):
            for y in range(16):
                pal = verso or [cor('6b4a2b'), cor('7a5634'), cor('5c3d22')]
                c = random.choice(pal)
                if y % 4 == 0: c = mix(c, 0.8)
                img.putpixel((x, y + TH * f), c)
            for y in range(16, 20): img.putpixel((x, y + TH * f), random.choice([cor('3e2a1e'), cor('4f3626')]))
    ku, kv = 16 / TW, 16 / TH
    uv = lambda a, b, c_, d: [a * ku, b * kv, c_ * ku, d * kv]
    els = []
    for y in range(H):
        x = 0
        while x < W:
            ch = linhas[y][x]
            if ch == '.': x += 1; continue
            x1 = x
            while x1 + 1 < W and linhas[y][x1 + 1] == ch: x1 += 1
            t = MAT[ch][1]
            if modo == 'arma':
                de, ate = [x - 8, 24 - y - 1, 8 - t / 2], [x1 + 1 - 8, 24 - y, 8 + t / 2]
                norte = uv(x1 + 1, y, x, y + 1)
            else:
                de, ate = [x - 8, 12 - y - 1, 1], [x1 + 1 - 8, 12 - y, 1 + t]
                norte = uv(32 + (x % 16), y % 16, 33 + (x % 16), y % 16 + 1)
            e = {'from': de, 'to': ate,
                 'faces': {'south': {'uv': uv(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'north': {'uv': norte, 'texture': '#0'},
                           'up': {'uv': uv(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'down': {'uv': uv(x, y, x1 + 1, y + 1), 'texture': '#0'},
                           'east': {'uv': uv(x1, y, x1 + 1, y + 1), 'texture': '#0'},
                           'west': {'uv': uv(x, y, x + 1, y + 1), 'texture': '#0'}}}
            if modo == 'arma': e['rotation'] = {'angle': -45, 'axis': 'z', 'origin': [8, 8, 8]}
            if MAT[ch][2]: e['light_emission'] = 15
            els.append(e)
            x = x1 + 1
    if modo == 'escudo':                                   # alça de couro atrás
        couro = uv(32, 16, 48, 20)
        for de, ate in (([-1.5, -4, -4], [1.5, 4, -3]), ([-1.5, 3, -4], [1.5, 4, 1]), ([-1.5, -4, -4], [1.5, -3, 1])):
            els.append({'from': de, 'to': ate, 'faces': {f: {'uv': couro, 'texture': '#0'} for f in ('north', 'south', 'east', 'west', 'up', 'down')}})
    for e in (extras or []): els.append(e)
    tex = f'big:item/{pasta}/{textura or nome}'
    m = {'texture_size': [TW, TH], 'textures': {'0': tex, 'particle': tex}, 'elements': els,
         'display': disp or (DISP_ARMA if modo == 'arma' else DISP_ESCUDO)}
    for d in (f'models/item/{pasta}', f'textures/item/{pasta}', f'items/{pasta}'):
        os.makedirs(f'{R}/{d}', exist_ok=True)
    json.dump(m, open(f'{R}/models/item/{pasta}/{nome}.json', 'w'))
    if modo == 'escudo':
        json.dump({'parent': f'big:item/{pasta}/{nome}', 'display': DISP_ESCUDO_BLOQ},
                  open(f'{R}/models/item/{pasta}/{nome}_bloqueando.json', 'w'), indent=1)
        item = {'model': {'type': 'minecraft:condition', 'property': 'minecraft:using_item',
                          'on_true': {'type': 'minecraft:model', 'model': f'big:item/{pasta}/{nome}_bloqueando'},
                          'on_false': {'type': 'minecraft:model', 'model': f'big:item/{pasta}/{nome}'}}}
    else:
        item = {'model': {'type': 'minecraft:model', 'model': f'big:item/{pasta}/{nome}'}}
    if not sem_item: json.dump(item, open(f'{R}/items/{pasta}/{nome}.json', 'w'), indent=1)
    img.save(f'{R}/textures/item/{pasta}/{textura or nome}.png')
    mc = f'{R}/textures/item/{pasta}/{textura or nome}.png.mcmeta'
    if frames > 1:
        json.dump({'animation': {'frametime': 6, 'interpolate': True, 'width': TW, 'height': TH}}, open(mc, 'w'))
    elif os.path.exists(mc):
        open(mc, 'w').write('{}')
    print(nome, len(els), 'elementos')


def icone(pasta, nome, linhas, cores):
    img = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, ch in enumerate(l.ljust(16, '.')[:16]):
            if ch in cores: img.putpixel((x, y), mix(random.choice(cores[ch]), 1.1 if y < 6 else 0.95))
    os.makedirs(f'{R}/textures/item/{pasta}', exist_ok=True); os.makedirs(f'{R}/models/item/{pasta}', exist_ok=True)
    os.makedirs(f'{R}/items/{pasta}', exist_ok=True)
    img.save(f'{R}/textures/item/{pasta}/{nome}.png')
    json.dump({'parent': 'minecraft:item/generated', 'textures': {'layer0': f'big:item/{pasta}/{nome}'}},
              open(f'{R}/models/item/{pasta}/{nome}.json', 'w'), indent=1)
    json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/{pasta}/{nome}'}},
              open(f'{R}/items/{pasta}/{nome}.json', 'w'), indent=1)
