<?php

const API_URL = 'http://165.22.13.172:8000';

$key = "q";
$inputJSON = file_get_contents('php://input');
$input = json_decode($inputJSON); //convert JSON into array
$url = $input->$key;

$ch = curl_init(API_URL . $url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
curl_setopt($ch, CURLOPT_HTTPHEADER, array(
    'Content-Type: application/json',
    'Cache-Control: no-cache'
));



$params =  json_encode([
    "route" => $_REQUEST['routes'],
    "user_id" => $_REQUEST['user_id'],
    "app_type" => $_REQUEST['app_type'],
    "tariff" => $_REQUEST['tariff'],
    "comment" => $_REQUEST['comment']
]);
curl_setopt($ch, CURLOPT_POSTFIELDS,$inputJSON  );
$response = curl_exec($ch);
curl_close($ch);



echo $response ;
