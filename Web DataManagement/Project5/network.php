<!--
Student Name: Samhitha Nagendla (sxn7208)
File Name: network.php
Description: Network part of "A Social Network using PHP and MySQL" assignment.
-->
<html>
<head><title>Message Board</title></head>
<body>
<?php
session_start();
//Setting the login Parameters to Session variables
if(isset($_POST["username"]) && isset($_POST["password"]))
{
$username=$_POST["username"];
$password=$_POST["password"];
$_SESSION["username"]=$username;
$_SESSION["password"]=$password ;
}
else
{
$username=$_SESSION["username"];
$password=$_SESSION["password"];
}
error_reporting(E_ALL);
ini_set('display_errors','On');
//Forces user to login to access this page.
if ( empty( $_SESSION["username"] )) 
	{
		session_regenerate_id(true );
		header("Location: login.php");
		exit (); 
	}
try 
	{
		$dbh = new PDO("mysql:host=127.0.0.1:3306;dbname=network","root","",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
		$result=$dbh->query("select * from users WHERE username='" . $_SESSION["username"] . "' AND password='" . md5($_SESSION["password"]) . "'");
		//Validates the user
		if (! $result || $result->rowCount() ==0 ) 
			{
				session_regenerate_id(true ); // to avoid session fixation attacks
				header("Location:http://localhost/project5/login.php"); // redirect
				exit ();
			} 
		else
			{
				$personLoggedIn = $result->fetch();
				//Logged-In User Details
				$currentuser = $personLoggedIn["username"];
				printf("<div><h2>".$personLoggedIn["username"]." Logged In Details:</h2>");
				printf("<ul><li>User Name: " .$personLoggedIn["username"] . "</li>");
				printf("<li>Full Nme: " .$personLoggedIn["fullname"] . "</li>");
				printf("<li>Email: " .$personLoggedIn["email"] . "</li></ul></div>");
				//Friends of Logged-In User
				printf("<div><h2>Friends</h2>");
				$friendResult=$dbh->query("select username, fullname, email from users WHERE username in (select friend from friends where user ='" . $personLoggedIn["username"] . "')");
				$param= $_SERVER['QUERY_STRING'];
				while ($friendResultDetails = $friendResult->fetch()) 
					{
						$removeuser = $friendResultDetails["username"]; 
						printf("<div><form  action=\"network.php\" method=\"post\"><label><b>".$removeuser. "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b></label><button type=\"submit\" formaction = \"network.php?remove=".$removeuser."&user=".$currentuser."&act=remove\">Remove Friend</button></form></div>");
						printf("Details:");
						printf("<ul><li>User Name:		" .$friendResultDetails["username"] . "</li>");
						printf("<li>Full Name:		" .$friendResultDetails["fullname"] . "</li>");
						printf("<li>Email: 			" .$friendResultDetails["email"] . "</li></ul>");
						printf("<br/><br/><br/>");
					} 
				printf("</div>");
				//Other Users
				printf("<div><h2>Others</h2>");
				$otherResult=$dbh->query("select username, fullname, email from users WHERE username not in (select friend from friends where user ='" . $personLoggedIn["username"] . "' union select '" . $personLoggedIn["username"] . "' from dual)");
				while ($otherResultDetails = $otherResult->fetch()) 
					{
						$adduser = $otherResultDetails["username"];
						printf("<div><form  action=\"network.php\" method=\"post\"><label><b>".$adduser. "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b></label><button type=\"submit\" formaction = \"network.php?add=".$adduser."&user=".$currentuser."&act=add\">Add Friend</button></form></div>");
						printf("Details:");
						printf("<ul><li>User Name:		"  .$otherResultDetails["username"] . "</li>");
						printf("<li>Full Name:		".$otherResultDetails["fullname"] . "</li>");
						printf("<li>Email: 			".$otherResultDetails["email"] . "</li></ul>");
						printf("<br/><br/><br/>");
					}
				printf("</div>");
				//Function to add Friend
				function addUser($user,$friend)
				{
					$dbha = new PDO("mysql:host=127.0.0.1:3306;dbname=network","root","",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
					$dbha->beginTransaction();
					$dbha->exec("insert into friends (user,friend) values('".$user."','".$friend."')")
							or die(print_r($dbha->errorInfo(), true));
					$dbha->commit();
					header("Location:http://localhost/project5/network.php");
				}
				//Function to remove Friend
				function removeUser($user,$friend)
				{
					$dbhr = new PDO("mysql:host=127.0.0.1:3306;dbname=network","root","",array(PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION));
					$dbhr->beginTransaction();
					$dbhr->exec("delete from friends where user='".$user."' and friend ='".$friend."'")
							or die(print_r($dbhr->errorInfo(), true));
					$dbhr->commit();
					header("Location:http://localhost/project5/network.php");
				}
				//Logout from current session
				printf("<div><form  action=\"login.php\" method=\"post\"><button type=\"submit\" formaction = \"login.php?logout\">Log Out</button></form></div>");
				//Assigning Session Variables to trigger addUser or removeUser functions
				if(!is_null($_SERVER['QUERY_STRING']) )
				{
				parse_str($param,$queryparam);
				if(isset($queryparam["remove"]))
				{
				$_SESSION["removeusername"]=$queryparam["remove"];
				}
				else
				{
					unset($_SESSION["removeusername"]);
				}
				if(isset($queryparam["user"]))
				{
				$_SESSION["currentusername"]=$queryparam["user"];
				}
				else
				{
					unset($_SESSION["currentusername"]);
				}
				if(isset($queryparam["act"]))
				{
				$_SESSION["actname"]=$queryparam["act"];
				}
				else
				{
					unset($_SESSION["actname"]);
				}
				if(isset($queryparam["add"]))
				{
				$_SESSION["addusername"]=$queryparam["add"];
				}
				else
				{
					unset($_SESSION["addusername"]);
				}
				if(isset($_SESSION["removeusername"]) && isset($_SESSION["currentusername"]) && isset($_SESSION["actname"]))
				{
					removeUser($_SESSION["currentusername"],$_SESSION["removeusername"]);
				}
				if(isset($_SESSION["addusername"]) && isset($_SESSION["currentusername"]) && isset($_SESSION["actname"]))
				{
					addUser($_SESSION["currentusername"],$_SESSION["addusername"]);
				}
				}
				
				
			}
	}
catch (PDOException $e) 
	{
		print "Error!: " . $e->getMessage() . "<br/>";
		die();
	}

?>
</body>
</html>
