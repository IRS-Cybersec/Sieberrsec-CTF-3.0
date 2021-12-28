<?php
  session_start();

  if (
    empty($_SERVER['HTTP_USER_AGENT']) ||
    (
      strpos($_SERVER['HTTP_USER_AGENT'], "Chrome") === false &&
      strpos($_SERVER['HTTP_USER_AGENT'], "Firefox") === false &&
      strpos($_SERVER['HTTP_USER_AGENT'], "Safari") === false
    )
  ) {
    die("Company intranet only supports allowed client configurations. Please use company-issued OS.");
  }

  try {
    if (empty($_POST["token"])) {
      if (empty($_SESSION["email"]) || !($_SESSION["email"] === "taiyang.it.solution@gmail.com")) {
        echo "You are not a verified TaiYang IT Solution employee or partner. Please log out and login again with the correct account!";
        $_SESSION["email"] = "";
      }
      else {
        echo "Welcome to IT Solution portal! Here is a flag: IRS{FLAG_REDACTED}";
      }
    }
    else {
      // verify JWT.
      $data1 = explode(".", $_POST["token"]);
      $data2 = base64_decode($data1[1]);
      $data3 = json_decode($data2, true);
      $_SESSION["email"] = $data3["email"];
      die("ok");
    }
  }
  catch (Exception $e) {
    die("Oh no! Error.");
  }

  // https://firebase.google.com/docs/auth/admin/verify-id-tokens
?>

<a href="javascript:signOut();">Sign Out</a>

<script src="https://www.gstatic.com/firebasejs/8.6.7/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/8.6.7/firebase-auth.js"></script>

<script>
  const firebaseConfig = {}; // replace with your own Firebase config

  // Initialize Firebase
  const app = firebase.initializeApp(firebaseConfig);

  var provider = new firebase.auth.GoogleAuthProvider();

  function signOut() {
    firebase.auth().signOut().then(() => {
      location.href = "login.html";
    }).catch((error) => {
      // An error happened.
    });
  }
</script>
