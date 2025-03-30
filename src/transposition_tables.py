import hashlib
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

    def hash_game_state(self, player: str, board: Dict[Tuple[int, int, int], str]) -> int:
        """
        Creates a hash of the game state based on board positions and current player.

        :param player: the colour of the player to make the current move
        :param board: the current board state
        :return: A unique integer hash value
        """
        # Convert board positions to a sorted string for consistency
        board_str = ",".join(
            f"{pos}:{color}" for pos, color in sorted(board.items())
        )
        # Include the current player to differentiate states
        state_str = f"{board_str}|{player}"
        # Use SHA-256 and take the first 8 bytes (64 bits) as an integer
        hash_obj = hashlib.sha256(state_str.encode('utf-8'))
        return int(hash_obj.hexdigest()[:16], 16)  # 64-bit hash (the hash_key)

    def lookup(self, player: str, board: Dict[Tuple[int, int, int], str]) -> Optional[TranspositionEntry]:
        """
        Retrieves an entry from the table if it exists.

        :param game_state: The game state to look up
        :return: TranspositionEntry if found, None otherwise
        """
        hash_key = self.hash_game_state(player, board)
        return self.table.get(hash_key)

    def store(self, player: str, board: Dict[Tuple[int, int, int], str], value: float, depth: int, flag: str) -> None:
        """
        Stores an entry in the transposition table.

        :param game_state: The game state to store
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
