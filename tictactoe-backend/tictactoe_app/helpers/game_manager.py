from django.core.exceptions import ValidationError
from tictactoe_project.settings import EMPTY_CHAR, X_CHAR, O_CHAR,\
    X_WON, O_WON, DRAW, RUNNING


def convert_string_to_board_dict(board_string):
    board = {}
    for index, char in enumerate(board_string):
        board[index+1] = char
    return board


def insertChar(board, char, position):
    space_is_free = board[position] == EMPTY_CHAR
    if not space_is_free:
        raise ValidationError('cant insert in this cell!')
    board[position] = char


def checkWhichMarkWon(board, mark):
    """check if player with mark is winner"""
    if board[1] == board[2] and board[1] == board[3] and board[1] == mark:
        return True
    if (board[4] == board[5] and board[4] == board[6] and board[4] == mark):
        return True
    if (board[7] == board[8] and board[7] == board[9] and board[7] == mark):
        return True
    if (board[1] == board[4] and board[1] == board[7] and board[1] == mark):
        return True
    if (board[2] == board[5] and board[2] == board[8] and board[2] == mark):
        return True
    if (board[3] == board[6] and board[3] == board[9] and board[3] == mark):
        return True
    if (board[1] == board[5] and board[1] == board[9] and board[1] == mark):
        return True
    if (board[7] == board[5] and board[7] == board[3] and board[7] == mark):
        return True

    return False


def checkDraw(board):
    """check if game is draw"""
    for key in board.keys():
        if (board[key] == EMPTY_CHAR):
            return False
    return True


def get_game_status(board_string):
    """get game status based on the provided board"""
    board = convert_string_to_board_dict(board_string)
    is_x_won = checkWhichMarkWon(board, X_CHAR)
    if is_x_won:
        return X_WON

    is_o_won = checkWhichMarkWon(board, O_CHAR)
    if is_o_won:
        return O_WON

    if (checkDraw(board)):
        return DRAW
    return RUNNING


def minmax(board, player, depth, isMaximizing):
    """implement minmax algorithm on the board"""
    # get other player char
    difference = set([X_CHAR, O_CHAR])-set([player])
    other_player = list(difference)[0]
    if (checkWhichMarkWon(board, player)):
        return 1
    if (checkWhichMarkWon(board, other_player)):
        return -1
    if (checkDraw(board)):
        return 0

    if (isMaximizing):
        bestScore = -800
        for key in board.keys():
            if (board[key] == EMPTY_CHAR):
                board[key] = player
                score = minmax(board, player, depth + 1, False)
                board[key] = EMPTY_CHAR
                if (score > bestScore):
                    bestScore = score
        return bestScore

    else:
        bestScore = 800
        for key in board.keys():
            if (board[key] == EMPTY_CHAR):
                board[key] = other_player
                score = minmax(board, player, depth + 1, True)
                board[key] = EMPTY_CHAR
                if (score < bestScore):
                    bestScore = score
        return bestScore
