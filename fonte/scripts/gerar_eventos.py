# Itens 3D dos EVENTOS (estilo Blockbench: cubos com textura pintada), usados pelo plugin (pacote evento):
#  batata_quente  - a batata que explode (vai na mão e na cabeça de quem está com ela)
#  taco           - taco de sinuca com repulsão (Sinuca de Gelo)
#  espada_torneio - espada de treino acolchoada (Resta 1)
#  pa_spleef      - pá de gelo que quebra neve na hora (Spleef)
#  travesseiro    - travesseiro de penas (Rei da Colina)
#  boneca_corpo / boneca_cabeca - a Boneca Caipira gigante (Batatinha Frita 1, 2, 3)
#  bola_1 / bola_3 / bola_8 / bola_branca - bolas de sinuca gigantes (decoração)
#  coroa          - coroa dourada que gira em cima da colina
import random
from voxel import cor, mix
import armadura as A

random.seed(31)
Modelo, TONS = A.carregar_modelo('eventos')


def pal(h, v=0.07):
    c = cor(h)
    return [mix(c, 1 - v), c, mix(c, 1 + v)]


TONS.update({
    'batata': [cor('a8743a'), cor('b98446'), cor('9a6630'), cor('c49352')], 'batata_clara': pal('d9a964', 0.05),
    'brasa': [cor('ff7a1a'), cor('ff9a2e'), cor('ffb347')], 'fogo': [cor('ffd23f'), cor('ffe680')], 'pavio': pal('3a2a1a'),
    'olho': [cor('141414')], 'boca': [cor('3a1208')], 'carvao': pal('2a2420'),
    'mad_escura': pal('3b2416'), 'mad_clara': pal('d8b07a', 0.05), 'mad_media': pal('8a5a32'), 'latao': pal('d9b13a'),
    'branco': pal('f2f2f2', 0.02), 'giz': pal('3a7bd5', 0.04), 'preto': pal('1a1a1e'), 'couro': pal('5a3720'),
    'tecido_vermelho': pal('c0262d'), 'tecido_azul': pal('2f6fd0'), 'acolchoado': pal('e8dcc4', 0.04), 'ferro': pal('a7adb3'),
    'gelo': [cor('a8d8ff'), cor('bfe3ff'), cor('93c9f5'), cor('d6eeff')], 'gelo_esc': pal('6fa8dc'), 'cabo_azul': pal('1f3f6a'),
    'fronha': [cor('f4f1ea'), cor('ebe6da'), cor('f8f6f0')], 'fronha_listra': pal('8fb8e8', 0.04), 'pena': pal('fafafa', 0.02),
    'pele': pal('f0c39b', 0.04), 'bochecha': pal('e8848a', 0.03), 'tranca': pal('8a4a1e'), 'laco': pal('d93a6a'),
    'xadrez_v': [cor('c0262d'), cor('f2f2f2')], 'xadrez_a': [cor('2f5fa8'), cor('f2f2f2')], 'palha': pal('e3c36a', 0.09),
    'avental': pal('f7f0d8', 0.03), 'sapato': pal('5a2a1a'), 'botao': pal('f2c230'),
    'bola_amarela': pal('f2c230', 0.04), 'bola_vermelha': pal('c8141f', 0.04), 'bola_preta': pal('141418', 0.05),
    'bola_branca': pal('f4f2ec', 0.02), 'ouro': [cor('f2c230'), cor('ffd84a'), cor('d9a520')], 'rubi': pal('d0142a'),
    'esmeralda': pal('22c55e'), 'safira': pal('2f6fd0'), 'veludo': pal('7a1830'),
})

# transformações de exibição (mão, cabeça, chão, inventário)
DISP_ITEM = {'thirdperson_righthand': {'rotation': [0, 0, 0], 'translation': [0, 3, 1], 'scale': [0.55, 0.55, 0.55]},
             'thirdperson_lefthand': {'rotation': [0, 0, 0], 'translation': [0, 3, 1], 'scale': [0.55, 0.55, 0.55]},
             'firstperson_righthand': {'rotation': [0, -90, 25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
             'firstperson_lefthand': {'rotation': [0, 90, -25], 'translation': [1.13, 3.2, 1.13], 'scale': [0.68, 0.68, 0.68]},
             'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
             'head': {'rotation': [0, 180, 0], 'translation': [0, 9, 0], 'scale': [1.1, 1.1, 1.1]},
             'fixed': {'rotation': [0, 180, 0], 'scale': [1, 1, 1]},
             'gui': {'rotation': [25, 145, 0], 'translation': [0, 0, 0], 'scale': [0.9, 0.9, 0.9]}}
DISP_LONGO = dict(DISP_ITEM)
DISP_LONGO.update({'thirdperson_righthand': {'rotation': [0, 90, 55], 'translation': [0, 4, 2.5], 'scale': [0.85, 0.85, 0.85]},
                   'thirdperson_lefthand': {'rotation': [0, -90, -55], 'translation': [0, 4, 2.5], 'scale': [0.85, 0.85, 0.85]},
                   'firstperson_righthand': {'rotation': [0, 90, 25], 'translation': [0, 1.6, 0.8], 'scale': [0.68, 0.68, 0.68]},
                   'firstperson_lefthand': {'rotation': [0, -90, -25], 'translation': [0, 1.6, 0.8], 'scale': [0.68, 0.68, 0.68]},
                   'gui': {'rotation': [0, 0, -45], 'translation': [0, 0, 0], 'scale': [0.62, 0.62, 0.62]}})
DISP_DECOR = {'fixed': {'rotation': [0, 0, 0], 'scale': [1, 1, 1]}, 'gui': {'rotation': [25, 145, 0], 'scale': [0.6, 0.6, 0.6]},
              'ground': {'scale': [0.3, 0.3, 0.3]}}


def eixo(m, nome, y0, y1, r, tom, cx=8, cz=8):
    m.cubo(nome, [cx - r, y0, cz - r], [cx + r, y1, cz + r], tom)


# ---------------------------------------------------------------- batata quente
m = Modelo('batata_quente', 128)
m.cubo('corpo', [3.5, 2, 4.5], [12.5, 9, 11.5], 'batata')
m.cubo('ponta_e', [2.2, 3, 5.5], [3.5, 8, 10.5], 'batata')
m.cubo('ponta_d', [12.5, 3, 5.2], [13.8, 7.6, 10.2], 'batata')
m.cubo('topo', [4.5, 9, 5.5], [11.5, 10.2, 10.5], 'batata')
m.cubo('base', [4.5, 1, 5.5], [11.5, 2, 10.5], 'batata')
m.cubo('frente', [4.5, 3, 3.6], [11.5, 8.4, 4.5], 'batata')
m.cubo('tras', [4.5, 3, 11.5], [11.5, 8.4, 12.4], 'batata')
for i, (x, y) in enumerate(((5.0, 3.8), (10.0, 7.4), (8.6, 2.6))):
    m.cubo(f'olhinho{i}', [x, y, 3.45], [x + 0.9, y + 0.7, 3.65], 'batata_clara')
m.cubo('olho_e', [5.6, 6.0, 3.4], [6.8, 7.3, 3.65], 'olho')
m.cubo('olho_d', [9.2, 6.0, 3.4], [10.4, 7.3, 3.65], 'olho')
m.cubo('boca', [6.6, 4.2, 3.4], [9.4, 5.0, 3.65], 'boca')
m.cubo('rachadura1', [4.6, 8.2, 3.5], [7.0, 8.6, 3.7], 'brasa', brilho=True)
m.cubo('rachadura2', [11.6, 4.0, 6.2], [12.6, 6.4, 6.6], 'brasa', brilho=True)
m.cubo('rachadura3', [8.0, 2.2, 11.6], [10.4, 2.6, 12.5], 'brasa', brilho=True)
m.cubo('pavio1', [7.5, 10.2, 7.5], [8.5, 12.2, 8.5], 'pavio')
m.cubo('pavio2', [8.0, 12.0, 7.5], [9.0, 13.6, 8.5], 'pavio', rot={'angle': -22.5, 'axis': 'z', 'origin': [8, 12, 8]})
m.cubo('faisca', [8.6, 13.4, 7.3], [10.0, 14.8, 8.7], 'fogo', brilho=True)
m.cubo('faisca2', [9.0, 14.6, 7.6], [9.8, 15.6, 8.4], 'brasa', brilho=True)
m.salvar(DISP_ITEM)

# ---------------------------------------------------------------- taco de sinuca
m = Modelo('taco', 64)
eixo(m, 'ponteira', -9.0, -8.2, 1.15, 'preto')
eixo(m, 'cabo', -8.2, 1.0, 1.05, 'mad_escura')
eixo(m, 'empunhadura', -6.5, -1.0, 1.12, 'couro')
eixo(m, 'anel', 1.0, 1.6, 1.1, 'latao')
eixo(m, 'meio', 1.6, 14.0, 0.85, 'mad_clara')
for i, y in enumerate((2.4, 4.4, 6.4)):
    m.cubo(f'losango{i}', [7.0, y, 7.05], [9.0, y + 1.2, 7.2], 'mad_escura')
eixo(m, 'ponta', 14.0, 26.0, 0.6, 'mad_clara')
eixo(m, 'virola', 26.0, 27.2, 0.62, 'branco')
eixo(m, 'sola', 27.2, 28.0, 0.58, 'giz')
m.salvar(DISP_LONGO)

# ---------------------------------------------------------------- espada de torneio (Resta 1)
m = Modelo('espada_torneio', 64)
eixo(m, 'pomo', -5.4, -4.2, 1.2, 'latao')
eixo(m, 'cabo', -4.2, 1.0, 0.85, 'tecido_vermelho')
for i, y in enumerate((-3.2, -1.6, 0.0)):
    eixo(m, f'faixa{i}', y, y + 0.5, 0.9, 'couro')
m.cubo('guarda', [3.4, 1.0, 7.0], [12.6, 2.4, 9.0], 'latao')
m.cubo('guarda_ponta_e', [2.6, 1.6, 7.2], [3.4, 3.2, 8.8], 'latao')
m.cubo('guarda_ponta_d', [12.6, 1.6, 7.2], [13.4, 3.2, 8.8], 'latao')
m.cubo('lamina', [6.2, 2.4, 7.2], [9.8, 19.0, 8.8], 'acolchoado')
m.cubo('costura_e', [6.0, 2.4, 7.3], [6.3, 19.0, 8.7], 'tecido_azul')
m.cubo('costura_d', [9.7, 2.4, 7.3], [10.0, 19.0, 8.7], 'tecido_azul')
m.cubo('ponta', [6.8, 19.0, 7.4], [9.2, 20.8, 8.6], 'acolchoado')
m.cubo('emblema', [7.2, 4.0, 7.0], [8.8, 5.6, 7.25], 'tecido_vermelho')
m.salvar(DISP_LONGO)

# ---------------------------------------------------------------- pá de spleef
m = Modelo('pa_spleef', 64)
m.cubo('alca_base', [6.0, -6.2, 7.3], [10.0, -5.4, 8.7], 'cabo_azul')
m.cubo('alca_e', [6.0, -5.4, 7.3], [6.8, -2.6, 8.7], 'cabo_azul')
m.cubo('alca_d', [9.2, -5.4, 7.3], [10.0, -2.6, 8.7], 'cabo_azul')
m.cubo('alca_topo', [6.0, -2.6, 7.3], [10.0, -1.8, 8.7], 'cabo_azul')
eixo(m, 'cabo', -1.8, 12.0, 0.7, 'mad_media')
eixo(m, 'presilha', 11.0, 12.6, 0.95, 'ferro')
m.cubo('lamina', [4.6, 12.6, 7.4], [11.4, 20.6, 8.6], 'gelo')
m.cubo('lamina_ponta', [5.4, 20.6, 7.5], [10.6, 22.0, 8.5], 'gelo')
m.cubo('lamina_borda_e', [4.2, 13.0, 7.3], [4.6, 20.4, 8.7], 'gelo_esc')
m.cubo('lamina_borda_d', [11.4, 13.0, 7.3], [11.8, 20.4, 8.7], 'gelo_esc')
m.cubo('floco', [7.4, 16.0, 7.2], [8.6, 17.2, 7.45], 'branco', brilho=True)
m.salvar(DISP_LONGO)

# ---------------------------------------------------------------- travesseiro
m = Modelo('travesseiro', 128)
m.cubo('miolo', [2.5, 4.5, 5.0], [13.5, 11.5, 11.0], 'fronha')
m.cubo('borda_cima', [3.0, 11.5, 5.6], [13.0, 12.2, 10.4], 'fronha')
m.cubo('borda_baixo', [3.0, 3.8, 5.6], [13.0, 4.5, 10.4], 'fronha')
m.cubo('borda_e', [1.8, 5.0, 5.6], [2.5, 11.0, 10.4], 'fronha')
m.cubo('borda_d', [13.5, 5.0, 5.6], [14.2, 11.0, 10.4], 'fronha')
for i, (x, y) in enumerate(((2.0, 11.6), (13.2, 11.6), (2.0, 3.6), (13.2, 3.6))):
    m.cubo(f'pontinha{i}', [x - 0.6, y - 0.6, 7.2], [x + 0.8, y + 0.8, 8.8], 'fronha')
for i, y in enumerate((6.0, 9.0)):
    m.cubo(f'listra{i}', [2.5, y, 4.9], [13.5, y + 1.0, 11.1], 'fronha_listra')
m.cubo('pena1', [11.0, 12.0, 7.2], [11.6, 14.0, 8.2], 'pena', rot={'angle': 22.5, 'axis': 'z', 'origin': [11.3, 12, 7.7]})
m.cubo('pena2', [4.2, 2.0, 7.4], [4.8, 3.9, 8.4], 'pena', rot={'angle': -22.5, 'axis': 'z', 'origin': [4.5, 3.9, 7.9]})
m.salvar(DISP_ITEM)

# ---------------------------------------------------------------- Boneca Caipira (Batatinha Frita)
# corpo: pés em y=-16, pescoço em y=13. A frente é -z.
m = Modelo('boneca_corpo', 128)
for lado, x0 in (('e', 4.6), ('d', 8.4)):
    m.cubo('perna_' + lado, [x0, -14.0, 6.8], [x0 + 3.0, -6.0, 9.2], 'pele')
    m.cubo('meia_' + lado, [x0 - 0.1, -14.0, 6.7], [x0 + 3.1, -11.5, 9.3], 'branco')
    m.cubo('sapato_' + lado, [x0 - 0.3, -16.0, 5.6], [x0 + 3.3, -14.0, 9.6], 'sapato')
m.cubo('saia', [2.0, -8.0, 3.8], [14.0, 1.0, 12.2], 'xadrez_v')
m.cubo('saia_barra', [1.8, -8.4, 3.6], [14.2, -7.4, 12.4], 'branco')
m.cubo('avental', [4.6, -7.0, 3.5], [11.4, 3.0, 3.8], 'avental')
m.cubo('tronco', [3.6, 1.0, 5.4], [12.4, 11.0, 10.6], 'xadrez_v')
m.cubo('gola', [4.2, 10.2, 5.0], [11.8, 11.6, 11.0], 'branco')
for i, y in enumerate((3.0, 5.5, 8.0)):
    m.cubo(f'botao{i}', [7.4, y, 5.2], [8.6, y + 1.0, 5.45], 'botao')
m.cubo('pescoco', [6.6, 11.0, 6.8], [9.4, 13.0, 9.2], 'pele')
for lado, x0, ang in (('e', 1.0, 10), ('d', 12.6, -10)):
    rot = {'angle': ang * 2.25, 'axis': 'z', 'origin': [x0 + 1.2, 10.5, 8]}
    m.cubo('manga_' + lado, [x0, 6.5, 6.2], [x0 + 2.6, 11.0, 9.8], 'xadrez_v', rot=rot)
    m.cubo('braco_' + lado, [x0 + 0.3, 0.5, 6.6], [x0 + 2.3, 6.5, 9.4], 'pele', rot=rot)
    m.cubo('mao_' + lado, [x0 + 0.1, -1.0, 6.4], [x0 + 2.5, 0.5, 9.6], 'pele', rot=rot)
m.salvar(DISP_DECOR)

# cabeça: pivô (pescoço) em (8, 0, 8)
m = Modelo('boneca_cabeca', 128)
m.cubo('cabeca', [2.0, 0.0, 2.0], [14.0, 12.0, 14.0], 'pele')
m.cubo('cabelo_topo', [1.6, 10.0, 1.8], [14.4, 12.8, 14.4], 'tranca')
m.cubo('cabelo_nuca', [1.6, 2.0, 13.4], [14.4, 12.0, 14.6], 'tranca')
m.cubo('franja', [1.8, 9.0, 1.6], [14.2, 10.6, 2.6], 'tranca')
for lado, x0 in (('e', 0.4), ('d', 14.4)):
    m.cubo('lateral_' + lado, [x0 + (0.8 if lado == 'e' else -0.4), 3.0, 2.4], [x0 + (1.6 if lado == 'e' else 0.4), 12.0, 14.0], 'tranca')
    m.cubo('tranca_' + lado, [x0, -8.0, 9.0], [x0 + 1.6, 4.0, 10.6], 'tranca')
    m.cubo('laco_' + lado, [x0 - 0.6, -6.0, 8.4], [x0 + 2.2, -4.6, 11.2], 'laco')
m.cubo('olho_e', [4.4, 5.6, 1.7], [6.6, 7.8, 2.0], 'olho')
m.cubo('olho_d', [9.4, 5.6, 1.7], [11.6, 7.8, 2.0], 'olho')
m.cubo('brilho_e', [5.6, 7.0, 1.6], [6.2, 7.6, 1.75], 'branco')
m.cubo('brilho_d', [10.6, 7.0, 1.6], [11.2, 7.6, 1.75], 'branco')
m.cubo('bochecha_e', [3.0, 3.8, 1.75], [5.0, 4.8, 2.0], 'bochecha')
m.cubo('bochecha_d', [11.0, 3.8, 1.75], [13.0, 4.8, 2.0], 'bochecha')
m.cubo('boca', [6.6, 2.8, 1.75], [9.4, 3.4, 2.0], 'laco')
m.cubo('chapeu_aba', [-2.0, 11.6, -2.0], [18.0, 12.6, 18.0], 'palha')
m.cubo('chapeu_copa', [3.0, 12.6, 3.0], [13.0, 17.0, 13.0], 'palha')
m.cubo('chapeu_fita', [2.9, 12.6, 2.9], [13.1, 13.8, 13.1], 'laco')
m.cubo('flor', [11.0, 13.0, 2.4], [13.0, 15.0, 2.9], 'bola_amarela')
m.salvar(DISP_DECOR)

# ---------------------------------------------------------------- bolas de sinuca
for nome, tom, listra in (('bola_1', 'bola_amarela', False), ('bola_3', 'bola_vermelha', False),
                          ('bola_8', 'bola_preta', False), ('bola_branca', 'bola_branca', False)):
    m = Modelo(nome, 128)
    m.cubo('nucleo', [3.0, 3.0, 3.0], [13.0, 13.0, 13.0], tom)
    m.cubo('x', [2.0, 4.5, 4.5], [14.0, 11.5, 11.5], tom)
    m.cubo('y', [4.5, 2.0, 4.5], [11.5, 14.0, 11.5], tom)
    m.cubo('z', [4.5, 4.5, 2.0], [11.5, 11.5, 14.0], tom)
    if nome != 'bola_branca':
        m.cubo('circulo', [6.0, 6.0, 1.8], [10.0, 10.0, 2.05], 'bola_branca')
        m.cubo('numero', [7.4, 6.8, 1.7], [8.6, 9.2, 1.85], 'preto')
    m.salvar(DISP_DECOR)

# ---------------------------------------------------------------- coroa
m = Modelo('coroa', 128)
m.cubo('aro', [2.5, 0.0, 2.5], [13.5, 3.0, 13.5], 'ouro')
m.cubo('veludo', [3.2, 2.0, 3.2], [12.8, 5.5, 12.8], 'veludo')
for i, (x, z) in enumerate(((2.5, 2.5), (7.0, 2.5), (11.5, 2.5), (2.5, 11.5), (7.0, 11.5), (11.5, 11.5), (2.5, 7.0), (11.5, 7.0))):
    m.cubo(f'ponta{i}', [x, 3.0, z], [x + 2.0, 6.5, z + 2.0], 'ouro')
    m.cubo(f'perola{i}', [x + 0.5, 6.5, z + 0.5], [x + 1.5, 7.5, z + 1.5], 'branco')
for i, (x, tom) in enumerate(((4.0, 'esmeralda'), (7.2, 'rubi'), (10.4, 'safira'))):
    m.cubo(f'gema{i}', [x, 0.8, 2.3], [x + 1.6, 2.2, 2.55], tom, brilho=True)
m.cubo('cruz_v', [7.4, 5.5, 7.4], [8.6, 10.0, 8.6], 'ouro')
m.cubo('cruz_h', [6.2, 8.0, 7.4], [9.8, 9.0, 8.6], 'ouro')
m.salvar(DISP_ITEM)

print('ok: batata_quente, taco, espada_torneio, pa_spleef, travesseiro, boneca_corpo, boneca_cabeca, bolas, coroa')
