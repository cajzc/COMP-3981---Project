globalvar turnPlayer;
globalvar turnCount;
globalvar whiteMarbles;
globalvar blackMarbles;
globalvar startingMarbles;
globalvar inFile;
globalvar running;

//Game wide variables, used in the other objects.
turnCount = 0;
turnPlayer = "w";
whiteMarbles = 0;
blackMarbles = 0;
startingMarbles = 14;
inFile = "board_input.txt";
running = false;

config = instance_find(ConfigHandler, 0);
board = instance_find(Board, 0);
player1 = instance_find(Player1, 0);
player2 = instance_find(Player2, 0);

//Handles the end of turn logic.
endTurn = function() {
	//Called to perform all end of turn actions.
	if (turnPlayer == "b") turnPlayer = "w";
	else turnPlayer = "b";
	
	turnCount++;
	player1.endOfTurn();
	player2.endOfTurn();
}

//Used for undoing a move.
rollback = function() {
	//used to undo moves.
	if (turnPlayer == "b") turnPlayer = "w";
	else turnPlayer = "b";
	
	turnCount--;
}

reset = function() {
	//Resets everything that needs to be reset.
	board.reset();
	player1.reset();
	player2.reset();
	selected[0] = noone;
	
	//Pause the game.
	running = false;
}

board.updateBoard(config.boardString);