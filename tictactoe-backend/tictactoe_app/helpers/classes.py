from tictactoe_project.settings import EMPTY_CHAR
from .game_manager import insertChar, minmax, convert_string_to_board_dict


# Implement Strategy pattern for playing
class PlayAlgorithm():
    """
    Base interface for making a move in the tictactoe board
    """

    def make_move(self, board, *args, **kwargs):
        """
        Make a move in the board
        params: board: string representing the game board
        returns: string representing the board after move
        """
        raise NotImplementedError


class MinMaxAlgorithm(PlayAlgorithm):
    """
    use minmax algorithm to make the move
    """

    def make_move(self, board_string, player, *args, **kwargs):
        """
        Make a move in the board
        """
        board = convert_string_to_board_dict(board_string)
        bestScore = -800
        bestMove = 0
        for key in board.keys():
            if (board[key] == EMPTY_CHAR):
                board[key] = player
                score = minmax(board, player, 0, False)
                board[key] = EMPTY_CHAR
                if (score > bestScore):
                    bestScore = score
                    bestMove = key
        insertChar(board, player, bestMove)
        board_string = ''.join(board.values())
        return board_string


class MoveHandler():
    def __init__(self, play_algo):
        self.play_algo = play_algo

    def play(self, board_string, player):
        return self.play_algo.make_move(board_string, player)
