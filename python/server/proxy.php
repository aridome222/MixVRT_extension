<?php
// proxy.php

// ターゲットURLを取得
$url = isset($_GET['url']) ? $_GET['url'] : '';

// ターゲットURLが指定されていない場合はエラーを返す
if (!$url) {
    http_response_code(400);
    die('Target URL is missing.');
}

// ターゲットURLからデータを取得
$data = file_get_contents($url);

// ターゲットURLからのデータが取得できなかった場合はエラーを返す
if ($data === false) {
    http_response_code(500);
    die('Failed to fetch data from the target URL.');
}

// ターゲットURLからのデータをクライアントに返す
header('Content-Type: text/html');
echo $data;
?>
