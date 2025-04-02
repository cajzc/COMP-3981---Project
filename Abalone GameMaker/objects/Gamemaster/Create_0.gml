globalvar turnPlayer;
globalvar turnCount;
globalvar whiteMarbles;
globalvar blackMarbles;
globalvar startingMarbles;
globalvar inFile;

//Game wide variables, used in the other objects.
turnCount = 0;
turnPlayer = "b";
whiteMarbles = 0;
blackMarbles = 0;
startingMarbles = 14;
inFile = "board_input.txt";


config = instance_find(ConfigHandler, 0);
board = instance_find(Board, 0);

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



board.updateBoard(config.boardString);