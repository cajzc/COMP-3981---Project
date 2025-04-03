//Used to store all information for player black.
config = instance_find(ConfigHandler, 0);

playerScore = 0;
timeLimit = ds_map_find_value(config.player1, "time_limit");
timeRemaining = timeLimit;
frameCount = 0;
totalTime = 0;
totalTimeMin = 0;

//Handles end of turn logic.
endOfTurn = function() {
	//Add the time used to the total time.
	totalTime += timeLimit - timeRemaining;
	if(totalTime >= 60) {
		//Track the minutes and seconds.
		totalTimeMin++;
		totalTime = totalTime % 60;
	}
	//Recalculate score.
	playerScore = startingMarbles - whiteMarbles;
	timeRemaining = timeLimit;
	frameCount = 0;
	
}

//Handles reset button logic
reset = function() {
	timeRemaining = timeLimit;
	frameCount = 0;
	totalTime = 0;
	totalTimeMin = 0;
}