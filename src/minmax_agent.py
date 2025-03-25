""" this agent will use all the modules to generate a best move"""
from state_space import GameState, generate_move
from typing import List
from moves import Move
from board import Board
import time
import copy
from heuristic import heuristic
import math

class MinimaxAgent:
    """
    Game-playing agent using Minimax algorithm with alpha-beta pruning
    and configurable heuristic evaluation

    Attributes:
        depth (int): Search depth for minimax algorithm
        weights (dict): Weight values for heuristic components
    """

    def __init__(self, board: Board, player_turn: str, time_limit=5, depth=3, weights=None):
        """
        Initialize minimax agent with search parameters

        Args:
            board (Board): The initial configuration of the Abalone game board
            player_turn (str): The player whose initial turn it is
            depth (int): Maximum search depth (default: 3)
            weights (dict): Heuristic component weights (default: predefined values)
        """
        self.depth = depth
        self.weights = weights or {
            'center_distance': -0.5,  # Negative weight (closer to center = better)
            'coherence': -0.3,  # Negative weight (lower variance = better)
            'danger': -1.0,  # Penalty for endangered marbles
            'opponent_break': 0.8,  # Reward for disrupting opponent
            'score': 2.0  # Direct score difference multiplier
        }
        self.game_state = GameState(player_turn, board)
        self.time_limit = time_limit
        self.board = board

    def iterative_deepening_search(self, current_player: str, moves: List[Move]):
        # NOTE: Use time module: limit 5s or given
        best_move = None
        best_score = 0

        # Iterative search
        for iter in range(1, self.depth + 1):
            # Visit every node (move)
            for move in moves:
                new_game_state = copy.deepcopy(self.game_state)
                self.mini_max(new_game_state)


    def mini_max(self, game_state: GameState):
        """
        Minimax algorithm.

        :param game_state: the game state to run the algorithm on
        :return: the move for the player to take as str
        """
        return self.max_value(game_state) 


    def max_value(self, game_state: GameState) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.
        
        :param game_state: the game state to run the algorithm on
        :return: the utility value of a given game state
        """
        if game_state.terminal_test() or self.depth == 0:
            return heuristic(game_state)

        v = -math.inf

        for move in generate_move(game_state.player, game_state.board):
            v = max(v, self.min_value(game_state))

        return v

    def min_value(self, game_state: GameState) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.
        
        :param game_state: the game state to run the algorithm on
        :return: the utility value of a given game state
        """
        if game_state.terminal_test() or self.depth == 0:
            return heuristic(game_state)
        
        v = math.inf

        for move in generate_move(game_state.player, game_state.board):
            v = min(v, self.max_value(game_state))

        return v


