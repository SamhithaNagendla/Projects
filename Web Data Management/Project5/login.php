<!--
Student Name: Samhitha Nagendla (sxn7208)
File Name: login.php
Description: login part of "A Social Network using PHP and MySQL" assignment.
-->
<?php
session_start();
?>
<!DOCTYPE html>
<html lang="en">
	<head>
		<title>Login Page</title>
		<meta charset="utf-8"/>
	</head>
	<body>
		<div id="login">
			<form  action="network.php" method="post">
				<label for="username" >UserName:</label><br/>
				<input type="text" id="username" name="username" /><br/>
				<label for="password" >Password:</label><br/>
				<input type="password" id="password" name="password" /><br/><br/>
				<input type="submit" value="Login" >
			</form>
			<br/><br/>
		</div>
	</body>
</html>
<?php
//To clear all session varaibles and destroy the session on logout.
if($_SERVER['QUERY_STRING'] == "logout" )
{
	session_unset();
	session_destroy();
	header("Location:http://localhost/project5/login.php");
}
?>