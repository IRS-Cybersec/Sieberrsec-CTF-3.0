<?php
  session_start();

  if (empty($_POST["user"]) || empty($_POST["pass"])) {
    echo "enter both user and password";
  }
  else {
    try {
      $pdo = new PDO("sqlite:96e56503-81fb-4a3c-8766-7286aa33b1cb.db");
    } catch (PDOException $e) {
      // handle the exception here
    }

    $user = $_POST["user"];
    $pass = $_POST["pass"];
    $query = $pdo -> prepare("SELECT * FROM users WHERE user = '$user' AND pass = '$pass'");
    $query -> execute();
    $result = $query -> fetchAll();

    if (count($result) != 1) {
      die("WRONG USERNAME OR PASSWORD");
    }
    else {
      $_SESSION["user"] = $result[0]["user"];
      setcookie("admin_role", "false");
      header("Location: camera.php");
      die();
    }
  }
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
    <form id="login-form" method="post">
      <h1>未来科技人工智能录像机</h1>
      <h3>
        FUTURE TECHNOLOGIES AI IOT FOURTH INDUSTRIAL REVOLUTION
        <br>SECURITY CAMERA
      </h3>

      <div style="height: 24px;">
      </div>

      <input type="text" name="user" placeholder="Username" />
      <br><input type="password" name="pass" placeholder="Password" />

      <br><input type="submit" value="ENTRY THE FUTURE CAMERA LOGIN" />

      <br>TECHNOLOGY
      <br>PLEASE FIRMWARE UPDATE YOUR CAMERA!!!
      <br>ADDRESS SECURITY VULNERABILITY OF daTABASE
    </form>
  </body>
</html>