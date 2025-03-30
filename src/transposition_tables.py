import hashlib
from typing import Dict, Tuple, Optional
from state_space import GameState

class TranspositionEntry:
    """Represents an entry in the transposition table."""
    def __init__(self, value: float, depth: int, flag: str):
        """
        :param value: The heuristic value of the game state
        :param depth: The depth at which this value was calculated
        :param flag: 'exact', 'lower', or 'upper' to indicate the type of bound
        """
        self.value = value
        self.depth = depth
        self.flag = flag

class TranspositionTable:
    """A transposition table to cache game state evaluations for performance enhancement."""
    def __init__(self):
        self.table: Dict[int, TranspositionEntry] = {}

    def hash_game_state(self, player: str, board: Dict[Tuple[int, int, int], str]) -> int:
        """
        Improved faster hashing.
        """
        board_items = tuple(sorted(board.items()))
        state_tuple = (board_items, player)
        return hash(state_tuple)  # Built-in hash is efficient

    def lookup(self, player: str, board: Dict[Tuple[int, int, int], str]) -> Optional[TranspositionEntry]:
        """
        Retrieves an entry from the table if it exists.

        :param player: The player whose turn it is
        :param board: The current board state
        :return: TranspositionEntry if found, None otherwise
        """
        hash_key = self.hash_game_state(player, board)
        return self.table.get(hash_key)

    def store(self, player: str, board: Dict[Tuple[int, int, int], str], value: float, depth: int, flag: str) -> None:
        """
        Stores an entry in the transposition table.

        :param player: The player whose turn it is
        :param board: The current board state
        :param value: The heuristic value
        :param depth: The depth at which this value was calculated
        :param flag: 'exact', 'lower', or 'upper'
        """
        hash_key = self.hash_game_state(player, board)
        # Only overwrite if the new depth is greater or equal (more reliable evaluation)
        if hash_key not in self.table or depth >= self.table[hash_key].depth:
            self.table[hash_key] = TranspositionEntry(value, depth, flag)

    def clear(self) -> None:
        """Clears the transposition table."""
        self.table.clear()
