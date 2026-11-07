<?php $DESC = 'Como proteger seu terreno, marcar casas e pegar kits.'; ?>
<h1><?= grad('Terrenos, casas e kits', '#fde68a,#f59e0b') ?></h1>

<h2>Protegendo seu terreno</h2>
<ol class="lista">
  <li>Pegue o kit com <?= cmd('/kit prot') ?>: vem uma <b>pá de ouro</b> e um <b>graveto</b> (a cada 60 minutos).</li>
  <li>Com a pá, clique com o botão direito em <b>dois cantos opostos</b> da área. Pronto: o terreno é seu.</li>
  <li>Para aumentar ou diminuir, clique num canto do terreno e depois no novo lugar.</li>
  <li>O <b>graveto</b> mostra de quem é o bloco. Agachado, mostra os terrenos por perto.</li>
</ol>
<p>Cada terreno gasta <b>blocos de proteção</b>. Todo jogador começa com <b>1000 blocos</b> e ganha <b>100 a cada 20 minutos</b> online. Também dá para ganhar nas <a href="<?= e(url('lootbox')) ?>">lootboxes</a> e com <a href="<?= e(url('vip')) ?>">VIP</a>. Veja quantos tem com <?= cmd('/prot blocos') ?>.</p>

<h2>Amigos no terreno</h2>
<table class="tabela">
  <tr><th>Comando</th><th>O que faz</th></tr>
  <tr><td><?= cmd('/prot confiar <jogador>') ?></td><td>Pode construir e quebrar.</td></tr>
  <tr><td><?= cmd('/prot bau <jogador>') ?></td><td>Pode abrir baús e usar fornalhas.</td></tr>
  <tr><td><?= cmd('/prot acesso <jogador>') ?></td><td>Pode usar portas, botões e camas.</td></tr>
  <tr><td><?= cmd('/prot remover <jogador>') ?></td><td>Tira a permissão.</td></tr>
  <tr><td><?= cmd('/prot opções') ?></td><td>Menu de opções do terreno (veja abaixo).</td></tr>
  <tr><td><?= cmd('/prot nome <nome>') ?></td><td>Dá um nome ao terreno (até 24 letras). Quem entra vê o nome na tela.</td></tr>
  <tr><td><?= cmd('/prot info') ?></td><td>Nome, dono, tamanho e opções do terreno.</td></tr>
  <tr><td><?= cmd('/prot abandonar') ?></td><td>Apaga o terreno onde você está.</td></tr>
</table>

<h2>Opções do terreno</h2>
<table class="tabela">
  <tr><th>Opção</th><th>Padrão</th><th>O que faz</th></tr>
  <tr><td>TNT explode</td><td>desligado</td><td>Explosões de TNT e creeper quebram blocos.</td></tr>
  <tr><td>Nasce mob hostil</td><td>ligado</td><td>Monstros aparecem sozinhos no terreno.</td></tr>
  <tr><td>Nasce animal</td><td>ligado</td><td>Porcos, vacas, ovelhas e outros animais aparecem sozinhos.</td></tr>
  <tr><td>Dano de queda</td><td>ligado</td><td>Desligado, ninguém se machuca caindo dentro do terreno.</td></tr>
  <tr><td>Sem fome</td><td>desligado</td><td>Ligado, ninguém perde fome dentro do terreno.</td></tr>
  <tr><td>Aviso de visitas</td><td>ligado</td><td>O dono recebe um aviso quando alguém entra ou sai.</td></tr>
  <tr><td><b style="color:#fbbf24">★ Fly</b></td><td>desligado</td><td>Você e quem tem <?= cmd('/prot confiar') ?> voam dentro do terreno.</td></tr>
  <tr><td><b style="color:#fbbf24">★ Durabilidade infinita</b></td><td>desligado</td><td>Ferramentas e armaduras não gastam dentro do terreno.</td></tr>
  <tr><td><b style="color:#fbbf24">★ Keep inventory</b></td><td>desligado</td><td>Morreu dentro do terreno? Não perde itens nem XP.</td></tr>
  <tr><td><b style="color:#fbbf24">★ Plantação 2x</b></td><td>desligado</td><td>As plantações normais do Minecraft crescem duas vezes mais rápido.</td></tr>
</table>
<p>As opções com <b style="color:#fbbf24">★</b> são <a href="<?= e(url('vip')) ?>">VIP</a>. Se o VIP acabar, elas desligam sozinhas.</p>

<h2>Kits</h2>
<table class="tabela">
  <tr><th>Kit</th><th>O que vem</th><th>Pode pegar</th></tr>
  <tr><td><?= cmd('/kit inicial') ?></td><td>Armadura completa e espada, picareta, machado, pá e enxada de ferro.</td><td>Uma vez só</td></tr>
  <tr><td><?= cmd('/kit plantação') ?></td><td>Enxada de pedra e 5 sementes de cada: trigo, beterraba, cenoura, batata, melancia, abóbora e as 6 safras do servidor.</td><td>A cada 24 horas</td></tr>
  <tr><td><?= cmd('/kit prot') ?></td><td>Pá de ouro e graveto.</td><td>A cada 60 minutos</td></tr>
</table>

<h2>Casas</h2>
<p>Casas são pontos de teleporte: <?= cmd('/casa criar <nome>') ?> marca o lugar e <?= cmd('/casa <nome>') ?> leva você até lá (com alguns segundos de espera).</p>
<table class="tabela">
  <tr><th>Cargo</th><th>Casas</th><th>Espera</th></tr>
  <tr><td>Membro</td><td>5</td><td>3 s</td></tr>
  <tr><td>VIP</td><td>10</td><td>3 s</td></tr>
  <tr><td>VIP+</td><td>20</td><td>sem espera</td></tr>
  <tr><td>Lendário</td><td>50</td><td>sem espera</td></tr>
</table>

<h2>Itens no chão</h2>
<p>A cada 10 minutos o chão é limpo (com aviso no chat). Itens valiosos ficam: itens do RPG, encantados, com nome, de diamante e netherite, shulkers, peixes, colheitas e outros. Itens que acabaram de cair também ficam por 30 segundos. <?= cmd('/limpeza') ?> mostra quanto falta.</p>
