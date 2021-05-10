"""all input validations goes here"""

from django.core.exceptions import ValidationError

import re

from tictactoe_project.settings import X_CHAR, O_CHAR, EMPTY_CHAR,\
    BOARD_LENGTH

DEFAULT_BOARD_VALUE = EMPTY_CHAR * BOARD_LENGTH


def validate_board_chars(value):
    """
    make sure board length is BOARD_LENGTH and contains only
    chars in [X_CHAR, O_CHAR, EMPTY_CHAR]
    """

    reg_to_match = fr'[{X_CHAR},{O_CHAR},{EMPTY_CHAR}]{ {BOARD_LENGTH} }$'
    reg = re.compile(reg_to_match)
    is_match = reg.match(value)
    if not is_match:
        error_msg = f"board must be of length {BOARD_LENGTH} and accepts only charecters in{[X_CHAR, O_CHAR, EMPTY_CHAR]}"
        raise ValidationError(error_msg)
    return value


def validate_new_move(old_board, new_board, current_player):
    """check if player played his correct role and made only one move"""
    moves_count = 0
    for x in range(BOARD_LENGTH):
        if old_board[x] == new_board[x]:
            # if both board cells are equal then
            # we dont need to check any thing, no changes there
            continue
        is_assigning_to_already_selected = old_board[x] != EMPTY_CHAR
        if is_assigning_to_already_selected:
            raise ValidationError(
                f"cannot change cell number {x+1}, it has been already selected!")
        played_other_role = new_board[x] != current_player
        if played_other_role:
            raise ValidationError(f"You must play using {current_player} sign")
        moves_count += 1
    if moves_count > 1:
        raise ValidationError("You can play only one move!")
