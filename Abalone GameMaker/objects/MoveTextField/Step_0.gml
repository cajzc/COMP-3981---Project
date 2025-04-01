if(mouse_check_button_pressed(mb_left)) {
	if(ClickedWithin(self)) {
		inFocus = true;
		keyboard_string = input;
	} else {
		inFocus = false;
	}
}

if(inFocus) {
	if (keyboard_check_pressed(vk_enter)) {
		inFocus = false;
		board.updateBoard(input);
	} else if (keyboard_check_pressed(vk_escape)) {
		inFocus = false;
		input = "";
	} else if (keyboard_check(ord("V")) && keyboard_check(vk_control)) {
		keyboard_string = clipboard_get_text();
	} else {
		input = keyboard_string;
	}
}