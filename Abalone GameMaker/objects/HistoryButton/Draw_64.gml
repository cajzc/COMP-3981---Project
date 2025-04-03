//Draw the mouseover window when the cursor is inside of the icon.
if(hover) {
	//Create a basic string to base all the height/width off of.
	var history = board.moveHistory;
	//Using the first move, since it will always be the longest (most marbles)
	var firstEntry = "Turn 888: " + ds_list_find_value(history, 0);
	
	//Draw a box for the first entry.
	draw_rectangle(x, y, x + string_width(firstEntry), y + string_height(firstEntry) * ds_list_size(history), false);

	draw_set_halign(fa_left);
	//Loop through the list and draw the moves, alternating between black and white backgrounds.
	for(var i = 0; i < ds_list_size(history); i++) {
		var move = "Turn " + string(i) + ":" + ds_list_find_value(history, i);
		//Odd turns are black.
		if(i % 2 == 1) {
			draw_rectangle_color(x, y + string_height(firstEntry) * i, 
						x + string_width(firstEntry), y + string_height(firstEntry) * (i + 1),
						c_gray, c_gray, c_gray, c_gray, false);
			draw_text(x, y + string_height(firstEntry) * i, move);
		} else {
			//Even turns for white.
			draw_text_color(x, y + string_height(firstEntry) * i, move, 0, 0, 0, 0, 1);
		}
	}
}