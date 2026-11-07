# Itens 3D da Expedição da Mata Sombria (masmorra nova):
#  chave_1..chave_5 - chaves de porta de cada região (Raiz, Vento, Ossos, Lodo, Brasa)
#  semente, gorro, ingrediente, escama - objetos das missões de coleta (ficam girando no chão, brilhando)
import random
from voxel import cor, mix
import armadura as A

random.seed(47)
Modelo, TONS = A.carregar_modelo('masmorra')


def pal(h, v=0.07):
    c = cor(h)
    return [mix(c, 1 - v), c, mix(c, 1 + v)]


TONS.update({
    'raiz': [cor('6b4428'), cor('7a5232'), cor('5a3a22')], 'folha': pal('4f9a3a', 0.1), 'musgo': pal('6b8e23'),
    'vento': [cor('dfe7ec'), cor('c9d3da'), cor('eef3f6')], 'vermelho': pal('c0262d'), 'ferro': pal('8a9096'),
    'osso': [cor('e8e1d2'), cor('d6cdb9'), cor('f2ece0')], 'olho_roxo': pal('a855f7'),
    'lodo': [cor('5a7d2c'), cor('4c6e25'), cor('6b8e32')], 'cogumelo_v': pal('c8141f'), 'branco': pal('f4f4f4', 0.02),
    'cogumelo_m': pal('a0703a'), 'talo': pal('e8dcc4', 0.03), 'veneno': pal('84cc16', 0.08),
    'brasa': [cor('ff7a1a'), cor('ff9a2e'), cor('ffb347')], 'fogo': [cor('ffd23f'), cor('ffe680')], 'carvao': pal('2a2420'),
    'ouro': [cor('f2c230'), cor('ffd84a'), cor('d9a520')], 'semente': [cor('8a5a2a'), cor('a06a32'), cor('6e4620')],
    'brilho_verde': pal('b6ff3a', 0.04), 'escama': [cor('d9541e'), cor('f07a2a'), cor('b8401a')], 'escama_borda': pal('ffd23f', 0.05),
})

DISP_CHAVE = {'thirdperson_righthand': {'rotation': [0, 90, 45], 'translation': [0, 3, 1], 'scale': [0.6, 0.6, 0.6]},
              'thirdperson_lefthand': {'rotation': [0, -90, -45], 'translation': [0, 3, 1], 'scale': [0.6, 0.6, 0.6]},
              'firstperson_righthand': {'rotation': [0, 90, 25], 'translation': [1, 3, 0], 'scale': [0.6, 0.6, 0.6]},
              'firstperson_lefthand': {'rotation': [0, -90, -25], 'translation': [1, 3, 0], 'scale': [0.6, 0.6, 0.6]},
              'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
              'gui': {'rotation': [0, 0, -45], 'translation': [0, 0, 0], 'scale': [0.85, 0.85, 0.85]},
              'fixed': {'rotation': [0, 180, 0], 'scale': [1, 1, 1]}}
DISP_OBJ = {'fixed': {'rotation': [0, 0, 0], 'scale': [1, 1, 1]},
            'gui': {'rotation': [25, 145, 0], 'scale': [0.9, 0.9, 0.9]},
            'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
            'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 3, 1], 'scale': [0.5, 0.5, 0.5]},
            'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.6, 0.6, 0.6]}}


def chave(k, haste, cabeca, detalhe, brilho_tom):
    m = Modelo(f'chave_{k}', 64)
    # argola (cabeça) em cima, haste descendo, dentes embaixo
    m.cubo('argola_cima', [5.5, 15.0, 7.3], [10.5, 16.0, 8.7], cabeca)
    m.cubo('argola_baixo', [5.5, 10.0, 7.3], [10.5, 11.0, 8.7], cabeca)
    m.cubo('argola_e', [4.5, 11.0, 7.3], [5.5, 15.0, 8.7], cabeca)
    m.cubo('argola_d', [10.5, 11.0, 7.3], [11.5, 15.0, 8.7], cabeca)
    m.cubo('gema', [7.0, 12.0, 7.6], [9.0, 14.0, 8.4], brilho_tom, brilho=True)
    m.cubo('haste', [7.3, 0.0, 7.4], [8.7, 10.0, 8.6], haste)
    m.cubo('anel', [6.8, 8.6, 7.2], [9.2, 9.6, 8.8], cabeca)
    m.cubo('dente1', [8.7, 0.0, 7.5], [11.2, 1.4, 8.5], haste)
    m.cubo('dente2', [8.7, 2.4, 7.5], [10.4, 3.6, 8.5], haste)
    m.cubo('ponta', [7.3, -1.0, 7.4], [8.7, 0.0, 8.6], cabeca)
    detalhe(m)
    m.salvar(DISP_CHAVE)


chave(1, 'raiz', 'raiz', lambda m: (m.cubo('folha1', [3.4, 15.2, 7.6], [5.2, 16.6, 8.4], 'folha'),
                                    m.cubo('folha2', [10.8, 9.6, 7.6], [12.4, 11.0, 8.4], 'folha'),
                                    m.cubo('musgo', [7.2, 4.0, 7.3], [8.8, 5.4, 8.7], 'musgo')), 'brilho_verde')
chave(2, 'ferro', 'vermelho', lambda m: (m.cubo('fita1', [3.0, 13.0, 7.7], [4.5, 13.8, 8.3], 'vento'),
                                         m.cubo('fita2', [1.6, 12.0, 7.7], [3.0, 12.8, 8.3], 'vento'),
                                         m.cubo('pena', [11.5, 13.4, 7.7], [13.6, 14.2, 8.3], 'vento')), 'vento')
chave(3, 'osso', 'osso', lambda m: (m.cubo('cranio', [6.0, 16.0, 7.0], [10.0, 19.0, 9.0], 'osso'),
                                    m.cubo('olho_e', [6.6, 17.2, 6.85], [7.6, 18.2, 7.0], 'carvao'),
                                    m.cubo('olho_d', [8.4, 17.2, 6.85], [9.4, 18.2, 7.0], 'carvao')), 'olho_roxo')
chave(4, 'lodo', 'lodo', lambda m: (m.cubo('gota1', [5.0, 9.0, 7.4], [6.0, 10.0, 8.6], 'veneno'),
                                    m.cubo('gota2', [9.6, 6.0, 7.4], [10.4, 7.2, 8.6], 'veneno'),
                                    m.cubo('cogumelo', [10.6, 15.0, 7.2], [12.6, 16.4, 8.8], 'cogumelo_v')), 'veneno')
chave(5, 'carvao', 'ouro', lambda m: (m.cubo('chama1', [7.2, 16.0, 7.5], [8.8, 18.6, 8.5], 'brasa', brilho=True),
                                      m.cubo('chama2', [7.6, 18.6, 7.7], [8.4, 19.8, 8.3], 'fogo', brilho=True),
                                      m.cubo('brasa_haste', [7.2, 5.0, 7.3], [8.8, 6.0, 8.7], 'brasa', brilho=True)), 'brasa')

# ---------------------------------------------------------------- objetos de missão
m = Modelo('semente', 64)   # semente sagrada com broto
m.cubo('casca', [5.0, 3.0, 5.5], [11.0, 9.0, 10.5], 'semente')
m.cubo('topo', [6.0, 9.0, 6.5], [10.0, 10.0, 9.5], 'semente')
m.cubo('base', [6.0, 2.0, 6.5], [10.0, 3.0, 9.5], 'semente')
m.cubo('runa', [7.0, 5.0, 5.3], [9.0, 7.0, 5.55], 'brilho_verde', brilho=True)
m.cubo('broto', [7.6, 10.0, 7.6], [8.4, 13.0, 8.4], 'folha')
m.cubo('folha_e', [5.4, 12.0, 7.6], [7.6, 13.0, 8.4], 'folha')
m.cubo('folha_d', [8.4, 12.6, 7.6], [10.6, 13.6, 8.4], 'folha')
m.salvar(DISP_OBJ)

m = Modelo('gorro', 64)    # gorro vermelho do Saci
m.cubo('aba', [3.5, 2.0, 3.5], [12.5, 4.0, 12.5], 'vermelho')
m.cubo('corpo', [4.5, 4.0, 4.5], [11.5, 8.0, 11.5], 'vermelho')
m.cubo('meio', [5.5, 8.0, 5.5], [10.5, 11.0, 10.5], 'vermelho', rot={'angle': -22.5, 'axis': 'z', 'origin': [8, 8, 8]})
m.cubo('ponta', [7.0, 10.5, 6.5], [10.0, 14.0, 9.5], 'vermelho', rot={'angle': -45, 'axis': 'z', 'origin': [8.5, 10.5, 8]})
m.cubo('pompom', [10.6, 12.0, 7.0], [12.6, 14.0, 9.0], 'branco')
m.salvar(DISP_OBJ)

m = Modelo('ingrediente', 64)   # cogumelo venenoso da Cuca
m.cubo('talo', [7.0, 0.0, 7.0], [9.0, 6.0, 9.0], 'talo')
m.cubo('chapeu', [3.5, 6.0, 3.5], [12.5, 9.0, 12.5], 'cogumelo_v')
m.cubo('chapeu_topo', [5.0, 9.0, 5.0], [11.0, 10.5, 11.0], 'cogumelo_v')
for i, (x, z) in enumerate(((4.5, 6.0), (9.0, 4.2), (10.6, 9.0), (6.4, 10.4))):
    m.cubo(f'pinta{i}', [x, 9.0, z], [x + 1.4, 9.3, z + 1.4], 'branco')
m.cubo('pinta_topo', [7.2, 10.5, 7.2], [8.8, 10.8, 8.8], 'branco')
m.cubo('gota', [11.4, 4.0, 7.6], [12.2, 5.4, 8.4], 'veneno', brilho=True)
m.salvar(DISP_OBJ)

m = Modelo('escama', 64)   # escama de fogo do Boitatá
m.cubo('placa', [3.5, 3.0, 7.0], [12.5, 12.0, 9.0], 'escama')
m.cubo('ponta', [5.0, 12.0, 7.2], [11.0, 14.0, 8.8], 'escama')
m.cubo('base', [5.0, 1.5, 7.2], [11.0, 3.0, 8.8], 'escama')
m.cubo('borda_e', [3.0, 3.5, 6.8], [3.5, 11.5, 9.2], 'escama_borda', brilho=True)
m.cubo('borda_d', [12.5, 3.5, 6.8], [13.0, 11.5, 9.2], 'escama_borda', brilho=True)
m.cubo('nucleo', [6.5, 6.0, 6.7], [9.5, 9.0, 7.0], 'brasa', brilho=True)
m.cubo('nucleo2', [6.5, 6.0, 9.0], [9.5, 9.0, 9.3], 'brasa', brilho=True)
m.salvar(DISP_OBJ)

print('ok: chave_1..5, semente, gorro, ingrediente, escama')
