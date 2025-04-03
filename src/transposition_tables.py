import random
from typing import Dict, Tuple, Optional

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
        self.zobrist_table = self._initialize_zobrist()
        self.player_hash = {'b': random.getrandbits(64), 'w': random.getrandbits(64)}

    def _initialize_zobrist(self) -> Dict[Tuple[Tuple[int, int, int], str], int]:
        """Precomputes random 64-bit values for each (position, piece) combination."""
        positions = [
            (q, r, s)
            for q in range(-4, 5)
            for r in range(-4, 5)
            for s in range(-4, 5)
            if q + r + s == 0
        ]
        pieces = ['w', 'b']
        return {(pos, piece): random.getrandbits(64) for pos in positions for piece in pieces}


    def hash_game_state(self, player: str, board: Dict[Tuple[int, int, int], str]) -> int:
        """Computes a Zobrist hash quickly and consistently."""
        hash_value = 0
        for pos, piece in board.items():
            hash_value ^= self.zobrist_table[(pos, piece)]
        hash_value ^= self.player_hash[player]  # Differentiates between players clearly
        return hash_value

    def lookup(self, player: str, board: Dict[Tuple[int, int, int], str]) -> Optional[TranspositionEntry]:
        """Retrieves an entry from the transposition table if it exists."""
        return self.table.get(self.hash_game_state(player, board))

    def store(self, player: str, board: Dict[Tuple[int, int, int], str], value: float, depth: int, flag: str) -> None:
        """Stores an entry using depth-based replacement policy."""
        hash_key = self.hash_game_state(player, board)
        if hash_key not in self.table or depth >= self.table[hash_key].depth:
            self.table[hash_key] = TranspositionEntry(value, depth, flag)

    def clear(self) -> None:
        """Clears the transposition table."""
        self.table.clear()
