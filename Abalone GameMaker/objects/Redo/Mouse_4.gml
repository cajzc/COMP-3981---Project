if(turnCount < ds_list_size(board.moveHistory)) {
	board.drawBoard(ds_list_find_value(board.moveHistory, turnCount));
	turnCount++;
	
	if(turnPlayer = "b") turnPlayer = "w";
	else turnPlayer = "b";
}