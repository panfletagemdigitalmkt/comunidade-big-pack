<?php $DESC = 'Fazenda BIG: 19 culturas, qualidade, solo e adubos, máquinas, irrigação, estufas, pragas, mutações, contratos e eventos.'; ?>
<h1><?= grad('Fazenda BIG', '#ecfccb,#84cc16,#eab308') ?></h1>
<p class="intro">Plante em terra arada, cuide da água, da luz e do solo e colha frutos de qualidade. Quem quer só plantar e vender continua podendo; quem quer ir fundo tem máquinas, estufas, mutações, contratos e uma profissão inteira para subir. Tudo começa no <?= cmd('/fazenda') ?>.</p>

<div class="vitrine">
  <?php foreach (['milho', 'morango', 'tomate', 'uva', 'cacau', 'pitaya', 'maquina_moinho', 'produto_geleia_morango', 'milho_azul'] as $n) echo img($n, '', 'ico-vitrine'); ?>
</div>

<h2>Como plantar</h2>
<ul class="lista">
  <li>Compre sementes com o <b>Tião Fazendeiro</b> na vila (ou na <?= cmd('/loja') ?> → Fazenda), are a terra com uma enxada e clique direito para plantar.</li>
  <li>A planta cresce em <b>tempo real</b>, inclusive com você offline. Terra <b>molhada</b> e <b>boa luz</b> mantêm o ritmo; terra seca ou sombra deixam mais lenta; <b>chuva</b> com céu aberto acelera 25%.</li>
  <li><b>Farinha de osso</b> adianta a planta (até 3 por safra).</li>
  <li>Clique direito na planta mostra o progresso. <b>Agachado + clique direito</b> (mão vazia) abre o painel completo: água, luz, solo, pragas e chances de qualidade.</li>
  <li>Agache e bata para arrancar uma planta que ainda não está pronta (a semente volta).</li>
</ul>

<h2>Culturas</h2>
<table class="tabela">
  <tr><th>Cultura</th><th>Tempo</th><th>Frutos</th><th>Venda</th><th>Tipo</th><th>Semente</th></tr>
  <?php foreach ($SAFRAS as $s): ?>
  <tr><td><?= img($s[0], '', 'ico-mini') ?> <b><?= e($s[1]) ?></b><br><small><?= e($s[7]) ?></small></td><td>~<?= $s[2] ?> min</td><td><?= e($s[3]) ?></td><td><?= moedas($s[4]) ?></td><td><?= $s[5] ? 'perene' : 'anual' ?></td><td><?= moedas($s[6]) ?></td></tr>
  <?php endforeach; ?>
</table>
<p><b>Mutações</b> (acontecem a partir do Agricultor 30, plantam a partir do 45): Morango Gigante, Milho Azul, Abacaxi Dourado, Café Ancestral, Tomate Carmesim, Uva Cristalina e Pitaya Radiante. Cada uma tem uma condição — a pista fica no Livro de Sementes. Valem 4x a cultura base.</p>

<h2>Qualidade e douradas</h2>
<p>Cada fruto sai <b>Comum</b>, <b>Boa</b> (×1,2), <b>Excelente</b> (×1,5) ou <b>Perfeita</b> (×2). Ajudam: terra sempre molhada, boa luz, solo rico em potássio, planta saudável, água limpa (filtro) e o seu nível de Agricultor. Nada garante Perfeita. Cada fruto ainda tem <b>5%</b> de chance de sair <b>dourado</b> (vale 5x), à parte da qualidade.</p>

<h2>Solo e adubos</h2>
<ul class="lista">
  <li>Cada bloco de terra tem <b>fertilidade</b> e <b>N, P e K</b> (começam em 60). <b>N</b> acelera, <b>P</b> dá mais frutos, <b>K</b> melhora a qualidade.</li>
  <li>Cada colheita gasta nutrientes. Plantar a <b>mesma cultura</b> no mesmo lugar cansa mais a terra; <b>trocar</b> recupera. A <b>soja devolve nitrogênio</b>. Terra parada volta sozinha até 60.</li>
  <li>Adubos (máx. 2 por safra em cada bloco): composto, nitrogenado, fosfatado, potássico, biofertilizante (protege de pragas), fertilizante líquido (+30% por 20 min) e fertilizante especial (terra Especial por 3 colheitas).</li>
</ul>

<h2>Pragas e doenças</h2>
<p>A partir do Agricultor 5 podem aparecer pulgões, lagartas, besouros, ácaros, fungos, podridão de raiz e mancha foliar. Elas atrasam e tiram um pouco de qualidade e frutos, mas <b>nunca matam a planta</b>. Trate com defensivo natural, antifúngico, recuperador de solo ou controle biológico. Estufa e biofertilizante reduzem o risco.</p>

<h2>Máquinas e depósitos</h2>
<p>Compre na <?= cmd('/loja') ?> → <b>Fazenda · Máquinas</b>, clique direito em cima de um bloco para instalar e clique nela para usar. Coloque os ingredientes clicando nos itens do seu inventário. A produção continua com você offline. Qualidade entra e sai igual; dourada sai dourada. Agache e bata para desmontar (vazia).</p>
<table class="tabela">
  <tr><th>Máquina</th><th>Agricultor</th><th>Faz</th></tr>
  <tr><td><b>Composteira</b></td><td>3</td><td>composto e biofertilizante</td></tr>
  <tr><td><b>Moinho</b></td><td>10</td><td>farinhas de milho, mandioca e arroz</td></tr>
  <tr><td><b>Prensa</b></td><td>10</td><td>óleo vegetal</td></tr>
  <tr><td><b>Tacho</b></td><td>10</td><td>geleias, molhos e doce de abóbora</td></tr>
  <tr><td><b>Espremedor</b></td><td>10</td><td>sucos</td></tr>
  <tr><td><b>Moenda</b></td><td>10</td><td>caldo de cana</td></tr>
  <tr><td><b>Torrefador</b></td><td>10</td><td>café e cacau torrados</td></tr>
  <tr><td><b>Descaroçador</b></td><td>10</td><td>fibra de algodão</td></tr>
  <tr><td><b>Desidratador</b></td><td>10</td><td>uva-passa e pitaya seca</td></tr>
  <tr><td><b>Secador</b></td><td>20</td><td>cacau seco</td></tr>
  <tr><td><b>Refinador</b></td><td>20</td><td>açúcar, chocolate, chocolate fino e fertilizante especial</td></tr>
  <tr><td><b>Tear</b></td><td>20</td><td>tecido</td></tr>
  <tr><td><b>Depósito / Armazém</b></td><td>10 / 35</td><td>guardam 2.000 / 20.000 itens da fazenda; máquinas ligadas puxam e guardam sozinhas</td></tr>
</table>

<h2>Irrigação e estufas</h2>
<ul class="lista">
  <li><b>Caixa d'água</b> guarda água da chuva, do balde e da <b>bomba</b>. <b>Canal</b> leva a água mais longe. <b>Aspersor</b> molha a terra num raio de 3. <b>Filtro</b> deixa a água limpa (mais qualidade).</li>
  <li><b>Estufa</b> (Agricultor 23): controlador no meio de uma área 9x9 com teto de vidro. Dentro não tem clima, a luz conta como boa e aparece menos praga. Baunilha e cacau só crescem nela. A <b>estufa avançada</b> (35) é 13x13, 10% mais rápida e mantém a terra molhada.</li>
</ul>

<h2>Agricultor</h2>
<p>A profissão sobe plantando, colhendo, caprichando na qualidade, processando, adubando, tratando pragas, cumprindo contratos e descobrindo culturas. Cada nível libera algo: compostagem (3), sementes novas (5), NPK (8), máquinas (10), especiais (12), qualidade avançada (15), irrigação (18), processamento em etapas (20), estufas (23), contratos de qualidade (25), controle biológico (28), mutações (30), máquinas avançadas (35), receitas exclusivas (40), culturas raras (45) e a <b>especialização</b> no 50: <b>Cultivador</b> (produtividade), <b>Botânico</b> (qualidade e mutações) ou <b>Produtor</b> (máquinas e contratos).</p>

<h2>Contratos, mercado e eventos</h2>
<ul class="lista">
  <li><b>Tião Fazendeiro</b>: 3 contratos por dia, 2 por semana, um de qualidade e um industrial. Pagam moedas, XP e <b>selos da feira</b>.</li>
  <li><b>Feira dos selos</b> (<?= cmd('/fazenda selos') ?>): troque selos por títulos, decorações (espantalho, cesto, placa, carrinho) e o chapéu de palha.</li>
  <li><b>Mercado</b> (<?= cmd('/fazenda mercado') ?>): preços por qualidade, encomendas e caixa de entrega. <?= cmd('/fazenda encomenda <item> <qtd> <preço>') ?> reserva o dinheiro na hora; quem entregar recebe direto.</li>
  <li><b>Eventos</b>: Festival da Colheita (XP e douradas em dobro), Competição de qualidade, Exposição de mutações, Feira comunitária (vendas +25% e selos em dobro) e Corrida de entrega (meta da comunidade).</li>
  <li><b>Livro de Sementes</b> (<?= cmd('/fazenda livro') ?>): coleção de culturas e mutações, recordes e 18 conquistas.</li>
</ul>
