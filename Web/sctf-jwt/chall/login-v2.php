<?php
  session_start();

  try {
    if (empty($_POST["token"])) {
      if (empty($_SESSION["email2"]) || !($_SESSION["email2"] === "taiyang.it.solution@gmail.com")) {
        echo "You are not a verified TaiYang IT Solution employee or partner. Please log out and login again with the correct account!";
        $_SESSION["email2"] = "";
      }
      else {
        echo "Welcome to IT Solution portal v2! Here is a flag: IRS{FLAG_REDACTED}";
      }
    }
    else {
      require("jwt.php");
      $google_keys = json_decode(file_get_contents("https://www.googleapis.com/robot/v1/metadata/x509/securetoken@system.gserviceaccount.com"), true);

      // verify JWT.
      $token = $_POST["token"];

      $which_key = json_decode(base64_decode(explode(".", $token)[0]), true)["kid"];
      
      try {
        $decoded = JWT::decode($token, $google_keys[$which_key], array("RS256"));
      }
      catch (Exception $e) {
        try {
          $google_keys = json_decode(file_get_contents("https://www.googleapis.com/oauth2/v1/certs"), true);
          $decoded = JWT::decode($token, $google_keys[$which_key], array("RS256"));
        }
        catch (Exception $e2) {
          die("ERROR 69: TOKEN INTEGRITY VIOLATED. YOU HAVE VIOLATED TAIYANG IT SOLUTION CORE VALUE... TOKEN ARE NOT ALLOW. ERROR.");
        }
      }

      $decoded_array = (array) $decoded;
      // if ($decoded_array["aud"] !== "") echo "AUDIENCE CHECK BYPASS?";

      $email = $decoded_array["email"];

      $_SESSION["email2"] = $decoded_array["email"];
    }
  }
  catch (Exception $e) {
    die("Oh no! Error.");
  }
?>
