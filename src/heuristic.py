import math
from typing import Dict, Tuple, Set, List

import numpy as np

from moves import DIRECTIONS
from state_space import GameState
from enums import Marble
from itertools import combinations

def heuristic(game_state: GameState) -> float:
    return 0

def c_heuristic(game_state: GameState, wdc: int, wmc: int, wt: int) -> float:
    """
    Implementation for a heuristic function that uses the following evaluation functions:
    - Distance to centre
    - Marble coherence
    - Triangular formation

    :param wdc: weight for the distance to centre evaluation
    :param wmc: weight for the marble coherence evaluation
    :param wt: weight for the distance to triangle formation
    """
    return wdc*distance_to_center(game_state) + wmc*marbles_coherence(game_state) + wt*triangle_formation(game_state)

def b_heuristic(game_state: GameState, wdc: int, wmc: int, wes: int) -> float:
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
    return wdc*distance_to_center(game_state) + wmc*marbles_coherence(game_state) + wes*marble_edge_safety(game_state)

def distance_to_center(game_state: GameState) -> float:
    """
    Calculate the average hex grid distance from the center (0,0,0) for the player's marbles.

    The hex grid distance for a position (q, r, s) from center is ( |q| + |r| + |s| ) / 2.
    """
    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items() if color ==
                 game_state.player]
    distances = [(abs(q) + abs(r) + abs(s)) / 2 for q, r, s in positions]
    return sum(distances) / len(distances)

def hex_distance(p1,p2):
    """helper method to calculate the steps between two marbles"""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]), abs(p1[2] - p2[2]))

def marbles_coherence(game_state: GameState) -> float:
    """
    Measure the spatial clustering of the player's marbles by calculating the average hex distance
    from each marble to the mean marble position. A lower score indicates higher coherence.
    """
    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items() if color == game_state.player]
    if not positions:
        return 0.0

    mean_q = sum(q for q, r, s in positions) / len(positions)
    mean_r = sum(r for q, r, s in positions) / len(positions)
    mean_s = -mean_q - mean_r  # Ensure q + r + s = 0 in cube coordinates

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


def triangle_formation(game_state: GameState):
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

    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items() if color == game_state.player]
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


def marble_edge_safety(game_state: GameState) -> float:
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
    player = game_state.player
    opponent = Marble.WHITE.value if player == Marble.BLACK.value else Marble.BLACK.value
    total_safety_score = 0.0
    marble_count = 0

    # Maximum distance from center to edge is 4 in this grid
    max_edge_distance = 4.0

    for (q, r, s), color in game_state.board.marble_positions.items():
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
            neighbor_color = game_state.board.marble_positions.get(neighbor_pos)
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
