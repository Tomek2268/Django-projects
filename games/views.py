from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import TicTacToeGame

import ast

from .utils import win_check
# Create your views here.

def tic_tac_toe(request):
    return render(request,'games/tic_tac_toe.html')

@login_required(login_url='login')
def ttt_lobby(request):
    rooms = TicTacToeGame.objects.all().values_list('room',flat=True)

    if request.POST:
        join_room = request.POST.get('join_room')
        create_room = request.POST.get('create_room')

        if join_room:
            game = TicTacToeGame.objects.filter(room=join_room)
            if game:
                game = game[0]
                if game.invited:
                    messages.warning(request,'Room already have 2 players!')
                else:
                    game.invited = request.user
                    game.save()
                    return redirect('tic_tac_toe_online',join_room)
            else:
                messages.warning(request,'Room does not exist!')
        elif create_room:
            game = TicTacToeGame.objects.filter(room=create_room)
            if game:
                messages.warning(request,f'Room "{create_room}" already exist!')
            else:
                TicTacToeGame.objects.create(room=create_room,host=request.user)

                return redirect('tic_tac_toe_online',create_room)



    context = {'rooms':rooms}
    return render(request,'games/ttt_lobby.html',context)

@login_required(login_url='login')
def tic_tac_toe_online(request,room):
    game = TicTacToeGame.objects.filter(room=room)
    if not game:
        messages.warning(request,'Room closed :(')
        return redirect('ttt_lobby')
    else:
        game = game[0]
    users = User.objects.all()

    context = {'users':users,
                'game':game,
                'room':room,
            }
    return render(request,'games/ttt_with_pusher.html',context)