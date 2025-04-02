config = instance_find(ConfigHandler, 0);

playerScore = 0;
timeRemaining = ds_map_find_value(config.player1, "time_limit");
totalTime = 0;