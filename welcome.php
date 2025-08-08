<?php
session_start();
if (!isset($_SESSION['user_name'])) {
  header("Location: login.php");
  exit();
}
?>

<h2>Welcome, <?php echo $_SESSION['user_name']; ?>!</h2>
<p>You are now logged in.</p>
<a href="logout.php">Logout</a>
