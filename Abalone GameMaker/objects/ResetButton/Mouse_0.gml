held = true;
heldTime++;

if(heldTime >= 120) {
	gamemaster.reset();
	
	heldTime = 0;
}