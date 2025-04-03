//Used to store all information for player white
config = instance_find(ConfigHandler, 0);

playerScore = 0;
timeLimit = ds_map_find_value(config.player2, "time_limit");
timeRemaining = timeLimit;
frameCount = 0;
totalTime = 0;
totalTimeMin = 0;

//Handles end of turn logic.
endOfTurn = function() {
	//Add used time to the remaining time.
	totalTime += timeLimit - timeRemaining;
	//Track the minutes and seconds separately.
	if(totalTime >= 60) {
		totalTimeMin++;
		totalTime = totalTime % 60;
	}
	//Recalculate score
	playerScore = startingMarbles - blackMarbles;
	//Reset timers.
	timeRemaining = timeLimit;
	frameCount = 0;
}

//Handles reset button logic.
reset = function() {
	timeRemaining = timeLimit;
	frameCount = 0;
	totalTime = 0;
	totalTimeMin = 0;
}