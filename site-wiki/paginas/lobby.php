<?php $DESC = 'A vila do lobby: feira, fazenda, santuário das caixas, masmorra e mais.'; ?>
<h1><?= grad('Lobby e a vila', '#fae8ff,#c084fc,#6366f1') ?></h1>
<p class="intro">O lobby é uma vila numa ilha flutuante sob a aurora. Os moradores são personagens 3D que acenam quando você chega perto e abrem os menus quando você clica. Você nasce na praça central, olhando para o portal. No lobby ninguém se machuca, não sente fome e não perde nada. Use <?= cmd('/lobby') ?> para voltar quando quiser.</p>
<?php
$lugares = [
    ['Praça e chafariz', 'Centro', 'Onde você nasce. O letreiro de boas-vindas e o chafariz ficam bem à frente.', 'comum', 'planta_cafe_3'],
    ['Portal JOGAR', 'Norte', 'Atravesse o portal para voltar de onde parou. Ao lado, o Guia Bento leva a um lugar aleatório.', 'epico', 'kusanagi'],
    ['Murais de ranking', 'Norte', '"Mais ricos" e "Mais tempo jogado", atualizados a cada minuto.', 'lendario', 'caixa_ultra_inteira'],
    ['Feira', 'Oeste', 'Peixaria do Zé (pesca), Hortifruti da Dona Cida (fazenda) e o Mercador Seu Juca (loja). Tem também o mural de recordes de pesca.', 'incomum', 'tucunare'],
    ['Fazenda modelo', 'Leste', 'Todas as safras já maduras, celeiro e lago. O Tião Fazendeiro vende sementes.', 'incomum', 'planta_milho_3'],
    ['Santuário das Caixas', 'Sul', 'As 6 caixas de classe giram nos pedestais. Clique para comprar com moedas.', 'epico', 'caixa_ninja'],
    ['Terraço das lootboxes', 'Sul, atrás do santuário', 'Caixa Comum, Ultra e dos Ovos. Abra com as chaves que você ganha jogando.', 'lendario', 'caixa_comum_inteira'],
    ['Casa de Leilões', 'Noroeste', 'Doutor Lauro abre o leilão e a Dona Moeda mostra seu saldo.', 'raro', 'chave_comum'],
    ['Entrada da Masmorra', 'Nordeste', 'Ruína escura com uma caveira em cima. Clique na entrada para ver como entrar.', 'lendario', 'trofeu_boitata'],
    ['Salão das Classes', 'Sudoeste', 'O Mestre Aurélio escolhe ou troca sua classe.', 'epico', 'tomo_luz'],
    ['Guia rápido', 'Sudeste', 'Placa com os comandos principais.', 'comum', 'semente_milho'],
];
?>
<div class="grade-lugares">
<?php foreach ($lugares as [$nome, $onde, $txt, $est, $ic]): ?>
  <?php card_abre($est); ?>
    <div class="lugar"><?= img($ic) ?><div><h3><?= e($nome) ?> <small><?= e($onde) ?></small></h3><p><?= e($txt) ?></p></div></div>
  <?php card_fecha(); ?>
<?php endforeach; ?>
</div>
<div class="dica">O lago da vila é só enfeite: não dá para pescar no lobby. A pescaria vale no mundo.</div>
