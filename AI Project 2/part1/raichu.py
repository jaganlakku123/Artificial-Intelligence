#
# raichu.py : Play the game of Raichu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, Oct 2021
#
import sys
import time
import copy
import math

# converts given 1d board to string
def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

# below function defines all moves taken by pichu, pikachu and raichu
def moves(board, n, player):
    fringe = []

    if player == 'w':                                       #predefining pieces of max player and opponent pieces so we could use the same function for boht white and black.
        my_p = 'w'
        my_pk = 'W'
        my_r = '@'
        opp_p = 'b'
        opp_pk = 'B'
        opp_r = '$'
    else:
        board = invert_board(board,n)                        #invert board if the max player is black
        my_p = 'b'
        my_pk = 'B'
        my_r = '$'
        opp_p = 'w'
        opp_pk = 'W'
        opp_r = '@'

    for i in range(0, n):
        for j in range(0, n):
                if board[i][j]!= '.':


                    # PICHU MOVES          
                    if board[i][j] == my_p: 
                        if i>0 and i<n:
                            #print("in pichu")
                            if j+1 < n:
                                if board[i+1][j+1] == '.':                                      #DiagonalRight - PICHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    if i+1 == n-1:
                                        changedboard[i+1][j+1] = my_r                           # Pichu -> Raichu if it reaches the end of the board
                                    else:
                                        changedboard[i+1][j+1] = my_p
                                    
                                    if(player == 'w'):                                     
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))            # invert the board back before appending if player is black
                                    #print2dboard(changedboard,n)
                                    
                            
                            if j-1 >= 0:      
                                if board[i+1][j-1] == '.':                                      #DiagonalLeft - PICHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    if i+1 == n-1:
                                        changedboard[i+1][j-1] = my_r
                                    else:
                                        changedboard[i+1][j-1] = my_p
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                    
                            if i+2 < n: 
                                if j+2 < n:
                                    if board[i+1][j+1] == opp_p and board[i+2][j+2] == '.':    #DiagonalRight jump - PICHU
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i+1][j+1] = '.'
                                        if i+2 == n-1:
                                            changedboard[i+2][j+2] = my_r
                                        else:
                                            changedboard[i+2][j+2] = my_p
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                        
   
                                if j-2 >= 0:
                                    if board[i+1][j-1] == opp_p and board[i+2][j-2] == '.':   #DiagonalLeft jump - PICHU
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i+1][j-1] = '.'
                                        if i+2 == n-1:
                                            changedboard[i+2][j-2] = my_r
                                        else:
                                            changedboard[i+2][j-2] = my_p
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                                                  
                    # PIKACHU MOVES               
                    if board[i][j] == my_pk:
                        if i>0 and i<n:
                            #print("in pikachu")
                            if board[i+1][j] == '.':                                    #Forward 1step - PIKACHU
                                changedboard = list(copy.deepcopy(board))
                                changedboard[i][j] = '.'
                                if i+1 == n-1:
                                    changedboard[i+1][j] = my_r
                                else:
                                    changedboard[i+1][j] = my_pk
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)    
                            if i+2 < n:
                                if (board[i+1][j] == opp_p or board[i+1][j] == opp_pk) and board[i+2][j] == '.':
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    changedboard[i+1][j] = '.'
                                    if i+2 == n-1:
                                        changedboard[i+2][j] = my_r
                                    else:
                                        changedboard[i+2][j] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                            if i+3 < n:
                                if (board[i+1][j] == opp_p or board[i+1][j] == opp_pk) and board[i+2][j] == '.' and board[i+3][j]:
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    changedboard[i+1][j] = '.'
                                    if i+3 == n-1:
                                        changedboard[i+3][j] = my_r
                                    else:
                                        changedboard[i+3][j] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                     
                            if j+1 < n:
                                if board[i][j+1] == '.':                                #Right 1step - PIKACHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    changedboard[i][j+1] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                if j+2 < n:
                                    if (board[i][j+1] == opp_p or board[i][j+1] == opp_pk) and board[i][j+2]== '.':   
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j+1] = '.'
                                        changedboard[i][j+2] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                if j+3 < n:
                                    if (board[i][j+1] == opp_p or board[i][j+1] == opp_pk) and board[i][j+2]== '.' and board[i][j+3]== '.':   
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j+1] = '.'
                                        changedboard[i][j+3] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                            
                            if j-1 >= 0:
                                if board[i][j-1] == '.':                                #Left 1step - PIKACHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    changedboard[i][j-1] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                if j-2 >= 0:
                                    if (board[i][j-1] == 'b' or board[i][j-1] == 'B') and board[i][j-2]== '.':
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j-1] = '.'
                                        changedboard[i][j-2] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                if j-3 >= 0:
                                    if (board[i][j-1] == 'b' or board[i][j-1] == 'B') and board[i][j-2]== '.'  and board[i][j-3]== '.':
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j-1] = '.'
                                        changedboard[i][j-3] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                            
                            
                            if i+2 < n:
                                if board[i+1][j] == '.' and board[i+2][j] == '.':                   #Forward 2step  - PIKACHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    if i+2 == n-1:
                                        changedboard[i+2][j] = my_r
                                    else:
                                        changedboard[i+2][j] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                    
                                if i+3 < n:
                                    if board[i+1][j] == '.' and (board[i+2][j] == opp_p or board[i+2][j] == opp_pk) and board[i+3][j] in '.':
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i+2][j] = '.'
                                        if i+3 == n-1:
                                            changedboard[i+3][j] = my_r
                                        else:
                                            changedboard[i+3][j] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                        
                            
                            if j+2 < n:
                                if board[i][j+1] == '.' and board[i][j+2] == '.':                   #Right 2STEP  - PIKACHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    board[i][j+2] == my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                if j+3 < n:
                                    if board[i][j+1] == '.' and (board[i][j+2] == opp_p or board[i][j+2] == opp_pk) and board[i][j+3] == '.':   
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j+2] = '.'
                                        changedboard[i][j+3] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                            if j-2 >= 0:
                                if board[i][j-1] == '.' and board[i][j-2] == '.':                   #Left 2 step - PIKACHU
                                    changedboard = list(copy.deepcopy(board))
                                    changedboard[i][j] = '.'
                                    changedboard[i][j-2] = my_pk
                                    if(player == 'w'):
                                        fringe.append(changedboard)
                                    else:
                                        fringe.append(invert_board(changedboard, n))
                                    #print2dboard(changedboard,n)
                                if j-3 >= 0:
                                    if board[i][j-1] == '.' and (board[i][j-2] == opp_p or board[i][j-2] == opp_pk) and board[i][j-3] == '.':
                                        changedboard = list(copy.deepcopy(board))
                                        changedboard[i][j] = '.'
                                        changedboard[i][j-2] = '.'
                                        changedboard[i][j-3] = my_pk
                                        if(player == 'w'):
                                            fringe.append(changedboard)
                                        else:
                                            fringe.append(invert_board(changedboard, n))
                                        #print2dboard(changedboard,n)
                                       
                    # RAICHU MOVES
                    #Below code was discussed with fellow classmate Sravani Wayangankar. I have taken her idea and implemented it as my code was going in an infinite loop when it discovers the opponent raichu for some reason.
                    if board[i][j]==my_r:    ############ RAICHU moves
                    
                        k=i+1       # Forward - RAICHU
                        a=100
                        b=100
                        c=0
                        while k<n:
                            if board[k][j]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[k][j]=my_r
                                changedboard[i][j]='.'
                                if c>0:
                                    changedboard[a][b]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif k!=n-1 and (board[k][j]==opp_p or board[k][j]==opp_pk or board[k][j]==opp_r) and board[k+1][j]=='.':
                                if k!=n-1 and board[k+1][j]=='.':
                                    if c>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[k][j]='.'
                                        changedboard[k+1][j]=my_r
                                        a=k
                                        b=j
                                        c=c+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        k=k+1
                            else:
                                break
                            k=k+1

                    
                        
                        l=i-1       #Backward - Raichu
                        x=100
                        y=100
                        cnt=0
                        while l>=0:
                            if board[l][j]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[l][j]=my_r
                                changedboard[i][j]='.'
                                if cnt>0:
                                    changedboard[x][y]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif l!=0 and (board[l][j]==opp_p or board[l][j]==opp_pk or board[l][j]==opp_r) and board[l-1][j]=='.':
                                if l!=0 and board[l-1][j]=='.':
                                    if cnt>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[l][j]='.'
                                        changedboard[l-1][j]=my_r
                                        x=l
                                        y=j
                                        cnt=cnt+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        l=l-1
                            else:
                                break
                            l=l-1
                        
                        
                        m=j+1       # Right - RAICHU
                        u=100
                        v=100
                        cn=0
                        while m<n:
                            if board[i][m]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][m]=my_r
                                changedboard[i][j]='.'
                                if cn>0:
                                    changedboard[u][v]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif m!=n-1 and (board[i][m]==opp_p or board[i][m]==opp_pk or board[i][m]==opp_r) and board[i][m+1]=='.':
                                if m!=n-1 and board[i][m+1]=='.':
                                    if cn>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[i][m]='.'
                                        changedboard[i][m+1]=my_r
                                        u=i
                                        v=m
                                        cn=cn+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        m=m+1
                            else:
                                break
                            m=m+1
                        

                        s=j-1       #left and jump
                        p=100
                        q=100
                        ct=0
                        while s>=0:
                            if board[i][s]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][s]=my_r
                                changedboard[i][j]='.'
                                if ct>0:
                                    changedboard[p][q]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif s!=0 and (board[i][s]==opp_p or board[i][s]==opp_pk or board[i][s]==opp_r) and board[i][s-1]=='.':
                                if s!=0 and board[i][s-1]=='.':
                                    if ct>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[i][s]='.'
                                        changedboard[i][s-1]=my_r
                                        p=i
                                        q=s
                                        ct=ct+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        s=s-1
                            else:
                                break
                            s=s-1


                        e=i+1       #Forward right Diagonal - Raichu
                        f=j+1
                        g=100
                        h=100
                        count=0
                        while e<n and f<n:
                            if board[e][f]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[e][f]=my_r
                                changedboard[i][j]='.'
                                if count>0:
                                    changedboard[g][h]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif e!=n-1 and f!=n-1 and (board[e][f]==opp_p or board[e][f]==opp_pk or board[e][f]==opp_r) and board[e+1][f+1]=='.':
                                if e!=n-1  and f!=n-1 and board[e+1][f+1]=='.':
                                    if count>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[e][f]='.'
                                        changedboard[e+1][f+1]=my_r
                                        g=e
                                        h=f
                                        count=count+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        e=e+1
                                        f=f+1
                            else:
                                break
                            e=e+1
                            f=f+1
                            

                        o=i-1       # Backward left diagonal - RAICHU
                        r=j-1
                        w=100
                        z=100
                        count=0
                        while o>=0 and r>=0:
                            if board[o][r]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[o][r]=my_r
                                changedboard[i][j]='.'
                                if count>0:
                                    changedboard[w][z]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif o!=0 and r!=0 and (board[o][r]==opp_p or board[o][r]==opp_pk or board[o][r]==opp_r) and board[o-1][r-1]=='.':
                                if o!=0  and r!=0 and board[o-1][r-1]=='.':
                                    if count>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[o][r]='.'
                                        changedboard[o-1][r-1]=my_r
                                        w=o
                                        z=r
                                        count=count+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        o=o-1
                                        r=r-1
                            else:
                                break
                            o=o-1
                            r=r-1
                        


                        e=i-1       #backward right diagonal and jump
                        f=j+1
                        g=100
                        h=100
                        count=0
                        while e>=0 and f<n:
                            if board[e][f]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[e][f]=my_r
                                changedboard[i][j]='.'
                                if count>0:
                                    changedboard[g][h]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif e!=0 and f!=n-1 and (board[e][f]==opp_p or board[e][f]==opp_pk or board[e][f]==opp_r) and board[e-1][f+1]=='.':
                                if e!=0  and f!=n-1 and board[e-1][f+1]=='.':
                                    if count>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[e][f]='.'
                                        changedboard[e-1][f+1]=my_r
                                        g=e
                                        h=f
                                        count=count+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        e=e-1
                                        f=f+1
                            else:
                                break
                            e=e-1
                            f=f+1
                        

                        e=i+1       # forward left diagonal - RAICHU
                        f=j-1
                        g=100
                        h=100
                        count=0
                        while e<n and f>=0:
                            if board[e][f]=='.':
                                changedboard=list(copy.deepcopy(board))
                                changedboard[e][f]=my_r
                                changedboard[i][j]='.'
                                if count>0:
                                    changedboard[g][h]='.'
                                if player=='w':
                                    fringe.append(changedboard)
                                else:
                                    b=invert_board(changedboard,n)
                                    fringe.append(b)
                            elif e!=n-1 and f!=0 and (board[e][f]==opp_p or board[e][f]==opp_pk or board[e][f]==opp_r) and board[e+1][f-1]=='.':
                                if e!=n-1  and f!=0 and board[e+1][f-1]=='.':
                                    if count>0:
                                        break
                                    else:
                                        changedboard=list(copy.deepcopy(board))
                                        changedboard[i][j]='.'
                                        changedboard[e][f]='.'
                                        changedboard[e+1][f-1]=my_r
                                        g=e
                                        h=f
                                        count=count+1
                                        if player=='w':
                                            fringe.append(changedboard)
                                        else:
                                            b=invert_board(changedboard,n)
                                            fringe.append(b)
                                        e=e+1
                                        f=f-1
                            else:
                                break
                            e=e+1
                            f=f-1
                        
                        
                        
                    # The code below for RAICHU was implemented by me from scratch earlier but it kept going into an infinite loop when it discovered an opponent raichu.
                    '''   
                    if board[i][j]==my_r:
                        check=True
                        k=i+1                                                                   # FORWARD - RAICHU
                        while k<n:
                            if board[k][j]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[k][j]= my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[k][j]==opp_p or board[k][j]==opp_pk or board[k][j]==opp_r) and k+1 < n and check:
                                if board[k+1][j]=='.':
                                    l=k+1
                                    while l<n:
                                        if board[l][j]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[k][j]='.'
                                            changedboard[l][j]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        l=l+1
                                    check = False
                            else:
                                break
                            k=k+1
                        

                        check=True
                        k=i-1                                                                       # BACKWARD - RAICHU
                        while k>=0:
                            if board[k][j]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[k][j]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[k][j]==opp_p or board[k][j]==opp_pk or board[k][j]==opp_r) and  k-1>= 0 and check:
                                if board[k-1][j]=='.':
                                    l=k-1
                                    while l>=0:
                                        if board[l][j]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[k][j]='.'
                                            changedboard[l][j]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        l=l-1
                                    check = False
                            else:
                                break
                            k=k-1
                    
                        check=True
                        k=j-1                                                                               # LEFT - RAICHU
                        while k>=0:
                            if board[i][k]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[i][k]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[i][k]==opp_p or board[i][k]==opp_pk or board[i][k]==opp_r) and k-1>=0 and check:
                                if board[i][k-1]=='.':
                                    l=k-1
                                    while l>=0:
                                        if board[i][l]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[i][k]='.'
                                            changedboard[i][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        l=l-1
                                    check = False
                            else:
                                break
                            k=k-1
                            
                    
                        check=True
                        k=j+1                                                                #right - rAICHU
                        while k<n:
                            if board[i][k]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[i][k]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[i][k]==opp_p or board[i][k]==opp_pk or board[i][k]==opp_r) and k+1<n and check:
                                if board[i][k+1]=='.':
                                    l=k+1
                                    while l<n:
                                        if board[i][l]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[i][k]='.'
                                            changedboard[i][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        l=l+1
                                    check = False
                            else:
                                break
                            k=k+1
                    
                        
                        check=True
                        o=i+1
                        p=j+1                                                               #diagonal right down - RAICHU
                        while o<n and p<n:
                            if board[o][p]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[o][p]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                # print2dboard(changedboard,n)
                            
                            elif (board[o][p]==opp_p or board[o][p]==opp_pk or board[o][p]==opp_r) and o+1<n and p+1<n and check:
                                if board[o+1][p+1]=='.':
                                    k=o+1
                                    l=p+1
                                    while k<n and l<n:
                                        if board[k][l]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[o][p]='.'
                                            changedboard[k][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            # print2dboard(changedboard,n)
                                        else:
                                            break
                                        k=k+1
                                        l=l+1
                                    check = False
                            else:
                                break
                            o=o+1
                            p=p+1
                        

                        check=True
                        o=i-1
                        p=j-1                                                                       #diagonal left up - RAICHU
                        while o>=0 and p>=0:
                            if board[o][p]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[o][p]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)                       
                            elif (board[o][p]==opp_p or board[o][p]==opp_pk or board[o][p]==opp_r) and o-1>=0 and p-1>=0 and check:
                                if board[o-1][p-1]=='.':
                                    k=o-1
                                    l=p-1
                                    while k>=0 and l>=0:
                                        if board[k][l]=='.':
                                            #print('i=',o," ",'k=',p," ",'j=',j)
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[o][p]='.'
                                            changedboard[k][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        k=k-1
                                        l=l-1
                                    check = False
                            else:
                                break
                            o=o-1
                            p=p-1
                        

                        check=True
                        o=i+1
                        p=j-1                                                                   #diagonal left down - RAICHU
                        while o<n and p>=0:
                            if board[o][p]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[o][p]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[o][p]==opp_p or board[o][p]==opp_pk or board[o][p]==opp_r) and o+1<n and p-1>=0 and check:
                                if board[o+1][p-1]=='.':
                                    k=o+1
                                    l=p-1
                                    while k<n and l>=0:
                                        if board[k][l]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[o][p]='.'
                                            changedboard[k][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        k=k+1
                                        l=l-1
                                    check = False
                                else:
                                    break
                                o=o+1
                                p=p-1
                            

                        check=True
                        o=i-1
                        p=j+1                                                                   #diagonal right up - RAICHU
                        while o>=0 and p<n:
                            if board[o][p]=='.' and check:
                                changedboard=list(copy.deepcopy(board))
                                changedboard[i][j]='.'
                                changedboard[o][p]=my_r
                                if(player == 'w'):
                                    fringe.append(changedboard)
                                else:
                                    fringe.append(invert_board(changedboard, n))
                                #print2dboard(changedboard,n)
                            elif (board[o][p]==opp_p or board[o][p]==opp_pk or board[o][p]==opp_r) and o-1>=0 and p-1<n and check:
                                if board[o-1][p-1]=='.':
                                    k=o-1
                                    l=p+1
                                    while k>=0 and l<n:
                                        if board[k][l]=='.':
                                            changedboard=list(copy.deepcopy(board))
                                            changedboard[i][j]='.'
                                            changedboard[o][p]='.'
                                            changedboard[k][l]=my_r
                                            if(player == 'w'):
                                                fringe.append(changedboard)
                                            else:
                                                fringe.append(invert_board(changedboard, n))
                                            #print2dboard(changedboard,n)
                                        else:
                                            break
                                        k=k-1
                                        l=l+1
                                    check = False
                            else:
                                break
                            o=o-1
                            p=p+1
                    '''
    return fringe


#Compute the evaluation for Pichu, Pikachu and Raichu
def evaluation_function(board, n, max_player):         # Costs are given according to number of moves a piece can make
                                                       # Therefore, pichu =2, Piakchu =3 and Raichu =8                                 
    w_cost = 0
    b_cost = 0
    cost = 0
    for i in range(n):
        for j in range(n):
            if board[i][j] != '.':
                if board[i][j] == 'w':
                    w_cost = w_cost + 2
                    #print("+2")
                if board[i][j] == 'W':
                    w_cost = w_cost + 3
                    #print("+3")
                if board[i][j] == '@':
                    w_cost = w_cost + 8
                    #print("+8")
                if board[i][j] == 'b':
                    b_cost = b_cost + 2
                    #print("-2")
                if board[i][j] == 'B':
                    b_cost = b_cost + 3
                    #print("-3")
                if board[i][j] == '$':
                    b_cost = b_cost + 8
                    #print("-8")
    if max_player == 'w':
        cost = w_cost - b_cost
    elif max_player == 'b':
        cost = b_cost - w_cost
    #print("Cost=",cost)
    return cost

# Checks if either black or white has won
def terminal_state(board, n, max_player):
    w_num = -1
    b_num = -1
    for i in range(n):                          
        for j in range(n):
            if board[i][j] in 'wW@':
                w_num = w_num + 1
            elif board[i][j] in 'bB$':
                b_num = b_num + 1
    if max_player == 'w' and b_num == 0:       
        return True
    elif max_player == 'b' and w_num == 0: 
        return True
    else:
        return False

# Converts given 2D board to string format for output
def string_to_board(board):
    return "".join(["".join(i) for i in board])

# Converts given 1D strign to 2d
def boardin2d(board, n):
    board2d=[]
    for i in range(0, len(board), n):
        row=[]
        for j in range(i, n+i):
            row.append(board[j])
        board2d.append(row)
    return board2d

# Prints the 2D board
'''def print2dboard(board, n):
        for i in range(0,n):
            for j in range(0,n):
                print(board[i][j], end="")
            print()
        print()
'''

# Inverts the board for black
def invert_board(board, n):
    #reversed_board = [elem[::-1] for elem in board][::-1]
    row=[]
    board1=[]
    for i in range(n-1, -1, -1):
        row=board[i][::-1]
        board1.append(row)
    #print("inverted board")
    #print2dboard(board1, n)
    return board1

# Calls successor fucntions
def successors(board, n, player):
    return moves(board, n, player)

# Performs MIN for alpha beta in minimax algorithm  
def min_method(board, max_player, min_player, alpha, beta, n, max_depth):
    #print("min")
    if max_depth == 0 or terminal_state(board, n, max_player):
        cost = evaluation_function(board, n, max_player)
        return cost

    else:
        for s in successors(board, n, min_player):
            #v = max_method(s, max_player, min_player, alpha, beta, n,  max_depth-1)
            beta = min(max_method(s, max_player, min_player, alpha, beta, n,  max_depth-1), beta)
            if beta <= alpha:
                return beta
    
    return beta

# Performs MAX for alpha beta in minimax algorithm
def max_method(board, max_player, min_player, alpha, beta, n, max_depth):
    #print("max")
    if max_depth == 0 or terminal_state(board, n, max_player):
        cost = evaluation_function(board, n, max_player)
        return cost

    else:
        for s in successors(board, n, max_player):
            #v = min_method(s, max_player, min_player, alpha, beta, n, max_depth-1)
            alpha = max(min_method(s, max_player, min_player, alpha, beta, n, max_depth-1), alpha)
            if alpha >= beta:
                return alpha

        return alpha

# Performs alpha beta algorithm
def alpha_beta(board, n, player, max_depth):
    alpha = float('-inf')
    beta = float('inf')
    min_val = float('-inf')
    best_move = None
    v=0

    if player == "w":
        max_player = "w"
        min_player = "b"
    else:
        max_player = "b"
        min_player = "w"

    for s in successors(board, n, player):
        v = min_method(s, max_player, min_player, alpha, beta, n, max_depth)
        if v > min_val:
            min_val = v
            best_move = s
    
    #print("best",best_move)
    #print(min_val)
    return best_move

# Random function gives a random output if the time limit exceeds
#Thisnis implemented on safer side in case no output is returned. This will keep the game going by performing some move. 
def randommove(board, n, player):
    random_moves = moves(board,n,player)
    if len(random_moves)>0:
        random_move = string_to_board(random_moves[0])
        return random_move

def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    
    board2d = boardin2d(board, N)

    end_time = time.time()+float(timelimit-1)                 # Gives end time by adding current_time + time_limit

    count=0
    for max_depth in range(2,10):                           #Performs iterative deepening from depth 2 to 10
        best_board  = alpha_beta(board2d, N, player, max_depth)
        next_board = best_board
        final_board = string_to_board(next_board)
        yield final_board

        count = count+1
        if(time.time()>end_time) and count==0 :
            print(randommove(board2d, N, player))
            sys.exit()
            break
    

if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: Raichu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB@$" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
        print(new_board)