# HUD da briga de pesca: fonte própria com segmentos e ícones em pixel art (barra de Puxar e de Tensão).
import json, os
from PIL import Image
from voxel import cor, mix, R

PASTA = f'{R}/textures/font/pesca'
os.makedirs(PASTA, exist_ok=True); os.makedirs(f'{R}/font', exist_ok=True)
prov = []

def glifo(ch, nome, img, ascent=8):
    img.save(f'{PASTA}/{nome}.png')
    prov.append({'type': 'bitmap', 'file': f'big:font/pesca/{nome}.png', 'ascent': ascent, 'height': img.height, 'chars': [ch]})

def segmento(nome, ch, base, cheio=True):
    im = Image.new('RGBA', (3, 9), (0, 0, 0, 0))
    c = cor(base)
    for x in range(3):
        for y in range(1, 8):
            if not cheio:
                v = cor('1c2230') if y in (1, 7) else cor('2a3142')
                if y == 2: v = cor('343c50')
            else:
                v = mix(c, 1.35) if y == 1 else mix(c, 1.12) if y == 2 else mix(c, 0.62) if y == 7 else mix(c, 0.82) if y == 6 else c
            im.putpixel((x, y), v)
    glifo(ch, nome, im)

def tampa(nome, ch, esquerda):
    im = Image.new('RGBA', (2, 9), (0, 0, 0, 0))
    for y in range(0, 9):
        for x in range(2):
            borda = (x == 0) if esquerda else (x == 1)
            if (y in (1, 7) and not borda) or (borda and 1 <= y <= 7):
                im.putpixel((x, y), cor('c9b48a') if y < 4 else cor('8a7650'))
    glifo(ch, nome, im)

def icone(nome, ch, linhas, cores):
    im = Image.new('RGBA', (9, 9), (0, 0, 0, 0))
    for y, l in enumerate(linhas):
        for x, k in enumerate(l):
            if k in cores: im.putpixel((x, y), cor(cores[k]))
    glifo(ch, nome, im)

segmento('vazio', '', '000000', cheio=False)
for i, c in enumerate(['1e88c8', '22a6d8', '35c2e6', '6ae0f2']): segmento(f'puxar{i}', chr(0xe002 + i), c)
segmento('verde', '', '3cc84a')
segmento('amarelo', '', 'e8c62a')
segmento('laranja', '', 'ec8a24')
segmento('vermelho', '', 'e2342c')
segmento('vermelho_pisca', '', 'ff8a7a')
tampa('tampa_e', '', True)
tampa('tampa_d', '', False)
icone('molinete', '', ['...ooo...', '..oOOOo..', '.oO.c.Oo.', '.oOcCcOo.', '.oO.c.Oo.', '..oOOOo..', '...ooo.hh', '....s..hk', '...sss...'],
      {'o': '6a7280', 'O': 'c8ccd4', 'c': 'e8c040', 'C': 'fff0a0', 'h': '3a3f48', 'k': 'e2342c', 's': '8a6a3a'})
icone('anzol', '', ['....w....', '....w....', '....w....', '...ggg...', '....g....', '.g..g....', '.gg.g....', '..ggg....', '...g.....'],
      {'w': 'e8eef4', 'g': 'c8ccd4'})
icone('alerta', '', ['....r....', '...rrr...', '...rwr...', '..rrwrr..', '..rrwrr..', '.rrrrrrr.', '.rrrwrrr.', 'rrrrrrrrr', '.........'],
      {'r': 'e2342c', 'w': 'fff4e0'})
icone('peixe', '', ['.........', '.........', '.b...bbb.', '.bb.bbbbb', '..bbbbobb', '.bb.bbbbb', '.b...bbb.', '.........', '.........'],
      {'b': '6ae0f2', 'o': '102030'})
prov.append({'type': 'space', 'advances': {'': 6, '': -1, '': 3}})
json.dump({'providers': prov}, open(f'{R}/font/pesca.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('hud pronto', len(prov))
