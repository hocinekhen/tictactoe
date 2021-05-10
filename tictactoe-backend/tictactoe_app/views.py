from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError

from .serializers import GameSerializer, GameInfoSerializer
from .models import Game, GameInfo


class GameViewset(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    model = Game

    def destroy(self, request, *args, **kwargs):
        # override this methode to inforce return 200 code instead
        # of 204_NO_CONTENT as specified in the challenge

        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def info_by_game_id(request):
    """return extra information about the game"""
    if not request.GET['game_id']:
        raise ValidationError('game_id is required')
    game_id = request.GET['game_id']
    game_info = GameInfo.objects.filter(game_id=game_id).first()
    ser = GameInfoSerializer(data=game_info)
    ser.is_valid()
    return Response(model_to_dict(game_info), status=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):
    return Response({'data': "api is working..."})
