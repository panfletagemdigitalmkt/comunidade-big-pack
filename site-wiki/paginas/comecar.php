<?php $DESC = 'Guia para os primeiros minutos na Comunidade BIG.'; ?>
<h1><?= grad('Como começar', '#fae8ff,#f0abfc,#a855f7') ?></h1>
<p class="intro">Bem-vindo à <b>Comunidade BIG</b>! É um servidor de sobrevivência com RPG: você escolhe uma classe, evolui jogando e usa habilidades em combate. Tudo funciona só com plugins e um pacote de texturas, sem precisar instalar mod nenhum.</p>

<h2>1. Entrando no servidor</h2>
<ul class="lista">
  <li>Use o Minecraft <b><?= e(VERSAO_MINECRAFT) ?></b> e o IP <code><?= e(SERVIDOR_IP_EXIBIDO) ?></code>.</li>
  <li>Na primeira vez, crie uma senha com <?= cmd('/register <senha> <senha>') ?>. Nas próximas, use <?= cmd('/login <senha>') ?> (contas originais entram direto).</li>
  <li><b>Aceite o pacote de texturas.</b> Sem ele os itens especiais aparecem como cubos roxos e pretos.</li>
</ul>
<div class="dica"><b>Deu "falha ao baixar a textura"?</b> Feche o jogo, apague a pasta <code>%appdata%\.minecraft\downloads</code> e entre de novo. Confira também se os pacotes de recursos do servidor estão como <em>Ativado</em> na lista de servidores.</div>

<h2>2. O lobby</h2>
<p>Você nasce na <a href="<?= e(url('lobby')) ?>">vila do lobby</a>. Lá ficam a feira, a fazenda modelo, o Santuário das Caixas, a casa de leilões, a masmorra e o portal para o mundo. Os moradores (NPCs) abrem os menus quando você clica neles.</p>

<h2>3. Escolha sua classe</h2>
<p>Fale com o <b>Mestre Aurélio</b> no Salão das Classes ou use <?= cmd('/classe') ?>. Veja as diferenças em <a href="<?= e(url('classes')) ?>">As 6 classes</a>. Dá para trocar depois, mas só a cada 24 horas.</p>
<div class="dica"><b>Presente de boas-vindas:</b> ao escolher sua <b>primeira classe</b> você ganha <b>20 caixas da classe</b>. Pegue também o <?= cmd('/kit inicial') ?> (armadura e ferramentas de ferro) e o <?= cmd('/kit plantação') ?>.</div>
<p>As habilidades ficam sempre prontas: segure <kbd>Shift</kbd> e aperte <kbd>1</kbd> a <kbd>6</kbd>. Veja <a href="<?= e(url('combate')) ?>">Combate e habilidades</a>.</p>

<h2>4. Vá para o mundo</h2>
<ul class="lista">
  <li>Atravesse o <b>portal JOGAR</b> (ou use <?= cmd('/jogar') ?>) para voltar de onde parou.</li>
  <li>Na primeira vez você cai num lugar aleatório. Para ir a outro lugar aleatório, use <?= cmd('/explorar') ?>.</li>
  <li><?= cmd('/lobby') ?> traz você de volta para a vila a qualquer momento.</li>
</ul>

<h2>5. Proteja sua base</h2>
<p>Você começa com 1000 blocos de proteção e ganha 100 a cada 20 minutos. Pegue o <?= cmd('/kit prot') ?> (pá de ouro + graveto) e marque dois cantos do terreno com a pá. Ninguém mexe no que estiver dentro. Detalhes em <a href="<?= e(url('protecao')) ?>">Terrenos, casas e kits</a>.</p>

<h2>6. Evolua jogando</h2>
<div class="grade-2">
  <?php card_abre('raro'); ?><h3>Pontos de Classe</h3><p>Cada hora jogando de verdade (não vale ficar parado) dá 1 ponto para acender estrelas na <a href="<?= e(url('constelacoes')) ?>">constelação</a> da sua classe.</p><?php card_fecha(); ?>
  <?php card_abre('epico'); ?><h3>Caixas e chaves</h3><p>A cada 3 horas ativas você ganha uma <a href="<?= e(url('itens')) ?>">caixa da sua classe</a>, e o tempo jogado também dá <a href="<?= e(url('lootbox')) ?>">chaves de lootbox</a>.</p><?php card_fecha(); ?>
  <?php card_abre('lendario'); ?><h3>Moedas</h3><p>Você começa com <?= moedas(200) ?> e ganha <?= moedas(25) ?> por hora ativa, além de tudo o que vender na <a href="<?= e(url('economia')) ?>">loja</a>.</p><?php card_fecha(); ?>
  <?php card_abre('epico'); ?><h3>Eventos e masmorra</h3><p>De 2 em 2 horas tem <a href="<?= e(url('eventos')) ?>">evento</a> (horas pares) e <a href="<?= e(url('masmorra')) ?>">masmorra</a> (horas ímpares), com moedas e chaves de prêmio.</p><?php card_fecha(); ?>
  <?php card_abre('incomum'); ?><h3>Profissões</h3><p>Plante na <a href="<?= e(url('fazenda')) ?>">fazenda</a>, pesque com a <a href="<?= e(url('pesca')) ?>">briga na linha</a> e venda tudo com <?= cmd('/vender') ?>.</p><?php card_fecha(); ?>
</div>
