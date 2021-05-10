from rest_framework import serializers
from django.core.exceptions import ValidationError

from tictactoe_project.settings import X_CHAR, O_CHAR, EMPTY_CHAR,\
    RUNNING
from .helpers import validation
from .helpers.classes import MinMaxAlgorithm, MoveHandler
from .helpers.game_manager import get_game_status
from .models import Game, GameInfo


class GameSerializer(serializers.HyperlinkedModelSerializer):
    location = serializers.HyperlinkedIdentityField(view_name="game-detail")

    class Meta:
        model = Game
        read_only_fields = ['status']
        fields = ['id', 'board', 'status', 'location']

    def create(self, validated_data):
        # when saving the game for the first time we check if the user
        # has made a move or not, otherwise let the computer play

        # initialize default info about the game
        info = {
            "player1": X_CHAR,
            "player2": O_CHAR,
            "current_player": X_CHAR
        }
        board_without_empty = validated_data['board'].replace(EMPTY_CHAR, '')
        moves_count = len(board_without_empty)
        if moves_count > 1:
            # if number of moves in the board is bigger than 1,
            # it means the user inserted more than one move
            raise ValidationError("Player can only play one move at once!")
        if moves_count == 1:
            # if number of moves in the board equals 1,
            # it means the user has made his first move

            # get the sign choosen by user (player2 always represents end user)
            info['player2'] = board_without_empty[0]
            # assign the other sign to the computer
            remaining_sign = list(
                set([X_CHAR, O_CHAR])-set(board_without_empty))
            info['player1'] = remaining_sign[0]
        if moves_count == 0:
            # if number of moves in the board equals 0,
            # it means the user did not make any move
            # so computer will play

            # assing computer any sign let it be X_CHAR
            info['player1'] = X_CHAR
            # assing end user the other sign, which is O_CHAR
            info['player2'] = O_CHAR
        # computer will play now
        min_max = MinMaxAlgorithm()
        move_handler = MoveHandler(min_max)
        new_board = move_handler.play(validated_data['board'],
                                      player=info['player1']
                                      )
        validated_data['board'] = new_board
        # end user will be playing next
        info['current_player'] = info['player2']
        validated_data["status"] = get_game_status(new_board)
        new_game = Game.objects.create(**validated_data)
        GameInfo.objects.create(game=new_game, **info)
        return new_game

    def update(self, game_instance, validated_data):
        game_info = GameInfo.objects.filter(game_id=game_instance.id).first()
        new_board = validated_data['board']
        if game_instance.status != RUNNING:
            raise ValidationError(
                "Cannot update a game which is already finished!")
        validation.validate_new_move(old_board=game_instance.board,
                                     new_board=validated_data['board'],
                                     current_player=game_info.current_player
                                     )
        # before computer play check if end user made a
        # move where he win or draw
        game_status = get_game_status(new_board)
        if game_status == RUNNING:
            # game still in running status which means computer can play
            min_max = MinMaxAlgorithm()
            move_handler = MoveHandler(min_max)
            new_board = move_handler.play(validated_data['board'],
                                          player=game_info.player1
                                          )
            # end user will be playing next
            game_info.current_player = game_info.player2
        game_instance.board = new_board
        game_instance.status = get_game_status(new_board)
        game_info.save()
        game_instance.save()
        return game_instance

    def to_representation(self, obj):
        """
        override the original representation to
        follow the schema defined response body
        """
        try:
            # get the original representation
            repres_ = super(
                serializers.HyperlinkedModelSerializer,
                self
            ).to_representation(obj)

            if self.context['view'].action in ['detail', 'retrieve', 'update']:
                # remove the location (hyperlink url)
                #  from the game information
                repres_.pop('location')
                return repres_
            if self.context['view'].action in ['create']:
                # return only the location (hyperlink url)
                #  of the created game
                to_return = {}
                to_return['location'] = repres_['location']
                return to_return
        except KeyError:
            return super(
                serializers.HyperlinkedModelSerializer,
                self
            ).to_representation(obj)

        return super(
            serializers.HyperlinkedModelSerializer,
            self
        ).to_representation(obj)


class GameInfoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = GameInfo
        fields = "__all__"
