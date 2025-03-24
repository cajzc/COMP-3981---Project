from moves import Move, DIRECTIONS
from typing import List, Tuple


def get_marble_group(start_pos: Tuple[int, int, int], direction: str, board_obj, player: str) -> List[
    Tuple[int, int, int, str]]:
    """
    Starting from start_pos, collect a contiguous group of friendly marbles
    in the given direction. Returns a list of tuples (q, r, s, player).
    (It can return up to 3 marbles if available.)
    """
    group = [(start_pos[0], start_pos[1], start_pos[2], player)]
    dq, dr, ds = DIRECTIONS[direction]
    current = start_pos
    for _ in range(1, 3):
        current = (current[0] + dq, current[1] + dr, current[2] + ds)
        if current in board_obj.marble_positions and board_obj.marble_positions[current] == player:
            group.append((current[0], current[1], current[2], player))
        else:
            break
    return group


def get_moveable_groups(player: str, board_obj) -> List[Tuple[str, List[Tuple[int, int, int, str]]]]:
    """
    For each marble belonging to the player and for each direction,
    return one or more candidate groups of contiguous friendly marbles.

    If get_marble_group returns 3 marbles, then this function produces candidate
    groups for moving 2 marbles as well:
      - For a group of 2, the candidate group is [m1, m2].
      - For a group of 3, candidate groups are:
            full group: [m1, m2, m3],
            subgroup1: [m1, m2],
            subgroup2: [m2, m3].

    Only candidate groups of size >= 2 are returned.
    Duplicate groups are filtered out using a canonical representation.
    Returns a list of tuples: (direction, group)
    """
    groups = []
    seen = set()
    for pos, color in board_obj.marble_positions.items():
        if color != player:
            continue
        for direction in DIRECTIONS:
            full_group = get_marble_group(pos, direction, board_obj, player)
            if len(full_group) < 2:
                continue
            # Generate candidate groups.
            candidate_groups = []
            if len(full_group) == 2:
                candidate_groups.append(full_group)
            elif len(full_group) == 3:
                candidate_groups.append(full_group)  # Full group of 3
                candidate_groups.append(full_group[:2])  # First two
                candidate_groups.append(full_group[1:])  # Last two
            else:
                candidate_groups.append(full_group)
            for group in candidate_groups:
                # Create a canonical representation: (direction, sorted tuple of positions)
                canonical = (direction, tuple(sorted((q, r, s) for (q, r, s, _) in group)))
                if canonical not in seen:
                    seen.add(canonical)
                    groups.append((direction, group))
    return groups

def get_single_moves(player: str, board_obj) -> List[Move]:
    """
    Generates all valid single-marble moves for the given player,
    using board_obj.marble_positions for occupied cells and
    board_obj.empty_positions for empties.

    A move is valid if, for a marble at (q,r,s) belonging to player,
    one of the six neighbors (computed via DIRECTIONS) is in board_obj.empty_positions.
    """
    moves = []
    for (q, r, s), color in board_obj.marble_positions.items():
        if color != player:
            continue
        for dir_symbol, (dq, dr, ds) in DIRECTIONS.items():
            new_pos = (q + dq, r + dr, s + ds)
            if new_pos in board_obj.empty_positions:
                move_obj = Move(
                    player=player,
                    direction=dir_symbol,
                    moved_marbles=[(q, r, s, color)],
                    dest_positions=[(new_pos[0], new_pos[1], new_pos[2], color)]
                )
                moves.append(move_obj)
    return moves

def get_inline_moves(player: str, board_obj) -> List[Move]:
    """
    Generate all valid inline moves (including push moves) for 2–3 aligned marbles.
    For a given movable group, if the cell immediately ahead of the group is empty, it's an inline move.
    If it's occupied by an opponent, check if a push is possible.
    """
    moves = []
    opponent = 'b' if player == 'w' else 'w'
    groups = get_moveable_groups(player, board_obj)
    for direction, group in groups:
        dq, dr, ds = DIRECTIONS[direction]
        # Destination: one step ahead of the last marble in the group.
        last = group[-1]
        dest = (last[0] + dq, last[1] + dr, last[2] + ds)
        # CASE 1: Destination is empty.
        if dest in board_obj.empty_positions:
            dest_positions = [(m[0] + dq, m[1] + dr, m[2] + ds, player) for m in group]
            move_obj = Move(
                player=player,
                direction=direction,
                move_type="inline",
                moved_marbles=group,
                dest_positions=dest_positions,
                push=False
            )
            moves.append(move_obj)
        # CASE 2: Destination is occupied by an opponent => potential push.
        elif dest in board_obj.marble_positions and board_obj.marble_positions[dest] == opponent:
            opponent_positions = [dest]
            no_adjacent = True
            # Check further along the same direction for additional opponent marbles (max 2).
            for i in range(1, 3):
                next_dest = (dest[0] + dq * i, dest[1] + dr * i, dest[2] + ds * i)
                if next_dest in board_obj.marble_positions and board_obj.marble_positions[next_dest] == opponent:
                    opponent_positions.append(next_dest)
                elif next_dest in board_obj.marble_positions and board_obj.marble_positions[next_dest] == player:
                    no_adjacent = False
                    break
                else:
                    break
            if len(group) > len(opponent_positions) and len(opponent_positions) <= 2 and no_adjacent:
                dest_positions = [(m[0] + dq, m[1] + dr, m[2] + ds, player) for m in group]
                move_obj = Move(
                    player=player,
                    direction=direction,
                    move_type="push",
                    moved_marbles=group,
                    dest_positions=dest_positions,
                    push=True,
                    pushed_marbles=[(op[0], op[1], op[2], opponent) for op in opponent_positions]
                )
                moves.append(move_obj)
    return moves

def get_side_step_directions(inline_direction: str) -> List[str]:
    """
    Return candidate side-step directions (perpendicular to inline_direction).
    For simplicity, here we use a fixed mapping.
    """
    side_map = {
        '→':  ['↗', '↘'],
        '←':  ['↖', '↙'],
        '↗':  ['→', '↖'],
        '↖':  ['↗', '←'],
        '↘':  ['↙', '→'],
        '↙':  ['←', '↘']
    }
    return side_map.get(inline_direction, [])


def get_side_step_moves(player: str, board_obj) -> List[Move]:
    """
    Generate all valid side-step moves for groups of 2–3 aligned marbles.
    Uses helper functions get_moveable_groups and get_side_step_directions.
    For each moveable group (i.e. a contiguous group in an inline direction),
    try each candidate side-step direction; if all destination positions are empty,
    create a Move of move_type "side_step".
    """
    moves = []
    groups = get_moveable_groups(player, board_obj)

    for inline_direction, group in groups:
        # For side-step, try each candidate side-step direction that is perpendicular
        for side_direction in get_side_step_directions(inline_direction):
            dq, dr, ds = DIRECTIONS[side_direction]
            dest_positions = [
                (m[0] + dq, m[1] + dr, m[2] + ds, player)
                for m in group
            ]
            # Check that all destination positions are empty.
            if all((pos[0], pos[1], pos[2]) in board_obj.empty_positions for pos in dest_positions):
                move_obj = Move(
                    player=player,
                    direction=side_direction,
                    move_type="side_step",
                    moved_marbles=group,
                    dest_positions=dest_positions,
                    push=False
                )
                moves.append(move_obj)
    return moves

class GameState:
    """Represents the complete game state an Abalone game."""

    def __init__(self, player, board):
        """
        Initialize a new game state.
        
        :param player: First player to move ('b' for black or 'w' for white)
        :param board: Dictionary representing the board state {(x, y): 'b'/'w'/'N'}
        """
        self._player = player
        self._board = board
        self._score = self.get_score()

    def get_score(self):
        """
        Calculates the score for both players based on the number of opponent marbles pushed off the board.

        :return: Dictionary with scores {'b': int, 'w': int}
        """
        initial_black_marbles = 14  # Standard Abalone setup
        initial_white_marbles = 14

        current_black_marbles = sum(1 for v in self._board.values() if v == 'b')
        current_white_marbles = sum(1 for v in self._board.values() if v == 'w')

        black_score = initial_white_marbles - current_white_marbles  # Black's score = White marbles pushed off
        white_score = initial_black_marbles - current_black_marbles  # White's score = Black marbles pushed off

        return {
            'b': black_score,
            'w': white_score}

    def check_victory(self):
        """
        Checks if either player has won the game by pushing 6 or more opponent marbles off the board.
        
        :return: 'b' if black wins, 'w' if white wins, None if no winner 
        """
        if self._score['b'] >= 6:
            print("Black wins!")
            return 'b'
        elif self._score['w'] >= 6:
            print("White wins!")
            return 'w'
        return None
