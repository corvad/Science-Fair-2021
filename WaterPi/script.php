<?php
$apikey = "";
$zip = "";
$config = "config.py";

#Takes input through POST and writes the apikey and zip to a file so that weather.py can access the configuration
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    #Calls the clean() function to clean the inputed data to improve security
    $apikey = clean($_POST["apikey"]);
    $apikey = '"'.$apikey.'"';
    $zip = clean($_POST["zip"]);
    $zip = '"'.$zip.'"';

    #Writes the apikey and zip to configuration file
    if(is_writable($config)){
        $config = fopen("config.py","w");
        fwrite($config,"apikey = " .  $apikey . "\n");
        fwrite($config,"zip = " . $zip . "\n");
        fclose($config);
        echo "Configuration Updated, You can exit out now.";
    }
}

#Cleans the data
function clean($dirty) {
    $clean = trim($dirty);
    $clean = stripslashes($clean);
    $clean = htmlspecialchars($clean);
    return $clean;
}
?>