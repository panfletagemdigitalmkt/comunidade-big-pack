# Modelos 3D ANIMADOS dos chefes e monstros da Masmorra da Mata Sombria.
# Cada monstro é dividido em "ossos" (cabeça, braços, pernas...). Cada osso vira um item 3D e o plugin
# junta tudo e toca as animações (parado, andar, ataque, grito) deste arquivo, quadro a quadro.
# Unidades: 16 = 1 bloco. O pé de todos fica em y = -16. A frente é -z.
import json, os, math, copy
from voxel import cor
import armadura as A

Modelo, TONS = A.carregar_modelo('dungeon')
TONS.update({
    'casca': [cor('3b2a1d'), cor('4a3524'), cor('2e2117'), cor('56402c')], 'casca_clara': [cor('6b5236'), cor('7a5f3f')],
    'musgo': [cor('3f6b2a'), cor('4f7d33'), cor('35592a')], 'folha': [cor('2f5e2b'), cor('3a6e34'), cor('284f25'), cor('4a7a2c')],
    'chama': [cor('ff3d00'), cor('ff6a00'), cor('ff9500'), cor('ffb000')], 'brasa': [cor('fff3b0'), cor('ffe680'), cor('ffd23f')],
    'olho_verde': [cor('b6ff3a'), cor('d9ff7a')], 'olho_vermelho': [cor('ff1a1a'), cor('ff4d4d')],
    'olho_ciano': [cor('5ff2ff'), cor('b8fbff')], 'olho_fogo': [cor('fffbe6'), cor('fff3b0')],
    'pele_escura': [cor('2a1a12'), cor('34211a'), cor('3d2a20')], 'vermelho': [cor('b3101a'), cor('c8141f'), cor('9a0d16')],
    'boca': [cor('120807'), cor('1c0d0b')], 'madeira': [cor('5a3a22'), cor('6b4428'), cor('4a2e1a')],
    'vento': [cor('dfe7ec'), cor('c9d3da'), cor('eef3f6')], 'pelo_negro': [cor('17120f'), cor('211a16'), cor('2b2320'), cor('120e0c')],
    'manto': [cor('2a1638'), cor('341b46'), cor('22112e'), cor('3d2152')], 'escama_verde': [cor('3d5a1e'), cor('4c6e25'), cor('324a19'), cor('5a7d2c')],
    'cabelo': [cor('d9b13a'), cor('e8c454'), cor('c49a2a')], 'escama_fogo': [cor('7a1c0a'), cor('9a2a0c'), cor('5c1407'), cor('b53a10')],
    'sombra': [cor('0a0a0d'), cor('121216'), cor('0e0e12'), cor('18181e')], 'fantasma': [cor('b9c6d3'), cor('a7b6c6'), cor('cbd6e0'), cor('95a5b6')],
    'roxo_marca': [cor('9b5cff'), cor('b98aff')], 'aranha': [cor('1e1a22'), cor('2a2430'), cor('16121a')],
    'basalto': [cor('2b2b30'), cor('3a3a40'), cor('222226')], 'ferro': [cor('6e7378'), cor('8a9096')],
})
R = 'assets/big'
PLUGIN = '../plugin/big-core/src/main/resources/modelos'
SEM = {'fixed': {'scale': [1, 1, 1]}, 'gui': {'rotation': [15, -150, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]}}


def onda(dur, ossos, n=8):
    """ossos: {osso: {'rot': (amp[x,y,z], fase, base[x,y,z]), 'pos': ...}} -> quadros de seno."""
    out = {}
    for o, canais in ossos.items():
        out[o] = {}
        for canal, (amp, fase, base) in canais.items():
            q = []
            for i in range(n + 1):
                t = dur * i / n
                s = math.sin(2 * math.pi * i / n + fase)
                q.append([round(t, 3), [round(base[k] + amp[k] * s, 2) for k in range(3)]])
            out[o][canal] = q
    return out


def quadros(ossos):
    return {o: {c: [[t, v] for t, v in q] for c, q in cs.items()} for o, cs in ossos.items()}


def junta(*partes):
    out = {}
    for p in partes:
        for o, cs in p.items():
            out.setdefault(o, {}).update(cs)
    return out


class Rig:
    def __init__(s, nome, tam=256):
        s.nome = nome
        s.m = Modelo(nome, tam)
        s.ossos = {}
        s.ordem = []
        s.atual = None
        s.anims = {}

    def osso(s, nome, pivo, pai=None):
        s.ossos[nome] = {'pivo': pivo, 'pai': pai, 'el': []}
        s.ordem.append(nome)
        s.atual = nome

    def cubo(s, *a, **k):
        n = len(s.m.el)
        s.m.cubo(*a, **k)
        s.ossos[s.atual]['el'].extend(s.m.el[n:])

    def anim(s, nome, dur, loop, ossos):
        s.anims[nome] = {'duracao': dur, 'loop': loop, 'ossos': ossos}

    def salvar(s):
        tex = f'big:item/dungeon/{s.nome}'
        os.makedirs(f'{R}/textures/item/dungeon', exist_ok=True)
        s.m.img.save(f'{R}/textures/item/dungeon/{s.nome}.png')
        for d in (f'{R}/models/item/dungeon/{s.nome}', f'{R}/items/dungeon/{s.nome}', PLUGIN):
            os.makedirs(d, exist_ok=True)
        for o in s.ordem:
            px, py, pz = s.ossos[o]['pivo']
            dx, dy, dz = 8 - px, 8 - py, 8 - pz
            els = []
            for e in s.ossos[o]['el']:
                e = copy.deepcopy(e)
                e['from'] = [e['from'][0] + dx, e['from'][1] + dy, e['from'][2] + dz]
                e['to'] = [e['to'][0] + dx, e['to'][1] + dy, e['to'][2] + dz]
                if 'rotation' in e:
                    og = e['rotation']['origin']
                    e['rotation']['origin'] = [og[0] + dx, og[1] + dy, og[2] + dz]
                for v in e['from'] + e['to']:
                    assert -16 <= v <= 32, (s.nome, o, e['name'], v)
                els.append(e)
            json.dump({'texture_size': [s.m.tam, s.m.tam], 'textures': {'0': tex, 'particle': tex}, 'elements': els, 'display': SEM},
                      open(f'{R}/models/item/dungeon/{s.nome}/{o}.json', 'w'))
            json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/dungeon/{s.nome}/{o}'}},
                      open(f'{R}/items/dungeon/{s.nome}/{o}.json', 'w'))
        rig = {'ossos': [{'nome': o, 'pivo': s.ossos[o]['pivo'], 'pai': s.ossos[o]['pai']} for o in s.ordem], 'animacoes': s.anims}
        json.dump(rig, open(f'{PLUGIN}/{s.nome}.json', 'w'), indent=1)
        print(s.nome, len(s.ordem), 'ossos', list(s.anims))


Z = [0, 0, 0]

# =============================================================== CURUPIRA
r = Rig('curupira')
r.osso('corpo', [8, -3, 8])
r.cubo('tanga', [1, -6, 4.5], [15, -1, 11.5], 'folha')
r.cubo('tanga_tiras', [1.5, -9, 5], [14.5, -6, 11], 'folha')
r.cubo('tronco', [2.5, -3, 5], [13.5, 8, 11], 'casca')
for i, y in enumerate((0, 2, 4)):
    r.cubo(f'costela{i}', [3, y, 4.6], [13, y + 0.7, 5], 'casca_clara')
r.cubo('musgo_ombro', [1.5, 6, 4.5], [14.5, 8.6, 11.5], 'musgo')
r.osso('cabeca', [8, 8, 8], 'corpo')
r.cubo('cabeca', [3, 8, 4], [13, 17, 12], 'casca')
r.cubo('queixo', [4, 6.5, 3.4], [12, 9, 8], 'casca')
r.cubo('boca', [4.5, 8.4, 3.2], [11.5, 10.2, 3.6], 'boca')
for i, x in enumerate((4.8, 6.2, 7.6, 9.0, 10.4)):
    r.cubo(f'dente{i}', [x, 9.4, 3.0], [x + 0.8, 10.6, 3.3], 'dente')
r.cubo('sobrancelha', [3.5, 13.8, 3.6], [12.5, 15, 4.2], 'casca_clara')
r.cubo('olho_e', [4.5, 12, 3.7], [7, 13.6, 4], 'olho_verde', brilho=True)
r.cubo('olho_d', [9, 12, 3.7], [11.5, 13.6, 4], 'olho_verde', brilho=True)
r.cubo('nariz', [7.2, 10.5, 2.8], [8.8, 12.6, 4], 'casca_clara')
r.cubo('fogo_base', [2, 16.5, 3.5], [14, 20, 12.5], 'chama', brilho=True)
r.cubo('fogo_e', [1, 18, 5], [6, 25, 10], 'chama', brilho=True, rot={'angle': 22.5, 'axis': 'z', 'origin': [4, 18, 8]})
r.cubo('fogo_d', [10, 18, 5], [15, 26, 10], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'z', 'origin': [12, 18, 8]})
r.cubo('fogo_meio', [5, 19, 6], [11, 29, 11], 'chama', brilho=True)
r.cubo('fogo_ponta', [6.5, 28, 7], [9.5, 32, 10], 'brasa', brilho=True)
r.cubo('fogo_tras', [4, 14, 11.5], [12, 22, 15], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 14, 12]})
for lado, x0, ang, piv in (('e', -2, -22.5, 0), ('d', 14, 22.5, 16)):
    r.osso('braco_' + lado, [piv, 7, 7.5], 'corpo')
    rot = {'angle': ang, 'axis': 'z', 'origin': [x0 + 2, 7, 7.5]}
    r.cubo('braco_' + lado, [x0, -6, 6], [x0 + 3.5, 7, 9], 'casca', rot=rot)
    r.cubo('mao_' + lado, [x0 - 0.5, -9.5, 5.5], [x0 + 4, -6, 9.5], 'casca', rot=rot)
    for i in range(3):
        r.cubo(f'garra_{lado}{i}', [x0 - 0.3 + i * 1.5, -12.5, 6 + i * 0.6], [x0 + 0.7 + i * 1.5, -9.5, 7 + i * 0.6], 'dente', rot=rot)
    if lado == 'd':
        r.cubo('tacape', [16.5, -14, 2], [19.5, 3, 5.5], 'madeira', rot={'angle': 22.5, 'axis': 'x', 'origin': [18, -6, 4]})
        r.cubo('tacape_ponta', [15.5, -16, 0.5], [20.5, -10, 7], 'madeira', rot={'angle': 22.5, 'axis': 'x', 'origin': [18, -6, 4]})
for lado, x0 in (('e', 2), ('d', 11)):
    r.osso('perna_' + lado, [x0 + 1.5, -3, 7.75])
    r.cubo('perna_' + lado, [x0, -14, 6], [x0 + 3, -3, 9.5], 'casca')
    r.cubo('pe_' + lado, [x0 - 0.5, -16, 7], [x0 + 3.5, -14, 14], 'casca')
    for i in range(3):
        r.cubo(f'garra_pe_{lado}{i}', [x0 - 0.3 + i * 1.3, -16, 14], [x0 + 0.6 + i * 1.3, -15, 15.6], 'dente')
r.anim('parado', 2.0, True, onda(2.0, {'corpo': {'pos': ([0, 0.3, 0], 0, Z)}, 'cabeca': {'rot': ([4, 6, 0], 1, Z)},
                                       'braco_e': {'rot': ([3, 0, 4], 0, Z)}, 'braco_d': {'rot': ([3, 0, -4], 0, Z)}}))
r.anim('andar', 0.8, True, junta(onda(0.8, {'perna_e': {'rot': ([32, 0, 0], 0, Z)}, 'perna_d': {'rot': ([32, 0, 0], math.pi, Z)},
                                            'braco_e': {'rot': ([28, 0, 0], math.pi, Z)}, 'braco_d': {'rot': ([28, 0, 0], 0, Z)},
                                            'cabeca': {'rot': ([0, 6, 0], 0, Z)}}),
                                 onda(0.4, {'corpo': {'pos': ([0, 0.6, 0], 0, [0, 0.6, 0])}})))
r.anim('ataque', 0.55, False, quadros({'braco_d': {'rot': [(0, Z), (0.2, [165, 0, 10]), (0.35, [40, 0, 0]), (0.55, Z)]},
                                       'braco_e': {'rot': [(0, Z), (0.2, [-30, 0, -20]), (0.55, Z)]},
                                       'corpo': {'rot': [(0, Z), (0.2, [8, 0, 0]), (0.35, [-12, 0, 0]), (0.55, Z)]},
                                       'cabeca': {'rot': [(0, Z), (0.35, [12, 0, 0]), (0.55, Z)]}}))
r.anim('grito', 1.0, False, quadros({'cabeca': {'rot': [(0, Z), (0.3, [-28, 0, 0]), (0.8, [-28, 0, 0]), (1.0, Z)]},
                                     'braco_e': {'rot': [(0, Z), (0.3, [20, 0, -55]), (0.8, [20, 0, -55]), (1.0, Z)]},
                                     'braco_d': {'rot': [(0, Z), (0.3, [20, 0, 55]), (0.8, [20, 0, 55]), (1.0, Z)]}}))
r.salvar()

# =============================================================== SACI
r = Rig('saci')
r.osso('redemoinho', [8, -14, 9])
r.cubo('redemoinho1', [3, -16, 4], [13, -14.5, 14], 'vento')
r.cubo('redemoinho2', [1, -14.5, 2], [15, -13, 16], 'vento', rot={'angle': 45, 'axis': 'y', 'origin': [8, -14, 9]})
r.cubo('redemoinho3', [4.5, -13, 5.5], [11.5, -11.5, 12.5], 'vento')
r.osso('corpo', [8, -8, 8.5])
r.cubo('pe', [5.5, -12, 6], [10.5, -10, 11.5], 'pele_escura')
r.cubo('perna', [6, -10, 7], [10, 3, 10], 'pele_escura')
r.cubo('calcao', [3.5, 1, 5], [12.5, 6, 11], 'vermelho')
r.cubo('tronco', [4, 6, 5.5], [12, 15, 10.5], 'pele_escura')
r.osso('cabeca', [8, 15, 8], 'corpo')
r.cubo('cabeca', [3.5, 15, 4], [12.5, 23, 12], 'pele_escura')
r.cubo('sorriso', [4.5, 16.4, 3.7], [11.5, 18.2, 4], 'boca')
for i, x in enumerate((4.8, 6.0, 7.2, 8.4, 9.6, 10.6)):
    r.cubo(f'dente{i}', [x, 17.4, 3.5], [x + 0.6, 18.2, 3.8], 'dente')
r.cubo('olho_e', [4.6, 19.5, 3.7], [6.8, 20.8, 4], 'olho_vermelho', brilho=True)
r.cubo('olho_d', [9.2, 19.5, 3.7], [11.4, 20.8, 4], 'olho_vermelho', brilho=True)
r.cubo('orelha_e', [2.5, 18, 7], [3.5, 21, 9], 'pele_escura')
r.cubo('orelha_d', [12.5, 18, 7], [13.5, 21, 9], 'pele_escura')
r.cubo('gorro', [3, 22, 3.5], [13, 25, 12.5], 'vermelho')
r.cubo('gorro2', [4.5, 25, 5], [11.5, 28, 11], 'vermelho', rot={'angle': -22.5, 'axis': 'z', 'origin': [8, 25, 8]})
r.cubo('gorro_ponta', [7, 27, 6.5], [11, 31, 9.5], 'vermelho', rot={'angle': -45, 'axis': 'z', 'origin': [9, 27, 8]})
r.cubo('cachimbo', [10.5, 16.6, 0.5], [11.5, 17.4, 4], 'madeira')
r.cubo('fornilho', [10.2, 17.4, -0.6], [12.8, 20.4, 1.6], 'madeira')
r.cubo('brasa', [10.5, 20, -0.3], [12.5, 20.8, 1.3], 'brasa', brilho=True)
for lado, x0, ang, piv in (('e', 1.5, -22.5, 2.75), ('d', 12, 22.5, 13.25)):
    r.osso('braco_' + lado, [piv, 14, 8], 'corpo')
    rot = {'angle': ang, 'axis': 'z', 'origin': [x0 + 1.2, 14, 8]}
    r.cubo('braco_' + lado, [x0, 4, 7], [x0 + 2.5, 15, 9], 'pele_escura', rot=rot)
    r.cubo('dedos_' + lado, [x0 - 0.3, 1.5, 6.6], [x0 + 2.8, 4, 9.4], 'pele_escura', rot=rot)
giro = lambda d: quadros({'redemoinho': {'rot': [(0, Z), (d / 2, [0, 180, 0]), (d, [0, 360, 0])]}})
r.anim('parado', 1.8, True, junta(onda(1.8, {'corpo': {'pos': ([0, 0.6, 0], 0, Z)}, 'cabeca': {'rot': ([0, 8, 7], 0, Z)},
                                             'braco_e': {'rot': ([10, 0, 5], 0, Z)}, 'braco_d': {'rot': ([10, 0, -5], math.pi, Z)}}),
                                  quadros({'redemoinho': {'rot': [(0, Z), (0.45, [0, 90, 0]), (0.9, [0, 180, 0]), (1.35, [0, 270, 0]), (1.8, [0, 360, 0])]}})))
r.anim('andar', 0.5, True, junta(quadros({'corpo': {'pos': [(0, Z), (0.25, [0, 3, 0]), (0.5, Z)], 'rot': [(0, Z), (0.25, [-10, 0, 0]), (0.5, Z)]}}),
                                 onda(0.5, {'braco_e': {'rot': ([25, 0, 0], 0, [0, 0, -15])}, 'braco_d': {'rot': ([25, 0, 0], math.pi, [0, 0, 15])}}),
                                 quadros({'redemoinho': {'rot': [(0, Z), (0.25, [0, 180, 0]), (0.5, [0, 360, 0])]}})))
r.anim('ataque', 0.45, False, quadros({'braco_d': {'rot': [(0, Z), (0.15, [130, 0, 0]), (0.3, [20, 0, 0]), (0.45, Z)]},
                                       'cabeca': {'rot': [(0, Z), (0.2, [-12, 0, 10]), (0.45, Z)]}}))
r.anim('grito', 1.0, False, quadros({'cabeca': {'rot': [(0, Z), (0.2, [-20, 0, 15]), (0.5, [-20, 0, -15]), (0.8, [-20, 0, 15]), (1.0, Z)]},
                                     'corpo': {'pos': [(0, Z), (0.25, [0, 4, 0]), (0.5, Z), (0.75, [0, 4, 0]), (1.0, Z)]}}))
r.salvar()

# =============================================================== MULA SEM CABEÇA
r = Rig('mula')
r.osso('corpo', [8, 2, 10])
r.cubo('corpo', [1, -4, -4], [15, 8, 24], 'pelo_negro')
r.cubo('anca', [0.5, -2, 16], [15.5, 9, 24.5], 'pelo_negro')
for i, z in enumerate((2, 7, 12, 17)):
    r.cubo(f'costela_e{i}', [0.6, -1, z], [0.9, 6, z + 1.2], 'dente')
    r.cubo(f'costela_d{i}', [15.1, -1, z], [15.4, 6, z + 1.2], 'dente')
r.cubo('arreio', [0.4, 2, 5], [15.6, 3.2, 6.2], 'ferro')
r.cubo('corrente', [7, -6, 5], [9, 2.4, 6], 'ferro')
r.cubo('crina_fogo', [6, 8, -6], [10, 13, 6], 'chama', brilho=True)
r.osso('pescoco', [8, 8, -4], 'corpo')
r.cubo('pescoco', [3.5, 3, -11], [12.5, 12, -3], 'pelo_negro', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 6, -4]})
r.cubo('toco', [4, 9, -15], [12, 12, -9], 'brasa', brilho=True, rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 6, -4]})
r.cubo('fogo1', [2.5, 11, -16], [13.5, 18, -7], 'chama', brilho=True)
r.cubo('fogo2', [4.5, 17, -15], [11.5, 25, -8], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 17, -11]})
r.cubo('fogo3', [6, 24, -14], [10, 31, -10], 'brasa', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 24, -12]})
r.osso('cauda', [8, 6, 24], 'corpo')
r.cubo('cauda_fogo', [6, 0, 24], [10, 8, 31], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 6, 24]})
for i, (x, z) in enumerate(((2, -2), (10, -2), (2, 18), (10, 18))):
    r.osso(f'perna{i}', [x + 2, -3, z + 2])
    r.cubo(f'perna{i}', [x, -14, z], [x + 4, -3, z + 4], 'pelo_negro')
    r.cubo(f'casco{i}', [x - 0.5, -16, z - 0.5], [x + 4.5, -14, z + 4.5], 'brasa', brilho=True)
r.anim('parado', 1.6, True, onda(1.6, {'pescoco': {'rot': ([5, 0, 0], 0, Z)}, 'cauda': {'rot': ([0, 14, 0], 0, Z)},
                                       'corpo': {'pos': ([0, 0.3, 0], 0, Z)}, 'perna0': {'rot': ([3, 0, 0], 0, Z)}}))
r.anim('andar', 0.6, True, junta(onda(0.6, {'perna0': {'rot': ([38, 0, 0], 0, Z)}, 'perna3': {'rot': ([38, 0, 0], 0, Z)},
                                            'perna1': {'rot': ([38, 0, 0], math.pi, Z)}, 'perna2': {'rot': ([38, 0, 0], math.pi, Z)},
                                            'pescoco': {'rot': ([8, 0, 0], 1, Z)}, 'cauda': {'rot': ([12, 10, 0], 0, Z)}}),
                                 onda(0.3, {'corpo': {'pos': ([0, 0.8, 0], 0, [0, 0.8, 0]), 'rot': ([3, 0, 0], 0.5, Z)}})))
r.anim('ataque', 0.8, False, quadros({'corpo': {'rot': [(0, Z), (0.3, [28, 0, 0]), (0.5, [28, 0, 0]), (0.65, [-6, 0, 0]), (0.8, Z)],
                                                'pos': [(0, Z), (0.3, [0, 3, 0]), (0.65, Z)]},
                                      'perna0': {'rot': [(0, Z), (0.3, [60, 0, 0]), (0.4, [20, 0, 0]), (0.5, [60, 0, 0]), (0.8, Z)]},
                                      'perna1': {'rot': [(0, Z), (0.3, [20, 0, 0]), (0.4, [60, 0, 0]), (0.5, [20, 0, 0]), (0.8, Z)]},
                                      'perna2': {'rot': [(0, Z), (0.3, [-28, 0, 0]), (0.65, Z)]}, 'perna3': {'rot': [(0, Z), (0.3, [-28, 0, 0]), (0.65, Z)]}}))
r.anim('grito', 1.0, False, quadros({'pescoco': {'rot': [(0, Z), (0.3, [-30, 0, 0]), (0.8, [-30, 0, 0]), (1.0, Z)]},
                                     'corpo': {'rot': [(0, Z), (0.3, [15, 0, 0]), (0.8, [15, 0, 0]), (1.0, Z)]}}))
r.salvar()

# =============================================================== CUCA
r = Rig('cuca')
r.osso('corpo', [8, -8, 9])
r.cubo('manto_baixo', [0, -16, 2], [16, -2, 16], 'manto')
r.cubo('barra', [-0.5, -16, 1.5], [16.5, -14, 16.5], 'sombra')
r.cubo('manto_meio', [1, -2, 3], [15, 8, 15], 'manto')
r.cubo('corcunda', [1.5, 6, 6], [14.5, 13, 16], 'manto')
r.cubo('ombros', [-0.5, 7, 2], [16.5, 11, 13], 'manto')
r.cubo('cabelo_costas', [1, -4, 11], [15, 14, 16.5], 'cabelo')
r.osso('cabeca', [8, 11, 6], 'corpo')
r.cubo('cabelo_topo', [2, 17, 1], [14, 20.5, 13], 'cabelo')
r.cubo('cabelo_lado_e', [0.5, 6, 1], [2.5, 19, 12], 'cabelo')
r.cubo('cabelo_lado_d', [13.5, 6, 1], [15.5, 19, 12], 'cabelo')
r.cubo('cranio', [2.5, 10, 0], [13.5, 18, 11], 'escama_verde')
r.cubo('focinho', [4, 10.5, -14], [12, 15.5, 0.5], 'escama_verde')
r.cubo('boca', [4.6, 10, -12.5], [11.4, 10.6, 0], 'boca')
for i, z in enumerate(range(-12, 0, 2)):
    r.cubo(f'dente_e{i}', [4.3, 9, z], [4.9, 10.8, z + 0.8], 'dente')
    r.cubo(f'dente_d{i}', [11.1, 9, z], [11.7, 10.8, z + 0.8], 'dente')
r.cubo('narinas', [6.5, 15.5, -13.5], [9.5, 16.2, -11.5], 'boca')
r.cubo('olho_e', [3.2, 15.8, -2], [6.2, 18.6, 1], 'escama_verde')
r.cubo('olho_d', [9.8, 15.8, -2], [12.8, 18.6, 1], 'escama_verde')
r.cubo('pupila_e', [3.6, 16.4, -2.3], [5.8, 18, -2], 'olho', brilho=True)
r.cubo('pupila_d', [10.2, 16.4, -2.3], [12.4, 18, -2], 'olho', brilho=True)
for i, z in enumerate((-8, -4, 2, 6)):
    r.cubo(f'escama_topo{i}', [7, 15.5 if z < 0 else 18, z], [9, 17 if z < 0 else 19.5, z + 2], 'escama_verde')
r.osso('mandibula', [8, 10, 0], 'cabeca')
r.cubo('mandibula', [4.5, 7.5, -13], [11.5, 10.5, 0.5], 'escama_verde')
for i, z in enumerate(range(-11, 0, 3)):
    r.cubo(f'dente_baixo{i}', [5, 10.5, z], [5.6, 11.6, z + 0.8], 'dente')
    r.cubo(f'dente_baixo_d{i}', [10.4, 10.5, z], [11, 11.6, z + 0.8], 'dente')
for lado, x0, piv in (('e', -4, -2), ('d', 16, 18)):
    r.osso('braco_' + lado, [piv, 10, 5.5], 'corpo')
    r.cubo('braco_' + lado, [x0, -3, 3], [x0 + 4, 10, 8], 'manto')
    r.cubo('mao_' + lado, [x0 - 0.5, -7, 2], [x0 + 4.5, -3, 8], 'escama_verde')
    for i in range(4):
        r.cubo(f'unha_{lado}{i}', [x0 - 0.3 + i * 1.2, -10, 2.5], [x0 + 0.5 + i * 1.2, -7, 3.5], 'dente')
r.anim('parado', 2.4, True, junta(onda(2.4, {'corpo': {'rot': ([0, 0, 3], 0, Z)}, 'cabeca': {'rot': ([3, 14, 0], 0.7, Z)},
                                             'braco_e': {'rot': ([8, 0, 4], 0, Z)}, 'braco_d': {'rot': ([8, 0, -4], math.pi, Z)}}),
                                  quadros({'mandibula': {'rot': [(0, Z), (0.6, [-10, 0, 0]), (0.9, Z), (2.4, Z)]}})))
r.anim('andar', 1.2, True, onda(1.2, {'corpo': {'rot': ([0, 0, 6], 0, [6, 0, 0])}, 'cabeca': {'rot': ([5, 0, 0], 1, Z)},
                                      'braco_e': {'rot': ([22, 0, 0], math.pi, Z)}, 'braco_d': {'rot': ([22, 0, 0], 0, Z)},
                                      'mandibula': {'rot': ([6, 0, 0], 0, [-6, 0, 0])}}))
r.anim('ataque', 0.6, False, quadros({'mandibula': {'rot': [(0, Z), (0.15, [-35, 0, 0]), (0.3, [5, 0, 0]), (0.6, Z)]},
                                      'cabeca': {'rot': [(0, Z), (0.15, [-12, 0, 0]), (0.3, [14, 0, 0]), (0.6, Z)]},
                                      'braco_e': {'rot': [(0, Z), (0.2, [110, 0, 25]), (0.35, [40, 0, 0]), (0.6, Z)]},
                                      'braco_d': {'rot': [(0, Z), (0.2, [110, 0, -25]), (0.35, [40, 0, 0]), (0.6, Z)]}}))
r.anim('grito', 1.2, False, quadros({'cabeca': {'rot': [(0, Z), (0.3, [-35, 0, 0]), (1.0, [-35, 0, 0]), (1.2, Z)]},
                                     'mandibula': {'rot': [(0, Z), (0.3, [-40, 0, 0]), (1.0, [-40, 0, 0]), (1.2, Z)]},
                                     'braco_e': {'rot': [(0, Z), (0.3, [60, 0, -50]), (1.0, [60, 0, -50]), (1.2, Z)]},
                                     'braco_d': {'rot': [(0, Z), (0.3, [60, 0, 50]), (1.0, [60, 0, 50]), (1.2, Z)]}}))
r.salvar()

# =============================================================== BOITATÁ (cabeça; o corpo são gomos separados)
r = Rig('boitata')
r.osso('cabeca', [8, 4, 8])
r.cubo('cranio', [0, -2, -2], [16, 10, 16], 'escama_fogo')
r.cubo('focinho', [2, 1, -15], [14, 8, -2], 'escama_fogo')
r.cubo('garganta', [3.5, -2, -13], [12.5, 1, -3], 'brasa', brilho=True)
for x in (2.8, 11.6):
    r.cubo(f'presa_cima{x}', [x, -3, -14.6], [x + 1.6, 1.2, -13], 'dente')
r.cubo('olho_e', [-0.4, 5, -5.5], [3.6, 8, -0.5], 'chama', brilho=True)
r.cubo('olho_d', [12.4, 5, -5.5], [16.4, 8, -0.5], 'chama', brilho=True)
r.cubo('pupila_e', [-0.7, 5.2, -3.4], [-0.4, 7.8, -2.6], 'boca')
r.cubo('pupila_d', [16.4, 5.2, -3.4], [16.7, 7.8, -2.6], 'boca')
r.cubo('sobrancelha_e', [-1, 8, -7], [5, 10.5, 0], 'escama_fogo', rot={'angle': -22.5, 'axis': 'z', 'origin': [2, 9, -3]})
r.cubo('sobrancelha_d', [11, 8, -7], [17, 10.5, 0], 'escama_fogo', rot={'angle': 22.5, 'axis': 'z', 'origin': [14, 9, -3]})
r.cubo('narina', [5, 8, -15.3], [11, 9, -14.6], 'brasa', brilho=True)
for i, z in enumerate((-10, -4, 2, 8, 14)):
    r.cubo(f'crista{i}', [5.5, 10, z], [10.5, 14 + (2 if i in (1, 2) else 0), z + 3], 'chama', brilho=True)
r.cubo('chifre_e', [-1, 8, 6], [2, 16, 9], 'escama_fogo', rot={'angle': -22.5, 'axis': 'z', 'origin': [1, 8, 8]})
r.cubo('chifre_d', [14, 8, 6], [17, 16, 9], 'escama_fogo', rot={'angle': 22.5, 'axis': 'z', 'origin': [15, 8, 8]})
r.cubo('pescoco', [2, -4, 15], [14, 8, 24], 'escama_fogo')
r.cubo('pescoco_fogo', [5, 8, 15], [11, 12, 24], 'chama', brilho=True)
r.osso('mandibula', [8, -1, -2], 'cabeca')
r.cubo('mandibula', [2.5, -6, -14], [13.5, -1, -2], 'escama_fogo')
for x in (2.8, 11.6):
    r.cubo(f'presa_baixo{x}', [x + 0.4, -1, -13], [x + 1.6, 2, -12], 'dente')
r.anim('parado', 1.6, True, junta(onda(1.6, {'cabeca': {'rot': ([5, 0, 5], 0, Z)}}), onda(1.6, {'mandibula': {'rot': ([8, 0, 0], 0, [12, 0, 0])}})))
r.anim('andar', 1.0, True, junta(onda(1.0, {'cabeca': {'rot': ([7, 8, 4], 0, Z)}}), onda(1.0, {'mandibula': {'rot': ([10, 0, 0], 0, [14, 0, 0])}})))
r.anim('ataque', 0.6, False, quadros({'mandibula': {'rot': [(0, Z), (0.2, [45, 0, 0]), (0.35, Z), (0.6, [10, 0, 0])]},
                                      'cabeca': {'rot': [(0, Z), (0.2, [-14, 0, 0]), (0.35, [12, 0, 0]), (0.6, Z)]}}))
r.anim('grito', 1.2, False, quadros({'mandibula': {'rot': [(0, Z), (0.3, [50, 0, 0]), (1.0, [50, 0, 0]), (1.2, Z)]},
                                     'cabeca': {'rot': [(0, Z), (0.3, [-25, 0, 0]), (0.6, [-25, 10, 0]), (1.0, [-25, -10, 0]), (1.2, Z)]}}))
r.salvar()

# =============================================================== monstros dos corredores
r = Rig('espirito_mata')
r.osso('raizes', [8, -14, 8])
r.cubo('raizes', [1, -16, 2], [15, -12, 14], 'casca')
for i, (x, z) in enumerate(((0, 6), (14, 6), (6, 0), (6, 14))):
    r.cubo(f'raiz{i}', [x - 1, -16, z - 1], [x + 3, -14, z + 3], 'casca')
r.osso('corpo', [8, -12, 8])
r.cubo('tronco', [3, -12, 4], [13, 10, 12], 'casca')
r.cubo('rosto', [3.5, 0, 3.6], [12.5, 9, 4], 'boca')
r.cubo('olho_e', [4.5, 6, 3.4], [7, 7, 3.7], 'olho_verde', brilho=True, rot={'angle': -22.5, 'axis': 'z', 'origin': [6, 6.5, 3.5]})
r.cubo('olho_d', [9, 6, 3.4], [11.5, 7, 3.7], 'olho_verde', brilho=True, rot={'angle': 22.5, 'axis': 'z', 'origin': [10, 6.5, 3.5]})
for i, x in enumerate((4.5, 6.3, 8.1, 9.9)):
    r.cubo(f'boca_galho{i}', [x, 1 + (i % 2), 3.3], [x + 1.4, 4.5 - (i % 2), 3.6], 'olho_verde', brilho=True)
r.cubo('musgo', [2.5, 8, 3.5], [13.5, 11, 12.5], 'musgo')
r.osso('copa', [8, 10, 8], 'corpo')
r.cubo('copa', [-1, 10, 0], [17, 18, 16], 'folha')
r.cubo('copa2', [2, 18, 3], [14, 22, 13], 'folha')
for lado, x0, ang, piv in (('e', -4, 22.5, -0.5), ('d', 13, -22.5, 16.5)):
    r.osso('galho_' + lado, [piv, 5, 8], 'corpo')
    r.cubo('galho_' + lado, [x0, 4, 6.5], [x0 + 7, 6, 9.5], 'casca', rot={'angle': ang, 'axis': 'z', 'origin': [x0 + 3.5, 5, 8]})
    r.cubo('garra_' + lado, [x0 - 1, -3, 6], [x0 + 2, 4, 10], 'casca')
r.anim('parado', 2.4, True, onda(2.4, {'copa': {'rot': ([0, 0, 4], 0, Z)}, 'galho_e': {'rot': ([5, 0, 6], 0, Z)}, 'galho_d': {'rot': ([5, 0, -6], 1, Z)}}))
r.anim('andar', 1.2, True, onda(1.2, {'corpo': {'rot': ([0, 0, 7], 0, Z)}, 'raizes': {'rot': ([0, 10, 0], 0, Z)}, 'copa': {'rot': ([0, 0, 5], 1, Z)},
                                      'galho_e': {'rot': ([25, 0, 0], 0, Z)}, 'galho_d': {'rot': ([25, 0, 0], math.pi, Z)}}))
r.anim('ataque', 0.6, False, quadros({'galho_e': {'rot': [(0, Z), (0.25, [120, 0, 0]), (0.4, [30, 0, 0]), (0.6, Z)]},
                                      'galho_d': {'rot': [(0, Z), (0.25, [120, 0, 0]), (0.4, [30, 0, 0]), (0.6, Z)]},
                                      'corpo': {'rot': [(0, Z), (0.25, [6, 0, 0]), (0.4, [-10, 0, 0]), (0.6, Z)]}}))
r.salvar()

r = Rig('vulto', 128)
r.osso('corpo', [8, -16, 8])
r.cubo('manto', [2, -16, 4], [14, 8, 12], 'sombra')
r.cubo('farrapos', [1, -16, 3], [15, -10, 13], 'sombra')
r.osso('capuz', [8, 8, 8], 'corpo')
r.cubo('capuz', [2.5, 8, 3.5], [13.5, 18, 12.5], 'sombra')
r.cubo('rosto', [4, 9.5, 3.2], [12, 15.5, 3.6], 'boca')
r.cubo('olho_e', [5, 12.5, 3], [7, 13.5, 3.3], 'olho_fogo', brilho=True)
r.cubo('olho_d', [9, 12.5, 3], [11, 13.5, 3.3], 'olho_fogo', brilho=True)
for lado, x0, piv in (('e', -1.5, 0.25), ('d', 14, 15.75)):
    r.osso('braco_' + lado, [piv, 7, 7.5], 'corpo')
    r.cubo('braco_' + lado, [x0, -12, 6], [x0 + 3.5, 7, 9], 'sombra')
    r.cubo('dedos_' + lado, [x0, -16, 6.2], [x0 + 3.5, -12, 8.8], 'aranha')
r.anim('parado', 2.0, True, onda(2.0, {'corpo': {'pos': ([0, 0.7, 0], 0, [0, 0.7, 0]), 'rot': ([0, 0, 2], 1, Z)}, 'capuz': {'rot': ([0, 18, 0], 0, Z)},
                                       'braco_e': {'rot': ([6, 0, 3], 0, Z)}, 'braco_d': {'rot': ([6, 0, -3], 1, Z)}}))
r.anim('andar', 1.4, True, onda(1.4, {'corpo': {'rot': ([0, 0, 3], 0, [-10, 0, 0]), 'pos': ([0, 0.5, 0], 0, [0, 0.8, 0])},
                                      'braco_e': {'rot': ([15, 0, 0], 0, [10, 0, 0])}, 'braco_d': {'rot': ([15, 0, 0], math.pi, [10, 0, 0])}}))
r.anim('ataque', 0.55, False, quadros({'braco_e': {'rot': [(0, Z), (0.2, [130, 0, -15]), (0.35, [60, 0, 0]), (0.55, Z)]},
                                       'braco_d': {'rot': [(0, Z), (0.2, [130, 0, 15]), (0.35, [60, 0, 0]), (0.55, Z)]},
                                       'capuz': {'rot': [(0, Z), (0.2, [-15, 0, 0]), (0.35, [12, 0, 0]), (0.55, Z)]}}))
r.salvar()

r = Rig('alma_cemiterio', 128)
r.osso('corpo', [8, -14, 8])
r.cubo('vestes', [3, -14, 4], [13, 6, 12], 'fantasma')
r.cubo('cauda', [5, -16, 6], [11, -14, 10], 'fantasma')
r.cubo('ombros', [2, 4, 3.5], [14, 7, 12.5], 'fantasma')
r.osso('cabeca', [8, 7, 8], 'corpo')
r.cubo('cranio', [4, 7, 4], [12, 15, 12], 'dente')
r.cubo('orbita_e', [4.8, 10, 3.7], [7.2, 12.4, 4], 'boca')
r.cubo('orbita_d', [8.8, 10, 3.7], [11.2, 12.4, 4], 'boca')
r.cubo('brilho_e', [5.4, 10.6, 3.5], [6.6, 11.6, 3.7], 'olho_ciano', brilho=True)
r.cubo('brilho_d', [9.4, 10.6, 3.5], [10.6, 11.6, 3.7], 'olho_ciano', brilho=True)
r.cubo('dentes', [5.5, 7.4, 3.6], [10.5, 8.6, 3.9], 'boca')
r.osso('braco', [14.25, 6, 7.5], 'corpo')
r.cubo('braco', [13, -4, 6], [15.5, 6, 9], 'fantasma')
r.cubo('lanterna', [13, -9, 5.5], [16.5, -4, 9.5], 'ferro')
r.cubo('chama_alma', [13.6, -8.4, 5.2], [15.9, -4.6, 5.5], 'olho_ciano', brilho=True)
r.anim('parado', 2.0, True, onda(2.0, {'corpo': {'pos': ([0, 1, 0], 0, [0, 1, 0]), 'rot': ([0, 0, 3], 1, Z)}, 'cabeca': {'rot': ([0, 0, 9], 0.5, Z)},
                                       'braco': {'rot': ([10, 0, 0], 0, Z)}}))
r.anim('andar', 1.2, True, onda(1.2, {'corpo': {'pos': ([0, 0.8, 0], 0, [0, 1, 0]), 'rot': ([0, 0, 3], 0, [-12, 0, 0])},
                                      'braco': {'rot': ([14, 0, 0], 0, Z)}, 'cabeca': {'rot': ([5, 0, 0], 1, [6, 0, 0])}}))
r.anim('ataque', 0.5, False, quadros({'braco': {'rot': [(0, Z), (0.2, [100, 0, 0]), (0.5, Z)]}, 'cabeca': {'rot': [(0, Z), (0.2, [-14, 0, 0]), (0.5, Z)]}}))
r.salvar()

r = Rig('aranha_cuca', 128)
r.osso('corpo', [8, -9, 4])
r.cubo('cefalo', [4, -12, -2], [12, -6, 6], 'aranha')
r.cubo('abdomen', [2, -13, 6], [14, -3, 18], 'aranha')
r.cubo('marca', [5, -3.2, 9], [11, -2.9, 15], 'roxo_marca', brilho=True)
for i, x in enumerate((5, 6.6, 8.6, 10.2)):
    r.cubo(f'olho{i}', [x, -9, -2.3], [x + 1.2, -7.8, -2], 'olho_vermelho', brilho=True)
r.cubo('quelicera', [6, -13, -3], [10, -11, -1.5], 'dente')
pernas = []
for i, z in enumerate((-1, 2, 5, 8)):
    for lado, x0, ang in (('e', -7, 22.5), ('d', 12, -22.5)):
        nome = f'perna_{lado}{i}'
        pernas.append((nome, (i + (0 if lado == 'e' else 1)) % 2))
        r.osso(nome, [8, -9, z + 0.75], 'corpo')
        r.cubo(nome, [x0, -10, z], [x0 + 11, -8.5, z + 1.5], 'aranha', rot={'angle': ang, 'axis': 'z', 'origin': [8, -9, z]})
        r.cubo('pe_' + nome, [x0 - 1 if lado == 'e' else x0 + 10, -16, z], [x0 + 0.5 if lado == 'e' else x0 + 11.5, -10, z + 1.5], 'aranha')
r.anim('parado', 1.6, True, junta(onda(1.6, {'corpo': {'pos': ([0, 0.3, 0], 0, Z)}}),
                                  onda(1.6, {n: {'rot': ([0, 0, 4], g * math.pi, Z)} for n, g in pernas})))
r.anim('andar', 0.45, True, junta(onda(0.45, {n: {'rot': ([0, 18, 6], g * math.pi, Z)} for n, g in pernas}),
                                  onda(0.225, {'corpo': {'pos': ([0, 0.5, 0], 0, [0, 0.4, 0])}})))
r.anim('ataque', 0.5, False, quadros({'corpo': {'rot': [(0, Z), (0.2, [22, 0, 0]), (0.32, [-8, 0, 0]), (0.5, Z)]},
                                      'perna_e0': {'rot': [(0, Z), (0.2, [0, 0, -40]), (0.32, Z)]}, 'perna_d0': {'rot': [(0, Z), (0.2, [0, 0, 40]), (0.32, Z)]}}))
r.salvar()

r = Rig('chama_errante', 128)
r.osso('cranio', [8, -2, 8])
r.cubo('cranio', [4, -6, 4], [12, 2, 12], 'dente')
r.cubo('orbita_e', [4.8, -3, 3.7], [7.2, -0.6, 4], 'boca')
r.cubo('orbita_d', [8.8, -3, 3.7], [11.2, -0.6, 4], 'boca')
r.cubo('olho_e', [5.3, -2.5, 3.5], [6.7, -1.2, 3.7], 'olho_fogo', brilho=True)
r.cubo('olho_d', [9.3, -2.5, 3.5], [10.7, -1.2, 3.7], 'olho_fogo', brilho=True)
r.cubo('fogo', [3, 1, 3], [13, 6, 13], 'chama', brilho=True)
r.cubo('fogo2', [5, 5, 5], [11, 11, 11], 'chama', brilho=True)
r.cubo('fogo3', [6.5, 10, 6.5], [9.5, 14, 9.5], 'brasa', brilho=True)
r.cubo('rastro', [5, -14, 9], [11, -6, 14], 'chama', brilho=True, rot={'angle': 22.5, 'axis': 'x', 'origin': [8, -6, 10]})
r.osso('queixo', [8, -6, 8.5], 'cranio')
r.cubo('queixo', [5, -8, 4.5], [11, -6, 9], 'dente')
r.anim('parado', 1.2, True, junta(onda(1.2, {'cranio': {'pos': ([0, 1.2, 0], 0, Z), 'rot': ([0, 12, 4], 0.5, Z)}}),
                                  quadros({'queixo': {'rot': [(0, Z), (0.2, [-18, 0, 0]), (0.4, Z), (0.6, [-10, 0, 0]), (0.8, Z), (1.2, Z)]}})))
r.anim('andar', 0.8, True, junta(onda(0.8, {'cranio': {'pos': ([0, 1, 0], 0, Z), 'rot': ([0, 0, 6], 0, [-12, 0, 0])}}),
                                 quadros({'queixo': {'rot': [(0, Z), (0.2, [-20, 0, 0]), (0.4, Z), (0.8, Z)]}})))
r.anim('ataque', 0.5, False, quadros({'queixo': {'rot': [(0, Z), (0.15, [-40, 0, 0]), (0.3, Z), (0.5, Z)]},
                                      'cranio': {'rot': [(0, Z), (0.15, [15, 0, 0]), (0.3, [-20, 0, 0]), (0.5, Z)]}}))
r.salvar()

r = Rig('brasa_viva', 128)
r.osso('corpo', [8, -16, 8])
r.cubo('corpo', [1, -16, 1], [15, -2, 15], 'basalto')
r.cubo('rachadura1', [0.7, -12, 3], [1, -4, 5], 'brasa', brilho=True)
r.cubo('rachadura2', [15, -14, 9], [15.3, -6, 11], 'brasa', brilho=True)
r.cubo('rachadura3', [5, -10, 0.7], [11, -9, 1], 'brasa', brilho=True)
r.cubo('olho_e', [3.5, -6, 0.6], [6.5, -4, 1], 'olho_fogo', brilho=True)
r.cubo('olho_d', [9.5, -6, 0.6], [12.5, -4, 1], 'olho_fogo', brilho=True)
r.cubo('boca', [4, -11, 0.6], [12, -8.5, 1], 'chama', brilho=True)
r.osso('topo', [8, -2, 8], 'corpo')
r.cubo('pedra_topo', [3, -2, 3], [13, 2, 13], 'basalto')
r.cubo('fogo_topo', [5, 2, 5], [11, 6, 11], 'chama', brilho=True)
r.anim('parado', 1.6, True, onda(1.6, {'corpo': {'rot': ([0, 0, 2], 0, Z)}, 'topo': {'rot': ([0, 14, 0], 0, Z), 'pos': ([0, 0.5, 0], 1, Z)}}))
r.anim('andar', 0.8, True, junta(onda(0.8, {'corpo': {'rot': ([0, 0, 9], 0, Z)}, 'topo': {'rot': ([0, 0, 6], 1, Z)}}),
                                 quadros({'corpo': {'pos': [(0, Z), (0.2, [0, 2.5, 0]), (0.4, Z), (0.6, [0, 2.5, 0]), (0.8, Z)]}})))
r.anim('ataque', 0.5, False, quadros({'corpo': {'rot': [(0, Z), (0.2, [14, 0, 0]), (0.32, [-24, 0, 0]), (0.5, Z)]},
                                      'topo': {'pos': [(0, Z), (0.2, [0, 3, 0]), (0.32, Z)]}}))
r.salvar()

# gomo do corpo do Boitatá (um modelo inteiro, sem ossos)
m = Modelo('boitata_corpo', 128)
m.cubo('gomo', [1, -14, 1], [15, 0, 15], 'escama_fogo')
m.cubo('barriga', [2.5, -15, 2.5], [13.5, -13.5, 13.5], 'brasa', brilho=True)
m.cubo('fogo', [5, 0, 3], [11, 6, 13], 'chama', brilho=True)
m.cubo('fogo_ponta', [6.5, 6, 5.5], [9.5, 9, 10.5], 'brasa', brilho=True)
m.cubo('espinho_e', [-1, -8, 6], [1, -5, 10], 'escama_fogo')
m.cubo('espinho_d', [15, -8, 6], [17, -5, 10], 'escama_fogo')
m.salvar(SEM)

os.makedirs(f'{R}/models/item/dungeon', exist_ok=True)
json.dump({'textures': {'particle': 'minecraft:block/air'}, 'elements': []}, open(f'{R}/models/item/dungeon/vazio.json', 'w'))
json.dump({'model': {'type': 'minecraft:model', 'model': 'big:item/dungeon/vazio'}}, open(f'{R}/items/dungeon/vazio.json', 'w'))
print('mobs animados ok')
