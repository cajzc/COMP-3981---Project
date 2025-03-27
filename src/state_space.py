import re

from moves import Move, DIRECTIONS
from typing import List, Tuple
from board import Board
import copy
from enums import Marble


def generate_move(player: str, board: Board) -> List[Move]:
    """
    Generates all possible legal moves given the player whose turn it is an a board configuration.

    :param player: the player who has the current turn
    :param board: the board configuration as a Board object
    :return: a list of Move objects
    """
    return get_single_moves(player, board) + get_inline_moves(player, board) + get_side_step_moves(player, board)

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
    opponent = Marble.BLACK.value if player == Marble.WHITE.value else Marble.WHITE.value
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


def parse_move_str(move_str: str) -> Move:
    """
    Parses a move string and returns a Move object.

    Expected example:
      (1,-2,1,b)-(1,-1,0,b)-(1,0,-1,b)↘p(1,1,-2,w)

    The parser looks for the first direction symbol in the string, then splits
    the string into two parts. The left part contains the player's moved marbles;
    the right part (after a possible prefix "p", "s", or "i") contains destination info.

    For push moves (prefix "p"), the pushed marbles are extracted.

    Conversion: The coordinates are assumed to be given in cube form (q, r, s).
    """
    # Extract the direction symbol.
    direction = next((d for d in DIRECTIONS if d in move_str), None)
    if not direction:
        raise ValueError(f"Invalid move format: {move_str}")

    # Split the move string on the direction symbol.
    parts = move_str.split(direction)
    if len(parts) < 2:
        raise ValueError(f"Invalid move format; missing destination part: {move_str}")

    # Pattern to match a marble: (number,number,number,color)
    marble_pattern = r"\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*([bw])\)"

    # Extract the moved marbles.
    moved_matches = re.findall(marble_pattern, parts[0])
    if not moved_matches:
        raise ValueError(f"No moved marbles found in move string: {move_str}")
    moved = [(int(x), int(y), int(z), c) for x, y, z, c in moved_matches]

    # Process destination part.
    dest_part = parts[1]
    if dest_part.startswith("p"):
        move_type = "push"
        dest_part = dest_part[1:]
        pushed_matches = re.findall(marble_pattern, dest_part)
        if not pushed_matches:
            raise ValueError(f"No pushed marbles found in move string: {move_str}")
        pushed = [(int(x), int(y), int(z), c) for x, y, z, c in pushed_matches]
        return Move(
            player=moved[0][3],
            direction=direction,
            move_type=move_type,
            moved_marbles=moved,
            dest_positions=[],  # not used for push moves
            push=True,
            pushed_marbles=pushed,
            pushed_dest_positions=[]
        )
    elif dest_part.startswith("s"):
        move_type = "side_step"
        dest_part = dest_part[1:]
    elif dest_part.startswith("i"):
        move_type = "inline"
        dest_part = dest_part[1:]
    else:
        move_type = "single"

    dest_matches = re.findall(marble_pattern, dest_part)
    if not dest_matches:
        raise ValueError(f"No destination marbles found in move string: {move_str}")
    dest = [(int(x), int(y), int(z), moved[0][3]) for x, y, z, _ in dest_matches]

    return Move(
        player=moved[0][3],
        direction=direction,
        move_type=move_type,
        moved_marbles=moved,
        dest_positions=dest,
        push=False
    )


def apply_move_obj(board_obj: Board, move: Move) -> None:
    """
    Applies the given Move object to the Board object in place.

    For push moves:
      - For each pushed opponent marble, its original cell is removed from
        marble_positions and marked empty.
      - Then, each opponent marble is moved to its destination (if that cell is empty)
        and that destination cell is removed from empty_positions.

    For the player's marbles:
      - Their original positions are deleted and marked empty.
      - Then, they are placed at their destination positions (removing those cells from empty_positions).

    Finally, empty_positions is recomputed.
    """
    dq, dr, ds = DIRECTIONS[move.direction]

    if move.push:
        # Process pushed opponent marbles.
        # First, remove each opponent marble from its original position and mark that cell empty.
        for (oq, or_, os, opp_color) in reversed(move.pushed_marbles):
            if (oq, or_, os) in board_obj.marble_positions:
                del board_obj.marble_positions[(oq, or_, os)]
                board_obj.empty_positions.add((oq, or_, os))
        # Now update pushed opponent marbles to their destination positions.
        for (oq, or_, os, opp_color) in move.pushed_marbles:
            new_pos = (oq + dq, or_ + dr, os + ds)
            if new_pos in board_obj.empty_positions:
                board_obj.marble_positions[new_pos] = opp_color
                board_obj.empty_positions.remove(new_pos)
            else:
                # Marble pushed off the board; update score if needed.
                pass

    # Process player's marbles: first remove originals.
    for (q, r, s, col) in reversed(move.moved_marbles):
        if (q, r, s) in board_obj.marble_positions:
            del board_obj.marble_positions[(q, r, s)]
            board_obj.empty_positions.add((q, r, s))
    # Now update them to their destination positions.
    for (q, r, s, col) in move.moved_marbles:
        new_pos = (q + dq, r + dr, s + ds)
        board_obj.marble_positions[new_pos] = col
        if new_pos in board_obj.empty_positions:
            board_obj.empty_positions.remove(new_pos)

def apply_move(board_obj: Board, move_str: str) -> None:
    """
    Parses move_str into a Move object and applies it to the Board object.
    """
    move = parse_move_str(move_str)
    apply_move_obj(board_obj, move)

class GameState:
    """Represents the complete game state an Abalone game."""

    def __init__(self, player: str, board: Board):
        """
        Initialize a new game state.
        
        :param player: the colour of the current turns player
        :param board: A Board object representing the initial board configuration
        """
        self.player = player
        self.board = board
        self.score = self.get_score()

    def get_score(self):
        """
        Calculates the score for both players based on the number of opponent marbles pushed off the board.

        :return: Dictionary with scores {'b': int, 'w': int}
        """
        initial_black_marbles = 14  # Standard Abalone setup
        initial_white_marbles = 14

        board_dict_values = self.board.marble_positions.values()

        current_black_marbles = sum(1 for v in board_dict_values if v == Marble.BLACK.value)
        current_white_marbles = sum(1 for v in board_dict_values if v == Marble.WHITE.value)

        black_score = initial_white_marbles - current_white_marbles  # Black's score = White marbles pushed off
        white_score = initial_black_marbles - current_black_marbles  # White's score = Black marbles pushed off

        return {
            Marble.BLACK.value: black_score,
            Marble.WHITE.value: white_score
        }

    def terminal_test(self) -> bool:
        """
        Determines whether the terminal state has been reached: either player has won.

        :return: True if reached else False
        """
        return self.check_win() is not None

    def check_win(self):
        """
        Checks if either player has won the game by pushing 6 or more opponent marbles off the board.
        
        :return: 'b' if black wins, 'w' if white wins, None if no winner 
        """
        if self.score[Marble.BLACK.value] >= 6:
            return Marble.BLACK.value
        elif self.score[Marble.WHITE.value] >= 6:
            return Marble.WHITE.value
        return None

    def apply_move(self, move: Move | Tuple[int, int, int, str]):
        """
        Applies a move to the GameState, updating the board and player turn.

        :param move: the Move object to apply
        """
        if isinstance(move, Move):
            apply_move_obj(self.board, move)
        elif isinstance(move, Tuple):
            pass
        # Swap player turn
        self.player = self.get_next_turn_colour()

    def get_next_turn_colour(self) -> str:
        """
        Returns the next player to moves colour.

        :return: the next marble to move as a str "b" or "w"
        """
        return Marble.WHITE.value if self.player == Marble.BLACK.value else Marble.BLACK.value

    def deep_copy(self):
        """
        Creates and returns a deepcopy for a GameState.

        :return: a new GameState object
        """
        # Copy the original board
        new_board = self.board.deep_copy()
        
        # Create the new GameState object, with the next player turn as the current player to move
        new_game_state = GameState(self.get_next_turn_colour(), new_board)

        return new_game_state

    def __str__(self):
        return f"Game status: {"over" if self.terminal_test() else "in progress"}\n" \
                f"Score: {self.get_score()}"

