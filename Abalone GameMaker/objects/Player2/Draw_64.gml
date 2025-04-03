draw_set_halign(fa_left);
draw_text_transformed(x,y, "White", 2, 2, 0);

var turnTimer = "Time: " + string(timeRemaining) + ":" 
if(frameCount < 10) turnTimer += "0" + string(frameCount);
else turnTimer += string(frameCount);

var totalTimer = "Total: " + string(totalTimeMin) + ":"
if(totalTime < 10) totalTimer += "0" + string(totalTime);
else totalTimer += string(totalTime);

var scoreText = "Score: " + string(playerScore);

draw_text_transformed(x, y + string_height(turnTimer), turnTimer, 2, 2, 0);
draw_text_transformed(x, y + string_height(totalTimer) * 2, totalTimer, 2, 2, 0);
draw_text_transformed(x, y + string_height(scoreText) * 3, scoreText, 2, 2, 0);