from django.db import models

import uuid

from tictactoe_project.settings import EMPTY_CHAR, X_CHAR, O_CHAR,\
                                       X_WON, O_WON, RUNNING, DRAW,\
                                       BOARD_LENGTH
from .helpers import validation

DEFAULT_BOARD_VALUE = EMPTY_CHAR * BOARD_LENGTH


class Game(models.Model):
    class Status(models.TextChoices):
        RUNNING = RUNNING
        X_WON = X_WON
        O_WON = O_WON
        DRAW = DRAW
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.CharField(max_length=BOARD_LENGTH,
                             default=DEFAULT_BOARD_VALUE,
                             validators=[validation.validate_board_chars]
                             )
    status = models.CharField(max_length=10,
                              choices=Status.choices,
                              default=Status.RUNNING)


class GameInfo(models.Model):
    class PlayerChars(models.TextChoices):
        X_CHAR = X_CHAR
        O_CHAR = O_CHAR
    game = models.ForeignKey(Game, null=True, blank=True,
                             related_name='extra_info',
                             on_delete=models.SET_NULL
                             )
    current_player = models.CharField(max_length=10,
                                      choices=PlayerChars.choices,
                                      default=PlayerChars.O_CHAR
                                      )
    # player1 is by default refers to computer
    player1 = models.CharField(max_length=10,
                               choices=PlayerChars.choices,
                               default=PlayerChars.X_CHAR
                               )
    player2 = models.CharField(max_length=10,
                               choices=PlayerChars.choices,
                               default=PlayerChars.O_CHAR
                               )
