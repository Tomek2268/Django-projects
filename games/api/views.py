from rest_framework.decorators import api_view
from rest_framework.response import Response

from .pusher import pusher_client
from ..models import TicTacToeGame

@api_view(['GET'])
def get_routes(request):

    routes = [

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'}
    ]

    return Response(routes)

@api_view(['POST'])
def user_joined(request):
    game = request.data['game']
    pusher_client.trigger(game, 'user_joined', {
        'username': request.data['username'],
        'game': game
        })

    return Response([])

@api_view(['POST'])
def user_left(request):
    game = request.data['game']
    username = request.data['username']
    current_game = TicTacToeGame.objects.get(id=int(game))
    if username == current_game.host.username:
        current_game.delete()
    else:
        current_game.invited = None
        current_game.save()
    pusher_client.trigger(game, 'user_left', {
        'username': username,
        'game': game
        })

    return Response([])

@api_view(['POST'])
def player_move(request):
    game = request.data['game']
    username = request.data['username']
    spot = request.data['spot']
    mark = request.data['mark']
    current_game = TicTacToeGame.objects.get(id=int(game))
    pusher_client.trigger(game, 'player_move', {
        'username': username,
        'game': game,
        'spot': spot,
        'mark': mark
        })

    return Response([])