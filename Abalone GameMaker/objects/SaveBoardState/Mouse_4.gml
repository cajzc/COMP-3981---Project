//Saves whatever changes were manually made to the board and counts it as a turn.
if(doubleClick)
	board.saveBoardState();
else{
	doubleClick = true;
	alarm[0] = 15;
}