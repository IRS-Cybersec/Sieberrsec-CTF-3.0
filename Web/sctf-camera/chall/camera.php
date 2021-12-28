<?php
  session_start();

  if (empty($_SESSION["user"])) {
    header("Location: index.php");
    die();
  }

  echo "IRS{w4y_t00_eZ_1nJ3c710n}";
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FUTURE TECHNOLOGIES CAMERA</title>

    <link rel="stylesheet" href="all.css">
  </head>

  <body>
    <div id="login-form">
      <h1>未来科技人工智能录像机</h1>
      <h3>
        FUTURE TECHNOLOGIES AI IOT FOURTH INDUSTRIAL REVOLUTION
        <br>SECURITY CAMERA
      </h3>

      <?php
        $user = $_SESSION["user"];
        echo "User is $user; role is admin: " . $_COOKIE["admin_role"];

        if (!empty($_GET["pan"]) && $_COOKIE["admin_role"] !== "true") {
          echo "<br>ONLY ADMIN MAY PAN THE CAMERA";
        }
        else {
          if (empty($_GET["pan"])) {}
          else if ($_GET["pan"] == "right") {
            echo "<br>CAMERA IS AT MAXIMUM RIGHT POSITION.<br>The camera is unable to pan to the right any further.<br>";
          }
          else if ($_GET["pan"] == "left") {
            echo "<br>The camera has been panned to the left. Press update video feed.<br>";
          }
        }
      ?>

      <div style="height: 24px;">
      </div>

      <style>
        video, img {
          width: 500px;
        }
      </style>

      <?php
        if ($_COOKIE["admin_role"] == "true") echo '<video src="videofeed.php">your browser does not support video :( try using Firefox</video>';
        else echo '<img src="videofeed.php" />';
      ?>

      <br><button onclick="play();">Update Video Feed</button>
      <button onclick="panleft();">Pan Camera to Left</button>
      <button onclick="panright();">Pan Camera to Right</button>

      <br><br>After camera is PANNED to see more,<br>you must press "update video feed" for see new video update.
    </div>

    <script>
      function play() {
        try {
          document.querySelector("video").play();
        }
        catch (e) {
          alert("No video feed updates. Try panning camera.");
        }
      }

      function panleft() {
        try {
          location.href = "camera.php?pan=left";
        }
        catch (e) {
        }
      }

      function panright() {
        try {
          location.href = "camera.php?pan=right";
        }
        catch (e) {
        }
      }
    </script>
  </body>
</html>
