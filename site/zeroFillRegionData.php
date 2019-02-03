<?php
  $regionPointsNames = $_POST["regionNames"];
  $regionPointsPoints = $_POST["regionPoints"];
  $temp = array_merge($regionPointsNames, $regionPointsPoints);
  $regionPointsJSON = array_combine($regionPointsNames, $regionPointsPoints);
  file_put_contents('region_data.json', json_encode($regionPointsJSON));
?>
