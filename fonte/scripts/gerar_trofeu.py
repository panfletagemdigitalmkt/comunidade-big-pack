# Troféu do Boitatá: taça dourada com fogo, serpente de fogo enrolada e base de madeira com plaquinha.
from voxel import cor
import armadura as A

Modelo, TONS = A.carregar_modelo('dungeon')
TONS.update({'ouro': [cor('d9a62e'), cor('f0c75a'), cor('c4952a'), cor('e8b93a')],
             'madeira': [cor('3b2416'), cor('4a2e1b'), cor('331f12')],
             'fogo': [cor('ff6a00'), cor('ffb000'), cor('ffd23f'), cor('ff3d00')],
             'escama': [cor('c2410c'), cor('ea580c'), cor('9a3412'), cor('f97316')],
             'brasa': [cor('fff3b0'), cor('ffe680')]})
t = Modelo('trofeu_boitata', 128)
t.cubo('base', [3, 0, 3], [13, 2, 13], 'madeira')
t.cubo('friso', [2.6, 2, 2.6], [13.4, 2.6, 13.4], 'ouro')
t.cubo('degrau', [4, 2.6, 4], [12, 4, 12], 'madeira')
t.cubo('placa', [5, 0.5, 2.6], [11, 1.7, 3], 'ouro')
t.cubo('haste', [7, 4, 7], [9, 6.2, 9], 'ouro')
t.cubo('no', [6.4, 6.2, 6.4], [9.6, 7, 9.6], 'ouro')
t.cubo('fundo', [5, 7, 5], [11, 8, 11], 'ouro')
t.cubo('taca', [4, 8, 4], [12, 11, 12], 'ouro')
t.cubo('borda', [3.5, 11, 3.5], [12.5, 11.8, 12.5], 'ouro')
t.cubo('alca_e', [2, 8.5, 7.2], [4, 10.6, 8.8], 'ouro')
t.cubo('alca_d', [12, 8.5, 7.2], [14, 10.6, 8.8], 'ouro')
t.cubo('fogo', [4.5, 11.2, 4.5], [11.5, 12.6, 11.5], 'fogo', brilho=True)
t.cubo('chama1', [6, 12.6, 6], [8.2, 15.2, 8.2], 'fogo', brilho=True)
t.cubo('chama2', [8.4, 12.6, 7.5], [10.2, 14.4, 9.3], 'fogo', brilho=True)
t.cubo('chama3', [6.8, 12.6, 8.8], [8.4, 14, 10.4], 'brasa', brilho=True)
t.cubo('chama_topo', [6.6, 15.2, 6.6], [7.6, 16, 7.6], 'brasa', brilho=True)
# serpente de fogo dando a volta na taça, subindo, com a cabeça na frente
t.cubo('cauda', [11.4, 4, 9], [12.4, 5, 12], 'escama')
t.cubo('corpo1', [11.6, 5, 4], [12.6, 6, 12], 'escama')
t.cubo('corpo2', [4, 6, 3.2], [12.6, 7, 4.2], 'escama')
t.cubo('corpo3', [3.2, 7, 3.2], [4.2, 8.4, 12.6], 'escama')
t.cubo('corpo4', [4.2, 8.4, 11.8], [12.4, 9.4, 12.8], 'escama')
t.cubo('corpo5', [12, 9.4, 5], [13, 10.6, 12.8], 'escama')
t.cubo('pescoco', [8, 10, 2.6], [12.8, 11, 3.6], 'escama')
t.cubo('cabeca', [5, 10.5, 1.4], [8.5, 12.8, 4], 'escama')
t.cubo('focinho', [5.6, 10.6, 0.4], [7.9, 12, 1.4], 'escama')
t.cubo('olho_e', [5, 12, 1.2], [5.8, 12.6, 1.5], 'olho', brilho=True)
t.cubo('olho_d', [7.7, 12, 1.2], [8.5, 12.6, 1.5], 'olho', brilho=True)
t.cubo('lingua', [6.5, 10.7, -0.6], [7, 11, 0.4], 'brasa', brilho=True)
t.salvar({'gui': {'rotation': [20, -150, 0], 'translation': [0, -0.5, 0], 'scale': [0.72, 0.72, 0.72]},
          'ground': {'translation': [0, 2, 0], 'scale': [0.5, 0.5, 0.5]},
          'fixed': {'rotation': [0, 0, 0], 'translation': [0, 0, 0], 'scale': [1, 1, 1]},
          'head': {'rotation': [0, 180, 0], 'translation': [0, 9, 0], 'scale': [0.8, 0.8, 0.8]},
          'thirdperson_righthand': {'rotation': [0, 180, 0], 'translation': [0, 2, 2], 'scale': [0.45, 0.45, 0.45]},
          'thirdperson_lefthand': {'rotation': [0, 180, 0], 'translation': [0, 2, 2], 'scale': [0.45, 0.45, 0.45]},
          'firstperson_righthand': {'rotation': [0, 200, 0], 'translation': [0, 2, 0], 'scale': [0.45, 0.45, 0.45]},
          'firstperson_lefthand': {'rotation': [0, 200, 0], 'translation': [0, 2, 0], 'scale': [0.45, 0.45, 0.45]}})
print('trofeu ok')
