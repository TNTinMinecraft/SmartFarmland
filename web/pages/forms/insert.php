<?php
$servername = "localhost";
$username = "smartfarmland";
$password = "smartfarmland";
$dbname = "smartfarmland";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $condition = $_POST["condition"];
  $compareValue = 0;

  switch($condition) {
    case "大于":
      $compareValue = 2;
      break;
    case "等于":
      $compareValue = 1;
      break;
    case "小于":
      $compareValue = 0;
      break;
    default:
      echo "无效的输入";
      return;
  }
  
  $sql = "INSERT INTO zidonghua (compare) VALUES ($compareValue)";

  if ($conn->query($sql) === TRUE) {
    echo "记录插入成功";
  } else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }
}

$conn->close();
?>