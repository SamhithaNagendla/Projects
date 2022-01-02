<?php
  // put your Yelp API key here:
  $API_KEY = 'tYn2HZ90N6Q4Gd7lQtshRGJE29z3i8zEajzr8ue_SopCdIXNLKMO46kTYu9trM-M-4VUIUIGe5DeqQy2gJQVY1RRF3W_dCC-kp4P1-4CRtF9EX2nif8hIwMJnLR_X3Yx';

  $API_HOST = "https://api.yelp.com";
  $SEARCH_PATH = "/v3/businesses/search";
  $BUSINESS_PATH = "/v3/businesses/";
  $curl = curl_init();
  if (FALSE === $curl)
     throw new Exception('Failed to initialize');
  $url = $API_HOST . $SEARCH_PATH . "?" . $_SERVER['QUERY_STRING'];
  curl_setopt_array($curl, array(
            CURLOPT_URL => $url,
            CURLOPT_RETURNTRANSFER => true,  // Capture response.
            CURLOPT_ENCODING => "",  // Accept gzip/deflate/whatever.
            CURLOPT_MAXREDIRS => 10,
            CURLOPT_TIMEOUT => 30,
            CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
            CURLOPT_CUSTOMREQUEST => "GET",
            CURLOPT_HTTPHEADER => array(
                "authorization: Bearer " . $GLOBALS['API_KEY'],
                "cache-control: no-cache",
            ),
        ));
  $response = curl_exec($curl);
  curl_close($curl);
  print $response;
?>
