#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Durga Sai Sailesh Chodabattula (dchodaba), Manideep Varma Penumatsa (mpenumat), and Lakku Sai Jagan (slakku)
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

import sys
import numpy as np
from queue import PriorityQueue


def outerBoard(ln, w):
    nextState = []
    for i in range(0,w):nextState.append((0, i))
    for i in range(1, ln):nextState.append((i, w - 1))
    for i in range(w - 2, -1, -1):nextState.append((ln - 1, i))
    for i in range(ln - 2, 0, -1):nextState.append((i, 0))
    return nextState


def turnBoard(state, turn, matrix):
    ln_kn,width_kn = Rows,Cols
    res = tuple(matrix[x:x + 5] for x in range(0, len(matrix), 5))
    matrix = (np.asarray(res))
    if state == 2:
        rotateBoard = outerBoard(ln_kn, width_kn)
        turn %= len(outerBoard(ln_kn, width_kn))
        new_state = rotateBoard[-turn:] + rotateBoard[:-turn]
        newArray={element: matrix[element[0]][element[1]] for element in rotateBoard}
        for i, element in enumerate(new_state):
            matrix[rotateBoard[i][0]][rotateBoard[i][1]] = newArray[element]
        matrix = (matrix.tolist())
        matrix_list = [i for matt in matrix for i in matt]
        if turn == 1:return (tuple(matrix_list), "Oc")
        return (tuple(matrix_list), "Occ")
    if state == 1:
        board_inner_ring = inner_board(ln_kn, width_kn)
        turn %= len(board_inner_ring)
        new_state = board_inner_ring[-turn:] + board_inner_ring[:-turn]
        newArray = {element: matrix[element[0]][element[1]] for element in board_inner_ring}
        for i, element in enumerate(new_state):
            matrix[board_inner_ring[i][0]][board_inner_ring[i][1]] = newArray[element]
        matrix = (matrix.tolist())
        matrix_list = [i for matt in matrix for i in matt]
        if turn == 1:return (tuple(matrix_list), "Ic")
        return (tuple(matrix_list), "Icc")



def printable_board(board):
    return [('%3d ') * Cols % board[j:(j + Cols)] for j in range(0, Rows * Cols, Cols)]

def inner_board(ln, w):
    nextState = []
    for i in range(1, 4, 1):nextState.append((1, i))
    for i in range(2, 4, 1):nextState.append((i, 3))
    for i in range(2, 0, -1):nextState.append((3, i))
    nextState.append((2, 1))
    return nextState

def is_goal(state):
    return sorted(state) == list(state)


def col_moves(c, d, s):
    list_state = list(s)
    Cols = s[c::5]
    list_state[c::5] = Cols[-d:] + Cols[:-d]
    if d == -1:return (tuple(list_state), "U" + str(c + 1))
    else:return (tuple(list_state), "D" + str(c + 1))


def row_moves(r, d, s):
    Rows = s[(r * 5):(r * 5 + 5)]
    if d == -1:return ((s[0:(r * 5)] + Rows[-d:] + Rows[:-d] + s[(r * 5 + 5):]), "L" + str(r + 1))
    else:return ((s[0:(r * 5)] + Rows[-d:] + Rows[:-d] + s[(r * 5 + 5):]), "R" + str(r + 1))

Rows,Cols = 5,5
def Succussors(state):
    Succesor = []
    for i in range(0, Rows):
        for d in (-1, 1):Succesor.append(row_moves(i, d, state))
    for i in range(0, Cols):
        for d in (-1, 1):Succesor.append(col_moves(i, d, state))
    for i in (1, 2):
        for d in (-1, 1):Succesor.append(turnBoard(i, d, state))
    return Succesor

def heuristicFn(pr):
    dist = 0
    goal = sorted(pr)
    goal_state = {0: (0, 0), 1: (0, 1), 2: (0, 2), 3: (0, 3), 4: (0, 4),5: (1, 0), 6: (1, 1), 7: (1, 2), 8: (1, 3), 9: (1, 4),10: (2, 0), 11: (2, 1), 12: (2, 2), 13: (2, 3), 14: (2, 4),15: (3, 0), 16: (3, 1), 17: (3, 2), 18: (3, 3), 19: (3, 4),20: (4, 0), 21: (4, 1), 22: (4, 2), 23: (4, 3), 24: (4, 4)}
    for i in range(0, 25):
        matrix = pr[i]
        pos = goal.index(matrix)
        x, y = goal_state[i]
        xs, ys = goal_state[pos]
        if ((y == 4 and ys == 0) or (y == 0 and ys == 4)):dist += (1 + abs(x - xs))
        elif ((x == 4 and xs == 0) or (x == 0 and xs == 4)):
            if ((x == 0 and xs == 4) and (y == 0 and ys == 4)):dist += 3
            elif (x == ys) and (y == xs):dist += 3
            else:dist += (1 + abs(y - ys))
        else:dist += (abs(x - xs) + abs(y - ys))
    return float(dist) / 5


def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    PriorityQ = PriorityQueue()
    PriorityQ.put((0, (initial_board, "")))
    while not (PriorityQ.empty()):
        (p, (state, route_so_far)) = PriorityQ.get()
        for (successor, move) in Succussors(state):
            if is_goal(successor):
                # test = ''.join(route_so_far)
                result = tuple(route_so_far.split(' '))
                result = result + tuple(move.split(' '))
                resultList = list(result)
                resultList.pop(0)
                return (resultList)
            route_ln = len(route_so_far.split())
            PriorityQ.put((heuristicFn(state) + route_ln, (successor, route_so_far + " " + move)))
    return False


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        raise (Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    if len(start_state) != Rows * Cols:
        raise (Exception("Error: couldn't parse start state file"))

    print("Start state: \n" + "\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))

    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))