globalvar showCoord;
globalvar showName;

//Flags for displaying data.
showCoord = true;
showName = true;

//Where all of the rows are stored.
rows = [array_create(5), array_create(6), array_create(7), array_create(8), array_create(9),
			array_create(8), array_create(7), array_create(6), array_create(5)];
			
moveHistory = ds_list_create();

gamemaster = instance_find(Gamemaster, 0);

enum rowLetters
{
	I,
	H,
	G,
	F,
	E,
	D,
	C,
	B,
	A
}

//Programmatically creates spaces to fill each row
createRow = function(array, row, start_q, start_r, start_s, start_num){
	/// @arg {array} the row to generate
	/// @arg {row} the letter label given to this row
	/// @arg {start_q} starting q coordinate
	/// @arg {start_r} starting r coordinate
	/// @arg {start_s} starting s coordinate
	for(var i = 0; i < array_length(array); i++) {
		array[i] = instance_create_layer(x, y, "Spaces", Space)
		with (array[i]) {
			//Initialize the space with the correct information
			q = start_q + i;
			r = start_r;
			s = start_s - i;
			row_num = string(start_num + i);
			name = string_concat(row, row_num);
		}
	}
}

placeSpaces = function(array, start_x, start_y, padding){
	/// @arg {array} the row to reposition
	/// @arg {start_x} starting x coordinate, relative to the board
	/// @arg {start_y} starting y coordinate, relative to the board
	/// @arg {padding} padding as a percentage of the sprite's width
	for(var i = 0; i < array_length(array); i++) {
		with array[i] {
			//positions spaces based on their position in the array.
			x = start_x + sprite_width * i + i * padding * sprite_width;
			y = start_y;
		}
	}
}

//Create the rows 1 by 1
createRow(rows[0], "I", 0, -4, 4, 5)
placeSpaces(rows[0], x + sprite_width * 5/20, y + sprite_height * 1/19, 1/3)

createRow(rows[1], "H", -1, -3, 4, 4)
placeSpaces(rows[1], x + sprite_width * 4/20, y + sprite_height * 3/19, 1/3)

createRow(rows[2], "G", -2, -2, 4, 3)
placeSpaces(rows[2], x + sprite_width * 3/20, y + sprite_height * 5/19, 1/3)

createRow(rows[3], "F", -0, -1, 4, 2)
placeSpaces(rows[3], x + sprite_width * 2/20, y + sprite_height * 7/19, 1/3)

createRow(rows[4], "E", -4, 0, 4, 1)
placeSpaces(rows[4], x + sprite_width * 1/25, y + sprite_height * 9/19, 1/3)

createRow(rows[5], "D", -4, 1, 3, 1)
placeSpaces(rows[5], x + sprite_width * 2/20, y + sprite_height * 11/19, 1/3)

createRow(rows[6], "C", -4, 2, 2, 1)
placeSpaces(rows[6], x + sprite_width * 3/20, y + sprite_height * 13/19, 1/3)

createRow(rows[7], "B", -4, 3, 1, 1)
placeSpaces(rows[7], x + sprite_width * 4/20, y + sprite_height * 15/19, 1/3)

createRow(rows[8], "A", -4, 4, 0, 1)
placeSpaces(rows[8], x + sprite_width * 5/20, y + sprite_height * 17/19, 1/3)

updateBoard = function(boardString){
	drawBoard(boardString);
	
	gamemaster.endTurn();
	
	//Add this board state to the move history.
	ds_list_insert(moveHistory, turnCount - 1, boardString);
	
	TrimList(moveHistory, turnCount);
}

drawBoard = function(boardString) {
	//Clean up the board first
	clearBoard(rows)
	//Use the comma as a delimiter to split the string up.
	var spaceList = string_split(boardString, ",");
	
	for (var i = 0; i < array_length(spaceList); i++) {
		//Make sure each move unit is at least 3 characters.
		if(string_length(spaceList[i]) >= 3) {
			//Get the space that is being modified.
			var currentSpace = string_copy(spaceList[i], 1, 2);
			var marbleColor = string_copy(spaceList[i], 3, 1);
			
			//Separate the row letter from the number to lookup the row.
			var currentRow = rows[RowLookup(string_copy(currentSpace, 1, 1))];
			
			//Search for the correct space
			for(var j = 0; j < array_length(currentRow); j++){
				if(currentSpace == currentRow[j].name) {
					//Create a marble at that space.
					with(currentRow[j]) {
						marble = instance_create_layer(x + sprite_width / 20 ,y + sprite_height / 20,"Marbles", Marble);
						marble.setColour(marbleColor);
						marble.changeCoordinate(q,r,s);
						marble.space = self;
					}
					//exit the inner loop.
					break;
				}
			}
		}
	}	
}

clearBoard = function(rows) {
	for(var i = 0; i < array_length(rows); i++) {
		for(var j = 0; j < array_length(rows[i]); j++) {
			instance_destroy(rows[i][j].marble);
		}
	}
}

saveBoardState = function() {
	var boardState = "";
	for(var i = 0; i < array_length(rows); i++) {
		for(var j = 0; j < array_length(rows[i]); j++) {
			if(rows[i][j].marble != noone) {
				var currentSpace = rows[i][j];
				//Create an entry for every space with a marble.
				boardState = string_concat(boardState, currentSpace.name, currentSpace.marble.colour, ",");
			}
		}
	}
	//Remove the last trailing comma.
	boardState = string_delete(boardState, string_length(boardState), 1);
	
	gamemaster.endTurn();
	ds_list_insert(moveHistory, turnCount - 1, boardState);
	
	TrimList(moveHistory,turnCount);
	
	show_debug_message(boardState);
}