<?php
session_start();
include 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $email = $_POST['email'];
  $password = $_POST['password'];

  $query = "SELECT * FROM users WHERE email = '$email'";
  $result = mysqli_query($conn, $query);

  if (mysqli_num_rows($result) == 1) {
    $user = mysqli_fetch_assoc($result);

    if (password_verify($password, $user['password'])) {
      $_SESSION['user_name'] = $user['name'];
      $_SESSION['user_id'] = $user['id'];
      
      // ✅ Redirect to Home Page (fix this!)
      header("Location: home.php");
      exit();
    } else {
      echo "<script>alert('Invalid password'); window.location.href='login.html';</script>";
    }
  } else {
    echo "<script>alert('User not found'); window.location.href='login.html';</script>";
  }
}
?>
