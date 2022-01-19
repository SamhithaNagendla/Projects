# Web Data Management Labs
Most of the projects will be done using HTML, JavaScript, PHP, SQL, Java and XQuery.
The software used for the projects is open-source, free, platform independent, and well-suited for Java. 
You can do most of the projects on your own PC/laptop under any platform (Linux, MAC OS X, MS Windows, etc)

# Table of Contents
Getting Started
Motivation
List of Projects
Key Learnings
References

# Getting Started
These instructions will get you to set up the environment on your local machine to do these projects.
#
XAMPP web server

Step 1:You need to install the XAMPP web server, which includes the Apache http web server, PHP, MySQL (MariaDB), and PHPMyAdmin (these are the only components you need). 

Step 2:This can be installed on Windows, Linux, and OS X. 

Step 3:The installation directory is \xampp for Windows, /opt/lampp for Linux, and /Applications/XAMPP for OS X. 

Step 4:To start the server on Windows, you run \xampp\xampp-control.exe and you start the Apache web server. 

Step 5:You may have to change the Security properties of this executable to Full Control for Users. 

Step 6:You will test the project on your PC/laptop using the Mozilla Firefox web browser. 
#
Zorba Platform

Step 1:Download Zorba.Use the following link to install https://github.com/zorba-processor/zorba/releases (Links to an external site.).

Step 2:On Mac, for example, after you install it, you may run it using /opt/local/bin/zorba.

Step 3:Put all XQueries in a file "queries.xq" and use the Zorba Command Line Utility (Links to an external site.) to evaluate the XQueries.

Note: If you get the error message on Windows: "The program can not start because libiconv.dll is missing from your computer. Try reinstalling the program to fix the problem", rename the iconv.dll library in the bin folder to libiconv.dll.


# Motivation
The labs were completed as a part of the Web Data Management (CSE 5335) course at The University of Texas at Arlington. The course is well structured to understand the concepts of Web Data Management.

# List of Projects
Project 1:A JavaScript Game

Description:To write a JavaScript file pong.js, used in the file pong.html (after you click on this link, you can get the HTML source if you right-click and use View Page Source). Your code must implement the following actions:
	initialize: initialize the game
	startGame: starts the game (when you click the mouse)
	setSpeed: sets the speed to 0 (slow), 1 (medium), 2 (fast)
	resetGame: resets the game
	movePaddle: moves the paddle up and down, by following the mouse
#	
Project 2:A Movie Web Application

Description:To develop a web application to get information about movies, their cast, their posters, etc. This application should be developed using plain JavaScript and Ajax. You should not use any JavaScript library, such as JQuery. Note that everything should be done asynchronously and your web page should never be redrawn/refreshed completely. This means that the buttons or any other input element in your HTML forms must have JavaScript actions, and should not be regular HTTP requests.
The application should have a text section where one can type a movie title (eg, The Matrix), one "Display Info" button to search, one section to display the search results, and one section to display information about a movie. The search results is an itemized clickable list of movie titles along with their years they were released. When you click on one of these movie titles, you display information about the movie: the poster of the movie as an image, the movie title, its genres (separated by comma), the movie overview (summary), and the names of the top five cast members (ie, actors who play in the movie).
#
Project 3:Web Mashup: Display Best Restaurants on a Map

Description:The HTML web page must have 3 sections:
	search text area to put search terms with a button "Find"
	Google map of size 600*500 pixels, initially centered at (32.75, -97.13) with zoom level 16
	text display area
When you write some search terms in the search text area, say "Indian buffet", it will find the 10 best restaurants in the map area that match the search terms. They may be less than 10 (including zero) sometimes. The map will display the location of these restaurants as map overlay markers with labels from 1 to 10. The text display area will display various information about these restaurants. It will be an ordered list from 1 to 10 that correspond to the best 10 matches. Each list item in the display area will include the following information about the restaurant: the image "image_url", the "name" as a clickable "url" to the Yelp page of this restaurant, and the rating (a number between 1-5). When you search for new terms, it will clear the display area and all the map overlay markers, and will create new ones based on the new search.
#
Project 4:The Movie Web Application in PHP

Description:To develop the movie web application described in Project #2 using PHP. First create a project4 directory inside your web server root directory. Your project is to write only one PHP program movies.php inside project4. You don't need to use JavaScript. You don't need any proxy. The initial page is a search form with a text area widget and a "Display Info" button. When you click on the button to search, you get a page that contains the search form and a section with the search results. The search results is an itemized clickable list of movie titles along with their years they were released. When you click on the title of one of the search results, you get a web page with the search form and information about the movie: the poster of the movie as an image, the movie title, its genres (separated by comma), the movie overview (summary), and the names of the top five cast members (ie, actors who play in the movie). You call movies.php script in two ways: for example, using movies.php?search=The+Matrix to get search results for "The Matrix" and movies.php?id=603 to get the page with the description of the movie 603.
#
Project 5:A Social Network using PHP and MySQL

Description:Create 10 users in the table users using phpMyAdmin. You need to write two PHP scrips login.php and network.php. The login.php script generates a form that has two text windows for username and password and a button "Login". The network.php script prints three sections and a "Logout" button. 
	The first section prints the username, fullname, and email of the current user (the user currently logged-in). 
	The second section "Friends" lists the friends of the current user. 
	The third section "Others" lists all the other users who are not friends (non-friends) of the current user. 
	For each friend or non-friend you display username, fullname, and email. 
	Each friend has a button "Remove" to remove her from the friends and add her to the non-friends. 
	Each non-friend has a button "Add" to add her to the friends and remove her from the non-friends.

From the login script, if the user enters a wrong username/password and pushes "Login", it should go to the login script again. 
If the user enters a correct username/password and pushes "Login", it should go to the network script. From the network script, if the user pushes "Logout", it should logout and go to the login script. 
The network script must always make sure that only authorized users (users who have logged-in properly) can use this script (you need to use a session to check this).
#
Project 6:Using Cloud Storage

Description:To develop a trivial photo-album application on Dropbox.To use Dropbox to store the photos and you need to be able to delete photos. Your task is to modify your album.php script in your project6 directory to support the following operations:
	Provide a form to upload a new image (a *.jpg). Look at the class slides for a PHP example that handles uploads.
	A display window that lists the names of the images in your dropbox directory. For each image name you have a link that, when you click it, it displays the image in the image section. Each image name also has a button to delete this image from the dropbox storage.
	An image section that displays the selected image. You can change the image by changing the src attribute value of the <img ...> element (you don't need Ajax; you just need to generate Javascript from your album.php). Hint: you may use the onclick method on a image file name to change the src attribute of the img to the o->GetLink($dropbox_file).
# 	
Project 7:Using DOM, XPath, and XSLT

Description:You will evaluate DOM, XPath, and XSLT over XML data that represents courses from Reed College, available at reed.xml, with DTD reed.dtd provided. More specifically:
	Write a plain Java program dom.java that uses the Java DOM API over the XML data in reed.xml to print the titles of all MATH courses that are taught in room LIB 204
	Write a plain Java program xpath.java that evaluates the following XPath queries over the XML data in reed.xml:
	Print the titles of all MATH courses that are taught in room LIB 204
	Print the instructor name who teaches MATH 412
	Print the titles of all courses taught by Wieting
	Write an XSLT program math.xsl to display all MATH courses in Reed College by transforming the XML file reed.xml to XHTML using XSLT. Your XHTML must contain a table, where each table row is a Math course. Modify the Java program xslt.java  Download xslt.javato test your XSLT and then load the resulting html output file on your web browser.	
#
Project 8:Using XQuery

Description:Consider the XML document available at reed.xml, with DTD reed.dtd used in Project #7. Express the following queries using XQuery and run them against the file reed.xml using Zorba:
	For each MATH course taught in room LIB 204, return an element tagged course with the title, the instructor, the start, and the end times of the course.
	For each different course, return an element tagged course with the course title and all the instructor names that teach this course.
	For each different department, display the department code and the number of courses taught by the department.
	For each different instructor, return an element tagged instructor that contains the name of the instructor and the number of courses taught by the instructor.
	For each different instructor, return an element tagged instructor that contains the name of the instructor and the titles of all courses taught by the instructor.

# Key Learnings
Learnt to use current web technologies to develop dynamic web sites. 
Developed web sites that use dynamic content generated from a database. 
Developed web services and dynamic web applications that use web services.

# References
Lecture slides, extra resources provided by Professor in the project descriptions.

Programming the World Wide Web, by Robert W. Sebesta (7th Edition), 2013,ISBN-10: 0132665816.
