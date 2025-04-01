if(mouse_check_button_pressed(mb_left)) {
	//Check if a click happened, and if it's inside of the textbox.
	if(ClickedWithin(self)) {
		inFocus = true;
		keyboard_string = input;
	} else {
		inFocus = false;
	}
}

if(inFocus) {
	if (keyboard_check_pressed(vk_enter)) {
		//If the user presses enter, send the inputs to the board.
		inFocus = false;
		board.updateBoard(input);
	} else if (keyboard_check_pressed(vk_escape)) {
		//If the user presses esc clear the input
		inFocus = false;
		input = "";
	} else if (keyboard_check(ord("V")) && keyboard_check(vk_control)) {
		//Handle pasting text
		keyboard_string = clipboard_get_text();
	} else {
		//Otherwise just let the input read.
		input = keyboard_string;
	}
}