player1 = ds_map_create();
player2 = ds_map_create();
globalvar configFile;

boardString = "";

startGame = function() {
	var finalMap = ds_map_create()
	boardString = BoardLayout.getLayout(boardConfig);
	
	//Add the basic values to the board.
	ds_map_set(finalMap, "initial_board_layout", boardConfig);
	ds_map_set(finalMap, "gameMode", gameMode);
	
	//Create each player object and add values to them.
	ds_map_set(player1, "move_limit", moveLimit);
	ds_map_set(player1, "time_limit", timeLimitBlack);
	
	ds_map_set(player2, "move_limit", moveLimit);
	ds_map_set(player2, "time_limit", timeLimitWhite);
	
	if(playerColour == "b") {
		ds_map_set(player1, "color", playerColour);
		ds_map_set(player2, "color", "w");
	} else {
		ds_map_set(player1, "color", playerColour);
		ds_map_set(player2, "color", "b");
	}
	
	//Add both players to the map.
	ds_map_add_map(finalMap, "player1", player1);
	ds_map_add_map(finalMap, "player2", player2);

	//Write the data to the config file.
	var jsonData = json_encode(finalMap, true);
	configFile = file_text_open_write(working_directory + "AbaloneConfig.json");
	file_text_write_string(configFile, jsonData);
	file_text_close(configFile);
	
	room_goto_next();
}