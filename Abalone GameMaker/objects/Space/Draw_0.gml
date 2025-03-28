draw_self()
if(showName)
draw_text_transformed_colour(x + sprite_width / 5, y + sprite_height / 5, name, 1.5, 1.5, 0,
								0,0,0,0,1);

if(showCoord){
	draw_text_colour(x + sprite_width / 10,y - sprite_height / 4, string(q), 0,0,0,0,1);
	draw_text_colour(x + sprite_width - sprite_width / 15, y + sprite_height / 2 - sprite_height / 5, string(r), 0,0,0,0,1);
	draw_text_colour(x + sprite_width / 10 ,y + sprite_height - sprite_height / 5, string(s), 0,0,0,0,1);
}