if(turnCount > 1) {
	turnCount--;
	board.drawBoard(ds_list_find_value(board.moveHistory, turnCount - 1));
	
}