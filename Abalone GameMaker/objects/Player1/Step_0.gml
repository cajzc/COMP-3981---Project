if(running && turnPlayer == "b") {
	if(frameCount > 0) frameCount--;
	else{
		frameCount = 59;
		timeRemaining--;
	}
}