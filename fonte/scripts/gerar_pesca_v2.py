# Pescaria v2: 17 peixes novos, varas de Fibra e Titânio, e as 5 iscas. Reaproveita as funções do gerar_fazenda_pesca.py
# (sem rodar as partes que geram plantas/colheitas). Ordem: gerar_fazenda_pesca.py -> gerar_plantas_v2.py -> gerar_pesca_v2.py
import json
src = open('gerar_fazenda_pesca.py', encoding='utf-8').read()
def corte(a, b): i = src.index(a); return src[i:src.index(b, i)]
codigo = (src[:src.index('DISP_PLANTA = ')]
          + corte('# ======================================================= itens extrudados', '# ---------------- colheitas')
          + corte('# ======================================================= peixes', 'PEIXES = [')
          + corte('# ======================================================= varas de pesca', "montar('vara_bambu'"))
exec(codigo)

# ---------------------------------------------------------------- peixes novos
NOVOS = [
 ('mandi', 11, 4, ['b8a870', 'a89860'], ['e8e0c0'], ['d8c060'], 'forquilha', 'pintas', ('bigode',), '5a4a30'),
 ('carpa', 15, 7, ['b08a40', 'c09a4a'], ['e8d8a0'], ['a07030'], 'redonda', 'escamas', ('bigode',), '8a6a2a'),
 ('baiacu', 10, 8, ['8a8a50', '9a9a5a'], ['f0f0e0'], ['7a7a40'], 'redonda', 'pintas', (), '3a3a20'),
 ('tainha', 14, 5, ['5a6a7a', '6a7a8a'], ['e0e6ea'], ['6a7a8a'], 'forquilha', 'linha', (), '4a5a6a'),
 ('truta', 13, 5, ['6a7a50', '7a8a5a'], ['f0d0c0', 'e8b8a8'], ['7a8a5a'], 'forquilha', 'pintas', (), '2a2a1a'),
 ('piau', 12, 5, ['a8a090', 'b8b0a0'], ['eeeae0'], ['e05030'], 'forquilha', 'manchas', (), '303030'),
 ('curimbata', 13, 6, ['8a8a80', '9a9a90'], ['dcdcd0'], ['c0a050'], 'forquilha', 'escamas', ('boca',), '6a6a60'),
 ('cavala', 15, 5, ['2a6a8a', '3a7a9a'], ['e8eef2'], ['2a5a7a'], 'forquilha', 'listras', (), '103040'),
 ('jaraqui', 12, 5, ['8a9098', '9aa0a8'], ['e8e8e8'], ['202020', 'f0f0f0'], 'forquilha', 'linha', (), '202020'),
 ('aruana', 18, 4, ['9aa080', 'aab090'], ['e0e0c8'], ['8a9070'], 'redonda', 'escamas', ('boca', 'bigode'), '707860'),
 ('pescada', 15, 6, ['c8a840', 'd8b84a'], ['f4ecc0'], ['b89830'], 'redonda', 'linha', ('dentes',), 'a08020'),
 ('salmao', 15, 6, ['8a9aa8', '9aaab8'], ['f0a080', 'e89070'], ['7a8a98'], 'forquilha', 'pintas', (), '2a2a3a'),
 ('pirarara', 18, 6, ['3a3a3a', '4a4a4a'], ['e8e0d0'], ['d84a20', 'e05a28'], 'forquilha', None, ('bigode',), '000000'),
 ('atum', 16, 8, ['1a2a5a', '24346a'], ['d8e0e8'], ['f0c020'], 'lua', 'linha', (), '8090a0'),
 ('lucio', 18, 5, ['5a7a4a', '6a8a5a'], ['e0e8c8'], ['5a6a3a'], 'redonda', 'manchas', ('boca', 'dentes'), 'c8d8a0'),
 ('peixeserra', 18, 4, ['8a8070', '9a9080'], ['e8e0d0'], ['d8d0c0'], 'redonda', None, ('bico',), 'f0f0e8'),
 ('esturjao', 19, 5, ['5a5a50', '6a6a5e'], ['d8d0c0'], ['4a4a40'], 'forquilha', 'escamas', ('bigode',), 'b8b0a0'),
]
for p in NOVOS:
    nome, comp, alt, dorso, ventre, barb, cauda, padrao, extras, cp = p
    peixe(nome, comp, alt, dorso, ventre, barb, cauda, padrao, extras, cp, esp=2.2 + alt * 0.25)

# ---------------------------------------------------------------- varas novas
def fibra(v):
    v.eixo(-3.3, -2.5, 1.1, '1e3a5a')
    v.eixo(-2.5, 3.0, 1.0, '2a2a30')                                       # cabo emborrachado
    for y in (-1.5, 0.0, 1.5): v.anel(y, 1.06, 0.3, '38bdf8')
    v.eixo(3.0, 3.9, 0.85, 'c8ccd0')                                       # porta-molinete
    v.anel(3.9, 0.75, 0.4, '38bdf8')
    v.eixo(4.3, 12.8, 0.55, 'eef4f8')                                      # fibra de vidro branca
    v.eixo(12.8, 19.4, 0.4, 'e0eaf2')
    for y in (7.0, 11.0, 14.8, 17.8):
        v.anel(y - 0.3, 0.62 if y < 12.8 else 0.48, 0.7, '0369a1')
        v.passador(y, 'b8c4cc', 1.0 if y < 10 else 0.8)
    v.c([8.85, 2.4, 7.55], [9.9, 3.0, 8.45], '9aa4ac')                    # molinete azul
    v.c([9.9, 1.0, 6.9], [12.2, 4.0, 9.1], '1e6aa0')
    v.c([12.2, 1.3, 7.2], [12.8, 3.7, 8.8], 'c8ccd0')
    v.c([10.9, 2.2, 9.1], [11.5, 2.8, 10.8], '1a1a1a')
    v.c([10.7, 2.0, 10.8], [11.7, 3.0, 11.8], '38bdf8')
    v.eixo(19.4, 20.0, 0.3, '0369a1')
    return 20.0

def titanio(v):
    v.eixo(-3.6, -2.6, 1.2, '3a3a40')
    v.anel(-2.6, 1.1, 0.4, 'f97316')
    v.eixo(-2.2, 2.6, 1.05, '52525b')                                      # cabo de neoprene
    for y in (-1.4, 0.3, 1.9): v.anel(y, 1.1, 0.2, 'f97316')
    v.eixo(2.6, 4.0, 0.95, 'd4d4d8')                                       # porta-molinete de titânio
    v.eixo(4.0, 13.2, 0.62, 'a1a1aa')
    v.eixo(13.2, 19.8, 0.45, 'b4b4bc')
    for y in (6.5, 9.5, 12.5, 15.4, 18.2):
        v.anel(y - 0.35, 0.72 if y < 13.2 else 0.55, 0.8, 'f97316')
        v.passador(y, 'e4e4e7', 1.2 if y < 10 else 0.9)
    v.c([8.95, 2.8, 7.5], [10.1, 3.4, 8.5], 'a1a1aa')                     # molinete grande de carretilha
    v.c([10.1, 0.8, 6.4], [13.2, 4.8, 9.6], '71717a')
    v.c([13.2, 1.2, 6.8], [13.9, 4.4, 9.2], 'f97316')
    v.c([10.2, 1.0, 9.6], [10.9, 4.4, 10.0], 'd4d4d8')
    v.c([11.3, 2.5, 9.6], [12.0, 3.2, 11.8], '1a1a1a')
    v.c([11.0, 2.2, 11.8], [12.3, 3.5, 12.9], 'f97316')
    v.eixo(19.8, 20.5, 0.32, 'f97316')
    return 20.5

montar('vara_fibra', fibra, lambda v, t: v.linha(t, 'f0f0f0', 'b0b4b8', ('38bdf8', 'e0f2fe')))
montar('vara_titanio', titanio, lambda v, t: v.linha(t, 'f0f0f0', 'd4d4d8', ('f97316', 'fdba74')))
for nome in ('vara_fibra', 'vara_titanio'):
    json.dump({'model': {'type': 'minecraft:condition', 'property': 'minecraft:fishing_rod/cast',
                         'on_false': {'type': 'minecraft:model', 'model': f'big:item/pesca/{nome}'},
                         'on_true': {'type': 'minecraft:model', 'model': f'big:item/pesca/{nome}_lancada'}}},
              open(f'{R}/items/pesca/{nome}.json', 'w'), indent=1)

# ---------------------------------------------------------------- iscas
ISCAS = {
 'isca_minhoca': (['................', '................', '..........rr....', '.........rRRr...', '........rRr.Rr..', '.......rRr...r..',
                   '......rRr.......', '.....rRr........', '....rRr.........', '...rRr..........', '..rRr...........', '.rRRr...........',
                   '.rbbr...........', '..rr............'],
                  {'r': ['c8707a', 'b8606a'], 'R': ['e8949a', 'f0a4a8'], 'b': ['a85060']}, {'r': 2.2, 'R': 2.6, 'b': 2.4}),
 'isca_massa': (['................', '................', '.....yyyyy......', '....yYYYYYy.....', '...yYYwYYYYy....', '...yYwYYYYYy....',
                 '..yYYYYYYYYYy...', '..yYYYYYoYYYy...', '..yYYYYYYYYYy...', '..yYYoYYYYYYy...', '...yYYYYYYoy....', '...yyYYYYYYy....',
                 '....yyyyyyy.....', '................'],
                {'y': ['d8a820', 'c89818'], 'Y': ['f2c84a', 'f8d860'], 'w': ['fff4c0'], 'o': ['b88010']}, {'y': 3, 'Y': 4.2, 'w': 4.4, 'o': 4.3}),
 'isca_camarao': (['................', '.aa.............', '..a.............', '...a..oooo......', '....aoOOOOo.....', '.....OOOOOOo....',
                   '.....oOkOOOOo...', '......oOOOOOOo..', '.......ooOOOOo..', '.........oOOOo..', '..........oOOo..', '.........ffOo...',
                   '........ffff....', '.........ff.....'],
                  {'a': ['e87a40'], 'o': ['e8783a', 'd86a2a'], 'O': ['fb923c', 'fca560'], 'k': ['101010'], 'f': ['f0a070']},
                  {'a': 0.6, 'o': 2.6, 'O': 3.2, 'k': 3.4, 'f': 1.2}),
 'isca_artificial': (['.......cc.......', '......c..c......', '.......cc.......', '......ssss......', '.....sSSSSs.....', '....sSWSSSSs....',
                      '....sSWSSSSs....', '....sSSrrSSs....', '....sSSrrSSs....', '....sSSSSSSs....', '.....sSSSSs.....', '......ssss......',
                      '.......gg.......', '......g..g......', '......gg.g......', '.........g......'],
                     {'c': ['b0b4b8'], 's': ['9aa4ac', 'a8b0b8'], 'S': ['dfe6ec', 'eef2f6'], 'W': ['ffffff'], 'r': ['e0402e'], 'g': ['e8c040']},
                     {'c': 0.6, 's': 1.2, 'S': 1.4, 'W': 1.5, 'r': 1.6, 'g': 0.6}),
 'isca_iara': (['................', '.......pp.......', '......pPPp......', '.....pPWPPp.....', '....pPWPPPPp....', '...gpPPPPPPpg...',
                '...gpPPPPPPpg...', '....pPPPPPPp....', '....gpPPPPpg....', '.....gpPPpg.....', '......gppg......', '.......gg.......',
                '................'],
               {'p': ['2ab0aa', '1e9a9a'], 'P': ['7ae8e0', '9af0ea'], 'W': ['f0ffff'], 'g': ['e8c040', 'f2d060']},
               {'p': 2.4, 'P': 3, 'W': 3.2, 'g': 1.6}),
}
for nome, (g, c, e) in ISCAS.items():
    extrudar('pesca', nome, g, c, e, DISP_ITEM, brilho='PW' if nome == 'isca_iara' else '', seed=len(nome))
print('pesca v2 ok')
