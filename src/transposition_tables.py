
import random
from typing import Dict, Tuple, Optional

class TranspositionEntry:
    """Represents an entry in the transposition table."""
    def __init__(self, value: float, depth: int, flag: str):
        self.value = value
        self.depth = depth
        self.flag = flag

class TranspositionTable:
    """A transposition table using Zobrist hashing for fast game state lookups."""
    
    def __init__(self):
        self.table: Dict[int, TranspositionEntry] = {}
        self.zobrist_table = self._initialize_zobrist()
    
    def _initialize_zobrist(self) -> Dict[Tuple[Tuple[int, int, int], str], int]:
        """Precomputes random 64-bit values for each (position, piece) combination."""
        positions = [(x, y, z) for x in range(3) for y in range(3) for z in range(3)]  # Adjust for your board size
        pieces = ['w', 'b', '']  # White, Black, Empty
        return {(pos, piece): random.getrandbits(64) for pos in positions for piece in pieces}

    def hash_game_state(self, player: str, board: Dict[Tuple[int, int, int], str]) -> int:
        """Computes Zobrist hash for the given board state and player."""
        hash_value = 0
        for pos, piece in board.items():
            if (pos, piece) not in self.zobrist_table:
                self.zobrist_table[(pos, piece)] = random.getrandbits(64)  # Assign dynamically
            hash_value ^= self.zobrist_table[(pos, piece)]
        hash_value ^= random.getrandbits(64) if player == 'w' else 0  # Differentiate players
        return hash_value
   
    def lookup(self, player: str, board: Dict[Tuple[int, int, int], str]) -> Optional[TranspositionEntry]:
        """Retrieves an entry from the transposition table if it exists."""
        return self.table.get(self.hash_game_state(player, board))

    def store(self, player: str, board: Dict[Tuple[int, int, int], str], value: float, depth: int, flag: str) -> None:
        """Stores an entry in the transposition table with depth-based replacement policy."""
        hash_key = self.hash_game_state(player, board)
        if hash_key not in self.table or depth >= self.table[hash_key].depth:
            self.table[hash_key] = TranspositionEntry(value, depth, flag)

    def clear(self) -> None:
        """Clears the transposition table."""
        self.table.clear()

