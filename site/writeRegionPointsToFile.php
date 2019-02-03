<?php
  $regionPoints = new \stdClass();
  $regionPoints->name = $_POST["regionName"];
  $regionPoints->value = $_POST["regionPoints"];
  // $regionPointsJSON = json_encode($regionPoints);
  // $file = fopen("region_data.txt", "a+");
  $input = file_get_contents("region_data.json");
  $temp = json_decode($input);
  array_push($temp, $regionPoints);
  $regionPointsJSON = json_encode($temp);
  file_put_contents('region_data.json', $regionPointsJSON);
  // fwrite($file, $regionPointsJSON);
  fclose($file);
?>
