if (selected[0] != noone) {
	marble = selected[0]
	marble.x = x + sprite_width / 20;
	marble.y = y + sprite_height / 20;
	
	marble.changeCoordinate(q,r,s);
	marble.changeTile(self);
}