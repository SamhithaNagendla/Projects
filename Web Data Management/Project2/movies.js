/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: movies.js
Description: Java Script for A Movie Web Application
*/

//To display all the matching searched movie titles along with the movie release year as clickable items.
function sendRequest () 
{
    var xhr = new XMLHttpRequest();
    var query = encodeURI(document.getElementById("form-input").value);
	document.getElementById("moviePoster").innerHTML = "&nbsp";
	document.getElementById("movieTitle").innerHTML = "&nbsp";
	document.getElementById("movieGenres").innerHTML = "&nbsp";
	document.getElementById("movieSummary").innerHTML = "&nbsp";
	document.getElementById("movieCast").innerHTML = "&nbsp";
    xhr.open("GET", "proxy.php?method=/3/search/movie&query=" + query, true);	
    xhr.onreadystatechange = function () 
   {
       if (this.readyState == 4) 
	   {
           json = JSON.parse(this.responseText);
		   document.getElementById("movieNames").innerHTML = "<h2> Movie Names ( Movie Release Year ) </h2>";
		  for( var index = 0; index < json.results.length ; index ++)
		  {
			mId = json.results[index].id;
			document.getElementById("movieNames").innerHTML = document.getElementById("movieNames").innerHTML + "<ul><li><a onclick='SendDetailRequest(" + mId + " );'>" + json.results[index].title +"( "+json.results[index].release_date.substring(0,4)+" )</a></li></ul>";
		  }
	   }		  
    };
   xhr.send(null);
}

//function that fetch movie details of the clicked movie by calling SendMovieCast(mId) for cast details and SendMovieDetails(mId) for other details
function SendDetailRequest(mId) 
{
	SendMovieDetails(mId);
	SendMovieCast(mId);
}

//function that fetch Movie Poster, Movie Title, Movie Genres, Movie Summary of the clicked Movie.
function SendMovieDetails(mId)
{
	var xhr = new XMLHttpRequest();
    var query = encodeURI(document.getElementById("form-input").value);
    xhr.open("GET", "proxy.php?method=/3/movie/" + mId, true);
    xhr.onreadystatechange = function () 
    {
       if (this.readyState == 4) 
	   {
           var json = JSON.parse(this.responseText);
			document.getElementById("moviePoster").innerHTML = "<h2>"+json.original_title+"( "+json.release_date.substring(0,4)+" ) Movie Details</h2>";
		    document.getElementById("moviePoster").innerHTML = document.getElementById("moviePoster").innerHTML+ "<h3>Movie Poster</h3>"
		   var imgSrc = "http://image.tmdb.org/t/p/w185"+json.poster_path;
		   document.getElementById("moviePoster").innerHTML = document.getElementById("moviePoster").innerHTML +"<img src ="+ imgSrc +" alt='Movie Poster' width = 500 px height =500 px/>";
		   document.getElementById("movieTitle").innerHTML = "<h3>Movie Title</h3>"
		   document.getElementById("movieTitle").innerHTML = document.getElementById("movieTitle").innerHTML + json.original_title;
		   document.getElementById("movieGenres").innerHTML = "<h3>Movie Genres</h3>"
		   for( var index = 0; index < json.genres.length ; index ++)
		    {
			  document.getElementById("movieGenres").innerHTML =  document.getElementById("movieGenres").innerHTML + json.genres[index].name;
			  if(index < json.genres.length - 1)
			   {
			     document.getElementById("movieGenres").innerHTML =  document.getElementById("movieGenres").innerHTML 	+ ",";
			   }
		    }
		  document.getElementById("movieSummary").innerHTML = "<h3>Movie Overview</h3>"
		  document.getElementById("movieSummary").innerHTML = document.getElementById("movieSummary").innerHTML + json.overview;
	   }
    };
   xhr.send(null);
}

//function that fetch Movie Cast of the clicked Movie.
function SendMovieCast(mId)
{
	var xhr = new XMLHttpRequest();
    var query = encodeURI(document.getElementById("form-input").value);
    xhr.open("GET", "proxy.php?method=/3/movie/" + mId+"/credits", true);
    xhr.onreadystatechange = function () 
    {
       if (this.readyState == 4) 
	   {
           var json = JSON.parse(this.responseText); 
           document.getElementById("movieCast").innerHTML = "<h3>Movie Maximum Top 5 Cast Members: Actor Name</h3>";	   
		   for( var index = 0; index < Math.min(json.cast.length,5) ; index ++)
		    {
			    document.getElementById("movieCast").innerHTML = document.getElementById("movieCast").innerHTML + json.cast[index].name+"<br/>";
		    }
		    
	   }
    };
   xhr.send(null);
}