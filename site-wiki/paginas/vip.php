<?php $DESC = 'Cargos, VIP e tags da Comunidade BIG.'; ?>
<h1><?= grad('VIP, tags e ranks', '#fff7c2,#fbbf24,#a855f7') ?></h1>
<p class="intro">Os cargos aparecem como tag no chat e no TAB. VIPs ajudam a manter o servidor e ganham vantagens de conforto, sem pagar para ganhar.</p>
<table class="tabela">
  <tr><th>Cargo</th><th>Blocos de proteção extra</th><th>Casas</th><th>/explorar</th><th>Anúncios no leilão</th></tr>
  <tr><td><span class="tag-rank">[Membro]</span></td><td>—</td><td>5</td><td>espera normal</td><td>3</td></tr>
  <tr><td><span class="tag-rank" style="color:#22d3ee">[VIP]</span></td><td>+1000</td><td>10</td><td>20 s</td><td>5</td></tr>
  <tr><td><span class="tag-rank"><?= grad('[VIP+]', '#e9d5ff,#a855f7') ?></span></td><td>+2000</td><td>20</td><td>15 s</td><td>8</td></tr>
  <tr><td><span class="tag-rank"><?= grad('[Lendário]', '#fde68a,#f59e0b') ?></span></td><td>+3000</td><td>50</td><td>10 s</td><td>12</td></tr>
</table>
<h2>Vantagens de todos os VIPs</h2>
<ul class="lista">
  <li><b>Nick colorido</b> com <?= cmd('/nick <código>') ?> (veja <a href="<?= e(url('chat')) ?>">Chat, emojis e nick</a>).</li>
  <li>Nos seus terrenos: <b>fly</b>, <b>durabilidade infinita</b>, <b>keep inventory</b> e <b>plantação 2x</b>, ligados em <?= cmd('/prot opções') ?>.</li>
</ul>
<p><?= cmd('/vip') ?> mostra seu VIP e quanto tempo falta. <?= cmd('/tags') ?> escolhe qual tag aparece no chat.</p>
<?php if (LINK_LOJA_VIP): ?><p><a class="btn primario" href="<?= e(LINK_LOJA_VIP) ?>" target="_blank" rel="noopener">Quero ser VIP</a></p><?php endif; ?>
