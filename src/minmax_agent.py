""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_obj, generate_move
from typing import List
from moves import Move
from board import Board
import time, copy, math
from heuristic import heuristic
from enums import Marble
from board import Board

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
        self.current_move = True if player_turn == Marble.BLACK.value else False

    def run_game(self):
        """
        Starts the game of Abalone with the model against an opponent.
        """
        # NOTE: We should be checking for time constraints
        while self.game_state.terminal_test():
            # Player turn
            if self.current_move:
                # Get the next move 
                move_to_make = self.iterative_deepening_search(generate_move(Marble.BLACK.value, self.game_state.board))
                if move_to_make is None:
                    print("(ERROR) Generated move is None")
                    return

                print("Generated move: ", move_to_make)

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)
            # Opponent turn
            else:
                opponent_move = input("Enter the opponent's move: ")
                # NOTE: Do some error handling here
                opponent_move = Board.convert_marble_notation(opponent_move)
                self.game_state.apply_move(opponent_move)

            # Alternate move
            self.current_move = not self.current_move
        
        # NOTE: We should be checking for time constraints
        print("Game over")
        print(self.game_state.check_win(), "won")
                

    def iterative_deepening_search(self, moves: List[Move]) -> Move | None:
        """
        Runs an iterative deepening search using the mini-max algorithm with a heuristic function to determine the best move to take
        for the agent, returning the best move for the agent to take.

        :return: the move for the agent to take as a Move object
        """
        best_move = None
        best_score = -math.inf

        # Iterative search
        for depth in range(1, self.depth + 1): # NOTE: Use time module: limit 5s or given
            # Visit every node (move)
            for move in moves:

                # Create the resulting game state
                board = Board()
                apply_move_obj(board, move)
                result_game_state = GameState(self.game_state.player, board)

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


