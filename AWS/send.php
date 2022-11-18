<?php

const API_URL = 'https://suggest-maps.yandex.ru/suggest-geo?apikey=a4018892-4411-4709-97ea-6881ac674715&v=7&search_type=all&lang=ru_RU&n=50&bbox=72.958828,49.730972~73.267132,49.989920&part=';

$ch = curl_init(API_URL . urlencode($_REQUEST['q']));
curl_setopt($ch,CURLOPT_RETURNTRANSFER,1);
curl_setopt($ch,CURLOPT_FOLLOWLOCATION,1);
$response = curl_exec($ch);
curl_close($ch);

$response = str_replace('suggest.apply(', '', $response);
$response = substr($response,0,-1);

echo $response;
