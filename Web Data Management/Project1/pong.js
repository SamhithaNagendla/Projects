/*
Student Name: Samhitha Nagendla (sxn7208)
File Name: pong.js
Description: Java script for Pong game
*/

//Global Variables
initialVelocity= 10;
stopInd = 0; 						//This variable is used to terminate the game
time= 0.5; 							//Varying the time attribute to change the speed of ball movement
strikes = 0;
maxScore = 0;

//To Initialize the values required for game, Called upon first start or refresh of page
function initialize()
{
    // Updating the speed to Slow, strikes and maxScore to zero, initial velocity and time to default values
    var speedSelected=document.getElementsByName("speed");
    speedSelected[0].checked=true;
    strikes = 0;
    document.getElementById("strikes").innerText = strikes;
    maxScore = 0;
    document.getElementById("score").innerText = maxScore;
    initialVelocity= 10;
    time= 0.5;

    //This indicator is used to terminate the game
    stopInd = 0;

    // To update the dimensions and position of court, ball and paddle
    topCourtPosition = court.getBoundingClientRect().top;
    leftCourtPosition = court.getBoundingClientRect().left;
    courtBorderWidth = parseInt(document.getElementById("court").style.borderWidth);
    courtWidth = parseInt(document.getElementById("court").style.width);
    courtHeight = parseInt(document.getElementById("court").style.height);
    ballWidth = parseInt(document.getElementById("ball").width);
    ballHeight = parseInt(document.getElementById("ball").height) ;
    paddleWidth = parseInt(document.getElementById("paddle").width) ;
    paddleHeight = parseInt(document.getElementById("paddle").height) ;

    //As both paddle and ball are relatively positioned, Ball top position needs to be adjusted to the difference in their height plus the border size
    topPositionAdjust = (paddleHeight - ballHeight) + courtBorderWidth;
    topBallReferencePosition = topCourtPosition - 2 * (paddleHeight + ballHeight + courtBorderWidth);
    leftBallReferencePosition = leftCourtPosition + courtBorderWidth ;
    leftPaddlePosition = 750 ;
    xPosition =0;
    yPosition =0;
    topBallRelativePosition = ball.getBoundingClientRect().top;

    document.getElementById("messages").innerHTML= document.getElementById("messages").innerHTML + '<p> Game is loaded. </p> <br/>' ;
}

//To move the paddle based on the mouse movement
function movePaddle(event)
{
    if (((event.pageY)) < (topCourtPosition) )
    {
      document.getElementById("paddle").style.top = 0  + "px" ;
    }
    else if ( ((event.pageY) + paddleHeight +ballHeight ) > ( topCourtPosition  + courtHeight + courtBorderWidth))
    {
      document.getElementById("paddle").style.top = ( 0 + courtHeight - paddleHeight )   + "px" ;
    }
    else
    {
      document.getElementById("paddle").style.top = ((event.pageY) - (1.5 * paddleHeight))  + "px";
    }
}

//To calculate a random position for the ball
function getRandomInitialBallPosition()
{
    var topCourtValue = topBallReferencePosition - 2 * courtBorderWidth;
    var courtSize= courtHeight - ballHeight;
    var randomValue=Math.random();
    var scaledRandomValue= Math.floor(randomValue * courtSize);
    return scaledRandomValue + topCourtValue;
}

//To calculate a random direction for the ball
function getRandomInitialBallDirection()
{
    var minDirection=-Math.PI / 4;
    var maxDirection=Math.PI / 4;
    var diffDirection=(maxDirection - minDirection);
    var randomValue=Math.random();
    var scaledRandomValue= Math.floor(randomValue * diffDirection);
    return scaledRandomValue + minDirection;
}

//To assign a random position to the ball when game starts / resets
function initialPosition()
{
    ballXPosition= 0;
    ballYPosition = getRandomInitialBallPosition();
    document.getElementById("ball").style.top = parseInt(ballYPosition)+"px";
    document.getElementById("ball").style.left = parseInt(ballXPosition)+"px";
    xPosition=document.getElementById("ball").style.left;
    yPosition=document.getElementById("ball").style.top;
}

//To assign a random angle to the ball when the game starts
function initialAngle()
{
    randomAngle=getRandomInitialBallDirection();
    xVelocity=initialVelocity * Math.cos(randomAngle);
    yVelocity=initialVelocity * Math.sin(randomAngle);
}

//Function that updates the ball position, stop indicator and scores
function moveBall()
{
    //Calculating the ball future coordinates
    var x1Position = parseFloat(xPosition) + xVelocity * time ;
    var y1Position = parseFloat(yPosition) + yVelocity * time ;

    //Calcuating the boundaries of the court
    var yTop = topBallReferencePosition - 2 * courtBorderWidth ;
    var yBottom = yTop + courtHeight - ballHeight;
    var xLeft = leftBallReferencePosition;
    var xRight = xLeft + leftPaddlePosition;

    //Bounce the ball if it hits top
    if(y1Position < (yTop))
    {
      y1Position = 2 * yTop -  y1Position;
      yVelocity = - yVelocity;
    }

    //Bounce the ball if it hits bottom
    if(y1Position > (yBottom))
    {
      y1Position = 2 * yBottom - y1Position;
      yVelocity = - yVelocity;
    }

    //Bounce the ball if it hits the left border
    if(x1Position < (xLeft - leftCourtPosition - courtBorderWidth))
    {
      x1Position = 2 * xLeft - x1Position;
      xVelocity = - xVelocity;
    }

    //Updating the current paddle positions
    yPaddle1T = parseFloat(document.getElementById("paddle").style.top);
    yPaddle1B = yPaddle1T + paddleHeight;

    //checks whether the ball strikes the paddle
    if(x1Position > xRight && ( ((y1Position + topPositionAdjust) >= yPaddle1T ) && ((y1Position + topPositionAdjust) <= yPaddle1B  ) ) )
    {
      x1Position = 2 * xRight - x1Position ;
      xVelocity = - xVelocity ;

      //Updating the scores
      strikes = strikes + 1;
      document.getElementById("strikes").innerText= strikes;

      maxScore = Math.max( maxScore , strikes );
      document.getElementById("score").innerText= maxScore;
    }

    //Updating ball position based on all the above scenarios
    xPosition = x1Position;
    yPosition = y1Position;
    document.getElementById("ball").style.left = parseFloat(xPosition) + "px";
    document.getElementById("ball").style.top = parseFloat(yPosition) + "px";

    //If paddle misses the ball
    if(x1Position > xRight && ( ((y1Position + topPositionAdjust) < yPaddle1T ) || ((y1Position + topPositionAdjust) > yPaddle1B ) ) ) //satisfies when ball miss to strike the paddle.
    {
      maxScore = Math.max( maxScore , strikes );
      document.getElementById("score").innerText= maxScore;

      document.getElementById("messages").innerHTML= document.getElementById("messages").innerHTML + '<p> Game ended with score ' + strikes + '. Maximum Score is ' + maxScore + '</p><br/>'	;

      //updated the stop indicator to stop the game
      stopInd = 1;
    }

    //To decide if the game continues or ends
    ballMovement();
}

//Function that triggers the ball position update every 50 milliseconds
function ballMovement()
{
    if(stopInd == 0)
    {
      setTimeout(moveBall, 50);
    }
    else
    {
      initialPosition();
    }
}

// Function used to change the speed of the ball based on option selected in the form
function setSpeed(a)
{
    // Time is used as a factor to modify speed as ball movement is a factor of velocity and time
    switch (a)
    {
      case 0:			//Slow speed
        time=0.5;
        break;
      case 1:			//Medium speed
        time=1;
        break;
      case 2:			//Fast speed
        time=1.5;
    }
}

//To start the game
function startGame()
{
    //Resetting the strikes
    strikes = 0;
    document.getElementById("strikes").innerText= strikes;

    //Resetting the stop indicator
    stopInd = 0;

    //To initialize position and move the ball
    initialAngle();
    document.getElementById("messages").innerHTML= document.getElementById("messages").innerHTML + '<p> Game Started. </p> <br/>' ;
    moveBall();
}

//To reset the game
function resetGame()
{
    //Resetting the time, speed, velocity, position and scores
    var speedSelected=document.getElementsByName("speed");
    speedSelected[0].checked=true;

    strikes = 0;
    document.getElementById("strikes").innerText= strikes;

    maxScore = 0;
    document.getElementById("score").innerText= maxScore;

    stopInd = 1;
    initialVelocity= 10;
    time= 0.5;

    document.getElementById("messages").innerHTML= '<p> Game is Reset. </p> <br/>' ;
    initialPosition();
}
