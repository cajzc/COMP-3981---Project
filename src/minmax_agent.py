""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_obj, generate_move
from typing import List, Tuple
from moves import Move
from board import Board
import  math
import time 
from heuristic import heuristic, c_heuristic
from enums import Marble
from board import Board
import random

class AgentConfiguration:
    """
    Contains data attributes related to a game configuration.
    """


    def __init__(self, ai_player: bool, ai_same_heuristic: bool, ai_diff_heuristic: bool, ai_random: bool, heuristic_one = None, heuristic_two = None):
        """
        A configuration for an abalone playing agent.

        :param ai_player: True if the model should run ai vs player (user input)
        :param ai_same_heuristic: True if the model should run ai vs its own heuristic
        :param ai_diff_heuristic: True if the model should run two different heuristics
        :param ai_random: True if the model should run ai vs random moves
        """
        self.ai_player = ai_player
        self.ai_same_heuristic = ai_same_heuristic
        self.ai_diff_heuristic = ai_diff_heuristic
        self.ai_random = ai_random
        self.heuristic_one = heuristic_one
        self.heuristic_two = heuristic_two


class MinimaxAgent:
    """
    Game-playing agent using Minimax algorithm with alpha-beta pruning
    and configurable heuristic evaluation

    Attributes:
        depth (int): Search depth for minimax algorithm
        weights (dict): Weight values for heuristic components
    """

    def __init__(self, board: Board, player_colour: Marble, config: AgentConfiguration, time_limit=5, depth=3, weights=None):
        """
        Initialize minimax agent with search parameters

        :param board: the initial configuration of the Abalone game board
        :param player_colour: the colour of the player as an enum
        :param depth:  maximum search depth (default: 3)
        :param weights: heuristic component weights as a dict 
        """
        self.board = board
        self.player_colour = player_colour.value
        self.time_limit = time_limit
        self.depth = depth
        self.weights = weights or {
            'center_distance': -0.5,  # Negative weight (closer to center = better)
            'coherence': -0.3,  # Negative weight (lower variance = better)
            'danger': -1.0,  # Penalty for endangered marbles
            'opponent_break': 0.8,  # Reward for disrupting opponent
            'score': 2.0,  # Direct score difference multiplier
            'triangle_formation': 1.0  # Multiplier for obtaining a triangle formation
        }
        self.game_state = GameState(self.player_colour, board)
        self.current_move = True if self.player_colour == Marble.BLACK.value else False
        self.opponent_colour = Marble.BLACK.value if self.player_colour == Marble.WHITE.value else Marble.WHITE.value
        self.config = config


    def run_game(self):
        """
        AI vs random
        Starts the game of Abalone with the model against an opponent.
        """
        # NOTE: We should be checking for time constraints
        while not self.game_state.terminal_test():
            if self.current_move: # Player turn
                print("\nPlayer Turn\n")

                s = time.time() # Debug
                # Get the next move 
                move_to_make = self.iterative_deepening_search(
                    True, 
                    generate_move(self.player_colour, self.game_state.board),
                    self.config.heuristic_one,
                )
                e = time.time() # Debug
                print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug

                # Terminal state reached
                if move_to_make is None:
                    break

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)

            # Opponent turn
            else:
                print("\nOpponent Turn\n")
                applied_move = self.apply_opponent_move_random()
                if not applied_move:
                    break

            print(self.game_state.board.marble_positions) # Debug

            self.current_move = not self.current_move # Alternate move

            print(self.game_state) # Debug
        
        print("Game over")
        print(self.game_state.check_win(), "won")


    def run_game_against_self(self):
        """
        AI vs AI
        Starts the game of Abalone with the model against an opponent.
        """
        # NOTE: We should be checking for time constraints
        while not self.game_state.terminal_test():
            if self.current_move: # Player turn
                print("\nPlayer Turn\n")

                s = time.time() # Debug
                # Get the next move 
                move_to_make = self.iterative_deepening_search(
                    True, 
                    generate_move(self.player_colour, self.game_state.board),
                    self.config.heuristic_one,
                )
                e = time.time() # Debug
                print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug

                # Terminal state reached
                if move_to_make is None:
                    break

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)

            # Opponent turn
            else:
                print("\nOpponent Turn\n")
                move_to_make = self.iterative_deepening_search(
                    False, 
                    generate_move(self.opponent_colour, self.game_state.board),
                    self.config.heuristic_one,
                )

                # Terminal state reached
                if move_to_make is None:
                    break


            print(self.game_state.board.marble_positions) # Debug

            self.current_move = not self.current_move # Alternate move

            print(self.game_state) # Debug
        
        print("Game over")
        print(self.game_state.check_win(), "won")


    def run_game_two_heuristics(self, h1, h2):
        """
        AI vs AI with different heuristics.
        Starts the game of Abalone with the model against an opponent.
        """
        # NOTE: We should be checking for time constraints
        while not self.game_state.terminal_test():
            if self.current_move: # Player turn
                print("\nPlayer Turn\n")

                s = time.time() # Debug
                # Get the next move 
                move_to_make = self.iterative_deepening_search(
                    True, 
                    generate_move(self.player_colour, self.game_state.board),
                    self.config.heuristic_one
                )
                e = time.time() # Debug
                print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug

                # Terminal state reached
                if move_to_make is None:
                    break

                # Apply the move to the game state
                self.game_state.apply_move(move_to_make)

            # Opponent turn
            else:
                print("\nOpponent Turn\n")
                move_to_make = self.iterative_deepening_search(
                    False, 
                    generate_move(self.opponent_colour, self.game_state.board),
                    self.config.heuristic_two
                )

                # Terminal state reached
                if move_to_make is None:
                    break


            print(self.game_state.board.marble_positions) # Debug

            self.current_move = not self.current_move # Alternate move

            print(self.game_state) # Debug
        
        print("Game over")
        print(self.game_state.check_win(), "won")


                
    
    def apply_opponent_move_random(self) -> bool:
        """
        Applies a randomly generated opponent move to the game state.

        :return: True if the move was applied, False if not and the game is over
        """
        move = self._get_opponent_move_random()
        if not move:
            return False
        self.game_state.apply_move(move)
        return True

    def apply_opponent_move_input(self):
        """Applies the move to the game state. This assumes the opponents move is a valid one."""
        move = self._get_opponent_move_input()
        self.game_state.apply_move(move)
    
    def _get_opponent_move_random(self) -> Move | None:
        """
        Generates all possible moves for the opponent, returning a randomly selected one.

        :return: a randomly selected move for the opponent or None if there are no generated moves
        """
        possible_opponent_moves = generate_move(self.opponent_colour, self.game_state.board)
        if len(possible_opponent_moves) == 0:
            return None
        r = random.randint(0, len(possible_opponent_moves) - 1)
        opponent_move = possible_opponent_moves[r]
        return opponent_move


    # FIXME: This should return a Move object
    def _get_opponent_move_input(self) -> Tuple[int, int, int, str]:
        """
        Gets the opponents move from user input. Handles errors appropriately, reprompting the opponent. 

        :return: the user inputted move as a tuple in notation (q, r, s, colour)
        """
        while True:
            opponent_move = input("Enter the opponent move position: ")
            try:
                opponent_move = f"{opponent_move}{self.opponent_colour}"
                opponent_move = Board.convert_marble_notation(opponent_move)
                # Convert the tuple into a Move object
            except ValueError:
                print("Invalid move entered")
            except Exception as e:
                print("Unknown error parsing opponent move:", e)
            else:
                return opponent_move


    def iterative_deepening_search(self, is_player: bool, moves: List[Move], heuristic) -> Move | None:
        """
        Runs an iterative deepening search using the mini-max algorithm with a heuristic function to determine the best move to take
        for the agent, returning the best move for the agent to take.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param moves: a List of the moves to run iterative deepening and mini max on
        :return: the move for the agent to take as a Move object
        """
        best_move = None
        best_score = -math.inf
        
        # Iterative search
        for depth in range(1, self.depth + 1): 
            # Visit every node (move)
            for move in moves:
                # Create the resulting game state
                result_game_state = self.game_state.deep_copy()
                apply_move_obj(result_game_state.board, move)

                score = self.mini_max(
                    is_player,
                    result_game_state, 
                    depth, 
                    heuristic,
                    self.weights["center_distance"], 
                    self.weights["coherence"], 
                    self.weights["triangle_formation"]
                )
                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move


    def mini_max(self, is_player: bool, game_state: GameState, depth: int, heuristic, *args) -> float:
        """
        Minimax algorithm.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the move for the player to take as str
        """
        if is_player:
            return self.max_value(
                game_state,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                *args
        )
        else:
            return self.min_value(
                game_state,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                *args
        )

        # return (
        #     self.max_value(
        #         game_state=game_state, 
        #         depth=depth, 
        #         alpha=-math.inf,
        #         beta=math.inf,
        #         heuristic=heuristic, 
        #         *args
        # )   if is_player else self.min_value(
        #         game_state=game_state, 
        #         depth=depth, 
        #         alpha=-math.inf,
        #         beta=math.inf,
        #         heuristic=heuristic, 
        #         *args
        #     )
        # )


    def max_value(self, game_state: GameState, depth: int, alpha: float, beta: float, heuristic, *args) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the utility value of a given game state
        """
        if depth == 0 or game_state.terminal_test():
            return heuristic(game_state, *args)

        v = -math.inf
        moves_generated = generate_move(game_state.player, game_state.board)
        for move in moves_generated:

            # Create the game state if we were to make the move
            result_game_state = game_state.deep_copy()
            apply_move_obj(result_game_state.board, move)

            v = max(v, self.min_value(result_game_state, depth-1, alpha, beta, heuristic, *args))
            if v > beta:
                return v
            alpha = max(alpha, v)

        return v


    def min_value(self, game_state: GameState, depth: int, alpha: float, beta: float, heuristic, *args) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.
        
        :param game_state: the game state to run the algorithm on
        :param depth: the depth to run the search
        :param args: the weights
        :return: the utility value of a given game state
        """
        if depth == 0 or game_state.terminal_test():
            return heuristic(game_state, *args)
        
        v = math.inf

        moves_generated = generate_move(game_state.player, game_state.board)
        #print("number moves generated in min", len(moves_generated))

        for move in moves_generated:
            # Create the game state if we were to make the move
            result_game_state = game_state.deep_copy()
            apply_move_obj(result_game_state.board, move)

            
            v = min(v, self.max_value(result_game_state, depth-1, alpha, beta, heuristic, *args))
            if v < alpha:
                return v
            beta = min(beta, v)


        return v


