draw_self();
draw_set_halign(fa_center);
draw_text_transformed_color(x + sprite_width / 2,
					y + sprite_height / 2 - string_height(label) / 2, label, 1.2, 1.2, 0,
					0,0,0,0,1);
					
if(config.boardConfig == value) sprite_index = SelectedLayoutButtonSprite;
else sprite_index = BoardLayoutButtonSprite;