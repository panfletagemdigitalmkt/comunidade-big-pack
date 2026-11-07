<?php $DESC = 'Eventos automáticos de 2 em 2 horas: Batata Quente, Sinuca de Gelo, Resta 1, Spleef e mais.'; ?>
<h1><?= grad('Eventos automáticos', '#f472b6,#facc15,#22d3ee') ?></h1>
<p class="intro">De <b>2 em 2 horas</b>, nas horas pares (18h, 20h, 22h, 0h...), começa um minigame num mundo só de eventos. Os eventos seguem um rodízio e só se repetem depois de passar por todos. 5 minutos antes aparece um aviso no chat.</p>

<div class="vitrine">
  <?php foreach (['batata_quente', 'taco', 'espada_torneio', 'pa_spleef', 'travesseiro', 'coroa', 'bola_8'] as $n) echo img($n, '', 'ico-vitrine'); ?>
</div>

<h2>Como participar</h2>
<ul class="lista">
  <li>Quando o evento abre, clique em <b>[PARTICIPAR]</b> no chat ou use <?= cmd('/evento entrar') ?>. A inscrição fica aberta por <b>90 segundos</b>.</li>
  <li>Precisa de pelo menos <b>2 jogadores</b>; senão o evento é cancelado.</li>
  <li>Seu inventário, XP, vida, efeitos e o lugar onde você estava ficam <b>guardados</b> e voltam no fim. Se cair do servidor no meio, recebe tudo de volta ao entrar.</li>
  <li>Dentro do evento ninguém morre de verdade nem perde fome, e as habilidades de classe ficam desligadas. Só o chat e alguns comandos funcionam.</li>
  <li>Eliminado? Você vira espectador e assiste até o fim. <?= cmd('/evento sair') ?> volta na hora.</li>
  <li>Quer só olhar? <?= cmd('/evento assistir') ?>.</li>
</ul>

<h2>Prêmios</h2>
<table class="tabela">
  <tr><th>Lugar</th><th>Prêmio</th></tr>
  <tr><td><b style="color:#fbbf24">1º</b></td><td><?= moedas(1000) ?> + uma <b>Chave da Caixa Comum</b></td></tr>
  <tr><td><b style="color:#d1d5db">2º</b></td><td><?= moedas(500) ?></td></tr>
  <tr><td><b style="color:#cd7f32">3º</b></td><td><?= moedas(250) ?></td></tr>
</table>
<p>No <b>Verdadeiro ou Falso</b>, se mais de um sobreviver, os sobreviventes dividem o prêmio do 1º lugar e cada um leva uma chave.</p>

<h2>Os 10 eventos</h2>
<?php
$ev = [
    ['batata_quente', 'Batata Quente', '#fde68a,#f97316,#dc2626', 'Quem está com a batata (na mão e na cabeça) passa batendo em alguém. Quando o pavio acaba, ela explode e quem estiver com ela sai. O último que sobrar vence.'],
    ['taco', 'Sinuca de Gelo', '#e0f2fe,#38bdf8,#15803d', 'Uma mesa de sinuca gigante de gelo com 6 caçapas. O taco empurra longe: encaçape os outros e não seja encaçapado. Depois de 2min30 a mesa fica turbinada.'],
    ['espada_torneio', 'Resta 1', '#fecaca,#ef4444,#7f1d1d', 'Todos contra todos no coliseu com a espada de torneio. Cada um tem 10 corações de evento; golpe crítico tira mais. Depois de 3 minutos entra a morte súbita.'],
    ['pa_spleef', 'Spleef', '#ffffff,#bae6fd,#0284c7', 'Dois andares de neve. A pá de gelo quebra a neve na hora e cada bloco vira uma bola de neve que empurra. Quem cai dos dois andares sai.'],
    ['coroa', 'Rei da Colina', '#fff7c2,#fbbf24,#b45309', 'Fique no topo dourado da colina para ganhar 1 ponto por segundo. Derrube os outros com o travesseiro. Vence quem chegar a 90 pontos ou tiver mais pontos em 3 minutos.'],
    ['bola_8', 'Chão que Cai', '#fbcfe8,#f472b6,#7c3aed', 'Três andares coloridos: cada bloco em que você pisa some em instantes. Não pare de andar!'],
    ['semente', 'Batatinha Frita 1, 2, 3', '#fef08a,#f59e0b,#dc2626', 'Corra até a Boneca Caipira gigante enquanto ela canta de costas. Quando ela virar, fique parado: quem se mexer sai. Os 3 primeiros a chegar ganham.'],
    ['chave_comum', 'Dança das Cores', '#f472b6,#facc15,#22d3ee', 'O chão é colorido e uma cor é sorteada. Corra para ela antes que todo o resto suma. Fica mais rápido a cada rodada.'],
    ['chave_ultra', 'Corrida Parkour', '#bbf7d0,#22c55e,#0ea5e9', 'Percurso de 48 pulos no céu com pontos de controle dourados. Caiu? Volta para o último ponto. Os 3 primeiros a chegar ganham.'],
    ['tomo_luz', 'Verdadeiro ou Falso', '#bbf7d0,#a3e635,#ef4444', 'Aparece uma afirmação sobre Minecraft, Brasil, folclore ou o próprio servidor. Fique no lado V ou F: o chão do lado errado some.'],
];
?>
<div class="grade-2">
<?php foreach ($ev as [$ic, $nome, $cores, $txt]): ?>
  <?php card_abre('epico'); ?>
    <div class="lugar"><?= img($ic) ?><div><h3><?= grad($nome, $cores) ?></h3><p><?= e($txt) ?></p></div></div>
  <?php card_fecha(); ?>
<?php endforeach; ?>
</div>

<h2>Comandos</h2>
<table class="tabela">
  <tr><td><?= cmd('/evento') ?></td><td>Qual é o próximo evento e a que horas.</td></tr>
  <tr><td><?= cmd('/evento entrar') ?></td><td>Participa do evento aberto.</td></tr>
  <tr><td><?= cmd('/evento assistir') ?></td><td>Assiste ao evento que está acontecendo.</td></tr>
  <tr><td><?= cmd('/evento sair') ?></td><td>Sai do evento e recebe suas coisas de volta.</td></tr>
  <tr><td><?= cmd('/evento lista') ?></td><td>Todos os eventos do rodízio.</td></tr>
</table>
<div class="dica">Os eventos acontecem nas horas pares e a masmorra nas horas ímpares, então dá para jogar os dois.</div>
