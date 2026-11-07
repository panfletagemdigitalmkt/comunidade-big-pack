<?php $DESC = 'Expedição da Mata Sombria: 5 regiões, missões, baús, chaves e os chefes do folclore brasileiro.'; ?>
<h1><?= grad('Masmorra da Mata Sombria', '#ffd23f,#ff7a00,#b91c1c') ?></h1>
<p class="intro">Uma expedição de 40 a 60 minutos por um mundo próprio, escuro e cheio de assombrações do folclore. Junte até <b>5 jogadores</b>, atravesse <b>5 regiões abertas</b>, cumpra as missões de cada uma, saqueie os baús e derrote os chefes até chegar ao Boitatá.</p>
<div class="vitrine">
  <?php foreach (['chave_1', 'semente', 'gorro', 'chave_3', 'ingrediente', 'escama', 'chave_5', 'trofeu_boitata'] as $n) echo img($n, '', 'ico-vitrine'); ?>
</div>

<h2>Horário</h2>
<ul class="lista">
  <li>A masmorra abre <b>de 2 em 2 horas, nas horas ímpares</b> (17h, 19h, 21h...).</li>
  <li>A entrada abre <b>3 minutos antes</b> do horário. Entre com <?= cmd('/dungeon entrar') ?> ou pela ruína no lobby; você espera no salão de entrada.</li>
  <li>No horário em ponto a entrada <b>fecha</b>, e <b>30 segundos depois</b> o portão abre e o grupo todo começa junto.</li>
  <li>Fora do horário, <?= cmd('/dungeon') ?> mostra quando a próxima entrada abre.</li>
</ul>

<h2>As regiões</h2>
<p>Cada região tem relevo, trilha, acampamentos de criaturas, baús escondidos e um cofre trancado. A arena do chefe só abre quando o grupo cumpre as <b>3 missões</b> da região.</p>
<table class="tabela">
  <tr><th>Região</th><th>Chefe</th><th>Missões</th></tr>
  <tr><td><?= grad('Floresta Viva', '#d9f99d,#4ade80,#166534', 'b') ?></td><td>Curupira</td><td>Expulsar 10 Espíritos da Mata · achar 5 Sementes Sagradas · acender as 3 fogueiras dos pajés</td></tr>
  <tr><td><?= grad('Campos do Redemoinho', '#fecaca,#ef4444,#7f1d1d', 'b') ?></td><td>Saci-Pererê</td><td>Derrotar 10 Vultos do Redemoinho · recuperar 4 gorros do Saci · tocar os 3 sinos de vento</td></tr>
  <tr><td><?= grad('Cemitério Esquecido', '#e5e7eb,#9ca3af,#f97316', 'b') ?></td><td>Mula sem Cabeça</td><td>Libertar 10 Almas · acender as 4 velas dos túmulos · abrir o Mausoléu com a Chave de Ossos</td></tr>
  <tr><td><?= grad('Pântano da Cuca', '#d9f99d,#84cc16,#365314', 'b') ?></td><td>Cuca</td><td>Derrotar 10 Aranhas da Cuca · colher 5 cogumelos do caldeirão · derramar os 3 caldeirões</td></tr>
  <tr><td><?= grad('Vulcão do Boitatá', '#fef08a,#ff7a00,#b91c1c', 'b') ?></td><td>Boitatá</td><td>Apagar 12 Chamas Errantes · apagar os 4 fogos-fátuos · recolher 3 Escamas de Fogo</td></tr>
</table>
<p>A barra no topo da tela mostra o progresso, e <?= cmd('/dungeon missoes') ?> lista tudo. Os objetos de coleta brilham e giram no chão; as criaturas aparecem quando o grupo chega perto dos acampamentos.</p>

<h2>Baús, chaves e cofres</h2>
<div class="grade-2">
  <?php card_abre('incomum'); ?><h3>Baús da região</h3><p>5 por região, divididos com o grupo: comida, ferro, ouro, flechas, poções, XP, esmeraldas e diamantes, além de moedas para todos. Têm chance de <b>chave de lootbox</b> (Comum, Ultra ou dos Ovos).</p><?php card_fecha(); ?>
  <?php card_abre('raro'); ?><h3>Chaves de porta</h3><p>Cada região esconde a sua chave (Raiz, Vento, Ossos, Lodo e Brasa) num dos baús. Ela abre o <b>cofre trancado</b> da região: segure a chave e clique no portão de ferro. As chaves de porta somem quando você sai da masmorra.</p><?php card_fecha(); ?>
  <?php card_abre('epico'); ?><h3>Cofres</h3><p>Diamantes, esmeraldas, maçãs douradas, poções fortes, livro encantado e chance bem maior de chaves de lootbox. No Vulcão pode ter netherite.</p><?php card_fecha(); ?>
  <?php card_abre('lendario'); ?><h3>Tesouro final</h3><p>Depois do Boitatá, cada jogador abre o próprio baú do tesouro: diamantes, ouro, netherite, chaves de lootbox e <?= moedas(500) ?>.</p><?php card_fecha(); ?>
</div>

<h2>Regras</h2>
<ul class="lista">
  <li>Cada jogador traz <b>3 vidas</b> para a equipe. Cada morte gasta uma; quem morre volta para o começo da região atual. Sem vidas, todos são expulsos.</li>
  <li>Tempo limite de <b>80 minutos</b>. Depois de jogar, espere 60 minutos para entrar de novo.</li>
  <li>Moedas a cada chefe: <?= moedas(150) ?>, <?= moedas(250) ?>, <?= moedas(350) ?>, <?= moedas(500) ?> e <?= moedas(1000) ?> para <b>cada</b> jogador do grupo.</li>
  <li>Ao vencer o Boitatá, cada um tem 25% de chance de ganhar uma caixa da sua classe e 10% de ganhar o troféu.</li>
  <li><?= cmd('/dungeon historia') ?> conta a lenda. <?= cmd('/dungeon sair') ?> abandona a masmorra.</li>
</ul>

<div class="destaque"><?= img('trofeu_boitata', '', 'ico-grande') ?><div><h3><?= grad('Troféu do Boitatá', '#ffd23f,#ff7a00,#ff3d00') ?></h3><p>Coloque no chão como enfeite 3D (clique direito) e bata nele para guardar de volta.</p></div></div>

<h2>Os chefes</h2>
<ol class="chefes">
  <li><b>Curupira</b><p>O guardião da mata, com os pés virados para trás. Engana quem tenta segui-lo.</p></li>
  <li><b>Saci-Pererê</b><p>Rápido e brincalhão, some num redemoinho e aparece onde você não espera.</p></li>
  <li><b>Mula sem Cabeça</b><p>Galopa em chamas e atropela tudo pela frente.</p></li>
  <li><b>Cuca</b><p>A bruxa jacaré. Feitiços, poções e muita paciência.</p></li>
  <li><b>Boitatá</b><p>A serpente de fogo. O chefe final, com corpo em várias partes.</p></li>
</ol>
