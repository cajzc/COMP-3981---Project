globalvar turnPlayer;
globalvar turnCount;
globalvar whiteMarbles;
globalvar blackMarbles;

turnCount = 0;
turnPlayer = "b";
whiteMarbles = 0;
blackMarbles = 0;

//Handles the end of turn logic.
endTurn = function() {
	if (turnPlayer == "b") turnPlayer = "w";
	else turnPlayer = "b";
	
	turnCount++;
}

//Used for undoing a move.
rollback = function() {
	if (turnPlayer == "b") turnPlayer = "w";
	else turnPlayer = "b";
	
	turnCount--;
}