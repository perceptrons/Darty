<?php
  if (file_exists("region_data.json")) {
    return;
  } else {
    $file = fopen("region_data.json", "w");
    fclose($file);
  }
?>
