"""
6.1010 Spring '23 Lab 7: Mines
"""

#!/usr/bin/env python3

import typing
import doctest

# NO ADDITIONAL IMPORTS ALLOWED!


def dump(game):
    """
    Prints a human-readable version of a game (provided as a dictionary)
    """
    for key, val in sorted(game.items()):
        if isinstance(val, list) and val and isinstance(val[0], list):
            print(f"{key}:")
            for inner in val:
                print(f"    {inner}")
        else:
            print(f"{key}:", val)


# 2-D IMPLEMENTATION


def new_game_2d(num_rows, num_cols, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.

    Parameters:
       num_rows (int): Number of rows
       num_cols (int): Number of columns
       bombs (list): List of bombs, given in (row, column) pairs, which are
                     tuples

    Returns:
       A game state dictionary

    >>> dump(new_game_2d(2, 4, [(0, 0), (1, 0), (1, 1)]))
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: [(0, 0), (1, 0), (1, 1)]
    dimensions: (2, 4)
    hidden:
        [True, True, True, True]
        [True, True, True, True]
    revealed: 0
    state: ongoing
    """
    # board = []
    # hidden = []
    # for r in range(num_rows):
    #     boardrow = []
    #     hiddenrow = []
    #     for c in range(num_cols):
    #         if (r, c) in bombs:
    #             boardrow.append(".")
    #         else:
    #             boardrow.append(count_neighbors(r,c,bombs))
    #         hiddenrow.append(True)
    #     board.append(boardrow)
    #     hidden.append(hiddenrow)

    # # for r in range(num_rows):
    # #     for c in range(num_cols):
    # #         if board[r][c] == 0:
    # #             neighbor_bombs = 0
    # #             if 0 <= r - 1 < num_rows:
    # #                 if 0 <= c - 1 < num_cols:
    # #                     if board[r - 1][c - 1] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r < num_rows:
    # #                 if 0 <= c - 1 < num_cols:
    # #                     if board[r][c - 1] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r + 1 < num_rows:
    # #                 if 0 <= c - 1 < num_cols:
    # #                     if board[r + 1][c - 1] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r - 1 < num_rows:
    # #                 if 0 <= c < num_cols:
    # #                     if board[r - 1][c] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r < num_rows:
    # #                 if 0 <= c < num_cols:
    # #                     if board[r][c] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r + 1 < num_rows:
    # #                 if 0 <= c < num_cols:
    # #                     if board[r + 1][c] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r - 1 < num_rows:
    # #                 if 0 <= c + 1 < num_cols:
    # #                     if board[r - 1][c + 1] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r < num_rows:
    # #                 if 0 <= c + 1 < num_cols:
    # #                     if board[r][c + 1] == ".":
    # #                         neighbor_bombs += 1
    # #             if 0 <= r + 1 < num_rows:
    # #                 if 0 <= c + 1 < num_cols:
    # #                     if board[r + 1][c + 1] == ".":
    # #                         neighbor_bombs += 1
    # #             board[r][c] = neighbor_bombs

    # return {
    #     "dimensions": (num_rows, num_cols),
    #     "board": board,
    #     "hidden": hidden,
    #     "state": "ongoing",
    #     "bombs": bombs,
    #     "revealed": 0
    # }
    return new_game_nd((num_rows,num_cols),bombs)

# def count_neighbors(row, col, bombs):
#     """
#     Counts the number of neighboring bombs at a given coordinate

#     Parameters:
#         row (int): the row at which the coordinate lies
#         col (int): the col at which the coordinate lies
#         bombs (list): a list of tuples containing all of the coordinates
#         of the bombs

#     Returns:
#         int: number of neighboring bombs
#     """
#     indexes = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
#     count = 0
#     for radd,cadd in indexes:
#         temprow = row+radd
#         tempcol = col+cadd

#         if (temprow,tempcol) in bombs:
#             count+=1
#     return count



def dig_2d(game, row, col):
    """
    Reveal the cell at (row, col), and, in some cases, recursively reveal its
    neighboring squares.

    Update game['hidden'] to reveal (row, col).  Then, if (row, col) has no
    adjacent bombs (including diagonally), then recursively reveal (dig up) its
    eight neighbors.  Return an integer indicating how many new squares were
    revealed in total, including neighbors, and neighbors of neighbors, and so
    on.

    The state of the game should be changed to 'defeat' when at least one bomb
    is revealed on the board after digging (i.e. game['hidden'][bomb_location]
    == False), 'victory' when all safe squares (squares that do not contain a
    bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Parameters:
       game (dict): Game state
       row (int): Where to start digging (row)
       col (int): Where to start digging (col)

    Returns:
       int: the number of new squares revealed

    >>> game = {'dimensions': (2, 4),
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'bombs': [(0,0),(1,0),(1,1)],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'revealed': 1,
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 3)
    4
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: [(0, 0), (1, 0), (1, 1)]
    dimensions: (2, 4)
    hidden:
        [True, False, False, False]
        [True, True, False, False]
    revealed: 5
    state: victory

    >>> game = {'dimensions': [2, 4],
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'bombs': [(0, 0), (1, 0),(1, 1)],
    ...         'hidden': [[True, False, True, True],
    ...                  [True, True, True, True]],
    ...         'revealed': 1,
    ...         'state': 'ongoing'}
    >>> dig_2d(game, 0, 0)
    1
    >>> dump(game)
    board:
        ['.', 3, 1, 0]
        ['.', '.', 1, 0]
    bombs: [(0, 0), (1, 0), (1, 1)]
    dimensions: [2, 4]
    hidden:
        [False, False, True, True]
        [True, True, True, True]
    revealed: 2
    state: defeat
    """
    # if game["state"] == "defeat" or game["state"] == "victory":
    #     # game["state"] = game["state"]  # keep the state the same
    #     return 0

    # if game["board"][row][col] == ".":
    #     game["hidden"][row][col] = False
    #     game["state"] = "defeat"
    #     game["revealed"]+=1
    #     return 1

    # # game state Check
    # # bombs = 0
    # # hidden_squares = 0
    # # for r in range(game["dimensions"][0]):
    # #     for c in range(game["dimensions"][1]):
    # #         if game["board"][r][c] == ".":
    # #             if game["hidden"][r][c] == False:
    # #                 bombs += 1
    # #         elif game["hidden"][r][c] == True:
    # #             hidden_squares += 1
    # # if bombs != 0:
    # #     # if bombs is not equal to zero, set the game state to defeat and
    # #     # return 0
    # #     game["state"] = "defeat"
    # #     return 0
    # # if hidden_squares == 0:
    # #     game["state"] = "victory"
    # #     return 0

    # # victory check


    # #checks if already revealed or not
    # if game["hidden"][row][col] != False:
    #     game["hidden"][row][col] = False
    #     game["revealed"]+=1
    #     revealed = 1
    # else:
    #     return 0
    # #checks if already revealed or not


    # indexes = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

    # if game["board"][row][col]==0:
    #     for radd,cadd in indexes:
    #         num_rows, num_cols = game["dimensions"]
    #         temprow = row+radd
    #         tempcol = col+cadd
    #         if 0<=temprow<num_rows and 0<=tempcol<num_cols:
    #             if game["hidden"][temprow][tempcol] == True:
    #                 revealed += dig_2d(game, temprow, tempcol)


    #hard coded logic to revealed when it is 0
    # if game["board"][row][col] == 0:
        
    #     num_rows, num_cols = game["dimensions"]
    #     if 0 <= row - 1 < num_rows:
    #         if 0 <= col - 1 < num_cols:
    #             if game["board"][row - 1][col - 1] != ".":
    #                 if game["hidden"][row - 1][col - 1] == True:
    #                     revealed += dig_2d(game, row - 1, col - 1)
    #     if 0 <= row < num_rows:
    #         if 0 <= col - 1 < num_cols:
    #             if game["board"][row][col - 1] != ".":
    #                 if game["hidden"][row][col - 1] == True:
    #                     revealed += dig_2d(game, row, col - 1)
    #     if 0 <= row + 1 < num_rows:
    #         if 0 <= col - 1 < num_cols:
    #             if game["board"][row + 1][col - 1] != ".":
    #                 if game["hidden"][row + 1][col - 1] == True:
    #                     revealed += dig_2d(game, row + 1, col - 1)
    #     if 0 <= row - 1 < num_rows:
    #         if 0 <= col < num_cols:
    #             if game["board"][row - 1][col] != ".":
    #                 if game["hidden"][row - 1][col] == True:
    #                     revealed += dig_2d(game, row - 1, col)
    #     if 0 <= row < num_rows:
    #         if 0 <= col < num_cols:
    #             if game["board"][row][col] != ".":
    #                 if game["hidden"][row][col] == True:
    #                     revealed += dig_2d(game, row, col)
    #     if 0 <= row + 1 < num_rows:
    #         if 0 <= col < num_cols:
    #             if game["board"][row + 1][col] != ".":
    #                 if game["hidden"][row + 1][col] == True:
    #                     revealed += dig_2d(game, row + 1, col)
    #     if 0 <= row - 1 < num_rows:
    #         if 0 <= col + 1 < num_cols:
    #             if game["board"][row - 1][col + 1] != ".":
    #                 if game["hidden"][row - 1][col + 1] == True:
    #                     revealed += dig_2d(game, row - 1, col + 1)
    #     if 0 <= row < num_rows:
    #         if 0 <= col + 1 < num_cols:
    #             if game["board"][row][col + 1] != ".":
    #                 if game["hidden"][row][col + 1] == True:
    #                     revealed += dig_2d(game, row, col + 1)
    #     if 0 <= row + 1 < num_rows:
    #         if 0 <= col + 1 < num_cols:
    #             if game["board"][row + 1][col + 1] != ".":
    #                 if game["hidden"][row + 1][col + 1] == True:
    #                     revealed += dig_2d(game, row + 1, col + 1)

    # hard coded logic to revealed when it is 0

    # game state check
    # bombs = 0  # set number of bombs to 0
    # hidden_squares = 0
    # for r in range(game["dimensions"][0]):
    #     # for each r,
    #     for c in range(game["dimensions"][1]):
    #         # for each c,
    #         if game["board"][r][c] == ".":
    #             if game["hidden"][r][c] == False:
    #                 # if the game hidden is False, and the board is '.', add 1 to
    #                 # bombs
    #                 bombs += 1
    #         elif game["hidden"][r][c] == True:
    #             hidden_squares += 1
    # bad_squares = bombs + hidden_squares
    # if bad_squares > 0:
        # game["state"] = "ongoing"
        # game["revealed"]+=revealed
        # return revealed
    # else:
    #     game["state"] = "victory"
    #     # print(game)
    #     # print("\n\n\n\n\n\n")
    #     game["revealed"]+=revealed
    
    # set_game_state(game)
    # return revealed
    
    # game state check

    return dig_nd(game,(row,col))

# def set_game_state(game):
#     """
#     updates the state of the game as either victory or ongoing
#     doesn't account for defeat since it's accounted for dig

#     Parameters:
#         game (dict): Game State

#     Returns:
#         None
#     """
#     total = game["dimensions"][0]*game["dimensions"][1]
#     if game["state"] != "defeat":
#         if game["revealed"]==total-len(game["bombs"]):
#             game["state"] = "victory"
#         else:
#             game["state"] = "ongoing"


def render_2d_locations(game, xray=False):
    """
    Prepare a game for display.

    Returns a two-dimensional array (list of lists) of '_' (hidden squares),
    '.' (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  game['hidden'] indicates which squares should be hidden.  If
    xray is True (the default is False), game['hidden'] is ignored and all
    cells are shown.

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the that are not
                    game['hidden']

    Returns:
       A 2D array (list of lists)

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, False, True],
    ...                   [True, True, False, True]]}, False)
    [['_', '3', '1', '_'], ['_', '_', '1', '_']]

    >>> render_2d_locations({'dimensions': (2, 4),
    ...         'state': 'ongoing',
    ...         'board': [['.', 3, 1, 0],
    ...                   ['.', '.', 1, 0]],
    ...         'hidden':  [[True, False, True, False],
    ...                   [True, True, True, False]]}, True)
    [['.', '3', '1', ' '], ['.', '.', '1', ' ']]
    """
    # display = []
    # values = {0:" ", 1:"1", 2:"2", 3:"3",4:"4",5:"5",
    #           6:"6", 7:"7", 8:"8", ".":"."
    #           }
    # for row in range(game["dimensions"][0]):
    #     temprow = []
    #     for col in range(game["dimensions"][1]):
    #         if xray or not game["hidden"][row][col]:
    #             current = game["board"][row][col]
    #             temprow.append(values[current])
    #         else:
    #             temprow.append("_")
    #     display.append(temprow)
    # return display

    return render_nd(game,xray)


def render_2d_board(game, xray=False):
    """
    Render a game as ASCII art.

    Returns a string-based representation of argument 'game'.  Each tile of the
    game board should be rendered as in the function
        render_2d_locations(game)

    Parameters:
       game (dict): Game state
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       A string-based representation of game

    >>> render_2d_board({'dimensions': (2, 4),
    ...                  'state': 'ongoing',
    ...                  'board': [['.', 3, 1, 0],
    ...                            ['.', '.', 1, 0]],
    ...                  'hidden':  [[False, False, False, True],
    ...                            [True, True, False, True]]})
    '.31_\\n__1_'
    """
    transformed = render_2d_locations(game,xray)
    strboard = ""
    for row in transformed:
        for val in row:
            strboard += val
        strboard+="\n"
    strboard = strboard[:-1]
    return strboard


# N-D IMPLEMENTATION


def new_game_nd(dimensions, bombs):
    """
    Start a new game.

    Return a game state dictionary, with the 'dimensions', 'state', 'board' and
    'hidden' fields adequately initialized.


    Args:
       dimensions (tuple): Dimensions of the board
       bombs (list): Bomb locations as a list of tuples, each an
                     N-dimensional coordinate

    Returns:
       A game state dictionary

    >>> g = new_game_nd((2, 4, 2), [(0, 0, 1), (1, 0, 0), (1, 1, 1)])
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: [(0, 0, 1), (1, 0, 0), (1, 1, 1)]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, True], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    revealed: 0
    state: ongoing
    """
    hidden = skeleton_maker(dimensions, True)
    board = skeleton_maker(dimensions,None)
    allcoords = possible_coordinates(dimensions)
    bombset = set(bombs)
    for coord in allcoords:
        if coord in bombset:
            val = "."
        else:
            val = ncount_neighbors(coord,dimensions,bombset)
        nset_val(board,coord,val)

    return {
        "board": board,
        "bombs": bombs,
        "dimensions": dimensions,
        "hidden": hidden,
        "revealed": 0,
        "state": "ongoing"
    }

def nset_val(board, coord, val):
    """
    Given a board and a coordinate, set
    the value at each coordinate to val

    Args:
        board (list): n dimensional list representing board
        coord (tuple): tuple representing desired coordinate
        val: desired val

    Returns
        None
    """
    if len(coord)==1:
        board[coord[0]] = val
    else:
        nset_val(board[coord[0]],coord[1:], val)

def nset_val_list(board, coords, val):
    """
    same as nset_val but instead takes in a list of coordinates

    Args:
        board (list): n dimensional list representing board
        coords (list): list of tuples representing desired coordinates
        val: desired val
    """
    for coord in coords:
        nset_val(board,coord,val)

def nget_val(board, coord):
    """
    Given a board and a coordinate, get
    the value at each coordinate

    Args:
        board (list): n dimensional list representing board
        coord (tuple): tuple representing desired coordinate

    Returns
        value at index
    """
    if len(coord)==1:
        return board[coord[0]]
    else:
        return nget_val(board[coord[0]],coord[1:])
    
def nget_val_list(board, coords):
    """
    same as nget_val but instead takes in a list of coordinates

    Args:
        board (list): n dimensional list representing board
        coords (list): list of tuples representing desired coordinates
        
    returns:
        list of values at coordinates
    """
    result = []
    for coord in coords:
        result.append(nget_val(board,coord))
    return result


    

    
def skeleton_maker(dimensions,val):
    """
    take in specified dimensions and returns a n dimensional
    list where each element at the innermost list is val

    Args:
        dimensions (tuple): board dimensions
        val: desired val

    return:
        n dimensional list
    """
    result = []
    if len(dimensions)==1:
        for _ in range(dimensions[0]):
            result.append(val)
    
    else:
        for _ in range(dimensions[0]):
            result.append(skeleton_maker(dimensions[1:],val))
    
    return result


def possible_coordinates(dimensions):
    """
    takes in specified dimensions and returns a list of tuples 
    where each tuple represents a coordinate

    Args:
        dimensions (tuple): board dimensions

    Returns:
        list
    """
    result = []

    if len(dimensions)==1:
        for i in range(dimensions[0]):
            result.append((i,))
    else:
        for i in range(dimensions[0]):
            for coord in possible_coordinates(dimensions[1:]):
                result.append((i,)+coord)
    
    return result

def nfind_neighbors(coord, dimensions):
    """
    takes in a coordinate of n dimension and returns a list of 
    tuples corresponding to the neighboring coordinates

    Args:
        coord (tuple): desired coordinate

    Returns:
        list
    """
    result = []
    if len(coord)==1:
        x = coord[0]
        if x-1>=0:
            result.append((x-1,))
        result.append((x,))
        if x+1<dimensions[0]:
            result.append((x+1,))
    
    else:
        for tup in nfind_neighbors(coord[1:],dimensions[1:]):
            x = coord[0]
            if x-1>=0:
                result.append((x-1,)+tup)
            result.append((x,)+tup)
            if x+1<dimensions[0]:
                result.append((x+1,)+tup)
    return result



def ncount_neighbors(coord, dimensions, bombs):
    """
    Computes how many bombs are neighboring a set coordinate

    Arguments:
        coord (tuple): desired coordinate
        dimensions (tuple): dimensions of game board
        bombs (list): list containg coordinates of bombs

    returns:
        int representing number of neighboring bombs
    """
    neighbors = nfind_neighbors(coord, dimensions)
    neighbors.remove(coord)
    count = 0
    for neighbor in neighbors:
        if neighbor in bombs:
            count+=1
    return count




def dig_nd(game, coordinates):
    """
    Recursively dig up square at coords and neighboring squares.

    Update the hidden to reveal square at coords; then recursively reveal its
    neighbors, as long as coords does not contain and is not adjacent to a
    bomb.  Return a number indicating how many squares were revealed.  No
    action should be taken and 0 returned if the incoming state of the game
    is not 'ongoing'.

    The updated state is 'defeat' when at least one bomb is revealed on the
    board after digging, 'victory' when all safe squares (squares that do
    not contain a bomb) and no bombs are revealed, and 'ongoing' otherwise.

    Args:
       coordinates (tuple): Where to start digging

    Returns:
       int: number of squares revealed

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'bombs': [(0,0,1),(1,0,0),(1,1,1)],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'revealed': 1,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 3, 0))
    8
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: [(0, 0, 1), (1, 0, 0), (1, 1, 1)]
    dimensions: (2, 4, 2)
    hidden:
        [[True, True], [True, False], [False, False], [False, False]]
        [[True, True], [True, True], [False, False], [False, False]]
    revealed: 9
    state: ongoing
    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'bombs': [(0,0,1),(1,0,0),(1,1,1)],
    ...      'hidden': [[[True, True], [True, False], [True, True],
    ...                [True, True]],
    ...               [[True, True], [True, True], [True, True],
    ...                [True, True]]],
    ...      'revealed': 1,
    ...      'state': 'ongoing'}
    >>> dig_nd(g, (0, 0, 1))
    1
    >>> dump(g)
    board:
        [[3, '.'], [3, 3], [1, 1], [0, 0]]
        [['.', 3], [3, '.'], [1, 1], [0, 0]]
    bombs: [(0, 0, 1), (1, 0, 0), (1, 1, 1)]
    dimensions: (2, 4, 2)
    hidden:
        [[True, False], [True, False], [True, True], [True, True]]
        [[True, True], [True, True], [True, True], [True, True]]
    revealed: 2
    state: defeat
    """

    if game["state"] == "defeat" or game["state"] == "victory":
        return 0

    if nget_val(game["board"],coordinates) == ".":
        nset_val(game["hidden"],coordinates,False)
        game["state"] = "defeat"
        game["revealed"]+=1
        return 1
    
    #checks if already revealed or not
    if nget_val(game["hidden"],coordinates) != False:
        nset_val(game["hidden"],coordinates,False)
        game["revealed"]+=1
        revealed = 1
    else:
        return 0
    


    

    if nget_val(game["board"],coordinates) == 0:
        # for radd,cadd in indexes:
        #     num_rows, num_cols = game["dimensions"]
        #     temprow = row+radd
        #     tempcol = col+cadd
        #     if 0<=temprow<num_rows and 0<=tempcol<num_cols:
        #         if game["hidden"][temprow][tempcol] == True:
        #             revealed += dig_2d(game, temprow, tempcol)
        neighbors = nfind_neighbors(coordinates, game["dimensions"])
        # print(neighbors)
        vals = nget_val_list(game["hidden"], neighbors)
        # print(vals)

        for i, neighbor in enumerate(neighbors):
            if vals[i]==True:
                revealed += dig_nd(game, neighbor)

    nset_game_state(game)
    return revealed



def nset_game_state(game):
    """
    scans the game and sets the state of the game accordingly
    It only handles ongoing vs victory because dig
    Args:
        game (dict): game to be adjusted
    """
    if game["state"] != "defeat":
        total = 1
        for i in game["dimensions"]:
            total*=i
        if total == len(game["bombs"])+game["revealed"]:
            game["state"] = "victory"
    
    
    

def render_nd(game, xray=False):
    """
    Prepare the game for display.

    Returns an N-dimensional array (nested lists) of '_' (hidden squares), '.'
    (bombs), ' ' (empty squares), or '1', '2', etc. (squares neighboring
    bombs).  The game['hidden'] array indicates which squares should be
    hidden.  If xray is True (the default is False), the game['hidden'] array
    is ignored and all cells are shown.

    Args:
       xray (bool): Whether to reveal all tiles or just the ones allowed by
                    game['hidden']

    Returns:
       An n-dimensional array of strings (nested lists)

    >>> g = {'dimensions': (2, 4, 2),
    ...      'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    ...                [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    ...      'hidden': [[[True, True], [True, False], [False, False],
    ...                [False, False]],
    ...               [[True, True], [True, True], [False, False],
    ...                [False, False]]],
    ...      'state': 'ongoing'}
    >>> render_nd(g, False)
    [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
     [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

    >>> render_nd(g, True)
    [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
     [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
    """

    result = skeleton_maker(game["dimensions"], None)
    allcoords = possible_coordinates(game["dimensions"])

    for coord in allcoords:

        if xray:
            val = nget_val(game["board"],coord)
            if type(val) != str:
                    val = str(val)
            if val =="0":
                val = " "
            nset_val(result,coord,val)

        else:
            ishidden = nget_val(game["hidden"],coord)
            if ishidden:
                nset_val(result,coord,"_")
            else:
                val = nget_val(game["board"],coord)
                if type(val) != str:
                    val = str(val)
                if val =="0":
                    val = " "
                nset_val(result,coord,val)
    return result

if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual lab.py functions.
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    # Alternatively, can run the doctests JUST for specified function/methods,
    # e.g., for render_2d_locations or any other function you might want.  To
    # do so, comment out the above line, and uncomment the below line of code.
    # This may be useful as you write/debug individual doctests or functions.
    # Also, the verbose flag can be set to True to see all test results,
    # including those that pass.
    #
    #doctest.run_docstring_examples(
    #    render_2d_locations,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=False
    # )

    # print(nfind_neighbors((5,13,0),(10,20,3)))
    # print(ncount_neighbors((0,0,0),(2,4,2),[(0, 0, 1), (1, 0, 0), (1, 1, 1)]))
    # skeleton = skeleton_maker((3,3,2),True)
    # print(possible_coordinates((3,3,2)))
    # nset_val(skeleton,(0,0,0),False)
    # print(skeleton)
    # print(nget_val(skeleton,(0,0,0)))
    # g = {'dimensions': (2, 4, 2),
    # 'board': [[[3, '.'], [3, 3], [1, 1], [0, 0]],
    #                 [['.', 3], [3, '.'], [1, 1], [0, 0]]],
    #       'bombs': [(0,0,1),(1,0,0),(1,1,1)],
    #       'hidden': [[[True, True], [True, False], [True, True],
    #                 [True, True]],
    #                [[True, True], [True, True], [True, True],
    #                 [True, True]]],
    #       'revealed': 1,
    #       'state': 'ongoing'}
    # dig_nd(g, (0, 0, 1))
    # dig_nd(g, (0, 3, 0))
    # print(skeleton_maker((2,4,2),False)) # skeletons is efficient
    print(possible_coordinates((10,10,10))) # possible coords effiecient
    
    
    
