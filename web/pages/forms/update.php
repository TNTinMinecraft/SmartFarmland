<?php
$servername = "localhost";
$username = "smartfarmland";
$password = "smartfarmland";
$dbname = "smartfarmland";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if (isset($_POST['in_id'])) {
    $in_id = $_POST['in_id'];
    $sql = "UPDATE zidonghua SET in_id=$in_id WHERE condition";

    if ($conn->query($sql) === TRUE) {
        echo "替换成功";
    } else {
        echo "Error updating record: " . $conn->error;
    }
}
$conn->close();
?>