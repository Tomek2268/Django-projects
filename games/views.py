from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TicTacToeGame
import ast

from .utils import win_check
# Create your views here.

def tic_tac_toe(request):
    win_line_spot = 'false'
    win_line_orientation = None
    outcome = 'false'
    if request.POST:
        spot = request.POST['spot']
        mark = request.POST['mark']
        legal_moves = ast.literal_eval(request.POST['legal_moves'])
        library_of_board = ast.literal_eval(request.POST['library_of_board'])
        if mark == 'O':
            mark = 'X'
        else:
            mark = 'O'
        
        legal_moves,library_of_board,outcome,win_line = win_check(spot,mark,legal_moves,library_of_board)
        win_line_spot,win_line_orientation = win_line
        js_library = {}
        for k,v in library_of_board.items():
            js_library[str(k)]=v
    else:
        mark = 'X'
        spot=''
        legal_moves = [7,8,9,4,5,6,1,2,3]
        library_of_board = {7:' ',8:' ',9:' ',4:' ',5:' ',6:' ',1:' ',2:' ',3:' '}
        js_library = {}
        for k,v in library_of_board.items():
            js_library[str(k)]=v

    context = {'legal_moves':legal_moves,
                'library_of_board':library_of_board,
                'js_library':js_library,
                'spot':spot,
                'mark':mark,
                'outcome':outcome,
                'win_line_spot':win_line_spot,
                'win_line_orientation':win_line_orientation}
    return render(request,'games/tic_tac_toe.html',context)

@login_required(login_url='login')
def ttt_lobby(request):

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



    context = {}
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
    return render(request,'games/t_t_t_with_channels.html',context)