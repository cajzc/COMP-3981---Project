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

    @staticmethod
    def tostring_board(player, board):
        """
        Converts the board state back to the input file format.

        :param player: Current player ('b' or 'w').
        :param board: Board dictionary {(x, y): 'b'/'w'/'N'}.
        :return: String formatted as the input file (player + marbles).
        """
        marble_list = []
        for (x, y), color in board.items():
            if color == 'N':
                continue  # Skip empty cells
            row = chr(y + 69)  # Convert y to row letter (A-I)
            column = x + 5  # Convert x to column number (1-9)
            marble_str = f"{row}{column}{color}"

            marble_list.append((color,row,column,marble_str)) # append tuple for sorting

        sorted_marbles = sorted(marble_list, key=lambda item: (item[0],item[1],item[2]))

        marble_strs = [item[3] for item in sorted_marbles]

        return f"{player}\n{','.join(marble_strs)}"