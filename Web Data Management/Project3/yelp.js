/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: yelp.js
Description: Java Script for a Web Mashup: Display Best Restaurants on a Map
*/


//Index of search results that are within range 
var a = 0  ;
//Initial property values of map
var centerLat = 32.75 ;
var centerLong = -97.13 ;
var zoom = 16; 
//To access method outside the initMap() function
var z;
var z1;
var z2;
//Marker Properties
var label1 = 0;
var latValue = 32.75;
var lngValue = -97.13; 
var titleName ;
var location1;
//Markers Arrays and to store marker properties
var markers = [];
var marIndex = 0 ;
var marValIndex = 0 ;
var mar = [] ;
var marVal = [] ;
var markIndex =1 ;
var marker =[];
 
 

//To initialize the values on loading the page.
function initialize () 
	{
		document.getElementById("output").innerHTML = "<h2>Search Results:</h2>&nbsp;"
		a = 0;
		minLat = 32.74548820090014 ;
		maxLat = 32.754511570584455 ;
		minLong = -97.13643730163575 ;
		maxLong = -97.12356269836427 ;
		centerLat = 32.75;
		centerLong = -97.13;
		location1 = { lat: 32.75, lng: -97.13 };
		markIndex =0;
		zoom = 16;
	}

let map;
//To initialize the map and to define methods that can be used to set / remove/ update markers.
function initMap() 
	{
		map = new google.maps.Map(document.getElementById("googleMap"), {center: { lat: centerLat, lng: centerLong },zoom: zoom });
	
		//Update the coordinates and the search results
		function updateCoord()
			{  zoom =  map.getZoom();
				coordinates = map.getBounds();
				minLat = coordinates.Ya.i ;
				maxLat = coordinates.Ya.j ;
				minLong = coordinates.Sa.i ;
				maxLong = coordinates.Sa.j ;
				centerLat = map.getCenter().lat();
				centerLong = map.getCenter().lng();
				sendRequest ();
			}
		//When the map is dragged, then cooradinates will be updated and triggers for search results
		google.maps.event.addListener(map, 'dragend', 
			function()
				{  
					if( zoom ==  map.getZoom())
						{
							updateCoord();
						}
				});
		//When the map is zoom-in/Zoom-Out, then cooradinates, zoom will be updated and triggers for search results
		google.maps.event.addListener(map, 'bounds_changed', 
			function()
				{  
					if( zoom !=  map.getZoom())
						{
							updateCoord();
							zoom =  map.getZoom();
						}
				});
		//To create markers 
		function addMarker() 
			{	
				location1 = { lat: latValue , lng: lngValue };
				marker = new google.maps.Marker
					({
						position: location1,
						label: label1+"",
						title: "Restaurant "+ label1+" : "+titleName,
						map: map,  
					});
				marker.setVisible(true);
				markers.push(marker);
			}
		//To set markers on the map or to remove markers on the map
		function setMapOnAll(map) 
			{
				for (let i = 0; i < markers.length; i++) 
					{
						markers[i].setMap(map);
					}
			}
		//To access the addMarkers method outside the initMap() function
		z = addMarker;
		//To update marker properties and to create markers. Once the markers are created all the markers are set on the map.		
		function setMarker()
			{
				if(  marIndex < marValIndex )
					{
						label1 = marVal[marIndex].label1 ;	
						latValue = marVal[marIndex].latValue ;
						lngValue = marVal[marIndex].lngValue ;
						titleName = marVal[marIndex].titleName ; 
						addMarker();
						marIndex = marIndex +1 ;
					}
				else if ( marIndex == marValIndex )
					{
						setMapOnAll(map);
					}
			}
		//To access setMarker method outside the initMap() function
		z1 = setMarker;
		//To remove the markers on changing the search string
		function removeMarker()
			{
				setMapOnAll(null);
			}
		// to access the removeMarker method outside the initMap() function 
		z2 = removeMarker;
	}



//To display matching results of restaurants.
function sendRequest () 
	{
		var xhr = new XMLHttpRequest();
		var query = encodeURI(document.getElementById("search").value);
		xhr.open("GET", "proxy.php?term="+query+"&latitude="+centerLat+"&longitude="+centerLong+"&sortby=recommended", true)
		if( query )
			{ 
				xhr.onreadystatechange = function () 
					{
						//Not to trigger search results until search term is entered.						
						if (this.readyState == 4 && !(typeof query ==='undefined') )
							{ 
								//To set initialize values
								z();
								//To remove the previous search results.
								z2();
								//To empty the array of markers of previous serach results
								markers = [];
								//To reset the old values before fetching the latest results
								document.getElementById("output").innerHTML = "<h2>Search Results:</h2>&nbsp;"
								a = 0;
								label1 = 0;
								marValIndex = 0;
								result = JSON.parse(this.responseText);	
								marIndex = 0 ;
								markIndex = 0 ;
								for( var index = 0; index < result.businesses.length ; index ++)
									{	
										if(result.businesses[index].coordinates.latitude >= minLat && result.businesses[index].coordinates.latitude <= maxLat && result.businesses[index].coordinates.longitude >= minLong && result.businesses[index].coordinates.longitude <= maxLong)
											{
												a = a+1;
												//Limiting the search results to not more than 10
												if( a > 10)
													{
														break;
													}
												//Updating the values that can be used to update marker properties.
												label1++ ;
												latValue = result.businesses[index].coordinates.latitude ;
												lngValue = result.businesses[index].coordinates.longitude ;
												titleName = result.businesses[index].name ;
												mar[0] = label1;
												mar[1] = latValue;
												mar[2] = lngValue;
												mar[3] = titleName ;
												marVal[marValIndex] = { label1 , latValue , lngValue , titleName }
												marValIndex ++ ;
												document.getElementById("output").innerHTML = document.getElementById("output").innerHTML+"<h4 style = 'text-decoration: underline;'>Restaurant "+label1+":</h4><div><img src ="+result.businesses[index].image_url+" width = 100px ; height = 100px;/><br/><br/><a href = '"+result.businesses[index].url+"' target='_blank' >"+result.businesses[index].name+"</a><br/><br/>Rating:"+result.businesses[index].rating+"<br/><br/><br/><br/></div>";			
											}
										//To add the markers and set them on map.	
										z1();
					
									}
								//When no matching restaurants are found in the visble area of map.
								if( a == 0)
									{
										document.getElementById("output").innerHTML = document.getElementById("output").innerHTML+"<p> No Matches Found!</p>";
									}			
							}
					};
			}
		xhr.send(null);
	}
