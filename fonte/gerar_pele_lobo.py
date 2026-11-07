# Gera as texturas do set "Pele de Lobo" (armadura vestida 64x32 + ícones 16x16).
import random, os
from PIL import Image
random.seed(7)
R='assets/big'
def cor(h):
    h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))+(255,)
PELO=[cor('4a423b'),cor('5b524a'),cor('6b6159'),cor('7a7067'),cor('857a70')]
ESCURO=[cor('3a332d'),cor('453d36'),cor('2f2924')]
CLARO=[cor('a39a8f'),cor('b5ab9f'),cor('c4bbb0')]
COURO=[cor('5c3a21'),cor('6e4527')]
def fur(img,x0,y0,x1,y1,paleta=PELO,listras=True):
    # pelo em mechas verticais: cada coluna tem um tom que muda devagar
    for x in range(x0,x1):
        i=random.randrange(len(paleta))
        for y in range(y0,y1):
            if random.random()<0.28: i=max(0,min(len(paleta)-1,i+random.choice((-1,1))))
            c=paleta[i]
            if listras and (y-y0)%5==4 and random.random()<0.6: c=random.choice(ESCURO)
            img.putpixel((x,y),c)
def box(img,u,v,w,h,d,paleta=PELO):
    # faces padrão de um cubo no layout do skin: topo, baixo, direita, frente, esquerda, trás
    fur(img,u+d,v,u+d+w,v+d,paleta); fur(img,u+d+w,v,u+d+2*w,v+d,paleta)
    fur(img,u,v+d,u+2*d+2*w,v+d+h,paleta)
camada=Image.new('RGBA',(64,32),(0,0,0,0))
# capuz (cabeça 8x8x8 em u=0,v=0)
box(camada,0,0,8,8,8)
for x in range(8,16):              # frente: só a testa do lobo, o rosto do jogador aparece
    for y in range(12,16): camada.putpixel((x,y),(0,0,0,0))
for x in range(9,15): camada.putpixel((x,8),random.choice(ESCURO))   # sobrancelha
camada.putpixel((10,10),cor('f5c542')); camada.putpixel((13,10),cor('f5c542'))   # olhos do lobo
camada.putpixel((10,9),cor('2a2420')); camada.putpixel((13,9),cor('2a2420'))
for x in range(11,13):
    camada.putpixel((x,11),cor('2a2420'))      # focinho em cima da testa
for (x,y) in [(9,0),(10,0),(13,0),(14,0),(9,1),(14,1)]: camada.putpixel((x,y),random.choice(CLARO))  # orelhas no topo
# peito (corpo 8x12x4 em u=16,v=16)
box(camada,16,16,8,12,4)
for y in range(20,32):
    for x in range(22,26): camada.putpixel((x,y),random.choice(CLARO))   # pelo claro na frente
for i in range(8):
    camada.putpixel((20+i,20+i if 20+i<32 else 31),random.choice(COURO))  # tira de couro
for x in (21,23,25,27): camada.putpixel((x,21),cor('ece6da'))  # colar de dentes
# braços (4x12x4 em u=40,v=16)
box(camada,40,16,4,12,4)
for x in range(40,56):
    camada.putpixel((x,30),random.choice(COURO)); camada.putpixel((x,31),random.choice(ESCURO))
# botas (pernas 4x12x4 em u=0,v=16): só a parte de baixo
for y in range(16,32):
    for x in range(0,16): camada.putpixel((x,y),(0,0,0,0))
box(camada,0,16,4,12,4,ESCURO)
for y in range(20,26):
    for x in range(0,16): camada.putpixel((x,y),(0,0,0,0))
for x in range(0,16): camada.putpixel((x,27),random.choice(COURO))
calca=Image.new('RGBA',(64,32),(0,0,0,0))
box(calca,0,16,4,12,4,PELO)
for y in (21,25):
    for x in range(0,16): calca.putpixel((x,y),random.choice(COURO))
box(calca,16,16,8,12,4,PELO)
for y in range(16,26):
    for x in range(16,40): calca.putpixel((x,y),(0,0,0,0))
for x in range(16,40): calca.putpixel((x,26),random.choice(COURO))
for d in ('humanoid','humanoid_leggings'): os.makedirs(f'{R}/textures/entity/equipment/{d}',exist_ok=True)
camada.save(f'{R}/textures/entity/equipment/humanoid/set_lobo.png')
calca.save(f'{R}/textures/entity/equipment/humanoid_leggings/set_lobo.png')
# ícones 16x16
ICONES={
'capacete':["..#..........#..","..##........##..","..###......###..","..############..",".##############.",".###o######o###.",".######..######.",".#####....#####.",".####......####.",".###........###.",".###........###.","..##........##.."],
'peitoral':[".####......####.","######....######","################","######llll######",".#####llll#####.","..####llll####..","..#=##llll##=#..","..##=#####=##...","..###=###=####..","..####===#####..","..############..","..############..","...##########..."],
'calcas':["..############..","..#====#=====#..","..############..","..#####..#####..","..####....####..","..=###....###=..","..####....####..","..####....####..","..####....####..","..=###....###=..","..####....####..","..####....####..","................"],
'botas':["................","...###....###...","...###....###...","...###....###...","...===....===...","..####...####...",".#####..#####...",".#####..#####...","................"],
}
os.makedirs(f'{R}/textures/item/berserker',exist_ok=True)
for nome,mapa in ICONES.items():
    im=Image.new('RGBA',(16,16),(0,0,0,0))
    off=(16-len(mapa))//2
    for y,linha in enumerate(mapa):
        for x,ch in enumerate(linha[:16]):
            c={'#':random.choice(PELO),'l':random.choice(CLARO),'=':random.choice(COURO),'o':cor('f5c542')}.get(ch)
            if c: im.putpixel((x,y+off),c)
    # contorno escuro
    px=im.load(); out=im.copy(); po=out.load()
    for y in range(16):
        for x in range(16):
            if px[x,y][3]==0 and any(0<=x+dx<16 and 0<=y+dy<16 and px[x+dx,y+dy][3]>0 for dx,dy in((1,0),(-1,0),(0,1),(0,-1))):
                po[x,y]=cor('1f1a16')
    out.save(f'{R}/textures/item/berserker/set_lobo_{nome}.png')
print('ok')
