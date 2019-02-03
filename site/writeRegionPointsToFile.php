<?php
  $regionPointsName = $_POST["regionName"];
  $regionPointsPoints = $_POST["regionPoints"];
  $input = file_get_contents("region_data.json");
  $temp = json_decode($input);
  $temp->$regionPointsName = $regionPointsPoints;
  $regionPointsJSON = json_encode($temp);
  file_put_contents('region_data.json', $regionPointsJSON);
?>
