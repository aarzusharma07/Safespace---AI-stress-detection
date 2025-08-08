<?php
include 'config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST['name'];
  $email = $_POST['email'];
  $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

  // Check if email already exists
  $check = mysqli_query($conn, "SELECT * FROM users WHERE email='$email'");
  if (mysqli_num_rows($check) > 0) {
    echo "<script>alert('Email already registered!'); window.location.href='register.html';</script>";
  } else {
    $sql = "INSERT INTO users (name, email, password) VALUES ('$name', '$email', '$password')";
    if (mysqli_query($conn, $sql)) {
      echo "<script>alert('Registered Successfully! Please login.'); window.location.href='login.html';</script>";
    } else {
      echo "Error: " . mysqli_error($conn);
    }
  }
}
?>
