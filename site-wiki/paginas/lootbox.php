<?php $DESC = 'Lootboxes do Santuário: Caixa Comum, Ultra e dos Ovos, e as chaves por tempo jogado.'; ?>
<h1><?= grad('Lootboxes e chaves', '#fde68a,#f0abfc,#22d3ee') ?></h1>
<p class="intro">No terraço atrás do Santuário das Caixas, no lobby, ficam três caixas de verdade. Segure a chave certa e clique com o botão direito: a tampa abre e os prêmios giram até parar no seu.</p>

<h2>Chaves pelo tempo jogado</h2>
<table class="tabela">
  <tr><th></th><th>Chave</th><th>Você ganha</th></tr>
  <?php foreach ($LOOTBOX as $id => [$nome, $cores, $min]): ?>
    <tr><td><?= img('chave_' . $id) ?></td><td><?= grad('Chave da ' . $nome, $cores, 'b') ?></td><td>1 a cada <b><?= $min / 60 ?> hora<?= $min > 60 ? 's' : '' ?></b> jogando</td></tr>
  <?php endforeach; ?>
</table>
<p>Ficar 5 minutos parado (sem mexer a câmera) não conta. Veja quantas chaves você tem e quanto falta com <?= cmd('/chaves') ?>.</p>
<p>Também dá para ganhar chaves vencendo os <a href="<?= e(url('eventos')) ?>">eventos</a> e nos baús e cofres da <a href="<?= e(url('masmorra')) ?>">masmorra</a>.</p>

<h2>As caixas</h2>
<div class="grade-3">
<?php foreach ($LOOTBOX as $id => [$nome, $cores, $min, $desc, $premios]): ?>
  <?php card_abre($id === 'ultra' ? 'lendario' : ($id === 'ovos' ? 'incomum' : 'comum')); ?>
    <div class="lootbox"><?= img('caixa_' . $id . '_inteira', $nome, 'ico-grande') ?>
      <h3><?= grad($nome, $cores) ?></h3><p><?= e($desc) ?></p>
      <ul class="premios"><?php foreach ($premios as [$t, $r]): ?><li><?= selo($r) ?> <?= e($t) ?></li><?php endforeach; ?></ul>
    </div>
  <?php card_fecha(); ?>
<?php endforeach; ?>
</div>
<div class="dica">Clique esquerdo numa caixa (ou clique sem a chave) mostra todos os prêmios com a chance exata de cada um. Prêmios épicos e lendários são anunciados no chat.</div>
