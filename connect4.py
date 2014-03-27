import re
import math
from copy import deepcopy


def retr(column,row,board):#function that retrieves a value from the board
    try:
        value = str(board[column][row])
    except:
        return ' '
    else:
        return value


def printboard(board):  #makes a visual representation of what the user expects the board to look like
    print '.---------------------------.'
    for i in range(5,-1,-1):
        if i > 0:
            print '|',
            for j in range(7):
                print retr( j, i, board ) + ' |',
            print '\n|---------------------------|'
        if i == 0:
            print '|',
            for j in range(7):
                print retr( j, i, board ) + ' |',
            print '\n*---------------------------*'
            print '  1   2   3   4   5   6   7'

def row_count(row_or_column):#searches a row, column, or diagonal for meaningfull seaquences
    #the teirs are listed in sets of 4 in a row, then three, then 2, then 1.
    teir_list = [[["'R', 'R', 'R', 'R', 'R'", "'R', 'R', 'R', 'R'",],
                  ["'R', 'R', ' ', 'R', 'R'", "'R', ' ', 'R', 'R', 'R'", "'R', 'R', 'R', ' ', 'R'",  "' ', 'R', 'R', 'R'", "'R', 'R', 'R', ' '",],
                  ["' ', 'R', ' ', 'R', ' '"],
                  ["' ', ' ', 'R', 'R'", "'R', 'R', ' ', ' '", "' ', 'R', ' ', 'R'", "'R', ' ', 'R', ' '", "' ', 'R', 'R', ' '",],
                  ["' ', ' ', ' ', 'R'", "' ', ' ', 'R', ' '", "' ', 'R', ' ', ' '", "'R', ' ', ' ', ' '"]],
                  [["'B', 'B', 'B', 'B', 'B'", "'B', 'B', 'B', 'B'",],
                  ["'B', 'B', ' ', 'B', 'B'", "'B', ' ', 'B', 'B', 'B'", "'B', 'B', 'B', ' ', 'B'",  "' ', 'B', 'B', 'B'", "'B', 'B', 'B', ' '",],
                  ["' ', 'B', ' ', 'B', ' '"],
                  ["' ', ' ', 'B', 'B'", "'B', 'B', ' ', ' '", "' ', 'B', ' ', 'B'", "'B', ' ', 'B', ' '", "' ', 'B', 'B', ' '",],
                  ["' ', ' ', ' ', 'B'", "' ', ' ', 'B', ' '", "' ', 'B', ' ', ' '", "'B', ' ', ' ', ' '"]]]
    counting = []
    for h in range(len(teir_list)):
        for i  in range(len(teir_list[h])):
            for j in range(len(teir_list[h][i])):
                s = re.findall(teir_list[h][i][j], row_or_column)
                if s != []:
                    counting.append([h,i])
    #print counting
    return counting#returns the list indexes of all the teirs that were in the row or column or diagonal

def num_generate(teirs):
    num = None
    for i in range(len(teirs)):#these are where I set values for different amounts of consecutive peices
        subnum = None
        if teirs[i][1] == 0:
            subnum = 1000000
        if teirs[i][1] == 1:
            subnum = 750
        if teirs[i][1] == 2:
            subnum = 250
        if teirs[i][1] == 3:
            subnum = 25
        if teirs[i][1] == 4:
            subnum = 5
        if teirs[i][0] == 0:
            subnum += 1
            subnum *= -1
        teirs.insert(i, subnum)
        teirs.pop(i+1)
    final = sum(teirs)
    return final
        
        
                  
def win(string):
    #print string
    redwins = "'R', 'R', 'R', 'R'"
    blackwins = "'B', 'B', 'B', 'B'"
    if re.findall(redwins, string) != []:
        #print 'RED WINS'
        return True
    elif re.findall(blackwins, string) != []:
        #print 'BLACK WINS'
        return True
    return False


class TooHigh(Exception):#exception raised when column is filled
    def __init__(self):
        pass


def check4stuff(board, use):#if use = 0 it checks for a win. if use = 1 it returns a score of the board
    num = 0
    if use == 0:#checks columns
        s = win(str(board))
        if s == True:
            return True
    if use == 1:
        num += num_generate(row_count(str(board)))
    for h in range(3,9):#checkingdiagonal slanting down
        diag = []
        for i in range(h-5 if h > 5 else 0, 7 if h > 7 else h + 1):
            j = -i + h
            if i < 7:
                diag.append(retr( i, j, board))#makes a list of values in all diagonal rows
            else:
                pass
            if use == 0:
                s = win(str(diag))
                if s == True:
                    return True
            if use == 1:
                num += num_generate(row_count(str(diag)))
    for h in range(-3,3):#diagonals slanting up
        diag = []
        for i in range( abs(h) if h <0 else 0, 7-h if h >-1 else 7):
            j = i +h
            if i < 7:
                diag.append(retr( i, j, board))
            else:
                pass
        if use == 0:
            s = win(str(diag))
            if s == True:
                return True
            if use == 1:
                num += num_generate(row_count(str(diag)))
    for i in range(6):#horizontal rows
        horizontals = []
        for j in range(7):
            horizontals.append(retr( j, i, board ))
        if use == 0:
            s = win(str(horizontals))
            if s == True:
                return True
        if use == 1:
            num += num_generate(row_count(str(horizontals)))
    if use == 1:
        return num
    elif use == 0:
        return False
    else:
        raise TooHigh

def larger(score1,score2):#takes two scores and returns the larger one
    s = cmp(score1,score2)
    if s < 0:
        return score2
    else:
        return score1

def smaller(score1,score2):
    s = cmp(score1,score2)#takes two scores and returns the smaller
    if s > 0:
        return score2
    else:
        return score1

def find_smlorlrg(scores, smallorlarge):#reduces a list of intagers to either the smallest or largest intager
    return reduce(smallorlarge, scores)


def generate_boards(board, color):#generates all possible moves 
    for i in range(7):
        if len(board[i]) < 6:#rules out all columns that are full
            board[i].append(color)
            yield board
            board[i].pop(len(board[i])-1)

def minimax(board, depth, turn = -1):#recurses down the game tree to find the best possible move
    newboard = deepcopy(board)
    turn += 1
    if check4stuff(newboard, 0) == True:
        return check4stuff(newboard, 1)
    if depth == turn:
        return check4stuff(newboard, 1)
    if depth > turn:
        moves = []
        if turn % 2 == 1:
            color = 'R'
        else:
            color = 'B'
        for i in generate_boards(newboard, color):
            s = minimax(i, depth, turn)
            moves.append(s)
        if turn != 0:
            return find_smlorlrg(moves, smaller if turn % 2 == 1 else larger)
        if turn == 0:
            for i in range(7):
                if moves[i] == find_smlorlrg(moves, larger):
                    return i


def full_board(board):#determines if there are no more possible moves
    full_count = 0
    for i in range(7):
        if len(board[i]) >= 6:
            full_count += 1
    if full_count >= 7:
        return True
    elif full_count < 7:
        return False

def get_count():#asks user wheather or not he/she will play  with the computer
    players = None
    while 1 > 0:
        try:
            players = int(raw_input('How many players? \n(enter 1 or 2): \n'))
        except ValueError:
            print "Not a number...\n"
        if players == 1:
            return players
        if players == 2:
            return players
    

def p_count(board):#asks user which column he/she wants to play in and returns index value
    place = None
    while 1 < 2:
        try:
            place = int(raw_input('What column would you like to play your piece in?\n'))
            if place > 7 or place < 1:
                print 'out of range\n'
            if len(board[place - 1]) > 5:
                raise TooHigh
            else:
                return place
        except ValueError:
            print 'Not a number...\n'
        except TooHigh:
            print 'That column is filled\n'

def difficulty():#asks the user what difficulty he/she would like
    while True:
        input_depth = int(raw_input('What difficulty ? \n*Hit 1 then enter for easy\n*Hit 2 then enter for hard\n*Hit 3 then enter for extremely difficult (only do this if you don\'t mind waiting a bit)\n'))
        if input_depth == 1 or input_depth == 2 or input_depth == 3:
            return input_depth * 2
        else:
            print 'Incorrect Entry...'
            
def main_game():    
    while 1 < 2:
        board = [[],[],[],[],[],[],[]]
        player_count = get_count()
        turn = 1
        if player_count == 1:
            depth = difficulty()
        printboard(board)
        if player_count < 3 and player_count >1:
            while check4stuff(board, 0) == False and full_board(board) == False:
                if turn % 2 == 1:
                    color = ['R', 'Red']
                else:
                    color = ['B', 'Black']
                print "{0}\'s turn".format(color[1])
                placement = p_count(board)
                board[placement - 1].append(color[0])
                turn += 1
                printboard(board)
        if player_count > 0 and player_count < 2:
            while check4stuff(board, 0) == False and full_board(board) == False:
                if turn % 2 == 1:
                    print 'Your turn.\n'
                    placement = p_count(board)
                    board[placement - 1].append('R')
                elif turn % 2 == 0:
                    print 'computer\'s turn...\n'
                    copy = deepcopy(board)
                    s = minimax(copy, depth)
                    print str(s)
                    board[s].append('B')
                turn += 1
                printboard(board)
        if check4stuff(board, 0) == True:
            if turn % 2 == 1:
                print 'BLACK WINS'
            if turn % 2 == 0:
                print 'RED WINS'
        if full_board(board) == True:
            print 'TIE GAME'
main_game()

