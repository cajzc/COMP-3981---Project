if(!fileOpen) {
	//If the file has not been read yet, ask the user.
	if(fileName == "") fileName = get_open_filename("any", "");
	
	//If it exists, begin reading from it.
	if(file_exists(fileName)){
		file = file_text_open_read(fileName);
		fileOpen = true;
	}
}

if(doubleClick) {
	//As long as there's text read the next line.
	if(!file_text_eof(file)){
		var nextLine = file_text_readln(file);
		if(string_char_at(nextLine, 0) == "b" || string_char_at(nextLine, 0) == "w") 
			nextLine = file_text_readln(file);
		board.updateBoard(nextLine);
	} else {
		//If we reach the end, reset the file and then reopen it.
		file_text_close(file)
		file = file_text_open_read(fileName);
		
		//Then read the first line.
		var nextLine = file_text_readln(file);
		if(string_char_at(nextLine, 0) == "b" || string_char_at(nextLine, 0) == "w") 
			nextLine = file_text_readln(file);
		board.updateBoard(nextLine);
	}
} else {
	doubleClick = true;
	alarm[0] = 15;
}