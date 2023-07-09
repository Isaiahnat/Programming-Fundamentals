"""
6.1010 Spring '23 Lab 4: Snekoban Game
"""

import json
import typing

# NO ADDITIONAL IMPORTS!


direction_vector = {
    "up": (-1, 0),
    "down": (+1, 0),
    "left": (0, -1),
    "right": (0, +1),
}


def new_game(level_description):
    """
    Given a description of a game state, create and return a game
    representation of your choice.

    The given description is a list of lists of lists of strs, representing the
    locations of the objects on the board (as described in the lab writeup).

    For example, a valid level_description is:

    [
        [[], ['wall'], ['computer']],
        [['target', 'player'], ['computer'], ['target']],
    ]

    The exact choice of representation is up to you; but note that what you
    return will be used as input to the other functions.

    Representation: dictionary with keys as row number and values
    as a list representing the contents of that row
    The values in the list will be sets representing what is held at that 
    inndex
    """
    transformed_game = {"height":len(level_description), 
                        "width":len(level_description[0]), 
                        "wall": set(),
                        "computer": set(),
                        "target": set()
                        }

    for i,val in enumerate(level_description):
        for j,val1 in enumerate(val):
            for k in val1:
                if k=="wall":
                    
                    transformed_game["wall"].add((i,j))

                elif k=="player":
                    transformed_game["player"] = (i,j)

                elif k=="target":
                    transformed_game["target"].add((i,j))
                
                elif k=="computer":
                    transformed_game["computer"].add((i,j))
    
    return transformed_game


def victory_check(game):
    """
    Given a game representation (of the form returned from new_game), return
    a Boolean: True if the given game satisfies the victory condition, and
    False otherwise.
    """
    if game["computer"]==game["target"] and len(game["target"])!=0:
        return True
    return False

def valid_move(game, direction):
    vector = direction_vector[direction]
    nextpos = (game["player"][0]+vector[0],game["player"][1]+vector[1])
    
    
    if nextpos in game["wall"]:
        return False
    
    doublemove = (nextpos[0]+vector[0],nextpos[1]+vector[1])

    if nextpos in game["computer"]:
        if doublemove in game["computer"] or doublemove in game["wall"]:
            return False
        
    return True





def step_game(game, direction):
    """
    Given a game representation (of the form returned from new_game), return a
    new game representation (of that same form), representing the updated game
    after running one step of the game.  The user's input is given by
    direction, which is one of the following: {'up', 'down', 'left', 'right'}.

    This function should not mutate its input.
    """

    
    if not valid_move(game, direction):
        return game.copy()
    
    newgame = {"height":game["height"], 
                        "width":game["width"], 
                        "wall": game["wall"].copy(),
                        "computer": game["computer"].copy(),
                        "target": game["target"].copy()
                        }
    
    vector = direction_vector[direction]
    new_player = (game["player"][0]+vector[0],game["player"][1]+vector[1])
    doublemove = (new_player[0]+vector[0],new_player[1]+vector[1])

    if new_player in newgame["computer"]:
        newgame["computer"].remove(new_player)
        newgame["computer"].add(doublemove)
    newgame["player"] = new_player

    return newgame

    



def dump_game(game):
    """
    Given a game representation (of the form returned from new_game), convert
    it back into a level description that would be a suitable input to new_game
    (a list of lists of lists of strings).

    This function is used by the GUI and the tests to see what your game
    implementation has done, and it can also serve as a rudimentary way to
    print out the current state of your game for testing and debugging on your
    own.
    """
    height = game["height"]
    width = game["width"]

    raw_game = []
    for i in range(height):
        raw_game.append([])
        for _ in range(width):
            raw_game[i].append([])

    place_objects(game,raw_game, "target")
    place_objects(game, raw_game, "computer")
    place_objects(game, raw_game, "wall")
    
    playerpos = game["player"]
    raw_game[playerpos[0]][playerpos[1]].append("player")

    return raw_game

def place_objects(game, rawgame, object_type):

    for i in game[object_type]:
        rawgame[i[0]][i[1]].append(object_type)



def test_state(state):
    player = state["player"]
    computer = state["computer"]
    target = state["target"]
    return (player, frozenset(computer), frozenset(target))


def solve_puzzle(game):
    """
    Given a game representation (of the form returned from new game), find a
    solution.

    Return a list of strings representing the shortest sequence of moves ("up",
    "down", "left", and "right") needed to reach the victory condition.

    If the given level cannot be solved, return None.
    """
    if victory_check(game):
        return []
    
    visited = {test_state(game)}
    queue = [game]
    paths = {test_state(game):None}
    end = None

    while queue:
        for i in direction_vector:
            next_state = step_game(queue[0],i)
            temp = test_state(next_state)

            if temp not in visited:
                queue.append(next_state)
                visited.add(temp)
                paths[temp] = (test_state(queue[0]),i)

                if victory_check(next_state):
                    end = temp
        if end!=None:
            break
        queue.pop(0)

    if end is None:
        return None

    return construct_path(paths, end)



def construct_path(path_dict, endi):
    
    moves = []
    current = endi
    while(1):
        
        if path_dict[current] is None:
            break
        direction = path_dict[current][1]
        current = path_dict[current][0]
        moves.append(direction)
    
    moves.reverse()
    return moves






if __name__ == "__main__":
    # level = [
    # [["wall"], ["wall"], ["wall"], ["wall"],     ["wall"],   ["wall"]],
    # [["wall"], [],       [],       ["target"],   ["wall"],   ["wall"]],
    # [["wall"], [],       [],       ["wall"],     ["player"], ["wall"]],
    # [["wall"], [],       [],       ["computer"], [],         ["wall"]],
    # [["wall"], [],       [],       [],           ["wall"],   ["wall"]],
    # [["wall"], ["wall"], ["wall"], ["wall"],     ["wall"],   ["wall"]]
    # ]
    # game = new_game(level)
    # next_state = step_game(game,"down")
    # next_state = step_game(next_state, "left")
    # next_state = step_game(next_state, "down")
    # next_state = step_game(next_state, "left")
    # next_state = step_game(next_state, "up")
    # next_state = step_game(next_state, "up")
    # next_state = step_game(next_state, "left")
    # next_state = step_game(next_state, "up")
    # next_state = step_game(next_state, "right")
    # print(dump_game(next_state))
    # print(victory_check(next_state))
    # test  = (frozenset({1,2,3}),frozenset({1,2,3}))
    # test1 = (frozenset({1,2,3}),frozenset({1,2,3}))
    # print(test1==test)
    # print(solve_puzzle(game))
    pass
