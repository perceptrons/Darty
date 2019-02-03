<?php
  // if (!file_exists("region_data.json")) {
  //   $file = fopen("region_data.json", "w");
  //   fclose($file);
  // }
  $regionPointsNames = $_POST["regionNames"];
  $regionPointsPoints = $_POST["regionPoints"];
  $temp = array_merge($regionPointsNames, $regionPointsPoints);
//   function toArr(){
//     return func_get_args();
// }
//
// $a = array ('a','b','c','d','e');
// $b = array(1,2,3,4,5);
// $c = json_encode(array_map ('toArr',$a,$b));
  $regionPointsJSON = array_combine($regionPointsNames, $regionPointsPoints);
  file_put_contents('region_data.json', json_encode($regionPointsJSON));
  // // $temp = new \stdClass();
  // // $temp = {};
  // for ($i = 0; $i < count($regionPointsNames); $i++) {
  //   $temp->$regionPointsNames[$i] = $regionPointsPoints[$i];
  // }
  // // $temp->$regionPointsName = $regionPointsPoints;
  // $regionPointsJSON = json_encode($temp);
  // file_put_contents('region_data.json', $regionPointsJSON);
?>
