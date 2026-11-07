<?php $DESC = 'Teclas das habilidades, vida, recurso e estilo de luta.'; ?>
<h1><?= grad('Combate e habilidades', '#fecaca,#ef4444,#7c3aed') ?></h1>
<p class="intro">O combate do servidor tem vida em números (ex.: <b>228/228</b>), uma barra de recurso da sua classe e habilidades sempre prontas: é só segurar <kbd>Shift</kbd> e apertar <kbd>1</kbd> a <kbd>6</kbd>.</p>

<h2>Usando as habilidades</h2>
<div class="grade-2">
  <?php card_abre('epico'); ?>
    <h3>Sempre prontas</h3>
    <p>Não precisa ligar nada: com classe, segure <kbd>Shift</kbd> e aperte <kbd>1</kbd> a <kbd>4</kbd> para as habilidades e <kbd>5</kbd> para a suprema. Com signo, <kbd>Shift</kbd> + <kbd>6</kbd> usa a habilidade do signo.</p>
  <?php card_fecha(); ?>
  <?php card_abre('raro'); ?>
    <h3>Hotbar normal</h3>
    <p>Sem Shift, as teclas 1 a 9 trocam de item normalmente e o <kbd>F</kbd> troca o item de mão. Enquanto você segura Shift (ou está em combate), a barra das habilidades mostra as recargas.</p>
  <?php card_fecha(); ?>
</div>
<p>Prefere outro jeito? Em <?= cmd('/atalhos') ?> dá para usar o modo combate antigo (só os números, sem Shift) ou um botão do mouse. As habilidades não funcionam no lobby nem nos eventos.</p>

<h2>Vida, dano e recurso</h2>
<ul class="lista">
  <li><b>Vida</b> aparece em números acima da barra de corações. A <b>Vitalidade</b> aumenta a vida máxima.</li>
  <li><b>Força</b> e <b>Destreza</b> aumentam o dano, <b>Sabedoria</b> aumenta a cura e <b>Defesa</b> reduz o dano recebido.</li>
  <li>O <b>recurso</b> (Fé, Ira, Energia, Mana, Sombra ou Chakra) paga as habilidades. Cada classe recupera de um jeito.</li>
  <li>Veja tudo com <?= cmd('/perfil') ?>. O estilo de luta da sua classe aparece em <?= cmd('/estilo') ?>.</li>
</ul>

<h2>Estilos de luta</h2>
<table class="tabela">
  <tr><th>Classe</th><th>Como luta</th></tr>
  <?php foreach ($CLASSES as $c): ?>
    <tr><td><?= grad($c['nome'], $c['cores'], 'b') ?></td><td><?= e($c['estilo']) ?></td></tr>
  <?php endforeach; ?>
</table>
<div class="dica">Os itens de classe só dão atributos para o dono, na classe certa e na mão certa (principal, secundária ou vestido).</div>
