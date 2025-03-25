import math
from typing import Dict, Tuple, Set
from src.moves import DIRECTIONS
from state_space import GameState

def heuristic(game_state: GameState) -> float:
    return 0

"""1. distance to center """
def distance_to_center(board_obj, player: str) -> float:
    """
    Calculate the average Euclidean distance from the center (0,0,0) for the player's marbles.

    In cube coordinates, one common conversion to Euclidean distance is:
        distance = sqrt(q^2 + r^2 + s^2) / sqrt(2)
    """
    positions = [(q, r, s) for (q, r, s), color in board_obj.marble_positions.items() if color == player]
    if not positions:
        return 0.0
    distances = [math.sqrt(q * q + r * r + s * s) / math.sqrt(2) for (q, r, s) in positions]
    return sum(distances) / len(distances)

""" 2. coherence, marbles stick together """
def marbles_coherence(board_obj, player: str) -> float:
    """
    Measure the spatial clustering (coherence) of the player's marbles.

    We project cube coordinates (q, r, s) to axial coordinates (q, r)
    (since s = -q - r) and compute the average variance in q and r.
    Lower variance indicates tighter clustering.
    """
    positions = [(q, r) for (q, r, s), color in board_obj.marble_positions.items() if color == player]
    if not positions:
        return 0.0
    mean_q = sum(q for q, r in positions) / len(positions)
    mean_r = sum(r for q, r in positions) / len(positions)
    variance_q = sum((q - mean_q) ** 2 for q, r in positions) / len(positions)
    variance_r = sum((r - mean_r) ** 2 for q, r in positions) / len(positions)
    return (variance_q + variance_r) / 2


def marbles_in_danger(board_obj, player: str) -> int:
    """
    Count the number of the player's marbles that are in danger.

    A marble is considered in danger if:
      - It has at least 2 of its 6 neighbors occupied by opponent marbles, OR
      - It is on the edge of the board (i.e. any coordinate |q|, |r|, or |s| equals 4)
        and has at least 1 adjacent opponent marble.
    """
    danger_count = 0
    opponent = 'w' if player == 'b' else 'b'

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
