<?php
  $scoreMonitoring = $_POST['scoreMonitoring'];
  file_put_contents("score_monitoring.txt", $scoreMonitoring); 
?>
