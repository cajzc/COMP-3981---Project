"""Houses the board representation methods."""

class Board:
    """Holds the implementation to parse and output a board's representation."""

    @staticmethod
    def initialize_board():
        """
        Initialize the board with all positions as 'N' (neutral/empty)
        
        :returns: the game board representation as dictionary, where keys represent tuples of positions and values represent the value in the position
        """
        return {(x, y): 'N' for x in range(-4, 5) for y in range(-4, 5) if -4 <= x - y <= 4}

    @staticmethod
    def get_input_board_representation(file_name):
        """
        Given the class example files with the suffix ".input", returns the player turn and converts a given input board position from an example format:

        Into the team's specific game board format, i.e:
        {(-4, -4): 'N', ..., (-2, -2): 'W', ..., (4, 4): 'N'}

        :param file_name: the name of the input file
        :returns: tuple containing (player turn, game board representation as dictionary)
        """
        current_board = Board.initialize_board()
        
        with open(file_name, 'r') as f:
            player = f.readline().strip()
            marbles = f.readline().strip().split(',')

        for marble in marbles:
            x = int(marble[1]) - 5
            y = ord(marble[0]) - ord('E')
            current_board[(x, y)] = marble[2]

        return player, current_board
