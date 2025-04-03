changeCoordinate = function(q,r,s) {
	self.q = q;
	self.r = r;
	self.s = s;
}

setColour = function(colour) {
	self.colour = colour;
	
	if(colour == "b") blackMarbles++;
	else whiteMarbles++;
}

changeTile = function(newSpace) {
	space.marble = noone;
	space = newSpace;
	space.marble = id;
}

space = noone;