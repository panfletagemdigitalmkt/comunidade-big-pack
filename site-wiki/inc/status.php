<?php
/** Consulta o servidor pelo protocolo de status do Minecraft (o mesmo da lista de servidores). */
function mc_varint($i) {
    $out = '';
    $i &= 0xFFFFFFFF;
    do { $b = $i & 0x7F; $i >>= 7; if ($i) $b |= 0x80; $out .= chr($b); } while ($i);
    return $out;
}

function mc_ler_varint($s) {
    $n = 0; $shift = 0;
    for ($k = 0; $k < 5; $k++) {
        $c = fgetc($s);
        if ($c === false) return false;
        $b = ord($c);
        $n |= ($b & 0x7F) << $shift;
        if (!($b & 0x80)) return $n;
        $shift += 7;
    }
    return false;
}

function mc_status() {
    $cache = __DIR__ . '/../cache/status.json';
    if (is_file($cache) && time() - filemtime($cache) < STATUS_CACHE_SEGUNDOS) {
        $d = json_decode(@file_get_contents($cache), true);
        if (is_array($d)) return $d;
    }
    $res = ['online' => false, 'jogadores' => 0, 'max' => 0, 'versao' => '', 'nomes' => []];
    $s = @fsockopen(SERVIDOR_HOST, SERVIDOR_PORTA, $errno, $errstr, 2.0);
    if ($s) {
        stream_set_timeout($s, 2);
        $host = SERVIDOR_HOST;
        $hs = mc_varint(0) . mc_varint(767) . mc_varint(strlen($host)) . $host . pack('n', SERVIDOR_PORTA) . mc_varint(1);
        fwrite($s, mc_varint(strlen($hs)) . $hs);
        fwrite($s, mc_varint(1) . mc_varint(0));
        $tam = mc_ler_varint($s);
        $id = mc_ler_varint($s);
        $len = mc_ler_varint($s);
        if ($tam !== false && $id === 0 && $len) {
            $json = '';
            while (strlen($json) < $len && !feof($s)) {
                $parte = fread($s, $len - strlen($json));
                if ($parte === false || $parte === '') break;
                $json .= $parte;
            }
            $d = json_decode($json, true);
            if (is_array($d)) {
                $res['online'] = true;
                $res['jogadores'] = (int)($d['players']['online'] ?? 0);
                $res['max'] = (int)($d['players']['max'] ?? 0);
                $res['versao'] = (string)($d['version']['name'] ?? '');
                foreach (($d['players']['sample'] ?? []) as $pl) $res['nomes'][] = (string)($pl['name'] ?? '');
            }
        }
        fclose($s);
    }
    // Muitas hospedagens (ex.: HostGator) bloqueiam conexões para portas fora do comum.
    // Se a consulta direta falhar, pergunta para a API pública mcsrvstat.us (HTTPS, porta 443).
    if (!$res['online']) $res = mc_status_api($res);
    @file_put_contents($cache, json_encode($res));
    return $res;
}

function mc_status_api(array $res) {
    $url = 'https://api.mcsrvstat.us/3/' . rawurlencode(SERVIDOR_HOST . ':' . SERVIDOR_PORTA);
    $corpo = false;
    if (function_exists('curl_init')) {
        $c = curl_init($url);
        curl_setopt_array($c, [CURLOPT_RETURNTRANSFER => true, CURLOPT_TIMEOUT => 5, CURLOPT_CONNECTTIMEOUT => 3,
            CURLOPT_USERAGENT => 'ComunidadeBIG-Site/1.0', CURLOPT_FOLLOWLOCATION => true]);
        $corpo = curl_exec($c);
        curl_close($c);
    } elseif (ini_get('allow_url_fopen')) {
        $ctx = stream_context_create(['http' => ['timeout' => 5, 'header' => "User-Agent: ComunidadeBIG-Site/1.0\r\n"]]);
        $corpo = @file_get_contents($url, false, $ctx);
    }
    $d = $corpo ? json_decode($corpo, true) : null;
    if (is_array($d) && !empty($d['online'])) {
        $res['online'] = true;
        $res['jogadores'] = (int)($d['players']['online'] ?? 0);
        $res['max'] = (int)($d['players']['max'] ?? 0);
        $res['versao'] = (string)($d['version'] ?? '');
        $res['nomes'] = [];
        foreach (($d['players']['list'] ?? []) as $pl) $res['nomes'][] = (string)(is_array($pl) ? ($pl['name'] ?? '') : $pl);
    }
    return $res;
}
