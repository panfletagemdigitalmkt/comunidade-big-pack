<?php $st = mc_status(); ?>
<section class="hero">
  <img class="hero-logo" src="<?= e(asset('img/logo.png')) ?>" alt="">
  <h1 class="hero-titulo"><?= grad('COMUNIDADE BIG', '#fae8ff,#f0abfc,#a855f7,#6366f1') ?></h1>
  <p class="hero-sub"><?= e(SITE_SLOGAN) ?></p>
  <div class="hero-ip">
    <button class="btn-ip grande" data-ip="<?= e(SERVIDOR_IP_EXIBIDO) ?>"><small>Clique para copiar o IP</small><span><?= e(SERVIDOR_IP_EXIBIDO) ?></span></button>
    <div class="hero-status <?= $st['online'] ? 'on' : 'off' ?>">
      <i></i>
      <?php if ($st['online']): ?>
        <b><?= e($st['jogadores']) ?></b> de <?= e($st['max']) ?> jogadores online
      <?php else: ?>Servidor offline no momento<?php endif; ?>
      <small>Minecraft <?= e(VERSAO_MINECRAFT) ?></small>
    </div>
  </div>
  <div class="hero-botoes">
    <a class="btn primario" href="<?= e(url('comecar')) ?>">Como começar</a>
    <a class="btn" href="<?= e(url('classes')) ?>">Ver as classes</a>
    <?php if (LINK_DISCORD): ?><a class="btn" href="<?= e(LINK_DISCORD) ?>" target="_blank" rel="noopener">Discord</a><?php endif; ?>
  </div>
  <div class="hero-itens" aria-hidden="true">
    <?php foreach (['espada_justica', 'machado_alfa', 'arco_falcao', 'cetro_aureo', 'adaga_viuva', 'kusanagi'] as $i => $n): ?>
      <span style="--d:<?= $i * 0.4 ?>s"><?= img($n) ?></span>
    <?php endforeach; ?>
  </div>
</section>

<section class="secao">
  <h2 class="titulo-secao"><?= grad('O que tem no servidor', '#f0abfc,#a855f7') ?></h2>
  <div class="grade-recursos">
    <?php
    $rec = [
        ['classes', 'espada_justica', 'epico', '6 classes de RPG', 'Paladino, Berserker, Arqueiro, Clérigo, Assassino e Ninja, cada um com 5 habilidades, passiva e estilo de luta próprio.'],
        ['constelacoes', 'tomo_luz', 'raro', 'Constelações e signos', 'Árvores de talentos em forma de estrelas e os 12 signos do zodíaco com habilidades extras.'],
        ['itens', 'caixa_paladino', 'lendario', 'Itens 3D de classe', 'Armas, escudos e armaduras feitos à mão no Blockbench, de comum a lendário.'],
        ['masmorra', 'trofeu_boitata', 'lendario', 'Expedição do folclore', '5 regiões com missões, baús e cofres trancados até o Curupira, o Saci, a Mula, a Cuca e o Boitatá.'],
        ['eventos', 'batata_quente', 'epico', 'Eventos de 2 em 2 horas', 'Batata Quente, Sinuca de Gelo, Resta 1, Spleef, Batatinha Frita e mais, com prêmios.'],
        ['chat', 'coroa', 'raro', 'Chat com emojis', 'Chat local, global e do clan, 41 emojis em pixel art e nick colorido para VIP.'],
        ['fazenda', 'abacaxi', 'incomum', 'Fazenda', '6 safras brasileiras que crescem em tempo real e podem sair douradas.'],
        ['pesca', 'pirarucu', 'raro', 'Pescaria', '16 peixes, briga na linha, varas 3D e recordes de peso.'],
        ['economia', 'caixa_ultra_inteira', 'epico', 'Economia e leilão', 'Moedas, loja do servidor, venda de tudo o que você produz e leilão entre jogadores.'],
        ['lootbox', 'chave_ultra', 'lendario', 'Lootboxes', 'Chaves pelo tempo jogado e caixas físicas na vila com prêmios de verdade.'],
        ['clans', 'falcao_capuz', 'raro', 'Clans', 'Tags coloridas, base, aliados, rivais, níveis e ranking.'],
    ];
    foreach ($rec as [$pg, $ic, $est, $tit, $txt]): ?>
      <a class="recurso" href="<?= e(url($pg)) ?>">
        <?php card_abre($est); ?>
          <?= img($ic, '', 'ico-grande') ?>
          <h3><?= e($tit) ?></h3>
          <p><?= e($txt) ?></p>
        <?php card_fecha(); ?>
      </a>
    <?php endforeach; ?>
  </div>
</section>

<section class="secao passos">
  <h2 class="titulo-secao"><?= grad('Como entrar', '#a5f3fc,#38bdf8,#6366f1') ?></h2>
  <ol class="lista-passos">
    <li><b>1</b><div><h3>Abra o Minecraft <?= e(VERSAO_MINECRAFT) ?></h3><p>Vá em <em>Multijogador → Adicionar servidor</em>.</p></div></li>
    <li><b>2</b><div><h3>Cole o IP</h3><p><code><?= e(SERVIDOR_IP_EXIBIDO) ?></code> e deixe os <em>Pacotes de recursos</em> como <em>Ativado</em> ou <em>Perguntar</em>.</p></div></li>
    <li><b>3</b><div><h3>Aceite o pacote de texturas</h3><p>É ele que mostra os itens 3D, as caixas, os peixes e as plantas.</p></div></li>
    <li><b>4</b><div><h3>Escolha sua classe</h3><p>No lobby, fale com o Mestre Aurélio ou use <?= cmd('/classe') ?>. Depois, entre no portal <b>JOGAR</b>.</p></div></li>
  </ol>
</section>
