function ClickedWithin(itemClicked){
	return point_in_rectangle(mouse_x, mouse_y, 
	itemClicked.x, itemClicked.y, itemClicked.x + itemClicked.sprite_width, itemClicked.y + itemClicked.sprite_height)
}