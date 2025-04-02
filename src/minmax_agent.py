""" this agent will use all the modules to generate a best move"""
from state_space import GameState, apply_move_dict, generate_move, terminal_test, generate_move_dict, check_win, game_status
from transposition_tables import TranspositionTable
from typing import Tuple, Dict, List
from moves import Move
import  math
import time
from enums import Marble
from board import Board
import random

# class AgentConfiguration:
#     """
#     Contains data attributes related to a game configuration.
#     """
#
#
#     def __init__(self,
#                  player_colour: Marble,
#                  board: Board,
#                  depth: int,
#                  time_limit: int,
#                  ai_same_heuristic: bool,
#                  ai_diff_heuristic: bool,
#                  ai_human: bool,
#                  ai_random: bool,
#                  h1,
#                  h1_weights,
#                  h2= None,
#                  h2_weights= None
#                  ):
#
#         """
#         A configuration for an abalone playing agent.
#
#         :param player_colour: The color of the player's marbles (BLACK or WHITE)
#         :param board: the game board instance
#         :param depth: maximum search depth for the minimax algorithm
#         :param time_limit: Maximum time in seconds allowed for move calculation
#         :param ai_same_heuristic: True if the model should run ai vs its own heuristic
#         :param ai_diff_heuristic: True if the model should run two different heuristics
#         :param ai_human: True if the model should run ai vs human (user input)
#         :param ai_random: True if the model should run ai vs random moves
#         :param h1: First heuristic function to use for evaluation
#         :param h1_weights: Weights for the first heuristic function
#         :param h2: Second heuristic function to use for evaluation (when using different heuristics)
#         :param h2_weights: Weights for the second heuristic function
#         """
#         self.player_colour = player_colour
#         self.board = board
#         self.depth = depth
#         self.time_limit = time_limit
#         self.ai_human = ai_human
#         self.ai_same_heuristic = ai_same_heuristic
#         self.ai_diff_heuristic = ai_diff_heuristic
#         self.ai_random = ai_random
#         self.h1 = h1
#         self.h2 = h2
#         self.h1_weights = h1_weights
#         self.h2_weights = h2_weights


# class MinimaxAgent:
#     """
#     Game-playing agent using Minimax algorithm with alpha-beta pruning
#     and configurable heuristic evaluation
#
#     Attributes:
#         depth (int): Search depth for minimax algorithm
#         weights (dict): Weight values for heuristic components
#         transposition_table (TranspositionTable): Cache for game state evaluations
#     """
#
#     def __init__(self,
#                  board: Board,
#                  player_colour: Marble,
#                  config: AgentConfiguration):
#         """
#         Initialize minimax agent with search parameters
#
#         :param board: the initial configuration of the Abalone game board
#         :param player_colour: the colour of the player as an enum
#         :param depth:  maximum search depth (default: 3)
#         :param weights: heuristic component weights as a dict
#         """
#         self.board = board
#         self.board_dict = board.marble_positions
#         self.player_colour = player_colour.value
#         self.time_limit = config.time_limit
#         self.depth = config.depth
#         self.game_state = GameState(self.player_colour, board)
#         self.current_move = True if self.player_colour == Marble.BLACK.value else False
#         self.opponent_colour = Marble.BLACK.value if self.player_colour == Marble.WHITE.value else Marble.WHITE.value
#         self.config = config
#         self.transposition_table = TranspositionTable()

        
    # def run_game(self):
    #     """
    #     Starts the game of Abalone with the model against an opponent.
    #     """
    #     self._display_agent_configuration()
    #     while not terminal_test(self.game_state.board.marble_positions):
    #         self.game_state.board.print_board() # Debug
    #         if self.current_move: # Player turn
    #             print("\nPlayer Turn\n")
    #
    #             s = time.time() # Debug
    #             # Get the next move
    #             move_to_make = self.iterative_deepening_search(
    #                 True,
    #                 self.config.h1,
    #                 self.config.h1_weights
    #             )
    #             e = time.time() # Debug
    #             print(f"Time to generate move of depth {self.depth}: ", e-s) # Debug
    #
    #             # Terminal state reached
    #             if move_to_make is None:
    #                 break
    #
    #             # Apply the move to the game state
    #             self.game_state.apply_move(move_to_make)
    #
    #         # Opponent turn
    #         else:
    #             print("\nOpponent Turn\n")
    #             if self.config.ai_random:
    #                 print("\nOpponent Turn\n")
    #                 applied_move = self.apply_opponent_move_random()
    #                 if not applied_move:
    #                     break
    #             else:
    #                 move_to_make = self.iterative_deepening_search(
    #                     False,
    #                     self.config.h2 if self.config.ai_diff_heuristic else self.config.h1,
    #                     self.config.h2_weights if self.config.ai_diff_heuristic else self.config.h1_weights,
    #                 )
    #                 if move_to_make:
    #                     self.game_state.apply_move(move_to_make)
    #
    #         self.current_move = not self.current_move # Alternate move
    #
    #         print(game_status(self.game_state.board.marble_positions)) # Debug
    #
    #     print("Game over")
    #     print(check_win(self.game_state.board.marble_positions), "won")

    # implement vs human

class AgentConfiguration:
    """
    Updated configuration that supports human play.
    The human chooses a colour (black or white) and the AI is set to play the opposite.
    """
    def __init__(self,
                 human_colour: Marble,
                 board: Board,
                 depth: int,
                 time_limit: int,
                 ai_human: bool,
                 ai_random: bool,
                 h1,
                 h1_weights,
                 h2=None,
                 h2_weights=None):
        self.human_colour = human_colour
        # AI plays the opposite side
        self.player_colour = Marble("w") if human_colour.value == "b" else Marble("b")
        self.board = board
        self.depth = depth
        self.time_limit = time_limit
        self.ai_human = ai_human
        self.ai_random = ai_random
        self.h1 = h1
        self.h1_weights = h1_weights
        self.h2 = h2
        self.h2_weights = h2_weights


class MinimaxAgent:
    def __init__(self, board: Board, config: AgentConfiguration):
        # AI's colour is stored in config.player_colour; human's in config.human_colour.
        self.board = board
        self.player_colour = config.player_colour.value
        self.config = config
        self.human_colour = config.human_colour.value
        # Initialize game state so that the starting turn is set appropriately.
        # Typically, black moves first.
        starting_player = "b"  # or use config.human_colour if you want human to start, adjust as needed
        self.game_state = GameState(starting_player, board)
        # Set current_move flag: if the current player is the AI's colour, then True.
        self.current_move = (starting_player == self.player_colour)

    def run_game(self):
        """
        Game loop that alternates turns. If the current player is the human's side, prompt for input;
        otherwise, compute the AI move.
        """
        print("Game started")
        while not terminal_test(self.game_state.board.marble_positions):
            self.game_state.board.print_board()
            current = self.game_state.player  # 'b' or 'w'
            if current == self.human_colour:
                print(f"\nYour Turn (you are playing as '{self.human_colour}')")
                human_move = self._get_opponent_move_input()
                self.game_state.apply_move(human_move)
            else:
                print(f"\nAI Turn (AI is playing as '{self.player_colour}')")
                best_move = self.iterative_deepening_search(True, self.config.h1, self.config.h1_weights)
                if best_move is None:
                    print("(ERROR) No move generated. Exiting.")
                    break
                move_str = str(best_move)
                print("AI Move:", move_str)
                self.game_state.apply_move(best_move)

            print(game_status(self.game_state.board.marble_positions))
        print("Game over")
        print(check_win(self.game_state.board.marble_positions), "won")


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

    def _get_opponent_move_input(self) -> Move:
        from state_space import parse_move_str
        while True:
            move_str = input("Enter your move string: ").strip()
            try:
                move = parse_move_str(move_str)
                return move
            except Exception as e:
                print("Invalid move format. Please try again. Error:", e)

    # def iterative_deepening_search(self, is_player: bool, heuristic, args) -> Move | None:
    #     self.transposition_table.clear()
    #     best_move = None
    #
    #     best_score = -math.inf
    #     for depth in range(1, self.depth + 1):
    #         current_best_move = None
    #
    #         # Generate moves for current depth
    #         moves = generate_move_dict(self.player_colour if is_player else self.opponent_colour, self.board.marble_positions)
    #
    #         # # 1) Separate pushes from non-pushes
    #         # push_moves = [mv for mv in moves if mv.push]
    #         # non_push_moves = [mv for mv in moves if not mv.push]
    #         #
    #         # # 2) Sort the non-push moves by your quick heuristic
    #         # non_push_moves_sorted = sorted(
    #         #     non_push_moves,
    #         #     key=lambda m: self.quick_heuristic_eval(
    #         #         m,
    #         #         self.player_colour if is_player else self.opponent_colour,
    #         #         heuristic,
    #         #         args
    #         #     ),
    #         #     reverse=True
    #         # )
    #         #
    #         # # 3) Keep the top 20 non-push moves
    #         # top_non_push = non_push_moves_sorted[:10]
    #         #
    #         # # 4) Combine them back. This ensures *all push moves* stay in the final list.
    #         # moves = push_moves + top_non_push
    #
    #         # moves = sorted(
    #         #     moves,
    #         #     key=lambda m: self.quick_heuristic_eval(
    #         #         m,
    #         #         self.player_colour if is_player else self.opponent_colour,
    #         #         heuristic,
    #         #         args
    #         #     ),
    #         #     reverse=True
    #         # )[:20]
    #
    #         for move in moves:
    #             new_board = self.board.copy()
    #             apply_move_dict(new_board, move)
    #
    #             score = self.mini_max(
    #                 not is_player,
    #                 new_board,
    #                 depth,
    #                 heuristic,
    #                 args,
    #             )
    #             if score > best_score:
    #                 best_score = score
    #                 current_best_move = move
    #
    #         if current_best_move is not None:
    #             best_move = current_best_move
    #         print(best_score,best_move)
    #     print("Best score:", best_score)
    #
    #     return best_move

    def iterative_deepening_search(self, is_player: bool, heuristic, args) -> Move | None:
        self.transposition_table.clear()
        best_move = None
        start_time = time.time()

        # Iterate from depth 1 up to self.depth
        for depth in range(1, self.depth + 1):
            current_best_move = None
            current_best_score = -math.inf
            inner_complete = True  # Flag to check if the entire depth was completed
            moves = generate_move_dict(
                self.player_colour if is_player else self.opponent_colour,
                self.board.marble_positions
            )

            for move in moves:
                # Check time before starting evaluation of each move.
                if time.time() - start_time >= self.time_limit:
                    inner_complete = False
                    break

                new_board = self.board.copy()
                apply_move_dict(new_board, move)
                score = self.mini_max(
                    not is_player,
                    new_board,
                    depth,
                    heuristic,
                    args,
                )
                if score > current_best_score:
                    current_best_score = score
                    current_best_move = move

            # If we did not complete the current depth iteration due to time, exit.
            if not inner_complete:
                break

            # Update best_move with the move found at this fully completed depth.
            best_move = current_best_move
            print(f"Depth {depth} score: {current_best_score}, move: {best_move}")

        print("Best move from deepest completed iteration:", best_move)
        return best_move

    def mini_max(self, is_player: bool, board: Dict[Tuple[int, int, int], str], depth: int, heuristic, args) -> float:
        """
        Minimax algorithm.

        :param is_player: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take 
        """
        if is_player:
            return self.max_value(
                self.player_colour,
                board,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                args,
        )
        else:
            return self.min_value(
                self.opponent_colour,
                board,
                depth,
                -math.inf,
                math.inf,
                heuristic,
                args 
        )


    def max_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            args
    ) -> float:
        """
        A minimax algorithm that determines the best move to take for the current player.

        :param player_colour: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param alpha: the alpha value of the caller
        :param beta: the beta value of the caller
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take for maximizing
        """
        entry = self.transposition_table.lookup(player_colour, board)
        if entry and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.value
            elif entry.flag == 'lower' and entry.value >= beta:
                return entry.value
            elif entry.flag == 'upper' and entry.value <= alpha:
                return entry.value

        if depth == 0 or terminal_test(board):
            value = heuristic(board, *args)
            self.transposition_table.store(player_colour, board, value, depth, 'exact')
            return value

        v = -math.inf
        moves_generated = generate_move_dict(player_colour, board)
        for move in moves_generated:
            # Create the resulting game state
            new_board = board.copy()
            apply_move_dict(new_board, move)

            v = max(v, self.min_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth-1,
                alpha,
                beta,
                heuristic,
                args
            ))

            if v >= beta:
                self.transposition_table.store(player_colour, board, v, depth, 'lower')
                return v
            alpha = max(alpha, v)

        flag = 'exact' if alpha < v < beta else 'upper' #important fixing from Yiming
        self.transposition_table.store(player_colour, board, v, depth, flag)
        return v

    def min_value(
            self,
            player_colour: str,
            board: Dict[Tuple[int, int, int], str],
            depth: int,
            alpha: float,
            beta: float,
            heuristic,
            args
        ) -> float:
        """
        A minimax algorithm that determines the best move to take for the opponent.

        :param player_colour: True if mini max should be ran for the player, False if it should be ran for the opponent
        :param board: the current board state as a dictionary
        :param depth: the depth to run the search
        :param alpha: the alpha value of the caller
        :param beta: the beta value of the caller
        :param heuristic: the heuristic function to use
        :param args: the weights
        :return: the move with the best score for the player to take for maximizing
        """
        entry = self.transposition_table.lookup(player_colour, board)
        if entry and entry.depth >= depth:
            if entry.flag == 'exact':
                return entry.value
            elif entry.flag == 'lower' and entry.value >= beta:
                return entry.value
            elif entry.flag == 'upper' and entry.value <= alpha:
                return entry.value

        if depth == 0 or terminal_test(board):
            value = heuristic(board, *args)
            self.transposition_table.store(player_colour, board, value, depth, 'exact')
            return value

        v = math.inf

        moves_generated = generate_move_dict(player_colour, board)

        for move in moves_generated:
            # Create the resulting game state
            new_board = board.copy()
            apply_move_dict(new_board, move)

            v = min(v, self.max_value(
                Marble.BLACK.value if player_colour == Marble.WHITE.value else Marble.WHITE.value,
                new_board,
                depth-1,
                alpha,
                beta,
                heuristic,
                args
                )
            )
            if v <= alpha:
                self.transposition_table.store(player_colour, board, v, depth, 'upper')
                return v
            beta = min(beta, v)

        flag = 'exact' if alpha < v < beta else 'lower'
        self.transposition_table.store(player_colour, board, v, depth, flag)

        return v

    def quick_heuristic_eval(self, move: Move, player_colour: str, heuristic, args):
        """
        Quickly evaluates a move using the heuristic without recursion.
        """
        temp_board = self.board.copy()
        apply_move_dict(temp_board, move)
        return heuristic(temp_board, *args)

    def _display_agent_configuration(self):
        """
        Displays the configuration of the agent, prompting a user to enter to begin the game.
        """
        print("\nCONFIGURATION")
        print("-------------")
        print("Depth: ", self.depth)
        print("Heuristic 1:", self.config.h1.__name__)
        print("Weights:", self.config.h1_weights)
        if self.config.h2:
            print("Heuristic 2:", self.config.h2.__name__)
            print("Weights:", self.config.h2_weights)
        print("-------------\n")
        input("Enter to begin")

