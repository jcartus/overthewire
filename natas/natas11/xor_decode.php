<?php

function xor_encrypt($in, $key) {
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
};

//--- get secret ---
$default_data = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");
$encoded_data = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw%3D";

$secret = xor_encrypt(base64_decode($encoded_data), json_encode($default_data));

print $secret;
//---

print "---";

$secret = "qw8J";

//--- encrpypt mal data ---
$newdata = array( "showpassword"=>"yes", "bgcolor"=>"#ffffff");

print base64_encode(xor_encrypt(json_encode($newdata), $secret));

?>
