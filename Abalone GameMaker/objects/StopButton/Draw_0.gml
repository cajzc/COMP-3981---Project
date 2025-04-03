draw_self();

var remainingTime = sprite_height - heldTime / 120 * sprite_height;
var normalSprite = sprite_height - remainingTime;

draw_sprite_part_ext(sprite_index, image_index, 0, remainingTime, sprite_width, normalSprite,
					x - sprite_xoffset, y - sprite_yoffset + remainingTime,
					1, 1, c_red, 1);