if (selected[0] != noone && marble = noone) {
	//Move the selected marble to this coordinate.
	marble = selected[0]
	marble.x = x + sprite_width / 20;
	marble.y = y + sprite_height / 20;
	
	//Update the marble's parameters.
	marble.changeCoordinate(q,r,s);
	marble.changeTile(id);
}