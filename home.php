
<?php
session_start();
if (!isset($_SESSION['user_name'])) {
  header("Location: login.html");
  exit();
}
?>



<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Home | Stress Detection App</title>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', sans-serif;
    }

    body {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background:
        linear-gradient(rgba(255, 255, 255, 0.12), rgba(255, 255, 255, 0.12)),
        url("static/bg.png") no-repeat center center/cover;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
    }

    nav {
      width: 100%;
      background: rgba(255, 255, 255, 0.3);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 16px 40px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      position: sticky;
      top: 0;
      z-index: 10;
    }

    .logo {
      font-size: 26px;
      font-weight: bold;
      color: #2343e1;
    }

    .nav-links {
      display: flex;
      gap: 22px;
    }

    .nav-links a {
      text-decoration: none;
      font-size: 15px;
      color: #111;
      font-weight: 500;
      padding: 8px 14px;
      border-radius: 8px;
      transition: all 0.3s ease;
    }

    .nav-links a:hover {
      background-color: #2343e1;
      color: white;
      box-shadow: 0 4px 12px rgba(35, 67, 225, 0.4);
    }

    .hero {
      flex-grow: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 80px 20px 40px;
    }

    .hero-box {
      background: rgba(255, 255, 255, 0.28);
      backdrop-filter: blur(18px);
      border-radius: 20px;
      padding: 40px 30px;
      text-align: center;
      box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
      max-width: 600px;
      animation: fadeUp 1s ease-in-out;
    }

    .hero-box h1 {
      font-size: 34px;
      color: #2343e1;
      margin-bottom: 20px;
    }

    .hero-box p {
      font-size: 16px;
      color: #333;
      line-height: 1.6;
      margin-bottom: 30px;
    }

    .cta a {
      display: inline-block;
      background-color: #2343e1;
      color: white;
      padding: 12px 24px;
      font-size: 16px;
      border: none;
      border-radius: 12px;
      text-decoration: none;
      box-shadow: 0 4px 16px rgba(35, 67, 225, 0.3);
      transition: all 0.3s ease;
    }

    .cta a:hover {
      background-color: #102dc4;
      transform: scale(1.05);
    }

    @keyframes fadeUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @media (max-width: 768px) {
      nav {
        flex-direction: column;
        align-items: flex-start;
      }

      .nav-links {
        flex-direction: column;
        width: 100%;
        margin-top: 10px;
      }

      .nav-links a {
        width: 100%;
      }

      .hero-box h1 {
        font-size: 26px;
      }
    }
  </style>
</head>
<body>

  <!-- Navbar -->
  <nav>
    <div class="logo">StressSense</div>
    <div class="nav-links">
      <a href="home.php">Home</a>
      <a href="http://localhost:5000">Webcam Detection</a>

      <a href="http://127.0.0.1:5001">Voice Analysis</a>
        <a href="logout.php">Logout</a>
    </div>
  </nav>

  <!-- Hero Section -->
  <div class="hero">
    <div class="hero-box">
      <h1>Welcome, <?php echo $_SESSION['user_name']; ?>!</h1>

      <p>AI-driven emotion detection using webcam and voice input, built with a focus on wellness and peace of mind. Start analyzing your stress levels with cutting-edge technology.</p>

      <div class="cta">
        <a href="http://localhost:5000">Start Webcam Detection</a>
      </div>
    </div>
  </div>

</body>
</html>
