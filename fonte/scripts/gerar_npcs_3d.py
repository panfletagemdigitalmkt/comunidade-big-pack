# NPCs 3D ANIMADOS da vila (lobby), no mesmo esquema dos chefes da masmorra (gerar_mobs.py):
# cada NPC é dividido em ossos (corpo, cabeça, braços, pernas); cada osso vira um item 3D e o plugin
# junta tudo e toca as animações deste arquivo: "parado" (respiração, em loop) e "acenar" (saudação).
# Unidades: 16 = 1 bloco. O pé fica em y = -16. A frente é -z.
#
# uso: python gerar_npcs_3d.py [pasta_da_previa]
import json, os, sys, copy, math, random
from voxel import cor, mix
import armadura as A

random.seed(23)
Modelo, TONS = A.carregar_modelo('npc')
R = 'assets/big'
PLUGIN = '../plugin/big-core/src/main/resources/modelos'
SEM = {'fixed': {'scale': [1, 1, 1]}, 'gui': {'rotation': [15, -150, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]}}
Z = [0, 0, 0]


def pal(h, v=0.06):
    c = cor(h)
    return [mix(c, 1 - v), c, mix(c, 1 + v)]


TONS.update({
    'olho_branco': [cor('f4f4f4'), cor('ebebeb')], 'preto': [cor('141416'), cor('1c1c20')], 'dourado': pal('e0b13a', 0.08),
    'gema_roxa': pal('a855f7'), 'madeira': pal('7a5232', 0.08), 'madeira_escura': pal('4a2e1a'), 'ferro': pal('9aa0a6'),
    'branco': pal('f2f2f2', 0.03), 'peixe': pal('7fa7c9', 0.08), 'peixe_barriga': pal('dfe9f0', 0.04), 'papel': pal('efe2bf', 0.05),
    'vermelho': pal('c0262d'), 'verde_folha': pal('4f8a2a', 0.08), 'abacaxi': pal('e6b422', 0.08), 'morango': pal('d42a3a', 0.06),
    'milho': pal('f2d04a', 0.06), 'palha': pal('e3c36a', 0.08), 'moeda': pal('f2c230', 0.05), 'couro': pal('6b4428', 0.08),
})


class Rig:
    def __init__(s, nome, tam=256):
        s.nome = nome
        s.m = Modelo(nome, tam)
        s.ossos, s.ordem, s.atual, s.anims = {}, [], None, {}

    def osso(s, nome, pivo, pai=None):
        s.ossos[nome] = {'pivo': pivo, 'pai': pai, 'el': []}
        s.ordem.append(nome)
        s.atual = nome

    def em(s, nome):
        s.atual = nome
        return s

    def cubo(s, *a, **k):
        n = len(s.m.el)
        s.m.cubo(*a, **k)
        s.ossos[s.atual]['el'].extend(s.m.el[n:])

    def anim(s, nome, dur, loop, ossos):
        s.anims[nome] = {'duracao': dur, 'loop': loop, 'ossos': ossos}

    def salvar(s):
        tex = f'big:item/npc/{s.nome}'
        os.makedirs(f'{R}/textures/item/npc', exist_ok=True)
        s.m.img.save(f'{R}/textures/item/npc/{s.nome}.png')
        for d in (f'{R}/models/item/npc/{s.nome}', f'{R}/items/npc/{s.nome}', PLUGIN):
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
                      open(f'{R}/models/item/npc/{s.nome}/{o}.json', 'w'))
            json.dump({'model': {'type': 'minecraft:model', 'model': f'big:item/npc/{s.nome}/{o}'}},
                      open(f'{R}/items/npc/{s.nome}/{o}.json', 'w'))
        rig = {'ossos': [{'nome': o, 'pivo': s.ossos[o]['pivo'], 'pai': s.ossos[o]['pai']} for o in s.ordem], 'animacoes': s.anims}
        json.dump(rig, open(f'{PLUGIN}/npc_{s.nome}.json', 'w'), indent=1)
        print(s.nome, len(s.ordem), 'ossos', sum(len(x['el']) for x in s.ossos.values()), 'cubos')


def onda(dur, ossos, n=8):
    out = {}
    for o, canais in ossos.items():
        out[o] = {}
        for canal, (amp, fase, base) in canais.items():
            q = []
            for i in range(n + 1):
                t = dur * i / n
                sn = math.sin(2 * math.pi * i / n + fase)
                q.append([round(t, 3), [round(base[k] + amp[k] * sn, 2) for k in range(3)]])
            out[o][canal] = q
    return out


def quadros(ossos):
    return {o: {c: [[t, v] for t, v in q] for c, q in cs.items()} for o, cs in ossos.items()}


# ================================================================ corpo base
# tons esperados no dicionário do NPC: pele, cabelo, olho, camisa, manga, calca, sapato
def humano(nome, t, cabelo='curto', barba=None, extras=None):
    for k, v in t.items():
        TONS[f'{nome}_{k}'] = v
    T = lambda k: f'{nome}_{k}' if f'{nome}_{k}' in TONS else k
    r = Rig(nome)
    # pernas
    for lado, x0 in (('e', 4.2), ('d', 8.2)):
        r.osso('perna_' + lado, [x0 + 1.8, -5, 8])
        r.cubo('perna_' + lado, [x0, -14, 6.2], [x0 + 3.6, -5, 9.8], T('calca'))
        r.cubo('sapato_' + lado, [x0 - 0.2, -16, 5.2], [x0 + 3.8, -14, 10], T('sapato'))
    # tronco
    r.osso('corpo', [8, -5, 8])
    r.cubo('tronco', [3.6, -5, 5.8], [12.4, 6, 10.2], T('camisa'))
    r.cubo('pescoco', [6.5, 5.5, 6.8], [9.5, 6.6, 9.2], T('pele'))
    # cabeça
    r.osso('cabeca', [8, 6, 8], 'corpo')
    r.cubo('cabeca', [3.5, 6.5, 3.5], [12.5, 15.5, 12.5], T('pele'))
    for lado, x in (('e', 4.8), ('d', 9.0)):
        r.cubo('olho_' + lado, [x, 10.4, 3.3], [x + 2.2, 11.9, 3.5], 'olho_branco')
        px = x + 1.1 if lado == 'e' else x
        r.cubo('pupila_' + lado, [px, 10.4, 3.2], [px + 1.1, 11.9, 3.35], T('olho'))
        r.cubo('sobrancelha_' + lado, [x - 0.2, 12.2, 3.25], [x + 2.4, 12.8, 3.5], T('sobrancelha') if f'{nome}_sobrancelha' in TONS else T('cabelo'))
    r.cubo('nariz', [7.2, 9.0, 2.7], [8.8, 10.6, 3.5], T('pele'))
    r.cubo('boca', [6.6, 7.9, 3.35], [9.4, 8.5, 3.5], T('boca') if f'{nome}_boca' in TONS else 'preto')
    r.cubo('orelha_e', [3.0, 9.2, 7.2], [3.5, 11.2, 8.8], T('pele'))
    r.cubo('orelha_d', [12.5, 9.2, 7.2], [13.0, 11.2, 8.8], T('pele'))
    c = T('cabelo')
    if cabelo != 'careca':
        r.cubo('cabelo_topo', [3.3, 14.6, 3.3], [12.7, 16.0, 12.7], c)
        r.cubo('cabelo_nuca', [3.3, 9.0 if cabelo != 'longo' else 2.5, 11.9], [12.7, 15.0, 12.9], c)
        r.cubo('cabelo_franja', [3.3, 13.6, 3.2], [12.7, 14.6, 4.2], c)
        for lado, x in (('e', 3.2), ('d', 12.1)):
            r.cubo('costeleta_' + lado, [x, 10.8 if cabelo != 'longo' else 3.0, 4.0], [x + 0.7, 15.0, 12.6], c)
    if cabelo == 'coque':
        r.cubo('coque', [5.8, 14.5, 12.3], [10.2, 18.0, 15.0], c)
    if cabelo == 'volume':
        r.cubo('volume_topo', [2.4, 14.0, 2.8], [13.6, 18.0, 13.6], c)
        r.cubo('volume_tras', [2.0, 6.0, 9.0], [14.0, 16.0, 14.2], c)
        for lado, x in (('e', 1.8), ('d', 12.6)):
            r.cubo('volume_' + lado, [x, 7.0, 3.6], [x + 1.6, 16.5, 13.0], c)
    b = T('barba') if f'{nome}_barba' in TONS else c
    if barba in ('bigode', 'barba', 'barba_longa'):
        r.cubo('bigode', [5.6, 8.5, 2.9], [10.4, 9.4, 3.4], b)
    if barba in ('barba', 'barba_longa'):
        r.cubo('barba', [3.4, 6.2, 3.1], [12.6, 8.5, 7.0], b)
        r.cubo('barba_lados', [3.3, 8.4, 4.5], [12.7, 10.6, 7.5], b)
        r.cubo('queixo', [5.0, 5.4, 3.0], [11.0, 6.4, 6.0], b)
    if barba == 'barba_longa':
        r.cubo('barba_longa', [4.6, 0.0, 3.2], [11.4, 5.6, 6.2], b)
        r.cubo('barba_ponta', [6.0, -3.0, 3.6], [10.0, 0.2, 5.8], b)
    # braços
    for lado, x0, piv in (('e', 0.8, 2.2), ('d', 12.4, 13.8)):
        r.osso('braco_' + lado, [piv, 5, 8], 'corpo')
        r.cubo('braco_' + lado, [x0, -5.5, 6.4], [x0 + 2.8, 6.0, 9.6], T('manga'))
        r.cubo('mao_' + lado, [x0 + 0.2, -7.2, 6.6], [x0 + 2.6, -5.5, 9.4], T('pele'))
    if extras:
        extras(r, T)
    # animações
    r.anim('parado', 3.2, True, onda(3.2, {'corpo': {'pos': ([0, 0.22, 0], 0, Z)}, 'cabeca': {'rot': ([2.5, 0, 1.5], 1, Z)},
                                           'braco_e': {'rot': ([2, 0, 2.5], 0, Z)}, 'braco_d': {'rot': ([2, 0, -2.5], 0, Z)}}))
    onda_mao = [(0, Z), (0.28, [-165, 0, 18]), (0.5, [-165, 0, -18]), (0.72, [-165, 0, 18]), (0.94, [-165, 0, -18]),
                (1.16, [-165, 0, 12]), (1.5, [-90, 0, 0]), (1.8, Z)]
    r.anim('acenar', 1.8, False, quadros({
        'braco_d': {'rot': onda_mao},
        'cabeca': {'rot': [(0, Z), (0.25, [6, 0, 9]), (1.2, [6, 0, 9]), (1.6, [10, 0, 0]), (1.8, Z)]},
        'corpo': {'rot': [(0, Z), (0.25, [0, 0, -2]), (1.2, [0, 0, -2]), (1.55, [7, 0, 0]), (1.8, Z)]},
        'braco_e': {'rot': [(0, Z), (0.3, [6, 0, 5]), (1.5, [6, 0, 5]), (1.8, Z)]}}))
    r.salvar()
    return r


# ================================================================ os NPCs
def chapeu_aba(r, T, tom, faixa, aba=2.5, alt=3.0, y0=15.3, copa_tom=None):
    r.em('cabeca')
    r.cubo('aba', [3.5 - aba, y0, 3.5 - aba], [12.5 + aba, y0 + 0.8, 12.5 + aba], tom)
    r.cubo('copa', [4.2, y0 + 0.8, 4.2], [11.8, y0 + 0.8 + alt, 11.8], copa_tom or tom)
    r.cubo('faixa', [4.1, y0 + 0.8, 4.1], [11.9, y0 + 1.7, 11.9], faixa)


def guia(r, T):
    chapeu_aba(r, T, 'guia_chapeu', 'couro', aba=2.2, alt=2.6)
    r.em('corpo')
    r.cubo('colete', [3.3, -3.0, 5.5], [12.7, 6.2, 10.5], 'couro', tons_face={'north': 'couro'})
    r.cubo('camisa_aberta', [6.6, -3.0, 5.3], [9.4, 6.2, 5.6], 'guia_camisa')
    r.cubo('cinto', [3.4, -4.6, 5.6], [12.6, -3.4, 10.4], 'madeira_escura')
    r.cubo('fivela', [7.2, -4.7, 5.4], [8.8, -3.3, 5.6], 'dourado')
    r.cubo('alca', [5.0, -4.0, 5.3], [6.2, 6.3, 5.6], 'madeira_escura', rot={'angle': -22.5, 'axis': 'z', 'origin': [8, 1, 5.4]})
    r.cubo('bolsa', [12.4, -6.5, 6.5], [14.0, -2.5, 9.8], 'couro')
    r.em('braco_e')
    r.cubo('mapa', [0.0, -9.5, 4.0], [4.4, -6.0, 4.4], 'papel')
    r.cubo('mapa_rolo', [-0.3, -9.9, 3.8], [4.7, -9.3, 4.6], 'madeira')
    r.cubo('mapa_x', [1.8, -8.4, 3.85], [2.6, -7.6, 4.0], 'vermelho')


def peixeiro(r, T):
    chapeu_aba(r, T, 'peixeiro_capa', 'peixeiro_faixa', aba=1.6, alt=2.4)
    r.em('cabeca')
    r.cubo('chapeu_nuca', [3.0, 12.0, 12.6], [13.0, 15.3, 14.2], 'peixeiro_capa')
    r.em('corpo')
    r.cubo('capa', [3.2, -6.5, 5.4], [12.8, 6.3, 10.6], 'peixeiro_capa')
    r.cubo('camisa_listrada', [6.3, -6.5, 5.2], [9.7, 6.3, 5.5], 'peixeiro_listra')
    r.cubo('gola', [4.0, 5.6, 5.0], [12.0, 7.0, 10.8], 'peixeiro_capa')
    r.em('braco_e')
    r.cubo('cordinha', [1.9, -8.2, 7.8], [2.5, -6.8, 8.4], 'madeira_escura')
    r.cubo('peixe', [0.2, -14.0, 7.4], [4.2, -8.2, 8.8], 'peixe')
    r.cubo('peixe_barriga', [0.8, -13.4, 7.2], [3.6, -9.0, 7.45], 'peixe_barriga')
    r.cubo('nadadeira', [1.4, -12.6, 6.9], [3.0, -10.6, 7.25], 'peixe')
    r.cubo('rabo', [0.6, -16.4, 7.6], [3.8, -14.0, 8.6], 'peixe')
    r.cubo('olho_peixe', [1.6, -9.4, 7.1], [2.6, -8.6, 7.3], 'preto')
    r.em('braco_d')
    r.cubo('luva', [12.2, -7.4, 6.4], [15.4, -5.2, 9.6], 'peixeiro_capa')


def hortifruti(r, T):
    r.em('cabeca')
    r.cubo('lenco', [3.2, 13.8, 3.2], [12.8, 16.2, 12.8], 'vermelho')
    r.cubo('lenco_no', [7.0, 11.0, 12.8], [9.0, 14.0, 13.6], 'vermelho')
    for i, x in enumerate((4.2, 6.6, 9.4, 11.4)):
        r.cubo(f'bolinha{i}', [x, 15.2, 3.0], [x + 0.8, 15.9, 3.25], 'branco')
    r.cubo('brinco_e', [2.7, 8.4, 7.6], [3.1, 9.2, 8.4], 'dourado')
    r.cubo('brinco_d', [12.9, 8.4, 7.6], [13.3, 9.2, 8.4], 'dourado')
    r.em('corpo')
    r.cubo('saia', [3.0, -11.0, 5.0], [13.0, -4.0, 11.0], 'hortifruti_camisa')
    r.cubo('avental', [4.4, -10.5, 5.5], [11.6, 3.5, 5.8], 'hortifruti_avental')
    r.cubo('bolso', [5.6, -7.0, 5.3], [10.4, -4.8, 5.55], 'hortifruti_bolso')
    r.cubo('alca_avental', [6.2, 3.5, 5.55], [9.8, 5.8, 5.8], 'hortifruti_avental')
    r.em('braco_e')
    r.cubo('cesta', [-0.8, -12.0, 4.2], [5.2, -8.5, 11.8], 'palha')
    r.cubo('alca_cesta', [1.7, -8.5, 5.0], [2.7, -5.5, 11.0], 'madeira')
    r.cubo('abacaxi', [-0.3, -8.5, 5.0], [2.0, -6.0, 7.3], 'abacaxi')
    r.cubo('abacaxi_folha', [0.3, -6.0, 5.6], [1.4, -4.6, 6.7], 'verde_folha')
    r.cubo('morango', [2.6, -8.5, 8.6], [4.2, -7.1, 10.2], 'morango')
    r.cubo('milho', [0.0, -8.5, 8.0], [1.6, -6.6, 11.2], 'milho')


def mercador(r, T):
    r.em('cabeca')
    r.cubo('boina', [3.1, 14.6, 3.6], [12.9, 17.0, 12.9], 'couro')
    r.cubo('boina_aba', [3.6, 14.6, 1.6], [12.4, 15.3, 3.8], 'couro')
    r.em('corpo')
    r.cubo('colete', [3.3, -4.0, 5.5], [12.7, 6.2, 10.5], 'mercador_colete')
    r.cubo('camisa_aberta', [6.6, -4.0, 5.3], [9.4, 6.2, 5.6], 'mercador_camisa')
    for i, y in enumerate((-2.0, 1.0, 4.0)):
        r.cubo(f'botao{i}', [5.6, y, 5.3], [6.4, y + 0.8, 5.5], 'dourado')
    r.cubo('lenco', [5.2, 4.6, 5.2], [10.8, 6.2, 5.6], 'vermelho')
    r.cubo('lenco_ponta', [7.2, 2.8, 5.25], [8.8, 4.6, 5.55], 'vermelho')
    r.cubo('cinto', [3.4, -5.0, 5.6], [12.6, -3.8, 10.4], 'madeira_escura')
    r.cubo('fivela', [7.2, -5.1, 5.4], [8.8, -3.7, 5.6], 'dourado')
    r.em('braco_e')
    r.cubo('saco', [-0.4, -12.4, 5.4], [4.8, -7.6, 10.6], 'mercador_saco')
    r.cubo('saco_boca', [0.6, -7.6, 6.4], [3.8, -6.6, 9.6], 'mercador_saco')
    r.cubo('saco_moeda', [0.9, -6.9, 7.0], [3.5, -6.3, 9.0], 'moeda')
    r.cubo('saco_simbolo', [1.4, -10.8, 5.2], [3.0, -9.0, 5.45], 'moeda')


def fazendeiro(r, T):
    chapeu_aba(r, T, 'palha', 'vermelho', aba=3.2, alt=2.6)
    r.em('corpo')
    r.cubo('macacao', [3.4, -5.5, 5.5], [12.6, 0.5, 10.5], 'fazendeiro_jeans')
    r.cubo('peitilho', [5.0, 0.5, 5.5], [11.0, 4.0, 5.8], 'fazendeiro_jeans')
    r.cubo('alca_e', [4.6, 0.5, 5.5], [5.8, 6.2, 10.5], 'fazendeiro_jeans')
    r.cubo('alca_d', [10.2, 0.5, 5.5], [11.4, 6.2, 10.5], 'fazendeiro_jeans')
    r.cubo('botao_e', [4.8, 3.2, 5.3], [5.6, 4.0, 5.5], 'dourado')
    r.cubo('botao_d', [10.4, 3.2, 5.3], [11.2, 4.0, 5.5], 'dourado')
    r.cubo('bolso_peito', [6.6, 1.2, 5.3], [9.4, 3.2, 5.55], 'fazendeiro_jeans_escuro')
    for lado, x0 in (('e', 4.2), ('d', 8.2)):
        r.em('perna_' + lado)
        r.cubo('jeans_' + lado, [x0 - 0.15, -12.0, 6.05], [x0 + 3.75, -5.0, 9.95], 'fazendeiro_jeans')
    r.em('braco_e')
    r.cubo('forcado_cabo', [1.7, -16.0, 7.5], [2.7, 10.0, 8.5], 'madeira')
    r.cubo('forcado_base', [-0.3, 10.0, 7.3], [4.7, 11.0, 8.7], 'ferro')
    for i, x in enumerate((-0.3, 1.75, 3.8)):
        r.cubo(f'dente{i}', [x, 11.0, 7.5], [x + 0.9, 15.5, 8.5], 'ferro')


def leiloeiro(r, T):
    r.em('cabeca')
    for lado, x in (('e', 4.5), ('d', 8.7)):
        r.cubo('lente_' + lado, [x, 10.0, 3.0], [x + 2.8, 12.3, 3.2], 'preto', tons_face={'north': 'preto'})
    r.cubo('ponte', [7.3, 11.4, 3.0], [8.7, 11.8, 3.2], 'preto')
    # tapa a lente (aro) deixando o olho visível
    r.cubo('lente_vidro_e', [4.9, 10.4, 2.95], [6.9, 11.9, 3.0], 'olho_branco')
    r.cubo('lente_vidro_d', [9.1, 10.4, 2.95], [11.1, 11.9, 3.0], 'olho_branco')
    r.cubo('pupila_vidro_e', [6.0, 10.4, 2.9], [6.9, 11.9, 2.95], 'leiloeiro_olho')
    r.cubo('pupila_vidro_d', [9.1, 10.4, 2.9], [10.0, 11.9, 2.95], 'leiloeiro_olho')
    r.em('corpo')
    r.cubo('paleto', [3.3, -5.3, 5.5], [12.7, 6.2, 10.5], 'leiloeiro_terno')
    r.cubo('camisa_aberta', [6.4, -2.0, 5.3], [9.6, 6.2, 5.6], 'branco')
    r.cubo('colete', [6.8, -2.0, 5.2], [9.2, 3.5, 5.4], 'leiloeiro_colete')
    r.cubo('gravata_borboleta', [6.0, 4.6, 5.0], [10.0, 5.8, 5.3], 'vermelho')
    r.cubo('no_gravata', [7.5, 4.5, 4.9], [8.5, 5.9, 5.1], 'leiloeiro_colete')
    r.cubo('lenco_bolso', [10.0, 2.8, 5.3], [11.4, 3.8, 5.5], 'dourado')
    r.cubo('corrente', [7.0, 0.2, 5.15], [10.6, 0.6, 5.3], 'dourado')
    r.em('braco_e')
    r.cubo('martelo_cabo', [1.8, -7.0, 1.6], [2.6, -6.2, 7.0], 'madeira')
    r.cubo('martelo_cabeca', [0.4, -8.4, 0.2], [4.0, -4.8, 2.4], 'madeira_escura')
    r.cubo('martelo_anel', [0.3, -6.9, 0.1], [4.1, -6.3, 2.5], 'dourado')


def banqueira(r, T):
    r.em('cabeca')
    r.cubo('brinco_e', [2.0, 7.6, 7.4], [2.6, 9.0, 8.6], 'dourado')
    r.cubo('brinco_d', [13.4, 7.6, 7.4], [14.0, 9.0, 8.6], 'dourado')
    r.em('corpo')
    r.cubo('blazer', [3.3, -5.3, 5.5], [12.7, 6.2, 10.5], 'banqueira_blazer')
    r.cubo('blusa', [6.4, -3.0, 5.3], [9.6, 6.2, 5.6], 'banqueira_blusa')
    r.cubo('colar', [6.0, 5.2, 5.15], [10.0, 5.7, 5.35], 'dourado')
    r.cubo('pingente', [7.4, 3.6, 5.0], [8.6, 5.2, 5.25], 'moeda')
    r.cubo('broche', [10.2, 2.4, 5.3], [11.2, 3.4, 5.55], 'dourado')
    r.cubo('cinto', [3.4, -5.0, 5.6], [12.6, -4.0, 10.4], 'preto')
    r.em('braco_e')
    for i in range(4):
        r.cubo(f'moeda{i}', [0.2, -9.0 + i * 0.7, 3.8], [3.4, -8.4 + i * 0.7, 6.8], 'moeda')


def mestre(r, T):
    r.em('cabeca')
    r.cubo('tiara', [3.3, 14.0, 3.3], [12.7, 14.8, 12.7], 'dourado')
    r.cubo('gema', [7.0, 14.0, 3.0], [9.0, 15.8, 3.3], 'gema_roxa', brilho=True)
    r.em('corpo')
    r.cubo('manto', [3.0, -14.5, 5.0], [13.0, 6.3, 11.0], 'mestre_manto')
    r.cubo('barra_frente', [7.0, -14.5, 4.8], [9.0, 2.0, 5.1], 'dourado')
    r.cubo('barra_baixo', [2.9, -14.6, 4.9], [13.1, -13.6, 11.1], 'dourado')
    r.cubo('faixa', [2.9, -3.0, 4.9], [13.1, -2.0, 11.1], 'dourado')
    r.cubo('faixa_gema', [7.3, -3.2, 4.7], [8.7, -1.8, 4.95], 'gema_roxa', brilho=True)
    r.cubo('gola', [3.6, 5.0, 4.8], [12.4, 6.6, 11.2], 'mestre_manto_escuro')
    for lado, x0 in (('e', 0.6), ('d', 12.2)):
        r.em('braco_' + lado)
        r.cubo('manga_larga_' + lado, [x0, -6.5, 6.0], [x0 + 3.2, -3.5, 10.0], 'mestre_manto')
        r.cubo('punho_' + lado, [x0 - 0.05, -6.6, 5.95], [x0 + 3.25, -5.9, 10.05], 'dourado')
    r.em('braco_e')
    r.cubo('cajado', [1.7, -17.0, 3.4], [2.7, 13.0, 4.4], 'madeira')
    r.cubo('cajado_garra', [0.7, 13.0, 2.4], [3.7, 14.5, 5.4], 'dourado')
    r.cubo('cajado_gema', [1.0, 14.5, 2.7], [3.4, 17.5, 5.1], 'gema_roxa', brilho=True)


NPCS = [
    ('guia', dict(pele=pal('c68e5d'), cabelo=pal('5a3a22'), olho=pal('2f6f9f'), camisa=pal('cdb684'), manga=pal('cdb684'),
                  calca=pal('5d5a3a'), sapato=pal('4a2e1a'), chapeu=pal('b59a6a', 0.08)), 'curto', 'barba', guia),
    ('peixeiro', dict(pele=pal('a86b45'), cabelo=pal('8a8a8a'), olho=pal('3b2a1d'), camisa=pal('f2c230'), manga=pal('f2c230'),
                      calca=pal('2b3a55'), sapato=pal('2f4f3a'), capa=pal('f2c230', 0.07), listra=[cor('f2f2f2'), cor('2f5fa8')], faixa=pal('2b3a55'),
                      barba=pal('9a9a9a')), 'curto', 'barba', peixeiro),
    ('hortifruti', dict(pele=pal('e0ac7e'), cabelo=pal('3b2414'), olho=pal('4a2e1a'), camisa=pal('f5d14a'), manga=pal('e0ac7e'),
                        calca=pal('e0ac7e'), sapato=pal('8a5a32'), avental=pal('4f9a3a'), bolso=pal('3d7a2c'), boca=pal('b8455a')),
     'coque', None, hortifruti),
    ('mercador', dict(pele=pal('8d5a3b'), cabelo=pal('1c1410'), olho=pal('2a1a12'), camisa=pal('f2efe6', 0.03), manga=pal('f2efe6', 0.03),
                      calca=pal('5a3a22'), sapato=pal('1c1410'), colete=pal('e07b1f'), saco=pal('b08a5a', 0.08)), 'curto', 'bigode', mercador),
    ('fazendeiro', dict(pele=pal('d29a6a'), cabelo=pal('6b4428'), olho=pal('3b5a2a'), camisa=[cor('b3202a'), cor('2a1a1a'), cor('7a1820')],
                        manga=[cor('b3202a'), cor('2a1a1a'), cor('7a1820')], calca=pal('3e6aa8'), sapato=pal('5a3a22'),
                        jeans=pal('3e6aa8'), jeans_escuro=pal('2f5590')), 'curto', None, fazendeiro),
    ('leiloeiro', dict(pele=pal('f0c39b'), cabelo=pal('9a9a9a'), olho=pal('3b5a7a'), camisa=pal('f7f7f7', 0.02), manga=pal('23232b'),
                       calca=pal('1e1e24'), sapato=pal('0e0e10'), terno=pal('23232b'), colete=pal('5a1820'), barba=pal('c5c5c5')),
     'curto', 'bigode', leiloeiro),
    ('banqueira', dict(pele=pal('6b4128'), cabelo=pal('1a1210', 0.1), olho=pal('2a1a12'), camisa=pal('237a4a'), manga=pal('237a4a'),
                       calca=pal('1f5a3a'), sapato=pal('121212'), blazer=pal('237a4a'), blusa=pal('f5f0e6', 0.03), boca=pal('8a2a3a')),
     'volume', None, banqueira),
    ('mestre', dict(pele=pal('e8b894'), cabelo=pal('e8e8ee', 0.03), olho=pal('6b4fbf'), sobrancelha=pal('cfcfd8'), camisa=pal('4c2a7a'),
                    manga=pal('4c2a7a'), calca=pal('4c2a7a'), sapato=pal('3b2a1d'), manto=pal('4c2a7a'), manto_escuro=pal('3d2266'),
                    barba=pal('eeeef2', 0.03)), 'longo', 'barba_longa', mestre),
]

if __name__ == '__main__':
    rigs = [humano(n, t, cab, bar, ex) for n, t, cab, bar, ex in NPCS]
    print('ok:', ', '.join(n for n, *_ in NPCS))
