<?php
  session_start();

  if (empty($_SESSION["user"])) {
    header("Location: index.php");
    die();
  }

  if (empty($_COOKIE["admin_role"]) || ($_COOKIE["admin_role"] == "false")) {
    echo file_get_contents("moement.jpg");
  }
  else {
    echo file_get_contents("1c8d7c66-4a8d-465e-9c1a-718d3c9312cd.mp4");
  }
?>