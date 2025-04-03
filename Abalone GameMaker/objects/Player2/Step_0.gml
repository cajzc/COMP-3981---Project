if(running && turnPlayer == "w") {
	if(frameCount > 0) frameCount--;
	else{
		frameCount = 59;
		timeRemaining--;
	}
}