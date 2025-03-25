import math
from typing import Dict, Tuple, Set
from src.moves import DIRECTIONS
from state_space import GameState
from enums import Marble
from itertools import combinations

def heuristic(game_state: GameState) -> float:
    return 0

def c_heuristic(game_state: GameState, wdc: int, wmc: int, wt: int) -> float:
    """
    Implemtation for a heuristic function that uses the following evaluation functions:
    - Distance to centre
    - Marble coherence
    - Triangular formation

    :param wdc: weight for the distance to centre evaluation
    :param wmc: weight for the marble coherence evaluation
    :param wt: weight for the distance to triangle formation
    """
    return wdc*distance_to_center(game_state) + wmc*marbles_coherence(game_state) + wt*triangle_formation(game_state)

"""1. distance to center """
def distance_to_center(game_state: GameState) -> float:
    """
    Calculate the average Euclidean distance from the center (0,0,0) for the player's marbles.

    In cube coordinates, one common conversion to Euclidean distance is:
        distance = sqrt(q^2 + r^2 + s^2) / sqrt(2)
    """
    positions = [(q, r, s) for (q, r, s), color in game_state.board.marble_positions.items() if color == game_state.player]
    if not positions:
        return 0.0
    distances = [math.sqrt(q * q + r * r + s * s) / math.sqrt(2) for (q, r, s) in positions]
    return sum(distances) / len(distances)

""" 2. coherence, marbles stick together """
def marbles_coherence(game_state: GameState) -> float:
    """
    Measure the spatial clustering (coherence) of the player's marbles.

    We project cube coordinates (q, r, s) to axial coordinates (q, r)
    (since s = -q - r) and compute the average variance in q and r.
    Lower variance indicates tighter clustering.
    """
    positions = [(q, r) for (q, r, s), color in game_state.board.marble_positions.items() if color == game_state.player]
    if not positions:
        return 0.0
    mean_q = sum(q for q, r in positions) / len(positions)
    mean_r = sum(r for q, r in positions) / len(positions)
    variance_q = sum((q - mean_q) ** 2 for q, r in positions) / len(positions)
    variance_r = sum((r - mean_r) ** 2 for q, r in positions) / len(positions)
    return (variance_q + variance_r) / 2


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

"""keep heuristic simple and get deeper search"""
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
