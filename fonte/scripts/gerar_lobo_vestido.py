# Pele de Lobo v2: textura vestida 128x64 (o dobro da padrão) com sombreado, mechas e detalhes.
import random, os
from PIL import Image
random.seed(21)
R='assets/big/textures/entity/equipment'
def cor(h): h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),255)
def mix(c,f): return tuple(max(0,min(255,int(x*f))) for x in c[:3])+(255,)
PELO=[cor('4d453e'),cor('5d544b'),cor('6c6258'),cor('7b7065'),cor('8a7e72')]
CLARO=[cor('a69d92'),cor('b8aea2'),cor('c9c0b4')]
COURO=[cor('4e2f1b'),cor('5f3a22'),cor('70462a')]
OSSO=[cor('ece6d6'),cor('d8cfba')]
FERRO=[cor('7d838a'),cor('a3a9b0'),cor('c5cad0')]
S=2
def face(img,x0,y0,w,h,pal,luz=1.0):
    for x in range(w):
        i=random.randrange(len(pal))
        for y in range(h):
            if random.random()<0.16: i=max(0,min(len(pal)-1,i+random.choice((-1,1))))
            c=mix(pal[i],luz*(1.1-0.3*y/max(1,h-1)))
            if random.random()<0.1: c=mix(c,0.82)
            img.putpixel((x0+x,y0+y),c)
        for y in (0,h-1): img.putpixel((x0+x,y0+y),mix(img.getpixel((x0+x,y0+y)),0.78))
def box(img,u,v,w,h,d,pal):
    u,v,w,h,d=u*S,v*S,w*S,h*S,d*S
    face(img,u+d,v,w,d,pal,1.15); face(img,u+d+w,v,w,d,pal,0.75)
    face(img,u,v+d,d,h,pal,0.9); face(img,u+d,v+d,w,h,pal,1.0); face(img,u+d+w,v+d,d,h,pal,0.9); face(img,u+2*d+w,v+d,w,h,pal,0.85)
def ret(img,x,y,w,h,pal,luz=1.0):
    for xx in range(x,x+w):
        for yy in range(y,y+h): img.putpixel((xx,yy),mix(random.choice(pal),luz))
def limpa(img,x,y,w,h):
    for xx in range(x,x+w):
        for yy in range(y,y+h): img.putpixel((xx,yy),(0,0,0,0))
cam=Image.new('RGBA',(64*S,32*S),(0,0,0,0))
# corpo (u=16,v=16, 8x12x4): frente em (20..28, 20..32) -> x2
box(cam,16,16,8,12,4,PELO)
ret(cam,44,40,8,22,CLARO)                    # pelo claro no peito
for i in range(16):                          # tira de couro diagonal com costura
    x,y=40+i,40+i+2
    for k in range(3): cam.putpixel((x,y+k),mix(random.choice(COURO),1.0 if k else 1.2))
for i,x in enumerate(range(41,56,3)):        # colar de presas
    cam.putpixel((x,42),OSSO[0]); cam.putpixel((x,43),OSSO[1]); cam.putpixel((x,44),mix(OSSO[1],0.8))
for x in range(40,56): cam.putpixel((x,41),mix(COURO[0],0.9))
for x in range(40,56):                       # gola de pelo claro mais grossa
    for y in range(40,41): cam.putpixel((x,y),random.choice(CLARO))
# costas: duas listras escuras
for y in range(40,64):
    for x in (68,69,74,75): cam.putpixel((x,y),mix(cam.getpixel((x,y)),0.7))
# escudo viking redondo pendurado nas costas (face de trás do corpo: x 64..80, y 40..64)
import math
VERM=[cor('8e1b1b'),cor('a12222'),cor('7a1717')]; BRANCO=[cor('d9d2c3'),cor('e6e0d2'),cor('cbc3b2')]
cx,cy,rr=71.5,51.5,7.9
for x in range(64,80):
    for y in range(41,63):
        dx,dy=x-cx,y-cy; r=math.hypot(dx,dy)
        if r>rr: continue
        ang=(math.degrees(math.atan2(dy,dx))+360)%360
        if r>rr-1.2: c=mix(random.choice(FERRO),0.85 if dy>0 else 1.05)          # aro de ferro
        elif r<2.0: c=mix(random.choice(FERRO),1.2 if dx+dy<0 else 0.8)         # bossa de ferro no meio
        elif r<2.8: c=mix(random.choice(FERRO),0.6)
        else:
            c=random.choice(VERM if int(ang//45)%2==0 else BRANCO)              # gomos vermelho e branco
            if int(r)%3==0 and random.random()<0.5: c=mix(c,0.88)              # tábuas de madeira
            c=mix(c,1.08-0.25*(dy+rr)/(2*rr))
        cam.putpixel((x,y),c)
for a in range(0,360,45):                                                       # rebites no aro
    x=int(round(cx+(rr-0.6)*math.cos(math.radians(a)))); y=int(round(cy+(rr-0.6)*math.sin(math.radians(a))))
    if 64<=x<80: cam.putpixel((x,y),cor('e2e6ea'))
for i in range(16):                                                             # alça de couro do ombro até o escudo
    x,y=64+i,40+i//4
    if math.hypot(x-cx,y-cy)>rr: cam.putpixel((x,y),random.choice(COURO))
# braços (u=40,v=16, 4x12x4)
box(cam,40,16,4,12,4,PELO)
for x in range(80,112):
    for y in (56,57): cam.putpixel((x,y),random.choice(COURO))
    for y in (58,59,60,61,62,63): cam.putpixel((x,y),random.choice(CLARO))   # punho de pelo
# ombreiras de pele presas ao peitoral (parte de cima dos braços)
for x in range(88,96):
    for y in range(32,40): cam.putpixel((x,y),mix(random.choice(CLARO),1.1))      # topo do ombro
for x in range(80,112):
    for y in range(40,48): cam.putpixel((x,y),mix(random.choice(CLARO),1.05-0.03*(y-40)))
    for y in (48,49): cam.putpixel((x,y),random.choice(COURO))                   # tira de couro
    if x%4==1:                                                                   # garras de osso penduradas
        cam.putpixel((x,50),OSSO[0]); cam.putpixel((x,51),OSSO[1]); cam.putpixel((x,52),mix(OSSO[1],0.75))
    if random.random()<0.5: cam.putpixel((x,47),mix(random.choice(PELO),0.8))      # franja irregular
# botas (pernas u=0,v=16) só embaixo
limpa(cam,0,32,32,32); box(cam,0,16,4,12,4,PELO); limpa(cam,0,40,32,14)
for x in range(0,32):
    for y in (54,55): cam.putpixel((x,y),random.choice(CLARO))
    cam.putpixel((x,58),random.choice(COURO)); cam.putpixel((x,59),random.choice(COURO))
for x in range(0,32): cam.putpixel((x,62),mix(cam.getpixel((x,62)),0.7)); cam.putpixel((x,63),mix(cam.getpixel((x,63)),0.6))
limpa(cam,0,0,64,32)                         # cabeça vazia: o capacete é 3D
cal=Image.new('RGBA',(64*S,32*S),(0,0,0,0))
box(cal,0,16,4,12,4,PELO)
for y in (42,43,50,51):
    for x in range(0,32): cal.putpixel((x,y),random.choice(COURO))
box(cal,16,16,8,12,4,PELO); limpa(cal,32,32,48,18)
for x in range(32,80):                        # cinto com fivela de ferro
    for y in (50,51,52): cal.putpixel((x,y),random.choice(COURO))
ret(cal,46,49,4,5,FERRO,1.1)
for d in ('humanoid','humanoid_leggings'): os.makedirs(f'{R}/{d}',exist_ok=True)
cam.save(f'{R}/humanoid/set_lobo.png'); cal.save(f'{R}/humanoid_leggings/set_lobo.png')
print('ok')

