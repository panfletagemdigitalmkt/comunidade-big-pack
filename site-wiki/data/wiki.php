<?php
// Conteúdo da wiki. Os números seguem a configuração atual do servidor.

$MENU = [
    'Primeiros passos' => [
        'comecar'   => ['Como começar', '✦'],
        'lobby'     => ['Lobby e a vila', '⌂'],
        'protecao'  => ['Terrenos, casas e kits', '⛨'],
    ],
    'RPG' => [
        'classes'     => ['As 6 classes', '⚔'],
        'combate'     => ['Combate e habilidades', '✴'],
        'constelacoes'=> ['Constelações e signos', '★'],
        'itens'       => ['Itens e caixas de classe', '❖'],
        'masmorra'    => ['Masmorra da Mata Sombria', '☠'],
        'eventos'     => ['Eventos automáticos', '✪'],
    ],
    'Economia' => [
        'economia' => ['Moedas, loja e leilão', '$'],
        'fazenda'  => ['Fazenda', '❀'],
        'pesca'    => ['Pescaria', '≈'],
        'lootbox'  => ['Lootboxes e chaves', '⚿'],
    ],
    'Comunidade' => [
        'chat'     => ['Chat, emojis e nick', '✉'],
        'clans'    => ['Clans', '⚑'],
        'vip'      => ['VIP, tags e ranks', '♛'],
        'comandos' => ['Todos os comandos', '⌘'],
        'regras'   => ['Regras e dúvidas', '§'],
    ],
];

$CLASSES = [
    'paladino' => ['nome' => 'Paladino', 'cores' => '#fef3c7,#f59e0b', 'papel' => 'Tanque sagrado', 'icone' => 'espada_justica',
        'desc' => 'Guerreiro sagrado da linha de frente. Aguenta o dano e protege o grupo.',
        'recurso' => ['Fé', '✦', 'Regenera devagar e enche quando você apanha.'],
        'passiva' => ['Égide', 'Recebe 10% menos dano.'],
        'atrib' => ['Força' => 8, 'Destreza' => 4, 'Inteligência' => 2, 'Sabedoria' => 8, 'Vitalidade' => 14, 'Defesa' => 12],
        'hab' => [
            ['Golpe Sagrado', 20, 6, 'Golpe de luz no inimigo à sua frente que também cura 5% da sua vida.'],
            ['Provocar', 15, 12, 'Chama todos os monstros num raio de 8 blocos para você por 4 s.'],
            ['Escudo da Fé', 30, 15, 'Escudo de 15% da sua vida em você e de 8% nos aliados num raio de 6 blocos, por 6 s.'],
            ['Martelo Investido', 25, 10, 'Avança com o martelo, acerta tudo em volta, joga os inimigos para cima e deixa lentos.'],
            ['Julgamento Divino', 100, 60, 'SUPREMA • Depois de 1 s de aviso, a luz desce num raio de 6 blocos: dano pesado nos inimigos e cura de 20%.'],
        ],
        'estilo' => 'Bloqueie com o escudo na hora certa (bloqueio perfeito) para refletir dano e ganhar Fé; a batida do escudo empurra e atordoa.'],
    'berserker' => ['nome' => 'Berserker', 'cores' => '#fca5a5,#dc2626', 'papel' => 'Dano corpo a corpo', 'icone' => 'machado_alfa',
        'desc' => 'Lutador furioso corpo a corpo. Quanto menos vida, mais forte ele bate.',
        'recurso' => ['Ira', '⚔', 'Enche batendo e apanhando, e esvazia fora de combate.'],
        'passiva' => ['Sede de Sangue', 'Até +30% de dano com pouca vida e rouba 5% do dano como vida.'],
        'atrib' => ['Força' => 15, 'Destreza' => 8, 'Inteligência' => 2, 'Sabedoria' => 3, 'Vitalidade' => 10, 'Defesa' => 4],
        'hab' => [
            ['Golpe Brutal', 20, 5, 'Machadada forte; se o alvo tiver menos da metade da vida, causa 50% a mais.'],
            ['Grito de Guerra', 25, 18, 'Você e os aliados num raio de 8 blocos ganham Força por 6 s.'],
            ['Redemoinho', 30, 10, 'Gira o machado e acerta 3 vezes tudo o que estiver em volta.'],
            ['Salto Selvagem', 25, 12, 'Salta para a frente e cai causando dano e empurrando os inimigos.'],
            ['Fúria Imortal', 100, 75, 'SUPREMA • Força II por 8 s e, no fim, recupera 15% da vida.'],
        ],
        'estilo' => 'Duas armas: a mão esquerda também ataca. Cada golpe seguido acumula frenesi (mais dano) e os golpes cortam em área.'],
    'arqueiro' => ['nome' => 'Arqueiro', 'cores' => '#bbf7d0,#16a34a', 'papel' => 'Dano à distância', 'icone' => 'arco_falcao',
        'desc' => 'Atirador ágil com arco e besta. Causa dano de longe e se reposiciona rápido.',
        'recurso' => ['Energia', '➹', 'Regenera rápido sozinha.'],
        'passiva' => ['Olho de Águia', '+15% de dano com arco e besta.'],
        'atrib' => ['Força' => 5, 'Destreza' => 15, 'Inteligência' => 4, 'Sabedoria' => 6, 'Vitalidade' => 8, 'Defesa' => 6],
        'hab' => [
            ['Tiro Perfurante', 20, 5, 'Flecha muito rápida que atravessa até 3 inimigos.'],
            ['Chuva de Flechas', 35, 14, 'Marca um ponto até 25 blocos e faz cair 4 ondas de flechas num raio de 4.'],
            ['Recuo', 20, 8, 'Salta para trás e deixa lentos os inimigos perto de você.'],
            ['Armadilha', 25, 15, 'Coloca uma armadilha (dura 20 s) que prende o inimigo por 3 s.'],
            ['Fúria do Falcão', 100, 70, 'SUPREMA • Por 6 s dispara flechas sem parar no alvo da mira.'],
        ],
        'estilo' => 'Tiros com o arco bem puxado marcam o alvo: cada marca aumenta o dano dos próximos tiros (até 5).'],
    'clerigo' => ['nome' => 'Clérigo', 'cores' => '#e0f2fe,#38bdf8', 'papel' => 'Cura e suporte', 'icone' => 'cetro_aureo',
        'desc' => 'Curandeiro do grupo. Mantém os aliados vivos e se recupera fora de combate.',
        'recurso' => ['Mana', '✧', 'Regenera sozinha.'],
        'passiva' => ['Graça', '+25% de cura recebida e recupera 1% da vida por segundo fora de combate.'],
        'atrib' => ['Força' => 3, 'Destreza' => 4, 'Inteligência' => 8, 'Sabedoria' => 15, 'Vitalidade' => 9, 'Defesa' => 7],
        'hab' => [
            ['Luz Curativa', 20, 4, 'Cura 20% da vida do aliado na mira (até 20 blocos) ou a sua.'],
            ['Círculo Sagrado', 35, 16, 'Círculo de 5 blocos por 6 s: aliados curam a cada segundo e inimigos se queimam.'],
            ['Purificação', 25, 12, 'Tira efeitos ruins dos aliados num raio de 7 e dá um escudo de 10% por 6 s.'],
            ['Raio Sagrado', 15, 3, 'Raio de luz até 18 blocos que causa dano e cura um pouco você.'],
            ['Milagre', 100, 80, 'SUPREMA • Cura metade da vida de todos os aliados num raio de 12 e dá Resistência II por 5 s.'],
        ],
        'estilo' => 'O cetro dispara orbes de luz; a cada 3 acertos, a bênção cura você.'],
    'assassino' => ['nome' => 'Assassino', 'cores' => '#e9d5ff,#7e22ce', 'papel' => 'Dano furtivo', 'icone' => 'adaga_viuva',
        'desc' => 'Matador silencioso das sombras. Some, aparece nas costas do alvo e termina o serviço.',
        'recurso' => ['Sombra', '☠', 'Regenera e enche ao acertar golpes.'],
        'passiva' => ['Golpe pelas Costas', '+40% de dano ao atacar o alvo pelas costas.'],
        'atrib' => ['Força' => 12, 'Destreza' => 14, 'Inteligência' => 3, 'Sabedoria' => 3, 'Vitalidade' => 7, 'Defesa' => 5],
        'hab' => [
            ['Apunhalar', 20, 7, 'Aparece nas costas do alvo (até 10 blocos) e crava a adaga.'],
            ['Frasco de Veneno', 25, 12, 'Arremessa um frasco que solta uma nuvem de veneno por 6 s.'],
            ['Bomba de Fumaça', 30, 18, 'Fumaça de 5 blocos por 5 s: os monstros perdem você e os inimigos ficam cegos.'],
            ['Leque de Adagas', 20, 6, 'Lança 5 adagas em leque.'],
            ['Execução Sombria', 100, 60, 'SUPREMA • Salta entre até 5 inimigos perto; quem estiver com menos de 30% da vida é executado.'],
        ],
        'estilo' => 'Atacar pelas costas causa muito mais dano; fique fora da vista dos monstros para começar a luta com vantagem.'],
    'ninja' => ['nome' => 'Ninja', 'cores' => '#ccfbf1,#0d9488', 'papel' => 'Mobilidade e combos', 'icone' => 'kusanagi',
        'desc' => 'Guerreiro ágil das técnicas secretas. Pula duas vezes, some numa nuvem e corta como um raio.',
        'recurso' => ['Chakra', '✴', 'Regenera rápido e enche ao acertar golpes.'],
        'passiva' => ['Passos de Sombra', 'Pulo duplo (aperte espaço no ar) e metade do dano de queda.'],
        'atrib' => ['Força' => 9, 'Destreza' => 15, 'Inteligência' => 6, 'Sabedoria' => 5, 'Vitalidade' => 8, 'Defesa' => 5],
        'hab' => [
            ['Corte Relâmpago', 20, 6, 'Dispara 8 blocos para a frente cortando quem estiver no caminho.'],
            ['Shurikens', 15, 4, 'Lança 3 shurikens (alcance de 16 blocos).'],
            ['Substituição', 25, 16, 'Por 5 s, se levar um golpe, troca de lugar com um tronco e reaparece longe.'],
            ['Chuva de Kunais', 30, 12, '8 kunais caem no ponto que você mira.'],
            ['Mil Lâminas', 100, 70, 'SUPREMA • 10 cortes relâmpago em todos os inimigos num raio de 8 blocos.'],
        ],
        'estilo' => 'Use o pulo duplo e o Corte Relâmpago para entrar e sair da luta sem parar.'],
];

$SIGNOS = [
    ['Áries', '♈', 'fogo', 'Primeiro Golpe', 'O primeiro golpe depois de um tempo sem atacar causa +25% de dano (a cada 10 s).', 'Carga do Carneiro', 'Avança e atropela os inimigos no caminho, causando dano e atordoando.'],
    ['Touro', '♉', 'terra', 'Firme como Rocha', 'Resistência a empurrões (+30%).', 'Muralha de Pedra', 'Levanta uma muralha temporária na sua frente.'],
    ['Gêmeos', '♊', 'ar', 'Duas Mentes', '15% de chance de a recarga da habilidade usada cair pela metade.', 'Reflexo Gêmeo', 'Fica invisível e rápido por alguns segundos.'],
    ['Câncer', '♋', 'água', 'Carapaça', 'Com menos de 40% da vida, recebe 15% menos dano.', 'Carapaça de Maré', 'Escudo de água de 20% da vida por 6 s.'],
    ['Leão', '♌', 'fogo', 'Coração Solar', 'Fora de combate regenera você e os aliados; +15% de dano contra mortos-vivos.', 'Rugido Solar', 'Revela e enfraquece inimigos e dá escudo leve aos aliados.'],
    ['Virgem', '♍', 'terra', 'Mãos que Curam', 'Fora de combate, toda cura recebida é 30% maior.', 'Colheita', 'Cura 15% da vida de até 5 aliados perto.'],
    ['Libra', '♎', 'ar', 'Equilíbrio', 'A cura que passaria da vida máxima vira escudo (até 15%).', 'Julgamento', 'Tira os efeitos bons do alvo e deixa ele fraco e lento.'],
    ['Escorpião', '♏', 'água', 'Veneno', 'Seus golpes corpo a corpo envenenam os monstros.', 'Ferrão', 'Golpe que causa o dobro em alvo envenenado.'],
    ['Sagitário', '♐', 'fogo', 'Mira do Centauro', '+10% de dano com arco, besta e flechas.', 'Flecha Celeste', 'Mira por um instante e dispara uma flecha muito forte.'],
    ['Capricórnio', '♑', 'terra', 'Teimosia', 'Em combate, a cada 2 s recebe menos dano (até 15%).', 'Ascensão', 'Salta bem alto e cai causando dano em área.'],
    ['Aquário', '♒', 'ar', 'Ventania', '+5% de velocidade de movimento.', 'Descarga', 'Um raio cai onde você mira (até 6 inimigos).'],
    ['Peixes', '♓', 'água', 'Correnteza', 'Lentidão dura 40% menos em você.', 'Corrente', 'Avanço rápido que também remove 1 efeito ruim.'],
];

$SAFRAS = [
    ['milho', 'Milho', 15, '1–3', 2.5, false, 5, 'Alto como gente. Devolve a semente na colheita.'],
    ['morango', 'Morango', 12, '2–4', 1.5, true, 8, 'Pé baixo que volta a dar frutos depois da colheita.'],
    ['pimenta', 'Pimenta', 20, '3–5', 2.0, true, 25, 'Arbusto ardido que continua produzindo.'],
    ['mandioca', 'Mandioca', 25, '2–4', 3.0, false, 8, 'Raiz farta. Devolve a rama na colheita.'],
    ['cafe', 'Café', 35, '3–6', 4.0, true, 60, 'Demora, mas produz para sempre.'],
    ['abacaxi', 'Abacaxi', 45, '1', 18.0, false, 35, 'Um fruto por planta, mas vale muito.'],
];

$PEIXES = [
    ['lambari', 'Lambari', 'comum', 'Rio/lago', '', '0,05–0,25 kg', 2],
    ['tilapia', 'Tilápia', 'comum', 'Rio/lago', '', '0,4–2,5 kg', 3],
    ['sardinha', 'Sardinha', 'comum', 'Mar', '', '0,05–0,25 kg', 2],
    ['bagre', 'Bagre', 'comum', 'Rio/lago', '', '0,8–5 kg', 3.5],
    ['traira', 'Traíra', 'incomum', 'Rio/lago', 'noite', '0,8–4 kg', 8],
    ['piranha', 'Piranha', 'incomum', 'Rio/lago', 'dia', '0,4–3 kg', 9],
    ['pacu', 'Pacu', 'incomum', 'Rio/lago', '', '1,5–8 kg', 10],
    ['robalo', 'Robalo', 'incomum', 'Mar', '', '1,5–10 kg', 11],
    ['tucunare', 'Tucunaré', 'raro', 'Rio/lago', 'dia', '1,5–9 kg', 28],
    ['tambaqui', 'Tambaqui', 'raro', 'Rio/lago', '', '4–30 kg', 30],
    ['garoupa', 'Garoupa', 'raro', 'Mar', '', '4–40 kg', 32],
    ['dourado', 'Dourado', 'epico', 'Rio/lago', 'dia', '4–25 kg', 90],
    ['pintado', 'Pintado', 'epico', 'Rio/lago', 'noite', '8–60 kg', 95],
    ['marlim', 'Marlim-azul', 'epico', 'Mar', '', '60–300 kg', 110],
    ['pirarucu', 'Pirarucu', 'lendario', 'Rio/lago', 'chuva', '40–200 kg', 450],
    ['mero', 'Mero', 'lendario', 'Mar', 'noite', '80–400 kg', 420],
];

$VARAS = [
    ['vara_bambu', 'Vara de Bambu', '#f5f0b0,#c8c070,#7a5a2a', 60, 1, 'Leve e simples. Um pouco mais de sorte.'],
    ['vara_carbono', 'Vara de Carbono', '#fca5a5,#e04040,#3f3f46', 900, 2, 'Fisga mais rápido e aguenta peixe grande.'],
    ['vara_iara', 'Vara da Iara', '#e0fffd,#2ad0c8,#e8c040', 6000, 3, 'Abençoada pela mãe-d\'água. Nunca quebra.'],
];

$LOOTBOX = [
    'comum' => ['Caixa Comum', '#fde68a,#d6a35a,#8a5a2b', 60, 'Itens do dia a dia para começar bem.', [
        ['Pão, carne, tochas, madeira, carvão, farinha de osso', 'comum'],
        ['40–120 moedas', 'comum'], ['100 blocos de proteção', 'incomum'], ['Lingotes de ferro e cenouras douradas', 'incomum'],
        ['Sementes de milho e morango, Vara de Bambu', 'incomum'], ['Frascos de experiência, 300 blocos de proteção, 200–400 moedas', 'raro'],
        ['Maçãs douradas', 'raro'], ['Diamantes', 'epico'], ['Chave da Caixa Ultra', 'epico']]],
    'ultra' => ['Caixa Ultra', '#e9d5ff,#a855f7,#22d3ee', 180, 'O tesouro: diamantes, netherite, livros e caixas de classe.', [
        ['6 diamantes, 2 sucatas de netherite', 'raro'], ['600–1500 moedas, 800 blocos de proteção', 'raro'],
        ['Livros de Remendo, Eficiência V e Proteção IV', 'epico'], ['Blocos de diamante, Totem da Imortalidade', 'epico'],
        ['Caixa da sua classe, Vara de Carbono', 'epico'],
        ['Lingote de netherite, Maçã encantada, Shulker', 'lendario'], ['Sinalizador, Élitro, Vara da Iara', 'lendario']]],
    'ovos' => ['Caixa dos Ovos', '#fbcfe8,#a5f3fc,#86efac', 300, 'Ovos para criar animais na sua base.', [
        ['Vaca, porco, ovelha, galinha, coelho', 'comum'], ['Cavalo, lobo, gato, raposa, cabra', 'incomum'],
        ['Papagaio, axolote, sapo, lhama, vaca-cogumelo', 'raro'], ['Panda, camelo, aldeão', 'epico'], ['Allay e ovo de farejador', 'lendario']]],
];

$COMANDOS = [
    'Geral' => [
        ['/jogar', 'Volta para onde você parou no mundo.'], ['/explorar', 'Vai para um lugar aleatório do mapa.'],
        ['/lobby', 'Volta para a vila do lobby (também /spawn).'], ['/perfil [jogador]', 'Classe, vida, recurso e atributos.'],
        ['/playtime [jogador|top]', 'Tempo jogado e ranking (também /tempo).'], ['/tags', 'Escolhe sua tag do chat.'],
        ['/vip', 'Mostra seu VIP.'], ['/limpeza', 'Quanto falta para limpar os itens do chão.'],
    ],
    'Chat' => [
        ['/l [mensagem]', 'Chat local (padrão, 120 blocos).'], ['/g [mensagem]', 'Chat global (ou comece com !).'],
        ['/c <mensagem>', 'Chat do clan.'], ['/emojis', 'Biblioteca de emojis (use :nome: no chat).'],
        ['/nick <código> | reset', 'Nick colorido com &#RRGGBB por letra (VIP).'], ['/msg <jogador> <mensagem>', 'Mensagem privada.'],
    ],
    'Eventos' => [
        ['/evento', 'Próximo evento e horário.'], ['/evento entrar | sair', 'Participa ou sai do evento.'],
        ['/evento assistir', 'Assiste ao evento em andamento.'], ['/evento lista', 'Todos os eventos do rodízio.'],
    ],
    'RPG' => [
        ['/classe', 'Escolhe ou troca sua classe (espera de 24h para trocar).'], ['/estilo', 'Estilo de luta da sua classe.'],
        ['/atalhos', 'Escolhe como usar as habilidades (padrão: Shift + 1 a 6).'], ['/arvore', 'Constelação de talentos da sua classe.'],
        ['/signo', 'Escolhe seu signo e abre a constelação dele.'], ['/caixa [colecao|loja]', 'Caixas de classe, coleção e loja de fragmentos.'],
        ['/dungeon [entrar|sair|historia]', 'Masmorra da Mata Sombria (também /dg).'], ['/dungeon missoes', 'Missões da região atual da masmorra.'],
    ],
    'Economia' => [
        ['/saldo [jogador]', 'Seu saldo de moedas.'], ['/pagar <jogador> <valor>', 'Paga outro jogador.'],
        ['/saldotop', 'Os mais ricos do servidor.'], ['/loja [categoria]', 'Abre a loja (comprar e vender).'],
        ['/vender [tudo]', 'Vende o item da mão ou tudo o que a loja compra.'],
        ['/leilao', 'Leilão entre jogadores.'], ['/leilao vender <preço>', 'Anuncia o item da mão.'], ['/leilao meus | coletar', 'Seus anúncios e itens para coletar.'],
        ['/fazenda', 'Guia das safras.'], ['/pesca [peixes|recordes]', 'Coleção de peixes e recordes.'], ['/chaves', 'Suas chaves de lootbox e quanto falta para a próxima.'],
    ],
    'Terreno e casas' => [
        ['/kit inicial', 'Armadura e ferramentas de ferro (uma vez só).'], ['/kit plantação', '5 sementes de cada e enxada de pedra (a cada 24h).'],
        ['/kit prot', 'Pá de ouro (cria terreno) e graveto (inspeciona).'], ['/prot opções', 'Menu de opções do terreno onde você está.'],
        ['/prot nome <nome>', 'Dá um nome ao terreno.'],
        ['/prot confiar <jogador>', 'Deixa um amigo construir no seu terreno.'], ['/prot acesso | bau <jogador>', 'Permissões menores: portas/botões ou baús.'],
        ['/prot remover <jogador>', 'Tira a permissão.'], ['/prot info | lista | blocos', 'Dono do terreno, seus terrenos e blocos de proteção.'],
        ['/prot abandonar', 'Apaga o terreno onde você está.'],
        ['/casa criar <nome>', 'Marca uma casa onde você está.'], ['/casa [nome]', 'Vai para a casa.'], ['/casa lista | deletar <nome>', 'Lista ou apaga casas.'],
    ],
    'Clans' => [
        ['/clan ajuda', 'Todos os comandos de clan.'], ['/clan criar <tag> <nome>', 'Cria um clan (5h jogadas).'],
        ['/clan convidar <jogador> | aceitar | recusar', 'Convites.'], ['/clan info | membros | lista', 'Informações dos clans.'],
        ['/clan sair | expulsar <jogador>', 'Sair ou tirar alguém.'], ['/clan promover | rebaixar | transferir <jogador>', 'Cargos (líder, oficial, membro).'],
        ['/clan base | definirbase | apagarbase', 'Base do clan.'],
        ['/clan aliado | rival <tag>', 'Alianças e rivalidades.'], ['/clan cor <#hex> | mudartag <tag>', 'Cores da tag (aceita &#RRGGBB por letra).'],
        ['/clan top', 'Ranking dos clans.'], ['/clan desfazer', 'Desfaz o clan (líder).'], ['/cc <mensagem>', 'Chat do clan.'], ['/ca <mensagem>', 'Chat com clans aliados.'],
    ],
];
