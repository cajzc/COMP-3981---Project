"""Houses the board representation methods."""
import os
import sys
from enum import Enum, auto
from typing import Tuple, Set, List
from enums import Marble
import copy
from file_paths import FilePaths

class BoardConfiguration(Enum):
    """Represents initial board configurations as an enum."""
    DEFAULT = auto()
    BELGIAN = auto()
    GERMAN = auto()

class Board:
    """Holds the implementation to parse and output a board's representation."""

    def __init__(self):
        self.marble_positions = {} # (q,r,s):color only store marbles in the dict saving space
        self.empty_positions = set((q,r,s) for q in range(-4,5)
                                           for r in range(-4,5)
                                           for s in range(-4,5)
                                          if q+r+s == 0)


    def reset_board(self):
        """
        Resets the board by clearing all marble positions and regenerating empty positions.
        """
        self.marble_positions.clear()
        self.empty_positions = set(
            (q, r, s) for q in range(-4, 5)
            for r in range(-4, 5)
            for s in range(-4, 5)
            if q + r + s == 0
        )

    def set_default_board(self):
        """
        Creates a standard Abalone board with black marbles on the bottom
        (rows A–C) and white marbles on top (rows G–I).
        """
        # White marble initial positions (top 3 rows)
        white_marble_initial_pos = [
            # Row G (r=-2), cols 4..6 => q=-1..1
            (0, -2, 2), (1, -2, 1), (2, -2, 0),
            # Row H (r=-3), cols 4..9 => q=-1..4
            (-1, -3, 4), (0, -3, 3), (1, -3, 2), (2, -3, 1), (3, -3, 0), (4, -3, -1),
            # Row I (r=-4), cols 5..9 => q=0..4
            (0, -4, 4), (1, -4, 3), (2, -4, 2), (3, -4, 1), (4, -4, 0)
        ]       

        # Black marble initial positions (bottom 3 rows)
        black_marble_initial_pos = [
            # Row A (r=+4), cols 1..5 => q=-4..0, s=-q-r
            (-4, 4, 0), (-3, 4, -1), (-2, 4, -2), (-1, 4, -3), (0, 4, -4),
            # Row B (r=+3), cols 1..6 => q=-4..1
            (-4, 3, 1), (-3, 3, 0), (-2, 3, -1), (-1, 3, -2), (0, 3, -3), (1, 3, -4),
            # Row C (r=+2), cols 4..6 => q=-1..1
            (-2, 2, 0), (-1, 2, -1), (0, 2, -2)
        ]
       
                
        self.reset_board()

        # Place black marbles
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = Marble.BLACK.value

        # Place white marbles
        for pos in white_marble_initial_pos:
            self.marble_positions[pos] = Marble.WHITE.value

        # Remove these positions from empty_positions
        self.empty_positions -= set(black_marble_initial_pos + white_marble_initial_pos)


    def set_belgian_daisy_board(self):
        """
        Places the Belgian Daisy layout with Black marbles on rows near A
        and White marbles on rows near I, using (q,r,s) with row A=+4, row I=-4.
        """

        # -----------------------------
        # Black marbles (two 'daisies' at the bottom left and top right)
        # -----------------------------
        black_marble_initial_pos = [
            # Bottom-left daisy (rows A to C):
            # Row A 
            (-4, 4, 0), (-3, 4, -1),
            # Row B 
            (-4, 3, 1), (-3, 3, 0), (-2, 3, -1),
            # Row C 
            (-3, +2, +1), (-2, +2, 0),

            # Top-right daisy (rows I to G):
            # Row I 
            (3, -4, 1), (4, -4, 0),
            # Row H 
            (2, -3, 1), (3, -3, 0), (4, -3, -1),
            # Row G 
            (2, -2, 0), (3, -2, -1)
        ]

        # -----------------------------
        # White marbles (two 'daisies' at the bottom right and top left)
        # -----------------------------
        white_marbles_initial_pos = [
            # Bottom-right daisy (rows A to C):
            # Row A 
            (-1, 4, -3), (0, 4, -4),
            # Row B 
            (-1, 3, -2), (0, 3, -3), (1, 3, -4),
            # Row C 
            (0, 2, -2), (1, 2, -3),

            # Top-left daisy (rows I to G):
            # Row I 
            (0, -4, 4), (1, -4, 3),
            # Row H 
            (-1, -3, 4), (0, -3, 3), (1, -3, 2),
            # Row G 
            (-1, -2, 3), (0, -2, 2)
        ]

        # Clear and place on board
        self.reset_board()
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = Marble.BLACK.value
        for pos in white_marbles_initial_pos:
            self.marble_positions[pos] = Marble.WHITE.value
        self.empty_positions -= set(black_marble_initial_pos + white_marbles_initial_pos)


    def set_german_daisy_board(self):
        """
        Places the German Daisy layout with Black on bottom daisies,
        White on top daisies, under the same row A=+4 -> row I=-4 orientation.
        """

        # -----------------------------
        # Black marbles (two arcs near the bottom-left and top-right)
        # -----------------------------
        black_marble_initial_pos = [

            # Top-right arc
            (-4, 3, 1), (-3, 3, 0),
            (-4, 2, 2), (-3, 2, 1), (-2, 2, 0),
            (-3, 1, 2), (-2, 1, 1),


            # Bottom-left arc
            (3, -3, 0), (4, -3, -1),
            (2, -2, 0), (3, -2, -1), (4, -2, -2),
            (2, -1, -1), (3, -1, -2)
        ]

        # -----------------------------
        # White marbles (two arcs near the top-left and bottom-right)
        # -----------------------------
        white_marbles_initial_pos = [
            # Bottom-right arc
            (1, 1, -2), (2, 1, -3),
            (0, 2, -2), (1, 2, -3), (2, 2, -4),
            (0, 3, -3), (1, 3, -4),

            # Top-left arc
            (-1, -3, 4), (0, -3, 3),
            (-2, -2, 4), (-1, -2, 3), (0, -2, 2),
            (-2, -1, 3), (-1, -1, 2)
        ]

        # Clear and place on board
        self.reset_board()
        for pos in black_marble_initial_pos:
            self.marble_positions[pos] = Marble.BLACK.value
        for pos in white_marbles_initial_pos:
            self.marble_positions[pos] = Marble.WHITE.value
        self.empty_positions -= set(black_marble_initial_pos + white_marbles_initial_pos)


    def place_marbles(self, coloured_marbles):
        """
        Places marbles on the board at specified positions with specified colours.

        :param coloured_marbles: List of tuples (q, r, s, colour) where q, r, s are coordinates and colour is 'b', 'w'
        """
        for (q, r, s, colour) in coloured_marbles:
            self.marble_positions[(q, r, s)] = colour
            self.empty_positions.discard((q, r, s))


    def get_input_board_representation(self, player: str, marble_moves: List[str]) -> Tuple[str, dict]:
        """
        Converts an input with a player move and marble moves to cube coordinates. Returns and sets the board positions.

        :param player: the letter of the player's turn
        :param marble_moves: a comma-separated list of marble notations (e.g., "C5b")
        :return: a converted .input move representation into cube coordinates and returns (player, marble_positions dictionary)
        """
        for notation in marble_moves:
            notation = notation.strip()
            if not notation:
                continue  # Skip empty tokens
            q, r, s, color = Board.convert_marble_notation(notation)
            # Only add if not already present.
            self.marble_positions[(q, r, s)] = color
            if (q, r, s) in self.empty_positions:
                self.empty_positions.remove((q, r, s))
        return (player, self.marble_positions)


    def to_string_board(self):
        """
        Converts the board's marble_positions (q,r,s -> 'b'/'w') into a
        comma-separated string like 'A1b,A2b,...'.
        Uses the row mapping: r=+4 -> 'A' down to r=-4 -> 'I',
        and the column mapping: q=-4 -> col=1 up to q=+4 -> col=9.
        """
        marble_list = []
        for (q, r, s), color in self.marble_positions.items():
            # Convert r to row letter: A=+4, B=+3, ... I=-4
            row_letter = chr(ord('A') + (4 - r))
            # Convert q to column (1..9)
            col_number = q + 5

            # Build something like "A2b" or "C3w"
            notation = f"{row_letter}{col_number}{color}"

            # Keep a tuple for sorting: (color, row_letter, col_number, "A2b")
            marble_list.append((color, row_letter, col_number, notation))

        # Sort by color first, then row letter, then column
        sorted_marbles = sorted(marble_list, key=lambda item: (item[0], item[1], item[2]))

        # Return just the comma-separated notation pieces
        return ",".join(item[3] for item in sorted_marbles)

    @staticmethod
    def convert_marble_notation(notation: str) -> Tuple[int, int, int, str]:
        """
        Converts a marble notation (e.g., "C5b") to cube coordinates (q, r, s, color).
        Convention: Row A = r=+4, B=+3, ... I=-4; Column 5 = q=0.
        s is computed as -q - r.
        """
        row_letter = notation[0]
        col_str = notation[1:-1]
        color = notation[-1]
        r = 4 - (ord(row_letter.upper()) - ord('A'))
        q = int(col_str) - 5
        s = -q - r
        return (q, r, s, color)

    @staticmethod
    def create_board(board_configuration: BoardConfiguration) -> 'Board':
        """
        Instantiates and returns a new board object setup with the given board configuration enum.

        :param board_configuration: the configuration of the board of which to return
        :return: the setup Board
        """
        board = Board()

        match board_configuration:
            case BoardConfiguration.DEFAULT:
                board.set_default_board()
            case BoardConfiguration.BELGIAN:
                board.set_belgian_daisy_board()
            case BoardConfiguration.GERMAN:
                board.set_german_daisy_board()

        return board

    def set_empty_positions(self):
        """
        Derives the empty board positions, setting it to the board objects state. 
        """
        keys = self.marble_positions.keys()
        empty_positions = {
                (q, r, s)
                for q in range(-4, 5)
                for r in range(-4, 5)
                for s in range(-4, 5)
                if q + r + s == 0 and (q, r, s) not in keys
            }
        self.empty_positions = empty_positions


    def update_board_from_str(self, board_str: str):
        """
        Given an input string in the format: `C5b,A2w,...`, parses every line, updating it's marble positions dictionary and empty positions
        """
        self.reset_board()
        for notation in board_str.split(","):
            q, r, s, colour = Board.convert_marble_notation(notation)
            self.marble_positions[(q, r, s)] = colour
        self.set_empty_positions()


    def print_board(self):
        """Prints the board configuration to stdout as a hexagonal board."""
        combined = [(pos, self.marble_positions.get(pos, '.')) for pos in (set(self.marble_positions.keys()) | self.empty_positions)]

        # Sort first by r (descending), then by q (ascending)
        sorted_combined = sorted(combined, key=lambda x: (x[0][1], x[0][0]))
        
        current_r = None
        row_values = []
        MAX_ROW_SIZE = 17
        row_str = ""

        """
             . . . # 3
        . . . . . . . # 7
        """
        for (_, r, _), val in sorted_combined:
            if r != current_r:
            # Print previous row before moving to the next one
                if row_values:
                    row_str = " ".join(row_values)
                    if len(row_str) < MAX_ROW_SIZE:
                        row_str = (MAX_ROW_SIZE - int(len(row_str)/2)) * " " + row_str
                        print(row_str)
                    else:
                        print(" " * 8, row_str)
        
                # Start new row
                row_values = []
                current_r = r

            row_values.append(str(val))  # Store values as strings for printing

        # Print the last row
        if row_values:
            row_str = " ".join(row_values)
            row_str = (MAX_ROW_SIZE - int(len(row_str)/2)) * " " + row_str
            print(row_str)

    def deep_copy(self) -> 'Board':
        """
        Creates and returns a deep copy of the current board.
        """
        new_board = Board()
        new_board.marble_positions = copy.deepcopy(self.marble_positions)
        new_board.empty_positions = copy.deepcopy(self.empty_positions)
        return new_board

    def copy(self):
        new_board = self.marble_positions.copy()
        return new_board

    
