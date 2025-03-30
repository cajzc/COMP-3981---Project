if(turnCount > 0) {
	board.drawBoard(ds_list_find_value(board.moveHistory, turnCount - 1));
	turnCount--;
}