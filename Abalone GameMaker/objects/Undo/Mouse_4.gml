//When clicked revert the board to the previous turn count.
if(turnCount > 1) {
	turnCount--;
	board.drawBoard(ds_list_find_value(board.moveHistory, turnCount - 1));
	
	if(turnPlayer = "b") turnPlayer = "w";
	else turnPlayer = "b";
}