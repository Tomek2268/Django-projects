import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
import sys

from .pusher import pusher_client
from ..models import TicTacToeGame

#sys.path.append('../users')
 
# importing
from users.models import Chat,Message

@api_view(['GET'])
def get_routes(request):

    routes = [

        {'POST':'/api/users/token'},
        {'POST':'/api/users/token/refresh'},
        {'POST':'/pusher/auth'}
    ]

    return Response(routes)



@api_view(['POST'])
def user_joined(request):
    game = request.data['game']
    current_game = TicTacToeGame.objects.get(id=int(game))
    current_game.game_continue = 0

    pusher_client.trigger(game, 'user_joined', {
        'username': request.data['username'],
        'game': game
        })

    return Response([])

@api_view(['POST'])
def user_left(request):
    game = request.data['game']
    username = request.data['username']
    current_game = TicTacToeGame.objects.filter(id=int(game))
    if current_game:
        current_game = current_game[0]
        if username == current_game.host.username:
            current_game.delete()
        else:
            current_game.game_continue = 0
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
    pusher_client.trigger(game, 'player_move', {
        'username': username,
        'game': game,
        'spot': spot,
        'mark': mark
        })

    return Response([])

@api_view(['POST'])
def game_continue(request):
    game = request.data['game']
    current_game = TicTacToeGame.objects.get(id=int(game))
    game_continue_value = 'false'
    current_game.game_continue += 1
    if current_game.game_continue == 2:
        current_game.game_continue = 0
        game_continue_value = 'true'
    current_game.save()
    pusher_client.trigger(game, 'game_continue', {
        'game_continue': game_continue_value,
        })

    return Response([])

@api_view(['POST'])
def user_joined_chat(request):
    room = request.data['room']
    username = request.data['username']

    pusher_client.trigger(room, 'user_joined_chat', {
        'username': username,
        })
    return Response([])

@api_view(['POST'])
def send_message(request):
    room = request.data['room']
    username = request.data['username']
    message = request.data['message']

    chat = Chat.objects.get(id=int(room))
    sender = User.objects.get(username=username)
    recipient = chat.members.exclude(username=username)[0]
    new_message = Message.objects.create(sender=sender,recipient=recipient,title=message,chat=chat)
    created_time = new_message.created_time
    new_message.save()

    pusher_client.trigger(room, 'send_message', {
        'username': username,
        'message': message,
        'created_time': created_time
        })

    return Response([])

@api_view(['POST'])
def user_left_chat(request):
    room = request.data['room']
    username = request.data['username']

    pusher_client.trigger(room, 'user_left_chat', {
        'username': username,
        })
    return Response([])