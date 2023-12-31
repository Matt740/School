import copy
## Works
def is_empty(board):
    '''returns True iff there are no stones on the board board'''
    for j in range(len(board)):
        for k in range(len(board[j])):
            if board[j][k] != " ":
                return False
    return True

## Works
def is_bounded_start(board, y_end, x_end, length, d_y, d_x): # Helper function for is_bounded
    '''returns True if the sequence of length length that ends at location (y_end, x_end) is bounded at the end opposite of (y_end, x_end)'''
    if y_end - length*d_y > 7 or y_end - length*d_y < 0:
        return True
    elif x_end - length*d_x > 7 or x_end - length*d_x < 0:
        return True
    elif board[y_end - length*d_y][x_end - length*d_x] != ' ':
        return True
    return False

## Works
def is_bounded_end(board, y_end, x_end, length, d_y, d_x): # Helper function for is_bounded
    '''returns True if the sequence of length length that ends at location (y_end, x_end) is bounded at the end (y_end, x_end)'''
    if y_end + d_y > 7 or y_end + d_y < 0:
        return True
    elif x_end + d_x > 7 or x_end + d_x < 0:
        return True
    elif board[y_end + d_y][x_end + d_x] != ' ':
        return True
    return False

##Works
def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''analyses the sequence of length length that ends at location (y_end, x_end). The function returns "OPEN" if the sequence is open, "SEMIOPEN" if the sequence if semi-open, and "CLOSED" if the sequence is closed.'''
    if is_bounded_start(board, y_end, x_end, length, d_y, d_x) == True and is_bounded_end(board, y_end, x_end, length, d_y, d_x) == True:
        return "CLOSED"
    elif is_bounded_start(board, y_end, x_end, length, d_y, d_x) == True and is_bounded_end(board, y_end, x_end, length, d_y, d_x) == False:
        return "SEMIOPEN"
    elif is_bounded_start(board, y_end, x_end, length, d_y, d_x) == False and is_bounded_end(board, y_end, x_end, length, d_y, d_x) == True:
        return "SEMIOPEN"
    elif is_bounded_start(board, y_end, x_end, length, d_y, d_x) == False and is_bounded_end(board, y_end, x_end, length, d_y, d_x) == False:
        return "OPEN"


def is_bounded_end_col(board, col, y_start, x_start, length, d_y, d_x):
    if y_start - d_y > 7 or y_start - d_y < 0 or x_start - d_x > 7 or x_start - d_x < 0:
        return False
    if 0 <= y_start - d_y <= 7 and 0 <= x_start - d_x <= 7:
        if board[y_start - d_y][x_start - d_x] == col:
            return True

def is_bounded_start_col(board, col, y_start, x_start, length, d_y, d_x):
    if  y_start + length*d_y > 7 or y_start + length*d_y < 0 or x_start + length*d_x > 7 or x_start + length*d_x < 0:
        return False
    if 0 <= y_start + length*d_y <= 7 and 0 <= x_start + length*d_x <= 7:
        if board[y_start + length*d_y][x_start + length*d_x] == col:
            return True

## Works
def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''This function analyses the row R of squares that starts at the location (y_start,x_start)
and goes in the direction (d_y,d_x). The function returns a tuple whose first element is the number of open sequences of colour col of length length in the row R, and whose second element is the number of
semi-open sequences of colour col of length length in the row R'''
    open_seq_count = 0
    semi_open_seq_count = 0
    counter = 0
    while 0 <= y_start + (length-1)*d_y <= 7 and 0 <= x_start + (length-1)*d_x <= 7:
        for i in range(length):
            if board[y_start + i*d_y][x_start + i*d_x] == col:
                counter += 1
        if counter == length:
            if is_bounded(board, y_start, x_start, length, -d_y, -d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
                if is_bounded_end_col(board, col, y_start, x_start, length, d_y, d_x) == True:
                    semi_open_seq_count -= 1
                elif is_bounded_start_col(board, col, y_start, x_start, length, d_y, d_x) == True:
                    semi_open_seq_count -= 1
            elif is_bounded(board, y_start, x_start, length, -d_y, -d_x) == "OPEN":
                open_seq_count += 1
        y_start += d_y
        x_start += d_x
        counter = 0
    return open_seq_count, semi_open_seq_count

##Helper Functions for detect_rows start here
def detect_rows_horizontal(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_horizontal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, y_horizontal_start, 0, length, 0, 1)
        y_horizontal_start = 0
        y_horizontal_start += i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count


def detect_rows_vertical(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    x_vertical_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, 0, x_vertical_start, length, 1, 0)
        x_vertical_start = 0
        x_vertical_start += i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count

def detect_rows_diagonal_left_bottom(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_diagonal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, y_diagonal_start, 0, length, 1, 1)
        y_diagonal_start = 0
        y_diagonal_start += i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count

def detect_rows_diagonal_left_top(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    x_diagonal_start = 1
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, 0, x_diagonal_start, length, 1, 1)
        x_diagonal_start = 1
        x_diagonal_start += i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count

def detect_rows_diagonal_right_bottom(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    y_diagonal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, y_diagonal_start, 7, length, 1, -1)
        y_diagonal_start = 0
        y_diagonal_start += i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count

def detect_rows_diagonal_right_top(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    x_diagonal_start = 6
    res = ()
    for i in range(1, 9):
        res += detect_row(board, col, 0, x_diagonal_start, length, 1, -1)
        x_diagonal_start = 6
        x_diagonal_start -= i
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count


##Helper functions for detect_rows ends here

##Works?
def detect_rows(board, col, length):
    '''This function analyses the board board. The function returns a tuple, whose first element is the
number of open sequences of colour col of length length on the entire board, and whose second
element is the number of semi-open sequences of colour col of length length on the entire board.'''
    open_seq_count, semi_open_seq_count = 0, 0
    res = ()
    res += detect_rows_horizontal(board, col, length)
    res += detect_rows_vertical(board, col, length)
    res += detect_rows_diagonal_left_bottom(board, col, length)
    res += detect_rows_diagonal_left_top(board, col, length)
    res += detect_rows_diagonal_right_bottom(board, col, length)
    res += detect_rows_diagonal_right_top(board, col, length)
    for j in range(1, len(res), 2):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 2):
        open_seq_count += res[k]
    return open_seq_count, semi_open_seq_count


## Works?
def search_max(board):
    '''This function uses the function score() to find the optimal move for black. It finds the location (y,x), such that (y,x) is empty and putting a black stone on (y,x) maximizes the score of the board as calculated by score(). The function returns a tuple (y, x) such that putting a black stone in coordinates (y, x) maximizes the potential score'''
    cur_max = -100000
    move_y = 0
    move_x = 0
    board_copy = copy.deepcopy(board)
    for j in range(len(board)):
        for k in range(len(board[j])):
            if board[j][k] == " ":
                board_copy[j][k] = "b"
                if score(board_copy) > cur_max:
                    move_y = j
                    move_x = k
                    cur_max = score(board_copy)
                    board_copy = copy.deepcopy(board)
                else:
                    board_copy = copy.deepcopy(board)
    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


###
def detect_row_is_win(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    counter = 0
    while 0 <= y_start + (length-1)*d_y <= 7 and 0 <= x_start + (length-1)*d_x <= 7:
        for i in range(length):
            if board[y_start + i*d_y][x_start + i*d_x] == col:
                counter += 1
        if counter == length:
            if is_bounded(board, y_start, x_start, length, -d_y, -d_x) == "SEMIOPEN":
                semi_open_seq_count += 1
            elif is_bounded(board, y_start, x_start, length, -d_y, -d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_start, x_start, length, -d_y, -d_x) == "CLOSED":
                closed_seq_count += 1
        y_start += d_y
        x_start += d_x
        counter = 0
    return open_seq_count, semi_open_seq_count, closed_seq_count

##Helper Functions for detect_rows_is_win start here
def detect_rows_horizontal_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    y_horizontal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, y_horizontal_start, 0, length, 0, 1)
        y_horizontal_start = 0
        y_horizontal_start += i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count


def detect_rows_vertical_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    x_vertical_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, 0, x_vertical_start, length, 1, 0)
        x_vertical_start = 0
        x_vertical_start += i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows_diagonal_left_bottom_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    y_diagonal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, y_diagonal_start, 0, length, 1, 1)
        y_diagonal_start = 0
        y_diagonal_start += i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows_diagonal_left_top_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    x_diagonal_start = 1
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, 0, x_diagonal_start, length, 1, 1)
        x_diagonal_start = 1
        x_diagonal_start += i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows_diagonal_right_bottom_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    y_diagonal_start = 0
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, y_diagonal_start, 7, length, 1, -1)
        y_diagonal_start = 0
        y_diagonal_start += i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows_diagonal_right_top_is_win(board, col, length):
    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0
    x_diagonal_start = 6
    res = ()
    for i in range(1, 9):
        res += detect_row_is_win(board, col, 0, x_diagonal_start, length, 1, -1)
        x_diagonal_start = 6
        x_diagonal_start -= i
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count

##
def detect_rows_is_win(board, col, length):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    res = ()
    res += detect_rows_horizontal_is_win(board, col, length)
    res += detect_rows_vertical_is_win(board, col, length)
    res += detect_rows_diagonal_left_bottom_is_win(board, col, length)
    res += detect_rows_diagonal_left_top_is_win(board, col, length)
    res += detect_rows_diagonal_right_bottom_is_win(board, col, length)
    res += detect_rows_diagonal_right_top_is_win(board, col, length)
    for j in range(1, len(res), 3):
        semi_open_seq_count += res[j]
    for k in range(0, len(res), 3):
        open_seq_count += res[k]
    for h in range(2, len(res), 3):
        closed_seq_count += res[h]
    return open_seq_count, semi_open_seq_count, closed_seq_count
###

def is_win(board):
    res_black = ()
    res_white = ()
    counter = 0
    res_black += detect_rows_is_win(board, "b", 5)
    for i in range(len(res_black)):
        if res_black[i] == 1:
            return "Black won"
    res_white += detect_rows_is_win(board, "w", 5)
    for j in range(len(res_white)):
        if res_white[j] == 1:
            return "White won"
    for k in range(len(board)):
        for h in range(len(board[k])):
            if board[k][h] == " ":
                counter += 1
    if counter > 0:
        return "Continue playing"
    else:
        return "Draw"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

if __name__ == "__main__":
    board = make_empty_board(8)
    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)
    #
    y = 3; x = 5; d_x = -1; d_y = 1; length = 2
    #
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    #
    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)
    play_gomoku(8)

