from django.shortcuts import render,redirect
import ast

from .utils import win_check
# Create your views here.

def tic_tac_toe(request):
    win_line_spot = 'false'
    win_line_orientation = None
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
                'win_line_spot':win_line_spot,
                'win_line_orientation':win_line_orientation}
    return render(request,'games/tic_tac_toe.html',context)