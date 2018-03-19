<?php
$servername = "localhost";
$username = "justlik6_travel";
$password = " ";
$dbname = "justlik6_trippie";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);
// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} 

$sql = "INSERT INTO data (lat, lng, temp) VALUES ('".$_POST['lat']."', '".$_POST['lon']."', '".$_POST['temp']."')";
echo $sql;

if ($conn->query($sql) === TRUE) {
    echo "New record created successfully";
} else {
    echo "Error: " . $sql . "<br>" . $conn->error;
}

$conn->close();
?>
