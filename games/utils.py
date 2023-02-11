def win_check(spot,mark,legal_moves,library_of_board):
    legal_moves.remove(int(spot))
    library_of_board[int(spot)] = mark

    x = library_of_board

    lines_list = [x[7]==x[8]==x[9]!=' ',
                    x[4]==x[5]==x[6]!=' ',
                    x[1]==x[2]==x[3]!=' ',
                    x[7]==x[4]==x[1]!=' ',
                    x[8]==x[5]==x[2]!=' ',
                    x[9]==x[6]==x[3]!=' ',
                    x[9]==x[5]==x[1]!=' ',
                    x[7]==x[5]==x[3]!=' '
                ]
    win_line = ('false',None)
    if lines_list[0]:
        win_line = (8,'horizontal')
    elif lines_list[1]:
        win_line = (5,'horizontal')
    elif lines_list[2]:
        win_line = (2,'horizontal')
    elif lines_list[3]:
        win_line = (4,'vertical')
    elif lines_list[4]:
        win_line = (5,'vertical')
    elif lines_list[5]:
        win_line = (6,'vertical')
    elif lines_list[6]:
        win_line = (5,'diagonal_135')
    elif lines_list[7]:
        win_line = (5,'diagonal_45')

    
    if x[7]==x[8]==x[9]=='O' or x[4]==x[5]==x[6]=='O' or x[1]==x[2]==x[3]=='O' or x[7]==x[4]==x[1]=='O' or x[8]==x[5]==x[2]=='O' or x[9]==x[6]==x[3]=='O' or x[9]==x[5]==x[1]=='O' or x[7]==x[5]==x[3]=='O':
        
        return legal_moves,library_of_board,'O',win_line

    elif x[7]==x[8]==x[9]=='X' or x[4]==x[5]==x[6]=='X' or x[1]==x[2]==x[3]=='X' or x[7]==x[4]==x[1]=='X' or x[8]==x[5]==x[2]=='X' or x[9]==x[6]==x[3]=='X' or x[9]==x[5]==x[1]=='X' or x[7]==x[5]==x[3]=='X':

        return legal_moves,library_of_board,'X',win_line

    elif len(legal_moves) == 0:

        return legal_moves,library_of_board,'tie',win_line
    else:
        return legal_moves,library_of_board,'false',win_line
