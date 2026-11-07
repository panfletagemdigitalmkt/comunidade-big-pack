# Modelos 3D dos chefes e monstros da Masmorra da Mata Sombria.
# Cada um é um item 3D mostrado por uma display entity em cima de um mob invisível (o plugin anima).
# Unidades: 16 = 1 bloco. O pé de todos fica em y = -16.
from voxel import cor
import armadura as A

Modelo, TONS = A.carregar_modelo('dungeon')
TONS.update({
    'casca': [cor('3b2a1d'), cor('4a3524'), cor('2e2117'), cor('56402c')],
    'casca_clara': [cor('6b5236'), cor('7a5f3f')],
    'musgo': [cor('3f6b2a'), cor('4f7d33'), cor('35592a')],
    'folha': [cor('2f5e2b'), cor('3a6e34'), cor('284f25'), cor('4a7a2c')],
    'chama': [cor('ff3d00'), cor('ff6a00'), cor('ff9500'), cor('ffb000')],
    'brasa': [cor('fff3b0'), cor('ffe680'), cor('ffd23f')],
    'olho_verde': [cor('b6ff3a'), cor('d9ff7a')],
    'olho_vermelho': [cor('ff1a1a'), cor('ff4d4d')],
    'olho_ciano': [cor('5ff2ff'), cor('b8fbff')],
    'olho_fogo': [cor('fffbe6'), cor('fff3b0')],
    'pele_escura': [cor('2a1a12'), cor('34211a'), cor('3d2a20')],
    'vermelho': [cor('b3101a'), cor('c8141f'), cor('9a0d16')],
    'boca': [cor('120807'), cor('1c0d0b')],
    'madeira': [cor('5a3a22'), cor('6b4428'), cor('4a2e1a')],
    'vento': [cor('dfe7ec'), cor('c9d3da'), cor('eef3f6')],
    'pelo_negro': [cor('17120f'), cor('211a16'), cor('2b2320'), cor('120e0c')],
    'manto': [cor('2a1638'), cor('341b46'), cor('22112e'), cor('3d2152')],
    'escama_verde': [cor('3d5a1e'), cor('4c6e25'), cor('324a19'), cor('5a7d2c')],
    'cabelo': [cor('d9b13a'), cor('e8c454'), cor('c49a2a')],
    'escama_fogo': [cor('7a1c0a'), cor('9a2a0c'), cor('5c1407'), cor('b53a10')],
    'sombra': [cor('0a0a0d'), cor('121216'), cor('0e0e12'), cor('18181e')],
    'fantasma': [cor('b9c6d3'), cor('a7b6c6'), cor('cbd6e0'), cor('95a5b6')],
    'roxo_marca': [cor('9b5cff'), cor('b98aff')],
    'aranha': [cor('1e1a22'), cor('2a2430'), cor('16121a')],
    'basalto': [cor('2b2b30'), cor('3a3a40'), cor('222226')],
    'ferro': [cor('6e7378'), cor('8a9096')],
})

def mob(nome, tam=128):
    return Modelo(nome, tam)

SEM = {'fixed': {'scale': [1, 1, 1]}, 'gui': {'rotation': [15, -150, 0], 'translation': [0, -2, 0], 'scale': [0.4, 0.4, 0.4]}}

# ======================================================== CURUPIRA: corpo de casca, cabelo de fogo, pés virados
m = mob('curupira', 256)
for lado, x0 in (('e', 2), ('d', 11)):
    m.cubo('perna_' + lado, [x0, -14, 6], [x0 + 3, -3, 9.5], 'casca')
    m.cubo('pe_' + lado, [x0 - 0.5, -16, 7], [x0 + 3.5, -14, 14], 'casca')          # pé virado para trás
    for i in range(3):
        m.cubo(f'garra_pe_{lado}{i}', [x0 - 0.3 + i * 1.3, -16, 14], [x0 + 0.6 + i * 1.3, -15, 15.6], 'dente')
m.cubo('tanga', [1, -6, 4.5], [15, -1, 11.5], 'folha')
m.cubo('tanga_tiras', [1.5, -9, 5], [14.5, -6, 11], 'folha')
m.cubo('tronco', [2.5, -3, 5], [13.5, 8, 11], 'casca')
for i, y in enumerate((0, 2, 4)):
    m.cubo(f'costela{i}', [3, y, 4.6], [13, y + 0.7, 5], 'casca_clara')
m.cubo('musgo_ombro', [1.5, 6, 4.5], [14.5, 8.6, 11.5], 'musgo')
for lado, x0, ang in (('e', -2, -22.5), ('d', 14, 22.5)):
    rot = {'angle': ang, 'axis': 'z', 'origin': [x0 + 2, 7, 7.5]}
    m.cubo('braco_' + lado, [x0, -6, 6], [x0 + 3.5, 7, 9], 'casca', rot=rot)
    m.cubo('mao_' + lado, [x0 - 0.5, -9.5, 5.5], [x0 + 4, -6, 9.5], 'casca', rot=rot)
    for i in range(3):
        m.cubo(f'garra_{lado}{i}', [x0 - 0.3 + i * 1.5, -12.5, 6 + i * 0.6], [x0 + 0.7 + i * 1.5, -9.5, 7 + i * 0.6], 'dente', rot=rot)
m.cubo('tacape', [16.5, -14, 2], [19.5, 3, 5.5], 'madeira', rot={'angle': 22.5, 'axis': 'x', 'origin': [18, -6, 4]})
m.cubo('tacape_ponta', [15.5, -18 + 2, 0.5], [20.5, -10, 7], 'madeira', rot={'angle': 22.5, 'axis': 'x', 'origin': [18, -6, 4]})
m.cubo('cabeca', [3, 8, 4], [13, 17, 12], 'casca')
m.cubo('queixo', [4, 6.5, 3.4], [12, 9, 8], 'casca')
m.cubo('boca', [4.5, 8.4, 3.2], [11.5, 10.2, 3.6], 'boca')
for i, x in enumerate((4.8, 6.2, 7.6, 9.0, 10.4)):
    m.cubo(f'dente{i}', [x, 9.4, 3.0], [x + 0.8, 10.6, 3.3], 'dente')
m.cubo('sobrancelha', [3.5, 13.8, 3.6], [12.5, 15, 4.2], 'casca_clara')
m.cubo('olho_e', [4.5, 12, 3.7], [7, 13.6, 4], 'olho_verde', brilho=True)
m.cubo('olho_d', [9, 12, 3.7], [11.5, 13.6, 4], 'olho_verde', brilho=True)
m.cubo('nariz', [7.2, 10.5, 2.8], [8.8, 12.6, 4], 'casca_clara')
# cabelo de fogo
m.cubo('fogo_base', [2, 16.5, 3.5], [14, 20, 12.5], 'chama', brilho=True)
m.cubo('fogo_e', [1, 18, 5], [6, 25, 10], 'chama', brilho=True, rot={'angle': 22.5, 'axis': 'z', 'origin': [4, 18, 8]})
m.cubo('fogo_d', [10, 18, 5], [15, 26, 10], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'z', 'origin': [12, 18, 8]})
m.cubo('fogo_meio', [5, 19, 6], [11, 29, 11], 'chama', brilho=True)
m.cubo('fogo_ponta', [6.5, 28, 7], [9.5, 32, 10], 'brasa', brilho=True)
m.cubo('fogo_tras', [4, 14, 11.5], [12, 22, 15], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 14, 12]})
m.salvar(SEM)

# ======================================================== SACI: perneta, gorro vermelho, sorriso e cachimbo em brasa
m = mob('saci', 256)
m.cubo('redemoinho1', [3, -16, 4], [13, -14.5, 14], 'vento')
m.cubo('redemoinho2', [1, -14.5, 2], [15, -13, 16], 'vento', rot={'angle': 45, 'axis': 'y', 'origin': [8, -14, 9]})
m.cubo('redemoinho3', [4.5, -13, 5.5], [11.5, -11.5, 12.5], 'vento')
m.cubo('pe', [5.5, -12, 6], [10.5, -10, 11.5], 'pele_escura')
m.cubo('perna', [6, -10, 7], [10, 3, 10], 'pele_escura')
m.cubo('calcao', [3.5, 1, 5], [12.5, 6, 11], 'vermelho')
m.cubo('tronco', [4, 6, 5.5], [12, 15, 10.5], 'pele_escura')
for lado, x0, ang in (('e', 1.5, -22.5), ('d', 12, 22.5)):
    rot = {'angle': ang, 'axis': 'z', 'origin': [x0 + 1.2, 14, 8]}
    m.cubo('braco_' + lado, [x0, 4, 7], [x0 + 2.5, 15, 9], 'pele_escura', rot=rot)
    m.cubo('dedos_' + lado, [x0 - 0.3, 1.5, 6.6], [x0 + 2.8, 4, 9.4], 'pele_escura', rot=rot)
m.cubo('cabeca', [3.5, 15, 4], [12.5, 23, 12], 'pele_escura')
m.cubo('sorriso', [4.5, 16.4, 3.7], [11.5, 18.2, 4], 'boca')
for i, x in enumerate((4.8, 6.0, 7.2, 8.4, 9.6, 10.6)):
    m.cubo(f'dente{i}', [x, 17.4, 3.5], [x + 0.6, 18.2, 3.8], 'dente')
m.cubo('olho_e', [4.6, 19.5, 3.7], [6.8, 20.8, 4], 'olho_vermelho', brilho=True)
m.cubo('olho_d', [9.2, 19.5, 3.7], [11.4, 20.8, 4], 'olho_vermelho', brilho=True)
m.cubo('orelha_e', [2.5, 18, 7], [3.5, 21, 9], 'pele_escura')
m.cubo('orelha_d', [12.5, 18, 7], [13.5, 21, 9], 'pele_escura')
m.cubo('gorro', [3, 22, 3.5], [13, 25, 12.5], 'vermelho')
m.cubo('gorro2', [4.5, 25, 5], [11.5, 28, 11], 'vermelho', rot={'angle': -22.5, 'axis': 'z', 'origin': [8, 25, 8]})
m.cubo('gorro_ponta', [7, 27, 6.5], [11, 31, 9.5], 'vermelho', rot={'angle': -45, 'axis': 'z', 'origin': [9, 27, 8]})
m.cubo('cachimbo', [10.5, 16.6, 0.5], [11.5, 17.4, 4], 'madeira')
m.cubo('fornilho', [10.2, 17.4, -0.6], [12.8, 20.4, 1.6], 'madeira')
m.cubo('brasa', [10.5, 20, -0.3], [12.5, 20.8, 1.3], 'brasa', brilho=True)
m.salvar(SEM)

# ======================================================== MULA SEM CABEÇA: corpo negro, cascos em brasa, fogo no pescoço
m = mob('mula', 256)
m.cubo('corpo', [1, -4, -4], [15, 8, 24], 'pelo_negro')
m.cubo('anca', [0.5, -2, 16], [15.5, 9, 24.5], 'pelo_negro')
for i, z in enumerate((2, 7, 12, 17)):
    m.cubo(f'costela_e{i}', [0.6, -1, z], [0.9, 6, z + 1.2], 'dente')
    m.cubo(f'costela_d{i}', [15.1, -1, z], [15.4, 6, z + 1.2], 'dente')
for i, (x, z) in enumerate(((2, -2), (10, -2), (2, 18), (10, 18))):
    m.cubo(f'perna{i}', [x, -14, z], [x + 4, -3, z + 4], 'pelo_negro')
    m.cubo(f'casco{i}', [x - 0.5, -16, z - 0.5], [x + 4.5, -14, z + 4.5], 'brasa', brilho=True)
m.cubo('arreio', [0.4, 2, 5], [15.6, 3.2, 6.2], 'ferro')
m.cubo('corrente', [7, -6, 5], [9, 2.4, 6], 'ferro')
m.cubo('pescoco', [3.5, 3, -11], [12.5, 12, -3], 'pelo_negro', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 6, -4]})
m.cubo('toco', [4, 9, -15], [12, 12, -9], 'brasa', brilho=True, rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 6, -4]})
m.cubo('fogo1', [2.5, 11, -16], [13.5, 18, -7], 'chama', brilho=True)
m.cubo('fogo2', [4.5, 17, -15], [11.5, 25, -8], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 17, -11]})
m.cubo('fogo3', [6, 24, -14], [10, 31, -10], 'brasa', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 24, -12]})
m.cubo('crina_fogo', [6, 8, -6], [10, 13, 6], 'chama', brilho=True)
m.cubo('cauda_fogo', [6, 0, 24], [10, 8, 31], 'chama', brilho=True, rot={'angle': -22.5, 'axis': 'x', 'origin': [8, 6, 24]})
m.salvar(SEM)

# ======================================================== CUCA: bruxa-jacaré, manto roxo, cabelo de palha, garras
m = mob('cuca', 256)
m.cubo('manto_baixo', [0, -16, 2], [16, -2, 16], 'manto')
m.cubo('barra', [-0.5, -16, 1.5], [16.5, -14, 16.5], 'sombra')
m.cubo('manto_meio', [1, -2, 3], [15, 8, 15], 'manto')
m.cubo('corcunda', [1.5, 6, 6], [14.5, 13, 16], 'manto')
m.cubo('ombros', [-0.5, 7, 2], [16.5, 11, 13], 'manto')
for lado, x0 in (('e', -4), ('d', 16)):
    m.cubo('braco_' + lado, [x0, -3, 3], [x0 + 4, 10, 8], 'manto')
    m.cubo('mao_' + lado, [x0 - 0.5, -7, 2], [x0 + 4.5, -3, 8], 'escama_verde')
    for i in range(4):
        m.cubo(f'unha_{lado}{i}', [x0 - 0.3 + i * 1.2, -10, 2.5], [x0 + 0.5 + i * 1.2, -7, 3.5], 'dente')
m.cubo('cabelo_costas', [1, -4, 11], [15, 14, 16.5], 'cabelo')
m.cubo('cabelo_topo', [2, 17, 1], [14, 20.5, 13], 'cabelo')
m.cubo('cabelo_lado_e', [0.5, 6, 1], [2.5, 19, 12], 'cabelo')
m.cubo('cabelo_lado_d', [13.5, 6, 1], [15.5, 19, 12], 'cabelo')
m.cubo('cranio', [2.5, 10, 0], [13.5, 18, 11], 'escama_verde')
m.cubo('focinho', [4, 10.5, -14], [12, 15.5, 0.5], 'escama_verde')
m.cubo('mandibula', [4.5, 7.5, -13], [11.5, 10.5, 0.5], 'escama_verde', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, 10, 0]})
m.cubo('boca', [4.6, 10, -12.5], [11.4, 10.6, 0], 'boca')
for i, z in enumerate(range(-12, 0, 2)):
    m.cubo(f'dente_e{i}', [4.3, 9, z], [4.9, 10.8, z + 0.8], 'dente')
    m.cubo(f'dente_d{i}', [11.1, 9, z], [11.7, 10.8, z + 0.8], 'dente')
m.cubo('narinas', [6.5, 15.5, -13.5], [9.5, 16.2, -11.5], 'boca')
m.cubo('olho_e', [3.2, 15.8, -2], [6.2, 18.6, 1], 'escama_verde')
m.cubo('olho_d', [9.8, 15.8, -2], [12.8, 18.6, 1], 'escama_verde')
m.cubo('pupila_e', [3.6, 16.4, -2.3], [5.8, 18, -2], 'olho', brilho=True)
m.cubo('pupila_d', [10.2, 16.4, -2.3], [12.4, 18, -2], 'olho', brilho=True)
for i, z in enumerate((-8, -4, 2, 6)):
    m.cubo(f'escama_topo{i}', [7, 15.5 if z < 0 else 18, z], [9, 17 if z < 0 else 19.5, z + 2], 'escama_verde')
m.salvar(SEM)

# ======================================================== BOITATÁ: cabeça de serpente com olhos de fogo + gomos do corpo
m = mob('boitata_cabeca', 256)
m.cubo('cranio', [0, -2, -2], [16, 10, 16], 'escama_fogo')
m.cubo('focinho', [2, 1, -15], [14, 8, -2], 'escama_fogo')
m.cubo('mandibula', [2.5, -6, -14], [13.5, -1, -2], 'escama_fogo', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, -1, -2]})
m.cubo('garganta', [3.5, -2, -13], [12.5, 1, -3], 'brasa', brilho=True)
for x in (2.8, 11.6):
    m.cubo(f'presa_cima{x}', [x, -3, -14.6], [x + 1.6, 1.2, -13], 'dente')
    m.cubo(f'presa_baixo{x}', [x + 0.4, -4.5, -11], [x + 1.6, -1.5, -10], 'dente', rot={'angle': 22.5, 'axis': 'x', 'origin': [8, -1, -2]})
m.cubo('olho_e', [-0.4, 5, -5.5], [3.6, 8, -0.5], 'chama', brilho=True)
m.cubo('olho_d', [12.4, 5, -5.5], [16.4, 8, -0.5], 'chama', brilho=True)
m.cubo('pupila_e', [-0.7, 5.2, -3.4], [-0.4, 7.8, -2.6], 'boca')
m.cubo('pupila_d', [16.4, 5.2, -3.4], [16.7, 7.8, -2.6], 'boca')
m.cubo('sobrancelha_e', [-1, 8, -7], [5, 10.5, 0], 'escama_fogo', rot={'angle': -22.5, 'axis': 'z', 'origin': [2, 9, -3]})
m.cubo('sobrancelha_d', [11, 8, -7], [17, 10.5, 0], 'escama_fogo', rot={'angle': 22.5, 'axis': 'z', 'origin': [14, 9, -3]})
m.cubo('narina', [5, 8, -15.3], [11, 9, -14.6], 'brasa', brilho=True)
for i, z in enumerate((-10, -4, 2, 8, 14)):
    m.cubo(f'crista{i}', [5.5, 10, z], [10.5, 14 + (2 if i in (1, 2) else 0), z + 3], 'chama', brilho=True)
m.cubo('chifre_e', [-1, 8, 6], [2, 16, 9], 'escama_fogo', rot={'angle': -22.5, 'axis': 'z', 'origin': [1, 8, 8]})
m.cubo('chifre_d', [14, 8, 6], [17, 16, 9], 'escama_fogo', rot={'angle': 22.5, 'axis': 'z', 'origin': [15, 8, 8]})
m.cubo('pescoco', [2, -4, 15], [14, 8, 24], 'escama_fogo')
m.cubo('pescoco_fogo', [5, 8, 15], [11, 12, 24], 'chama', brilho=True)
m.salvar(SEM)

m = mob('boitata_corpo', 128)
m.cubo('gomo', [1, -14, 1], [15, 0, 15], 'escama_fogo')
m.cubo('barriga', [2.5, -15, 2.5], [13.5, -13.5, 13.5], 'brasa', brilho=True)
m.cubo('fogo', [5, 0, 3], [11, 6, 13], 'chama', brilho=True)
m.cubo('fogo_ponta', [6.5, 6, 5.5], [9.5, 9, 10.5], 'brasa', brilho=True)
m.cubo('espinho_e', [-1, -8, 6], [1, -5, 10], 'escama_fogo')
m.cubo('espinho_d', [15, -8, 6], [17, -5, 10], 'escama_fogo')
m.salvar(SEM)

# ======================================================== monstros dos corredores
m = mob('espirito_mata', 256)            # árvore-fantasma
m.cubo('raizes', [1, -16, 2], [15, -12, 14], 'casca')
for i, (x, z) in enumerate(((0, 6), (14, 6), (6, 0), (6, 14))):
    m.cubo(f'raiz{i}', [x - 1, -16, z - 1], [x + 3, -14, z + 3], 'casca')
m.cubo('tronco', [3, -12, 4], [13, 10, 12], 'casca')
m.cubo('rosto', [3.5, 0, 3.6], [12.5, 9, 4], 'boca')
m.cubo('olho_e', [4.5, 6, 3.4], [7, 7, 3.7], 'olho_verde', brilho=True, rot={'angle': -22.5, 'axis': 'z', 'origin': [6, 6.5, 3.5]})
m.cubo('olho_d', [9, 6, 3.4], [11.5, 7, 3.7], 'olho_verde', brilho=True, rot={'angle': 22.5, 'axis': 'z', 'origin': [10, 6.5, 3.5]})
for i, x in enumerate((4.5, 6.3, 8.1, 9.9)):
    m.cubo(f'boca_galho{i}', [x, 1 + (i % 2), 3.3], [x + 1.4, 4.5 - (i % 2), 3.6], 'olho_verde', brilho=True)
m.cubo('musgo', [2.5, 8, 3.5], [13.5, 11, 12.5], 'musgo')
for lado, x0, ang in (('e', -4, 45), ('d', 13, -45)):
    m.cubo('galho_' + lado, [x0, 4, 6.5], [x0 + 7, 6, 9.5], 'casca', rot={'angle': ang / 2, 'axis': 'z', 'origin': [x0 + 3.5, 5, 8]})
    m.cubo('garra_' + lado, [x0 - 1, -3, 6], [x0 + 2, 4, 10], 'casca')
m.cubo('copa', [-1, 10, 0], [17, 18, 16], 'folha')
m.cubo('copa2', [2, 18, 3], [14, 22, 13], 'folha')
m.salvar(SEM)

m = mob('vulto', 128)                     # sombra alta de manto rasgado
m.cubo('manto', [2, -16, 4], [14, 8, 12], 'sombra')
m.cubo('farrapos', [1, -16, 3], [15, -10, 13], 'sombra')
m.cubo('capuz', [2.5, 8, 3.5], [13.5, 18, 12.5], 'sombra')
m.cubo('rosto', [4, 9.5, 3.2], [12, 15.5, 3.6], 'boca')
m.cubo('olho_e', [5, 12.5, 3], [7, 13.5, 3.3], 'olho_fogo', brilho=True)
m.cubo('olho_d', [9, 12.5, 3], [11, 13.5, 3.3], 'olho_fogo', brilho=True)
for lado, x0 in (('e', -1.5), ('d', 14)):
    m.cubo('braco_' + lado, [x0, -12, 6], [x0 + 3.5, 7, 9], 'sombra')
    m.cubo('dedos_' + lado, [x0, -16, 6.2], [x0 + 3.5, -12, 8.8], 'aranha')
m.salvar(SEM)

m = mob('alma_cemiterio', 128)           # fantasma de caveira com lanterna de alma
m.cubo('vestes', [3, -14, 4], [13, 6, 12], 'fantasma')
m.cubo('cauda', [5, -16, 6], [11, -14, 10], 'fantasma')
m.cubo('ombros', [2, 4, 3.5], [14, 7, 12.5], 'fantasma')
m.cubo('cranio', [4, 7, 4], [12, 15, 12], 'dente')
m.cubo('orbita_e', [4.8, 10, 3.7], [7.2, 12.4, 4], 'boca')
m.cubo('orbita_d', [8.8, 10, 3.7], [11.2, 12.4, 4], 'boca')
m.cubo('brilho_e', [5.4, 10.6, 3.5], [6.6, 11.6, 3.7], 'olho_ciano', brilho=True)
m.cubo('brilho_d', [9.4, 10.6, 3.5], [10.6, 11.6, 3.7], 'olho_ciano', brilho=True)
m.cubo('dentes', [5.5, 7.4, 3.6], [10.5, 8.6, 3.9], 'boca')
m.cubo('braco', [13, -4, 6], [15.5, 6, 9], 'fantasma')
m.cubo('lanterna', [13, -9, 5.5], [16.5, -4, 9.5], 'ferro')
m.cubo('chama_alma', [13.6, -8.4, 5.2], [15.9, -4.6, 5.5], 'olho_ciano', brilho=True)
m.salvar(SEM)

m = mob('aranha_cuca', 128)              # aranha com a marca roxa da Cuca
m.cubo('cefalo', [4, -12, -2], [12, -6, 6], 'aranha')
m.cubo('abdomen', [2, -13, 6], [14, -3, 18], 'aranha')
m.cubo('marca', [5, -3.2, 9], [11, -2.9, 15], 'roxo_marca', brilho=True)
for i, x in enumerate((5, 6.6, 8.6, 10.2)):
    m.cubo(f'olho{i}', [x, -9, -2.3], [x + 1.2, -7.8, -2], 'olho_vermelho', brilho=True)
m.cubo('quelicera', [6, -13, -3], [10, -11, -1.5], 'dente')
for i, z in enumerate((-1, 2, 5, 8)):
    for lado, x0, ang in (('e', -7, 22.5), ('d', 12, -22.5)):
        m.cubo(f'perna_{lado}{i}', [x0, -10, z], [x0 + 11, -8.5, z + 1.5], 'aranha', rot={'angle': ang, 'axis': 'z', 'origin': [8, -9, z]})
        m.cubo(f'pe_{lado}{i}', [x0 - 1 if lado == 'e' else x0 + 10, -16, z], [x0 + 0.5 if lado == 'e' else x0 + 11.5, -10, z + 1.5], 'aranha')
m.salvar(SEM)

m = mob('chama_errante', 128)            # caveira em chamas
m.cubo('cranio', [4, -6, 4], [12, 2, 12], 'dente')
m.cubo('queixo', [5, -8, 4.5], [11, -6, 9], 'dente')
m.cubo('orbita_e', [4.8, -3, 3.7], [7.2, -0.6, 4], 'boca')
m.cubo('orbita_d', [8.8, -3, 3.7], [11.2, -0.6, 4], 'boca')
m.cubo('olho_e', [5.3, -2.5, 3.5], [6.7, -1.2, 3.7], 'olho_fogo', brilho=True)
m.cubo('olho_d', [9.3, -2.5, 3.5], [10.7, -1.2, 3.7], 'olho_fogo', brilho=True)
m.cubo('fogo', [3, 1, 3], [13, 6, 13], 'chama', brilho=True)
m.cubo('fogo2', [5, 5, 5], [11, 11, 11], 'chama', brilho=True)
m.cubo('fogo3', [6.5, 10, 6.5], [9.5, 14, 9.5], 'brasa', brilho=True)
m.cubo('rastro', [5, -14, 9], [11, -6, 14], 'chama', brilho=True, rot={'angle': 22.5, 'axis': 'x', 'origin': [8, -6, 10]})
m.salvar(SEM)

m = mob('brasa_viva', 128)               # monte de basalto rachado em brasa
m.cubo('corpo', [1, -16, 1], [15, -2, 15], 'basalto')
m.cubo('rachadura1', [0.7, -12, 3], [1, -4, 5], 'brasa', brilho=True)
m.cubo('rachadura2', [15, -14, 9], [15.3, -6, 11], 'brasa', brilho=True)
m.cubo('rachadura3', [5, -10, 0.7], [11, -9, 1], 'brasa', brilho=True)
m.cubo('olho_e', [3.5, -6, 0.6], [6.5, -4, 1], 'olho_fogo', brilho=True)
m.cubo('olho_d', [9.5, -6, 0.6], [12.5, -4, 1], 'olho_fogo', brilho=True)
m.cubo('boca', [4, -11, 0.6], [12, -8.5, 1], 'chama', brilho=True)
m.cubo('pedra_topo', [3, -2, 3], [13, 2, 13], 'basalto')
m.cubo('fogo_topo', [5, 2, 5], [11, 6, 11], 'chama', brilho=True)
m.salvar(SEM)

# item invisível (para esconder arcos/armas dos mobs)
import json, os
os.makedirs('assets/big/models/item/dungeon', exist_ok=True)
json.dump({'textures': {'particle': 'minecraft:block/air'}, 'elements': []}, open('assets/big/models/item/dungeon/vazio.json', 'w'))
json.dump({'model': {'type': 'minecraft:model', 'model': 'big:item/dungeon/vazio'}}, open('assets/big/items/dungeon/vazio.json', 'w'))
print('mobs ok')
