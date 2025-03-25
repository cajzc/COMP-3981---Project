""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_obj, generate_move
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
        best_move = None
        best_score = -math.inf

        # Iterative search
        for depth in range(1, self.depth + 1): # NOTE: Use time module: limit 5s or given
            # Visit every node (move)
            for move in moves:
                board = Board()
                apply_move_obj(board, move)
                # Create the resulting game state
                result_game_state = GameState(self.game_state.player, board)

                result_game_state = copy.deepcopy(self.game_state)
                score = self.mini_max(result_game_state, depth)
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move


    def mini_max(self, game_state: GameState, depth: int):
        """
        Minimax algorithm.

        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :return: the move for the player to take as str
        """
        # Assuming the player (not opponent) has the first move
        return self.max_value(game_state, depth) 


    def max_value(self, game_state: GameState, depth: int) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :return: the utility value of a given game state
        """
        if game_state.terminal_test() or depth == 0:
            return heuristic(game_state)

        v = -math.inf

        for move in generate_move(game_state.player, game_state.board):
            # Create the resulting board with the generated move
            board = Board()
            apply_move_obj(board, move)

            # Create the resulting game state
            result_game_state = GameState(game_state.player, board)
            
            v = max(v, self.min_value(result_game_state, depth-1))

        return v

    def min_value(self, game_state: GameState, depth: int) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :return: the utility value of a given game state
        """
        if game_state.terminal_test() or depth == 0:
            return heuristic(game_state)
        
        v = math.inf

        for move in generate_move(game_state.player, game_state.board):
            # Create the resulting board with the generated move
            board = Board()
            apply_move_obj(board, move)

            # Create the resulting game state
            result_game_state = GameState(game_state.player, board)

            v = min(v, self.max_value(result_game_state, depth-1))

        return v


