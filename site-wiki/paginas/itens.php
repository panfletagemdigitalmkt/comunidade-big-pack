<?php $DESC = 'Itens 3D de classe, raridades, caixas de classe e fragmentos.'; ?>
<h1><?= grad('Itens e caixas de classe', '#fff7c2,#fbbf24,#f97316') ?></h1>
<p class="intro">Cada classe tem armas, escudos, livros e armaduras próprios, todos em 3D e no nível do netherite. Eles saem das <b>caixas de classe</b>.</p>

<div class="vitrine">
  <?php foreach (['espada_justica', 'escudo_egide', 'sol_elmo', 'machado_alfa', 'lobo_cabeca', 'arco_falcao', 'falcao_capuz', 'cetro_aureo', 'tomo_luz', 'adaga_viuva', 'corvo_capuz', 'kusanagi', 'nevoa_mascara'] as $n) echo img($n, '', 'ico-vitrine'); ?>
</div>

<h2>Como ganhar caixas</h2>
<ul class="lista">
  <li><b>20 caixas</b> de presente ao escolher a sua <b>primeira classe</b>.</li>
  <li><b>1 caixa da sua classe a cada 3 horas</b> jogando de verdade.</li>
  <li>Comprando no Santuário das Caixas ou em <?= cmd('/loja') ?> → Caixas de classe, por <?= moedas(1500) ?>.</li>
  <li>Na masmorra (25% de chance ao vencer) e na <a href="<?= e(url('lootbox')) ?>">Caixa Ultra</a>.</li>
</ul>
<p>Abra a caixa com o botão direito. Os itens são <b>vinculados a você</b>: só funcionam para o dono.</p>

<h2>Raridades</h2>
<table class="tabela">
  <tr><th>Raridade</th><th>Chance</th><th>Repetido vira</th><th>Custo na loja de fragmentos</th></tr>
  <?php foreach ([['comum', 50, 5, 30], ['raro', 30, 10, 60], ['epico', 15, 20, 120], ['lendario', 5, 50, 300]] as [$r, $ch, $fr, $cu]): ?>
    <tr><td><?= selo($r) ?></td><td><?= $ch ?>%</td><td><?= $fr ?> fragmentos</td><td><?= $cu ?> fragmentos</td></tr>
  <?php endforeach; ?>
</table>
<p>Item repetido vira <b>fragmento</b> da classe. Junte fragmentos e escolha o item que quiser em <?= cmd('/caixa loja') ?>. Sua coleção fica em <?= cmd('/caixa colecao') ?>.</p>

<h2>Caixas das classes</h2>
<div class="vitrine">
  <?php foreach ($CLASSES as $id => $c): ?><figure><?= img('caixa_' . $id, '', 'ico-vitrine') ?><figcaption><?= grad($c['nome'], $c['cores']) ?></figcaption></figure><?php endforeach; ?>
</div>
