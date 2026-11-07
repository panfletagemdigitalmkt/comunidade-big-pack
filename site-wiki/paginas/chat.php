<?php $DESC = 'Chat local, global e do clan, emojis e nick colorido.'; ?>
<h1><?= grad('Chat, emojis e nick', '#a5f3fc,#38bdf8,#a855f7') ?></h1>
<p class="intro">Toda mensagem aparece com a <b>cabeça da sua skin</b>, a tag do seu cargo e a do seu clan. Passe o mouse no nome de alguém para mandar uma mensagem privada.</p>

<h2>Canais</h2>
<table class="tabela">
  <tr><th>Canal</th><th>Como usar</th><th>Quem lê</th></tr>
  <tr><td><b style="color:#a3e635">[L] Local</b></td><td>É o padrão. <?= cmd('/l <mensagem>') ?> ou só <?= cmd('/l') ?> para voltar a ele.</td><td>Quem está a até 120 blocos de você.</td></tr>
  <tr><td><b style="color:#fbbf24">[G] Global</b></td><td><?= cmd('/g <mensagem>') ?>, ou comece a mensagem com <code>!</code>. <?= cmd('/g') ?> sozinho deixa o global fixo.</td><td>Todo o servidor.</td></tr>
  <tr><td><b style="color:#c084fc">Clan</b></td><td><?= cmd('/c <mensagem>') ?> (o mesmo que <?= cmd('/cc') ?>).</td><td>Só o seu clan. <?= cmd('/ca') ?> fala também com os aliados.</td></tr>
</table>

<h2>Emojis</h2>
<p>São <b>41 emojis em pixel art</b> feitos para o servidor. Use <?= cmd('/emojis') ?> para ver todos e clique num deles para colocar na mensagem. No chat, escreva o nome entre dois-pontos, como <code>:coracao:</code>, ou use atalhos como <code>:)</code> e <code>&lt;3</code>. A tecla Tab completa os nomes.</p>
<p><img class="print" src="<?= e(asset('img/emojis.png')) ?>" alt="Os 41 emojis do servidor" loading="lazy" style="max-width:100%;border-radius:12px"></p>

<h2>Nick colorido (VIP)</h2>
<p>VIPs podem pintar o próprio nick, letra por letra, do mesmo jeito que a tag do clan: <?= cmd('/nick <código>') ?> com <code>&amp;#RRGGBB</code> antes de cada letra. As letras precisam formar o seu nick de verdade, e o nick colorido aparece no chat e no TAB.</p>
<p class="exemplo-tag"><?= cmd('/nick &#FF5500B&#FFAA00l&#FFFF00o&#88FF00c&#00FFAAa&#00AAFFo') ?> → <b style="color:#FF5500">B</b><b style="color:#FFAA00">l</b><b style="color:#FFFF00">o</b><b style="color:#88FF00">c</b><b style="color:#00FFAA">a</b><b style="color:#00AAFF">o</b></p>
<p><?= cmd('/nick reset') ?> volta ao nick normal.</p>
