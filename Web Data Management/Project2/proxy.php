<?php
  // put your TMDb API key here:
  $api_key = "a72a43294b54711320e4c25ffce46245";

  header("Content-type: application/json\n\n");
  $method = $_GET['method'];
  $params = $_SERVER['QUERY_STRING'];
  $pos = strpos($params,'&');
  if ($pos === false) {
    $host = "http://api.themoviedb.org$method?api_key=$api_key";
  } else {
    $params = substr($params,$pos);
    $host = "http://api.themoviedb.org$method?api_key=$api_key$params";
  };
  $ch = curl_init($host);
  curl_exec($ch);
  curl_close($ch);
?>
