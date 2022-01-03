<!--
Student Name: Samhitha Nagendla (sxn7208)
File Name: movies.php
Description: The Movie Web Application in PHP
-->

<!DOCTYPE html>
<!-- HTML code for search form for The Movie Web Application-->
<html lang="en">
	<head>
		<title>Display Movie Information</title>
		<meta charset="utf-8"/>
	</head>
	<body>
		<div id="display">
			<div id="search">
				<form  action="movies.php" method="get">
					<label>Movie title: <input type="text" id="form-input" name="form-input" /></label>
					<input type="submit" value="Display Info" >
				</form>
				<br/>
				<br/>
	</body>
</html>

<?php 
//To call sendRequest() for displaying search results as an itemized clickable list.
if(isset($_GET["form-input"]))
{
sendRequest( urlencode($_GET["form-input"]) );
}
//To display search results as an itemized clickable list of movie titles along with their years they were released.
function sendRequest( $query )
{
	$homepage = file_get_contents( "https://api.themoviedb.org/3/search/movie?api_key=".$query);
	$json = json_decode($homepage,true);
	$movieList = $json['results'];
	if(count($movieList) == 0)
	{
		printf("<h3>No Matching Results!!</h3>");
	}
	printf("<div id=\"movieNames\">&nbsp;");
	foreach( $movieList as $movieListItem )
		{
			$mId = $movieListItem['id'];
			echo "<ul><li><a href=\"movies.php?id=".$mId ."\">" ;
			Print("<br/>");
			if(isset($movieListItem['release_date']) )
				{ 			
					print_r($movieListItem['title']."(".substr($movieListItem['release_date'],0,4).")");
				} 
			else 
				{ 			
					print_r($movieListItem['title']."()");
				}
			echo "</a></li></ul>" ;
		}
	printf("</div>");
	
}
//To call SendDetailRequest() for displaying details of clicked Movie Item.
if(isset($_GET["id"]))
{
	SendDetailRequest($_GET["id"]);
}
//To display the poster of the movie as an image, the movie title, its genres (separated by comma), the movie overview and the names of the top five cast members.
function SendDetailRequest($mId)
{
	$moviePageLink = "https://api.themoviedb.org/3/movie/".$mId."?api_key=" ;
	$moviePageContents = file_get_contents($moviePageLink);
	$movieDetails = json_decode($moviePageContents, true);
	if(isset($movieDetails['release_date']) )
		{ 			
			printf("<h2>".$movieDetails['original_title']."( ".substr($movieDetails['release_date'],0,4)." ) Movie Details</h2>");
		} 
	else 
		{ 			
			printf("<h2>".$movieDetails['original_title']."( ) Movie Details</h2>");
		}	
	Printf("<br/><div id=\"moviePoster\"><h4>Movie Poster</h4>");
	$imgSrc = "http://image.tmdb.org/t/p/w185".$movieDetails['poster_path'];
	printf("<img src =". $imgSrc ." alt='Movie Poster is unavailable!!' width = 500 px height =500 px /></div>");
	printf("<br/><div id=\"movieTitle\"><h4>Movie Title</h4>");
	printf($movieDetails['original_title']."</div>");
	printf("<br/><div id=\"movieGenres\">"."<h4>Movie Genres</h4>");
	$counter = 0;
	if(count($movieDetails['genres']) == 0)
		{
			print("Movie Genres details are unavailable!!");
		}
	foreach($movieDetails['genres'] as $g)
		{
			print($g['name']);
			if($counter++ < count($movieDetails['genres'])-1 )
			{
				print(", ");
			}
		}
	printf("</div>");
	printf("<br/><div id=\"movieSummary\">"."<h4>Movie Overview</h4>");
	
	if(isset($movieDetails['overview']) and !($movieDetails['overview']===""))
		{
			printf($movieDetails['overview']."</div>");
		}
	else
		{
			printf("Movie Summary is unavailable!!</div>");
		}
	$creditsPageLink = "https://api.themoviedb.org/3/movie/".$mId."/credits?api_key=" ;
	$creditPageContents = file_get_contents($creditsPageLink);
	$creditDetails = json_decode($creditPageContents, true);
	Printf("<br/><div id=\"movieCast\">"."<h4>Movie Maximum Top 5 Cast Members: Actor Name</h4>");
	$counter = 0;
	if(count($creditDetails['cast']) == 0)
		{
			print("Movie Cast details are unavailable!!");
		}
	foreach($creditDetails['cast'] as $castName)
		{
			print_r("<ul><li>".$castName['name']."</li></ul>");
			$counter++;
			if($counter == 5)
				{
					break;
				}
		}
	printf("</div>");
}
?>
