# Pele de Lobo v2: modelos 3D (cabeça de lobo, cauda, ombreiras) e textura vestida em alta resolução.
import json, os, random, math
from PIL import Image
random.seed(11)
R='assets/big'
def cor(h,a=255):
    h=h.lstrip('#'); return (int(h[0:2],16),int(h[2:4],16),int(h[4:6],16),a)
def mix(c,f):  # escurece (f<1) ou clareia (f>1)
    return tuple(max(0,min(255,int(x*f))) for x in c[:3])+(c[3],)
PELO=[cor('4d453e'),cor('5d544b'),cor('6c6258'),cor('7b7065'),cor('8a7e72')]
CLARO=[cor('a69d92'),cor('b8aea2'),cor('c9c0b4')]
ESC=[cor('2e2823'),cor('3a332d')]
TONS={'pelo':PELO,'claro':CLARO,'escuro':ESC,'couro':[cor('5a3720'),cor('6b4327'),cor('7a4e2e')],
      'osso':[cor('e8e1d2'),cor('d6cdb9')],'nariz':[cor('1c1916'),cor('26211d')],'rosa':[cor('7d5a55'),cor('8c6560')],
      'olho':[cor('ffd23f')],'dente':[cor('f3efe4'),cor('e2dccb')],'ferro':[cor('8e9399'),cor('b4b9bf')]}

def pintar_face(img,x0,y0,w,h,tom,face):
    pal=TONS[tom]
    luz={'up':1.15,'down':0.7,'north':1.0,'south':0.85,'east':0.92,'west':0.92}[face]
    for x in range(w):
        i=random.randrange(len(pal))
        for y in range(h):
            if random.random()<0.18: i=max(0,min(len(pal)-1,i+random.choice((-1,1))))
            c=pal[i]
            grad=1.08-0.25*(y/max(1,h-1)) if face not in('up','down') else 1
            c=mix(c,luz*grad)
            if tom in('pelo','claro') and random.random()<0.12: c=mix(c,0.82)
            if tom in('pelo','claro') and random.random()<0.06: c=mix(c,1.15)
            img.putpixel((x0+x,y0+y),c)
    if tom in('pelo','claro') and w>2 and h>2:   # borda escura para dar volume
        for x in range(w):
            img.putpixel((x0+x,y0+h-1),mix(img.getpixel((x0+x,y0+h-1)),0.8))

class Modelo:
    def __init__(s,nome,tam=64):
        s.nome=nome; s.tam=tam; s.img=Image.new('RGBA',(tam,tam),(0,0,0,0)); s.el=[]; s.cx=0; s.cy=0; s.linha=0
    def cubo(s,nome,de,ate,tom,brilho=False,rot=None,tons_face=None):
        w,h,d=[max(1,math.ceil(ate[i]-de[i])) for i in range(3)]
        lw,lh=2*(d+w),d+h
        if s.cx+lw>s.tam: s.cx=0; s.cy+=s.linha; s.linha=0
        u,v=s.cx,s.cy; s.cx+=lw; s.linha=max(s.linha,lh)
        assert v+lh<=s.tam,(s.nome,nome)
        reg={'up':(u+d,v,w,d),'down':(u+d+w,v,w,d),'east':(u,v+d,d,h),'north':(u+d,v+d,w,h),
             'west':(u+d+w,v+d,d,h),'south':(u+2*d+w,v+d,w,h)}
        k=16/s.tam; faces={}
        for f,(x,y,ww,hh) in reg.items():
            pintar_face(s.img,x,y,ww,hh,(tons_face or {}).get(f,tom),f)
            faces[f]={'uv':[x*k,y*k,(x+ww)*k,(y+hh)*k],'texture':'#0'}
        e={'name':nome,'from':de,'to':ate,'faces':faces}
        if brilho: e['light_emission']=15
        if rot: e['rotation']=rot
        s.el.append(e); return reg
    def salvar(s,display,frames=None):
        tex=f'big:item/berserker/{s.nome}'
        m={'texture_size':[s.tam,s.tam],'textures':{'0':tex,'particle':tex},'elements':s.el,'display':display}
        os.makedirs(f'{R}/models/item/berserker',exist_ok=True); os.makedirs(f'{R}/textures/item/berserker',exist_ok=True)
        os.makedirs(f'{R}/items/berserker',exist_ok=True)
        json.dump(m,open(f'{R}/models/item/berserker/{s.nome}.json','w'),indent=1)
        json.dump({'model':{'type':'minecraft:model','model':f'big:item/berserker/{s.nome}'}},open(f'{R}/items/berserker/{s.nome}.json','w'),indent=1)
        img=s.img
        if frames:
            alt=Image.new('RGBA',(s.tam,s.tam*2),(0,0,0,0)); alt.paste(img,(0,0))
            fechado=img.copy()
            for (x,y,w,h) in frames: 
                for xx in range(x,x+w):
                    for yy in range(y,y+h): fechado.putpixel((xx,yy),cor('2a241f'))
            alt.paste(fechado,(0,s.tam)); img=alt
            json.dump({'animation':{'frametime':3,'frames':[0]*40+[1,0,1]+[0]*20+[1]}},open(f'{R}/textures/item/berserker/{s.nome}.png.mcmeta','w'))
        img.save(f'{R}/textures/item/berserker/{s.nome}.png')

# ---------------- cabeça de lobo (capacete 3D) ----------------
c=Modelo('lobo_cabeca',128)
c.cubo('cranio',[0,8,0],[16,16.5,16],'pelo')
c.cubo('lado_e',[-0.5,1,1],[2,8,16],'pelo')
c.cubo('lado_d',[14,1,1],[16.5,8,16],'pelo')
c.cubo('nuca',[0,0,13.5],[16,8,16.5],'pelo')
c.cubo('testa',[3,12.5,-1.5],[13,16,0],'pelo')
c.cubo('focinho',[4.5,9,-7],[11.5,13.5,0],'pelo',tons_face={'up':'pelo','down':'claro'})
c.cubo('ponte',[5.5,13.5,-5],[10.5,14.5,-1],'escuro')
c.cubo('nariz',[6.2,11.5,-8],[9.8,13.8,-6.8],'nariz')
c.cubo('mandibula',[5,7.6,-6],[11,9,-0.5],'claro')
for i,x in enumerate([5.2,6.6,9.0,10.4]):
    c.cubo(f'dente{i}',[x,7,-5.8 if i in(0,3) else -6.4],[x+0.8,8.2,-5.2 if i in(0,3) else -5.8],'dente')
olhoE=c.cubo('olho_e',[3.4,12.6,-1.7],[5.8,13.8,-1.4],'olho',brilho=True)
olhoD=c.cubo('olho_d',[10.2,12.6,-1.7],[12.6,13.8,-1.4],'olho',brilho=True)
c.cubo('sobrancelha_e',[3,13.9,-1.9],[6.4,14.7,-1.2],'escuro')
c.cubo('sobrancelha_d',[9.6,13.9,-1.9],[13,14.7,-1.2],'escuro')
for nome,x0,ang in (('e',0.3,22.5),('d',12.2,-22.5)):   # orelhas pontudas abertas para fora
    rot={'angle':ang,'axis':'z','origin':[x0+1.75,16.5,6]}
    c.cubo('orelha_base_'+nome,[x0,16.2,4.5],[x0+3.5,19.5,7.8],'pelo',rot=rot)
    c.cubo('orelha_meio_'+nome,[x0+0.5,19.5,5],[x0+3,22,7.3],'pelo',rot=rot)
    c.cubo('orelha_ponta_'+nome,[x0+1,22,5.5],[x0+2.5,24.5,6.8],'escuro',rot=rot)
    c.cubo('orelha_dentro_'+nome,[x0+0.75,16.6,4.2],[x0+2.75,21.5,4.5],'rosa',rot=rot)
c.cubo('juba',[-1,-1,9],[17,4,17.5],'claro')
# olhos fechando: as regiões das faces da frente dos olhos
fr=[olhoE['north'],olhoD['north']]
c.salvar({'head':{'rotation':[0,0,0],'translation':[0,0,0],'scale':[1.05,1.05,1.05]},
          'gui':{'rotation':[25,-145,0],'translation':[0,-1.5,0],'scale':[0.62,0.62,0.62]},
          'ground':{'translation':[0,2,0],'scale':[0.5,0.5,0.5]},
          'fixed':{'rotation':[0,180,0],'scale':[0.8,0.8,0.8]},
          'thirdperson_righthand':{'rotation':[75,180,0],'translation':[0,1,-2],'scale':[0.4,0.4,0.4]},
          'firstperson_righthand':{'rotation':[0,225,0],'scale':[0.4,0.4,0.4]}},frames=fr)

# ---------------- cauda (fica numa display entity atrás do jogador) ----------------
t=Modelo('lobo_cauda',64)
t.cubo('base',[6,6,4],[10,10,9],'pelo')
t.cubo('meio',[5.5,4.5,-2],[10.5,9.5,4.5],'pelo',rot={'angle':-22.5,'axis':'x','origin':[8,8,4]})
t.cubo('ponta',[6,2,-7],[10,7,-1.5],'pelo',rot={'angle':-22.5,'axis':'x','origin':[8,8,4]})
t.cubo('pontinha',[6.5,1.2,-9.5],[9.5,5,-6.5],'claro',rot={'angle':-22.5,'axis':'x','origin':[8,8,4]})
t.salvar({'gui':{'rotation':[30,135,0],'scale':[0.7,0.7,0.7]},'fixed':{'scale':[1,1,1]}})

# ---------------- ombreiras de pele com garras ----------------
for lado,s in (('esq',1),('dir',-1)):
    o=Modelo(f'lobo_ombreira_{lado}',64)
    o.cubo('pele',[3,6,3],[13,10,13],'pelo')
    o.cubo('topo',[4,10,4],[12,12,12],'claro')
    o.cubo('franja',[2.5,3.5,2.5],[13.5,6,13.5],'pelo')
    for i,z in enumerate([4,7.5,11]):
        x=13 if s==1 else 2
        o.cubo(f'garra{i}',[x-0.6,1.5,z],[x+0.6,4,z+1],'osso')
    o.cubo('tira',[7,5.5,1.8],[9,11,14.2],'couro')
    o.salvar({'gui':{'rotation':[30,135,0],'scale':[0.8,0.8,0.8]},'fixed':{'scale':[1,1,1]}})
print('modelos ok')
