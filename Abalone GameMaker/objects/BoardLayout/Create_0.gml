getLayout = function(layout) {
	switch(layout){
		//Converts the name of the board style to coordinates.
		case "german": 
			return("H4w,H5w,H8b,H9b,G3w,G4w,G5w,G7b,G8b,G9b,F3w,F4w,F7b,F8b,D2b,D3b,D6w,D7w,C1b,C2b,C3b,C5w,C6w,C7w,B1b,B2b,B5w,B6w");
		case "belgian": 
			return("I5w,I6w,I8b,I9b,H4w,H5w,H6w,H7b,H8b,H9b,G4w,G5w,G7b,G8b,C2b,C3b,C5w,C6w,B1b,B2b,B3b,B4w,B5w,B6w,A1b,A2b,A4w,A5w");
		default:
		case "standard": 
			return("I5w,I6w,I7w,I8w,I9w,H4w,H5w,H6w,H7w,H8w,H9w,G5w,G6w,G7w,C3b,C4b,C5b,B1b,B2b,B3b,B4b,B5b,B6b,A1b,A2b,A3b,A4b,A5b");
	}
}