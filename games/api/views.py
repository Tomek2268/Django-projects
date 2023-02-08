from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.response import Response

from .pusher import pusher_client
from .serializers import TicTacToeGameSerializer
from ..models import TicTacToeGame

@api_view(['GET'])
def get_routes(request):

    routes = [
        {'GET':'/api/tic_tac_toe/id'},
        {'PUT':'/api/tic_tac_toe/id/update'},

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'}
    ]

    return Response(routes)

@api_view(['GET'])
def get_tic_tac_toe(request,pk):
    game = TicTacToeGame.objects.get(id=pk)
    serializer = TicTacToeGameSerializer(game,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def update_tic_tac_toe(request,pk):
    game = TicTacToeGame.objects.get(id=pk)
    try:
        library_of_board = request.data['library_of_board']
        game.library_of_board = library_of_board
        game.legal_moves.remove(request.data['spot'])
    except:
        try:
            game.canceled = request.data['canceled']
        except:
            try:
                game.accepted = request.data['accepted']
            except:
                try:
                    game.rejected = request.data['rejected']
                except:
                    pass
    game.save()
    serializer = TicTacToeGameSerializer(game,many=False)

    return Response(serializer.data)

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