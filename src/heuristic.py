import math
from typing import List
import numpy as np
from typing import Dict, Tuple
from moves import DIRECTIONS
from state_space import GameState, get_score
from enums import Marble
from itertools import combinations


def heuristic(player_colour: str, board: Dict[Tuple[int, int, int], str], wdc: float, wmc: float, wsc: float) -> float:
    """
    Combined heuristic that computes:
    - Distance to center (lower is better)
    - Marble coherence (lower is better)
    - Score difference (higher is better)

    :param board: Dictionary of cube coordinates to marble colors.
    :param wdc: weight for distance to center
    :param wmc: weight for marble coherence
    :param wsc: weight for score difference
    :return: heuristic value
    """
    positions_b = [(q, r, s) for (q, r, s), color in board.items() if color == 'b']
    positions_w = [(q, r, s) for (q, r, s), color in board.items() if color == 'w']

    # Distance to center
    dist_b = [(abs(q) + abs(r) + abs(s)) / 2 for q, r, s in positions_b]
    dist_w = [(abs(q) + abs(r) + abs(s)) / 2 for q, r, s in positions_w]
    distance_to_center_val = sum(dist_w)/len(dist_w) - sum(dist_b)/len(dist_b)

    # Marble coherence for 'b' only
    mean_qb = sum(q for q, r, s in positions_b) / len(positions_b)
    mean_rb = sum(r for q, r, s in positions_b) / len(positions_b)
    mean_sb = -mean_qb - mean_rb
    distances_b = [max(abs(q - mean_qb), abs(r - mean_rb), abs(s - mean_sb)) for q, r, s in positions_b]
    coherence_val_b = sum(distances_b) / len(distances_b)

    # Marble coherence for 'b' only
    mean_qw = sum(q for q, r, s in positions_w) / len(positions_w)
    mean_rw = sum(r for q, r, s in positions_w) / len(positions_w)
    mean_sw = -mean_qw - mean_rw
    distances_w = [max(abs(q - mean_qw), abs(r - mean_rw), abs(s - mean_sw)) for q, r, s in positions_w]
    coherence_val_w = sum(distances_w) / len(distances_w)

    coherence_val = coherence_val_w - coherence_val_b


    # Score difference
    score_diff = len(positions_b) - len(positions_w)

    return (wdc * distance_to_center_val
            + wmc * coherence_val
            + wsc * score_diff)

# def heuristic(player_colour: str, board: Dict[Tuple[int, int, int], str], wdc: float, wmc: float, wsc: float) -> float:
#     """ add the score diff to the heuristic """
#     return (wdc*distance_to_center(player_colour, board)
#             + wmc*marbles_coherence(player_colour, board)
#             + wsc*score_difference(player_colour, board))

def c_heuristic(player_colour: str, board: Dict[Tuple[int, int, int], str], wdc: float, wmc: float, wt: float) -> float:
    """
    Implementation for a heuristic function that uses the following evaluation functions:
    - Distance to centre
    - Marble coherence
    - Distance to center
    """
    return wdc*distance_to_center(player_colour, board) + wmc*marbles_coherence(player_colour, board) + wt*triangle_formation(player_colour, board)

def b_heuristic(player_colour: str, board: Dict[Tuple[int, int, int], str], wdc: int, wmc: int, wes: int) -> float:
    """
    Implementation for a heuristic function that uses the following evaluation functions:
    - Distance to centre
    - Marble coherence
    - Edge safety

    :param game_state:
    :param wdc: weight for the distance to centre evaluation
    :param wmc: weight for the marble coherence evaluation
    :param wes: weight for the edge safety evaluation
    """
    return (wdc*distance_to_center(player_colour, board)
            + wmc*marbles_coherence(player_colour, board)
            + wes*marble_edge_safety(player_colour, board))

def yz_heuristic(player_colour: str, board: Dict[Tuple[int, int, int], str], wdc: float, wmc: float, wsc: float) -> (
        float):
    """ add the score diff to the heuristic """
    return (wdc*distance_to_center(player_colour, board)
            + wmc*marbles_coherence(player_colour, board)
            + wsc*score_difference(player_colour, board))

def score_difference(player_colour: str, board: Dict[Tuple[int, int, int], str]) -> int:
    """
    Returns the difference in score between the current player and the opponent.

    Positive values favor the current player, negative values favor the opponent.
    """
    opponent_colour = GameState.get_next_turn_colour(player_colour)
    score = get_score(board)
    return score[player_colour] - score[opponent_colour]

def distance_to_center(player_colour: str, board: Dict[Tuple[int, int, int], str]) -> float:
    """
    Calculate the average hex grid distance from the center (0,0,0) for the player's marbles.

    The hex grid distance for a position (q, r, s) from center is ( |q| + |r| + |s| ) / 2.
    """
    positions = [(q, r, s) for (q, r, s), color in board.items() if color ==
                 player_colour]
    distances = [(abs(q) + abs(r) + abs(s)) / 2 for q, r, s in positions]
    return sum(distances) / len(distances)

def hex_distance(p1,p2):
    """helper method to calculate the steps between two marbles"""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]))

def marbles_coherence(player_colour: str, board: Dict[Tuple[int, int, int], str]) -> float:
    """
    Measure the spatial clustering of the player's marbles by calculating the sum of variance in q and r coordinates plus their covariance.

    This provides a measure of how spread out the marbles are from their mean position.
    """
    positions = [(q, r, s) for (q, r, s), color
                 in board.items()
                 if color == player_colour]

    mean_q = sum(q for q, r, s in positions) / len(positions)
    mean_r = sum(r for q, r, s in positions) / len(positions)
    mean_s = -mean_q - mean_r

    mean_pos = (mean_q, mean_r, mean_s)
    distances = [hex_distance((q, r, s), mean_pos) for q, r, s in positions]

    return sum(distances) / len(distances)

def euclidean_distance(pos1: Tuple[int, int, int], pos2: Tuple[int, int, int]):
    """
    Determines the euclidean distance between points on a hexagonal grid. Each point is represented as a tuple.

    :param pos1: the first position
    :param pos2: the second position
    :return: the euclidean distance betwen the two points
    """
    return math.sqrt((pos2[0]-pos1[1]) ** 2 + (pos2[1] - pos1[1]) ** 2 + (pos2[2] - pos1[2]) ** 2)

def triangle_formation(player_colour: str, board: Dict[Tuple[int, int, int], str]):
    """
    A triangle formation is one where three or more marbles group up to form at the minimum, the three edges of a triangle.
    When marbles are in a triangle formation, it requires the opponent to make an additional few moves to push the player
    marbles off the map.

    Triangle definition:
    pos1, pos2, pos3. Each pos contains coordinates (q, r, s).
    q1 + 2 == (q2, q3)
    r3 - 2 == (r1, r2)
    s2 - 2 == (s1, s3)
    """
    max_score = 10.0
    min_score = 0.0

    positions = [(q, r, s) for (q, r, s), color in board.items() if color == player_colour]
    if not positions or len(positions) < 3:
        return 0.0

    scores = []

    # Lots of iterations
    for c in combinations(positions, 3):
        d1 = euclidean_distance(c[0], c[1])
        d2 = euclidean_distance(c[0], c[2])
        d3 = euclidean_distance(c[1], c[2])

        score = min(max_score, max_score - abs(d1-d2)+abs(d1-d3)+abs(d2-d3))
        score = max(min_score, score)
        scores.append(score)

    return sum(scores)/len(scores)


# test this one
def marbles_in_danger(board_obj, player: str) -> int:
    """
    Count the number of the player's marbles that are in danger.

    A marble is considered in danger if:
      - It has at least 2 of its 6 neighbors occupied by opponent marbles, OR
      - It is on the edge of the board (i.e. any coordinate |q|, |r|, or |s| equals 4)
        and has at least 1 adjacent opponent marble.
    """
    danger_count = 0
    opponent = Marble.WHITE.value if player == Marble.BLACK.value else Marble.BLACK.value

    for (q, r, s), color in board_obj.marble_positions.items():
        if color != player:
            continue

        # Count opponent neighbors.
        opponent_neighbors = 0
        for (dq, dr, ds) in DIRECTIONS.values():
            neighbor_pos = (q + dq, r + dr, s + ds)
            if board_obj.marble_positions.get(neighbor_pos) == opponent:
                opponent_neighbors += 1

        # Check if this marble is on the edge.
        on_edge = abs(q) == 4 or abs(r) == 4 or abs(s) == 4

        # Count as "in danger" if:
        # - It has 2 or more opponent neighbors, OR
        # - It is on the edge and has at least 1 opponent neighbor.
        if opponent_neighbors >= 2 or (on_edge and opponent_neighbors >= 1):
            danger_count += 1

    return danger_count


def marble_edge_safety(player: str, board: Dict[Tuple[int, int, int], str]) -> float:
    """
    Measure the safety of a player's marbles with respect to their position near the board's edges.

    A higher score indicates safer marbles (farther from edges or well-protected),
    while a lower score indicates vulnerability (near edges with opponent presence).

    Safety is calculated based on:
    - Distance from the edge (marbles farther from edges are safer)
    - Presence of friendly marbles nearby (support reduces vulnerability)
    - Presence of opponent marbles nearby (increases vulnerability)

    :param game_state: The current game state
    :return: A float representing the edge safety score (higher is safer)
    """
    opponent = Marble.WHITE.value if player == Marble.BLACK.value else Marble.BLACK.value
    total_safety_score = 0.0
    marble_count = 0

    # Maximum distance from center to edge is 4 in this grid
    max_edge_distance = 4.0

    for (q, r, s), color in board.items():
        if color != player:
            continue

        marble_count += 1
        # Calculate distance from edge
        edge_distance = min(max_edge_distance, abs(q), abs(r), abs(s))
        base_safety = edge_distance / max_edge_distance  # Normalized [0,1]

        # Count friendly and opponent neighbors
        friendly_neighbors = 0
        opponent_neighbors = 0
        for (dq, dr, ds) in DIRECTIONS.values():
            neighbor_pos = (q + dq, r + dr, s + ds)
            neighbor_color = board.get(neighbor_pos)
            if neighbor_color == player:
                friendly_neighbors += 1
            elif neighbor_color == opponent:
                opponent_neighbors += 1

        # Adjust safety based on neighbors
        # Each friendly neighbor increases safety, each opponent decreases it
        safety_modifier = (friendly_neighbors * 0.2) - (opponent_neighbors * 0.3)
        marble_safety = max(0.0, min(1.0, base_safety + safety_modifier))  # Clamp between 0 and 1
        total_safety_score += marble_safety

    # Return average safety score, or 0 if no marbles
    return total_safety_score / marble_count if marble_count > 0 else 0.0

"""
keep heuristic simple and get deeper search, and it overlaps with coherence
If the agent's search is deep enough, then break_opponent_formation() becomes partially redundant.

break_opponent_formation() can still be a useful shortcut or enhancer. You can:
Include it in low-depth or time-limited searches.
Leave it as an optional weighted term for testing.
"""
# def opponent_territory(board_obj, opponent: str) -> Set[Tuple[int, int]]:
#     """
#     Identify positions in the opponent's territory.
#
#     For this example, we convert cube coordinates to axial (q, r)
#     and define territory arbitrarily as positions where q > 0.
#     Adjust this rule according to your strategy.
#     """
#     opp_positions = [(q, r) for (q, r, s), color in board_obj.marble_positions.items() if color == opponent]
#     return {(q, r) for (q, r) in opp_positions if q > 0}
#
# def break_opponent_formation(board_obj, player: str) -> float:
#     """
#     Estimate the disruption to the opponent's formation caused by the player's moves.
#
#     This function calculates the opponent's coherence and then subtracts a disruption
#     factor based on how many of the player's marbles are present in the opponent's territory.
#     """
#     opponent = 'w' if player == 'b' else 'b'
#     opp_coherence = marbles_coherence(board_obj, opponent)
#     territory = opponent_territory(board_obj, opponent)
#     disruption = sum(1 for (q, r, s), color in board_obj.marble_positions.items()
#                      if color == player and (q, r) in territory)
#     return opp_coherence - disruption


# ---------------------------
# Basic Functions (Prefixed with t_)
# ---------------------------

def t_distance_to_center(game_state: GameState) -> float:
    """
    Evaluates the average distance of the player's marbles from the board's center.

    This function applies weighted distance calculations and provides a bonus for marbles closer to the center.

    :param game_state: The current state of the game
    :return: A heuristic score where lower values indicate a better position
    """
    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items()
                 if color == game_state.player]

    if not positions:
        return 0.0

    total_score = 0.0
    center_count = 0
    for q, r, s in positions:
        dist = (abs(q) + abs(r) + abs(s)) / 2  # Hexagonal distance
        weight = 1.0 / (1 + dist)  # Decay factor
        total_score += dist * weight

        # Bonus for marbles close to the center (Distance <= 2)
        if dist <= 2:
            center_count += 1

    avg_dist = total_score / len(positions)
    center_bonus = center_count * 0.5  # Each center-positioned marble gets a bonus

    return -avg_dist + center_bonus  # Negative because a smaller distance is better


def t_euclidean_distance(pos1: Tuple[int, int, int],
                         pos2: Tuple[int, int, int]) -> float:
    """
    Computes the Euclidean distance between two points in a hexagonal coordinate system.

    :param pos1: First position as a tuple (q, r, s)
    :param pos2: Second position as a tuple (q, r, s)
    :return: The Euclidean distance between the two positions
    """
    return math.sqrt(
        (pos2[0] - pos1[0]) ** 2 +
        (pos2[1] - pos1[1]) ** 2 +
        (pos2[2] - pos1[2]) ** 2
    )


def t_marbles_coherence(game_state: GameState) -> float:
    """
    Measures how closely grouped the player's marbles are using a covariance-based approach.

    This function calculates the trace of the covariance matrix, which represents overall dispersion,
    and the average nearest-neighbor distance, which represents local density.

    :param game_state: The current state of the game
    :return: A heuristic score where lower values indicate better cohesion
    """
    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items()
                 if color == game_state.player]

    if len(positions) < 2:
        return 0.0

    # Compute covariance matrix trace (measuring dispersion)
    pos_array = np.array(positions)
    cov_matrix = np.cov(pos_array, rowvar=False)
    trace = np.trace(cov_matrix)

    # Compute average nearest neighbor distance
    distances = []
    for i in range(len(positions)):
        min_dist = min(
            t_euclidean_distance(positions[i], positions[j])
            for j in range(len(positions)) if j != i
        )
        distances.append(min_dist)

    avg_nn_dist = np.mean(distances)

    return -trace - avg_nn_dist  # Lower values indicate better grouping


# ---------------------------
# Danger Detection (Prefixed with t_)
# ---------------------------

def t_marbles_in_danger(board_obj, player: str) -> int:
    """
    Identifies marbles that are in a vulnerable position (near an edge or surrounded by opponents).

    Args:
        board_obj: The current board state.
        player: The player whose marbles are being evaluated.

    Returns:
        The number of marbles in a dangerous position.
    """
    opponent = Marble.WHITE.value if player == Marble.BLACK.value else Marble.BLACK.value
    danger_count = 0

    edge_positions = {
        (q, r, s)
        for q in range(-4, 5)
        for r in range(-4, 5)
        for s in range(-4, 5)
        if q + r + s == 0 and (abs(q) == 4 or abs(r) == 4 or abs(s) == 4)
    }

    for (q, r, s), color in board_obj.marble_positions.items():
        if color != player:
            continue

        # Quick edge check
        on_edge = (q, r, s) in edge_positions

        # Count neighboring opponent marbles
        opponent_neighbors = 0
        for dq, dr, ds in DIRECTIONS.values():
            neighbor_pos = (q + dq, r + dr, s + ds)
            if board_obj.marble_positions.get(neighbor_pos) == opponent:
                opponent_neighbors += 1
                # Early termination: if danger condition is met
                if opponent_neighbors >= 2 or (on_edge and opponent_neighbors >= 1):
                    break

        # Check danger condition
        if opponent_neighbors >= 2 or (on_edge and opponent_neighbors >= 1):
            danger_count += 1

    return danger_count


# ---------------------------
# Formation Detection (Prefixed with t_)
# ---------------------------

def t_is_triangle(pos1: Tuple[int, int, int],
                  pos2: Tuple[int, int, int],
                  pos3: Tuple[int, int, int]) -> bool:
    """
    Checks if three marbles form an equilateral triangle in hexagonal space.
    Strict Equilateral Triangle Detection (Allows 10% Tolerance)

    :param pos1: First marble position
    :param pos2: Second marble position
    :param pos3: Third marble position
    :return: True if the three positions form an equilateral triangle, False otherwise
    """
    d1 = t_euclidean_distance(pos1, pos2)
    d2 = t_euclidean_distance(pos1, pos3)
    d3 = t_euclidean_distance(pos2, pos3)

    return (
            math.isclose(d1, d2, rel_tol=0.1) and
            math.isclose(d1, d3, rel_tol=0.1) and
            math.isclose(d2, d3, rel_tol=0.1)
    )


def t_detect_wedge(positions: List[Tuple[int, int, int]]) -> int:
    """
    Detects wedge formations, where three marbles are aligned in an arrow shape suitable for pushing.
    (Three Marbles in a Straight Line with Distance of 1)

    :param positions: List of marble positions
    :return: Number of wedge formations detected
    """
    wedge_count = 0
    direction_set = set(DIRECTIONS.values())
    for trio in combinations(positions, 3):
        sorted_trio = sorted(trio)
        delta1 = (
            sorted_trio[1][0] - sorted_trio[0][0],
            sorted_trio[1][1] - sorted_trio[0][1],
            sorted_trio[1][2] - sorted_trio[0][2]
        )
        delta2 = (
            sorted_trio[2][0] - sorted_trio[1][0],
            sorted_trio[2][1] - sorted_trio[1][1],
            sorted_trio[2][2] - sorted_trio[1][2]
        )
        if delta1 == delta2 and delta1 in direction_set:
            wedge_count += 1
    return wedge_count


def t_detect_chains(positions: List[Tuple[int, int, int]],
                    min_length=3) -> int:
    """
    Detects linear formations of marbles, where marbles are aligned in a straight line.
    (Linear Alignment of at Least min_length Marbles)

    :param positions: List of marble positions
    :param min_length: Minimum number of marbles required to form a chain
    :return: Number of chains detected
    """
    chain_count = 0
    visited = set()
    pos_set = set(positions)

    for pos in positions:
        if pos in visited:
            continue
        # Checking chain length in six directions
        for direction in DIRECTIONS.values():
            current = pos
            current_chain = []
            while current in pos_set:
                current_chain.append(current)
                current = (
                    current[0] + direction[0],
                    current[1] + direction[1],
                    current[2] + direction[2]
                )
            if len(current_chain) >= min_length:
                chain_count += 1
                visited.update(current_chain)
    return chain_count


# ---------------------------
# Combined Heuristic Function
# ---------------------------

def t_heuristic(
        game_state: GameState,
        w_center: float = 1.0,
        w_coherence: float = 0.8,
        w_triangle: float = 1.2,
        w_wedge: float = 1.5,
        w_chain: float = 0.7,
        w_danger: float = -1.3
) -> float:
    """
    Computes a comprehensive heuristic score based on multiple evaluation factors.

    Factors considered include:
    - Distance to the board center (negative weight, closer is better)
    - Marble cohesion (negative weight, more compact formations are better)
    - Triangle formations (positive weight, beneficial formations)
    - Wedge formations (positive weight, suitable for offensive moves)
    - Chain formations (positive weight, useful for defense and mobility)
    - Danger factor (negative weight, penalty for vulnerable marbles)

    :param game_state: Current state of the game
    :param w_center: Center Distance Weight (Negative, Smaller is Better)
    :param w_coherence: Cohesion Weight (Negative)
    :param w_triangle: Triangle Formation Bonus
    :param w_wedge: Wedge Formation Bonus
    :param w_chain: Chain Formation Defense Bonus
    :param w_danger: Danger Penalty
    :return: Heuristic evaluation score
    """
    # Compute Basic Metrics
    positions = [pos for pos, color in game_state.board.marble_positions.items()
                 if color == game_state.player]

    # Example of Dynamic Weight Adjustment (Can be Adjusted Based on Game Phase)
    # if game_state.score[game_state.player] >= 3: # Endgame Phase - Increase Danger Penalty
    #     w_danger *= 2

    return (
            w_center * t_distance_to_center(game_state) +
            w_coherence * t_marbles_coherence(game_state) +
            w_triangle * sum(1 for c in combinations(positions, 3) if t_is_triangle(*c)) +
            w_wedge * t_detect_wedge(positions) +
            w_chain * t_detect_chains(positions) +
            w_danger * t_marbles_in_danger(game_state.board, game_state.player)
    )
