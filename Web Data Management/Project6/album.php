<!--
Student Name: Samhitha Nagendla (sxn7208)
File Name: album.php
Description: "Using Cloud Storage" assignment.
Reference : Referred the Sample.php file provided in the Zip file.
-->
<html>
<head>
<title>Cloud Storage</title>
</head>
<body>
<h2>Image Upload Form</h2>
<div id= "Upload">
<form action="album.php" method="post" enctype="multipart/form-data">
  Select image to upload:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <input type="file" name="updfile" id="updfile"><br/><br/>
  <input type="submit" value="Upload Image" name="submit">
</form>
</form>
</div>


<?php

// display all errors on the browser
error_reporting(E_ALL);
ini_set('display_errors','On');
$imgName=NULL;

//Image upload to local folder.
if(isset($_POST["submit"])) 
	{
		$target_dir = "C:/xampp/htdocs/project6/";
		$target_file = $target_dir . basename($_FILES["updfile"]["name"]);
		move_uploaded_file($_FILES["updfile"]["tmp_name"], $target_file);
		$imgName = $_FILES["updfile"]["name"];
	}



require_once 'demo-lib.php';
demo_init(); // this just enables nicer output
require_once 'DropboxClient.php';
$dropbox = new DropboxClient( array(
	'app_key' => "",	
	'app_secret' => "",
	'app_full_access' => false,
) );
//Dropbox will redirect the user here
$return_url = "https://" . $_SERVER['HTTP_HOST'] . $_SERVER['SCRIPT_NAME'] . "?auth_redirect=1";
// first, try to load existing access token
$bearer_token = demo_token_load( "bearer" );
if ( $bearer_token ) {
	$dropbox->SetBearerToken( $bearer_token );
} elseif ( ! empty( $_GET['auth_redirect'] ) ) // are we coming from dropbox's auth page?
{
	// get & store bearer token
	$bearer_token = $dropbox->GetBearerToken( null, $return_url );
	demo_store_token( $bearer_token, "bearer" );
} elseif ( ! $dropbox->IsAuthorized() ) {
	// redirect user to Dropbox auth page
	$auth_url = $dropbox->BuildAuthorizeUrl( $return_url );
	die( "Authentication required. <a href='$auth_url'>Continue.</a>" );
}



//To Delete Image from Dropbox
if(isset($_GET['remove']))
{
	$removeImg = $_GET['remove'];
	echo "Removed ".$removeImg. " successfully!!";
	$dropbox->Delete($removeImg);	
}

//Image Upload to Dropbox
 if(!is_null($imgName))
 {
	if( $imgName != NULL)
	{
		$dropbox->UploadFile($imgName);
		echo $imgName." is uploaded successfully!";
		$imgName=NULL;
	}
 }

$files = $dropbox->GetFiles( "", false );
if(!empty($files))
{
 //To display the contents of Dropbox
echo "<div id = \"dropboxContents\">" ;
echo "</br>";
echo "<h2>Files Available</h2></br>";
foreach( $files as $file)
{
	echo "<ul><li><a href='album.php?imgFile=".$file->path."'>".basename($file->path)."</a></li></ul>";
}

//To Preview the image and display
if(isset($_GET['imgFile']))
{
	
	$indexVal=$_GET['imgFile'];
	$a = $dropbox->GetMetadata( $indexVal );
		
	/*
	//Code to show the preview of Image from Dropbox
	echo "<br/><h2>Image Preview of ". basename($a->path).":</h2>";
	$img_data = base64_encode( $dropbox->GetThumbnail( $a->path ) );
	echo "<img src=\"data:image/jpeg;base64,$img_data\" alt=\"Generating PDF thumbnail failed!\" style=\"border: 1px solid black;\" /><br/><br/>";
	*/
		
	//Code to downlod and Preview the image
	echo "<br/><h2>Image Preview of ". basename($a->path).":</h2>";
	$test_file = "download_" . basename( $a->path );
	$dropbox->DownloadFile( $a, $test_file );
	echo "<img src =\"http://localhost/project6/".$test_file."\" width=100px height=100px/>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
	
	echo "<a href='album.php?remove=".$a->path."'><button>Delete</button></a>";
	echo "<br/>".basename($a->path);
}
}
else
{
	echo "<h2>No files are available!! Dropbox Content is empty.</h2></br>";
}

?>

</body>
</html>
