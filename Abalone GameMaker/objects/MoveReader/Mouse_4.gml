if(!fileOpen) {
	if(fileName == "") fileName = get_open_filename("any", "");
	
	if(file_exists(fileName)){
		file = file_text_open_read(fileName);
		fileOpen = true;
	}
}

if(doubleClick) {
	if(!file_text_eof(file)){
		var nextLine = file_text_readln(file);
		if(string_char_at(nextLine, 0) == "b" || string_char_at(nextLine, 0) == "w") 
			nextLine = file_text_readln(file);
		board.updateBoard(nextLine);
	} else {
		file_text_close(file)
		file = file_text_open_read(fileName);
	
		var nextLine = file_text_readln(file);
		if(string_char_at(nextLine, 0) == "b" || string_char_at(nextLine, 0) == "w") 
			nextLine = file_text_readln(file);
		board.updateBoard(nextLine);
	}
} else {
	doubleClick = true;
	alarm[0] = 15;
}