"""
6.1010 Spring '23 Lab 8: SAT Solver
"""

#!/usr/bin/env python3

import sys
import typing
import doctest

sys.setrecursionlimit(10_000)
# NO ADDITIONAL IMPORTS


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """

    result = {}
    # base case success
    if not formula:
        return result
    
    # base case failure
    if formula ==[[]]:
        return None
    
    # check for unit clause

    unitclause = find_unit_clause(formula)
    if unitclause is not None:
        newform = update_formula(formula,unitclause)
        if newform ==[[]]:
            # print("Unit")
            return None
        recursive = satisfying_assignment(newform)
        if recursive is not None:
            result.update({unitclause[0]:unitclause[1]})
            result.update(recursive)
            return result
        else:
            return None


    if formula[0]==[]:
        return None
    else:
        variable = formula[0][0] # variable in form ('a', True)
    # test with setting variable to native value

    # new formula is variable is set to native value
    formula1 = update_formula(formula, variable) 
    # base case failure
    if formula1 != [[]]:
    #    return None
    
        recursive1 = satisfying_assignment(formula1)

        if recursive1 is not None:
            # print("recursive1")
            result.update(recursive1)
            result.update({variable[0]:variable[1]})
            return result
   
    # test with setting variable to False

    variable = (variable[0],not variable[1]) # set variable to  opposite
    formula2 = update_formula(formula, variable)
    if formula2 == [[]]:
        return None
    recursive2 = satisfying_assignment(formula2)

    if recursive2 is not None:
        # print("recursive2")
        result.update(recursive2)
        result.update({variable[0]:variable[1]})
        return result
    
    else:
        return None

    # new
    # result = {}

    # if len(formula)==0:
    #     return result
    
    # if [] in formula:
    #     return None
    
    # unitclause = find_unit_clause(formula)
    # if unitclause is not None:
    #     newform = update_formula(formula)

def update_formula(formula, value):
    """
    Update a boolean formula given a set boolean value for a variable
    Parameter: 
        formula (list): formula to update
        value (tuple): contains boolean variable name and value in the form
        ('var', Boolean)
    Returns:
        new formula
    """
   


    new_formula = []
    for clause in formula:
        new_clause = []
        to_add = True
        for literal in clause:
            if literal[0]==value[0]:
                if literal[1] is False and not value[1]:
                    to_add = False
                    break
                elif literal[1] is True and value[1]:
                    to_add = False
                    break
        #     to_add = False
        #     continue
        # elif (value[0],not value[1]) in clause:
        #     temp[i].remove((value[0],not value[1]))
            else:
                new_clause.append(literal)

        if not new_clause and to_add:
            return [[]]
        elif to_add:
            new_formula.append(new_clause)
        # new_formula.append(list(temp[i]))
    return new_formula

def find_unit_clause(formula):
    """
    Takes in a formula and returns the first occurence of a unit clause
    Returns None if unit clause is not found
    """

    for clause in formula:
        if len(clause)==1:
            return clause[0]
    return None
                
            
def sudoku_board_to_sat_formula(sudoku_board):
    """
    Generates a SAT formula that, when solved, represents a solution to the
    given sudoku board.  The result should be a formula of the right form to be
    passed to the satisfying_assignment function above.
    """
    cnf = []
    dimension = len(sudoku_board)
    for rownum, rowvals in enumerate(sudoku_board):
        for colnum, value in enumerate(rowvals):
            
            if value!=0:
                cnf.insert(0,[((value,rownum,colnum),True)])
                # constraints = get_constraint_coords((rownum,colnum),dimension)
                # for coord in constraints:
                #     cnf.append([((value,coord[0],coord[1]),False)])

            else:
                constraints = get_constraint_coords((rownum,colnum),dimension,sudoku_board)
                possible = []
                for val in range(1,dimension+1):
                    possible.append(((val,rownum,colnum),True))
                    for num in range(1,dimension+1):
                        if num!=val:
                            cnf.append([((val,rownum,colnum),False),((num,rownum,colnum),False)])
                    for thing in constraints:
                        needed = []
                        if val in thing[1]:
                            cnf.insert(0,[((val,rownum,colnum),False)])
                        else:
                            needed.append(((val,rownum,colnum),True))
                            for coord in thing[0]:
                                needed.append(((val,coord[0],coord[1]),True))
                                cnf.append([((val,rownum,colnum),False),((val,coord[0],coord[1]),False)])
                            cnf.append(needed)
                cnf.append(possible)
    cnf = simplify(cnf)
    cnf.sort(key=len)
    return cnf

def simplify(cnf):
    visited = set()
    newcnf = []
    for i in cnf:
        reverse = i[::-1]
        if tuple(i) not in visited and tuple(reverse) not in visited:
            newcnf.append(i)
            visited.add(tuple(i))
    return newcnf
    




    



def assignments_to_sudoku_board(assignments, n):
    """
    Given a variable assignment as given by satisfying_assignment, as well as a
    size n, construct an n-by-n 2-d array (list-of-lists) representing the
    solution given by the provided assignment of variables.

    If the given assignments correspond to an unsolvable board, return None
    instead.
    """
    
    if assignments is None:
        return None

    row = [0 for i in range(n)]
    solution_board = [row.copy() for i in range(n)]

    for i in assignments:
        if assignments[i] is True:
            solution_board[i[1]][i[2]] = i[0]

    return solution_board

def get_constraint_coords(coordinate, dimension, board):
    """
    Takes in a given coordinate on a board and a dimension, and returns
    the other coordinates that constrain that coordinate
    """

    row = coordinate[0]
    col = coordinate[1]

    rows = []
    rownums = set()
    columns = []
    colnums = set()
    subs = []
    subnums = set()
    
    for i in range(dimension):
        if (row,i)!=coordinate:
            rows.append((row,i))
            rownums.add(board[row][i])
        if (i,col)!=coordinate:
            columns.append((i,col))
            colnums.add(board[i][col])
    
    subdim = int(dimension**(.5))

    subrow = int(row/subdim)*subdim
    subcol = int(col/subdim)*subdim

    for i in range(subdim):
        for j in range(subdim):
            if (subrow+i,subcol+j)!=coordinate:
                subs.append((subrow+i,subcol+j))
                subnums.add(board[subrow+i][subcol+j])

    return [(rows,rownums),(columns,colnums),(subs,subnums)]

if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    # new_form = update_formula([[('a', True), ('b', True), ('c', False)], [('c', True), ('d', True)]],('c',False))
    # print(update_formula(new_form,('d',False)))
    # formula = [
    # [('a', True), ('b', True), ('c', True)],
    # [('a', False), ('f', True)],
    # [('d', False), ('e', True), ('a', True), ('g', True)],
    # [('h', False), ('c', True), ('a', False), ('f', True)],
    # ]

    # print(update_formula(update_formula(formula, ('a',True)),('f',False)))
    # formtest = [[('e',True)],[('a', True), ('b', True), ('c', False)], [('c', True), ('d', True)]]
    # print(satisfying_assignment(formtest))
    # print(update_formula(update_formula(formtest, ('a',True)),('c',True)))
    # board = [
    #     [1,0,4,0,0,0,0,0,0],
    #     [2,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,5,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,7,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0],
    #     [0,0,0,0,0,0,0,0,0]
    # ]

    
    # test = [
    #     [1,2,3,4],
    #     [3,4,0,0],
    #     [2,0,4,0],
    #     [4,0,0,1]
    # ]

    # test = [
    #         [5, 1, 7, 6, 0, 0, 0, 3, 4],
    #         [0, 8, 9, 0, 0, 4, 0, 0, 0],
    #         [3, 0, 6, 2, 0, 5, 0, 9, 0],
    #         [6, 0, 0, 0, 0, 0, 0, 1, 0],
    #         [0, 3, 0, 0, 0, 6, 0, 4, 7],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #         [0, 9, 0, 0, 0, 0, 0, 7, 8],
    #         [7, 0, 3, 4, 0, 0, 5, 6, 0],
    #         [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     ]

    # 3
    # test = [ 
    #     [0, 0, 1, 0, 0, 9, 0, 0, 3],
    #     [0, 8, 0, 0, 2, 0, 0, 9, 0],
    #     [9, 0, 0, 1, 0, 0, 8, 0, 0],
    #     [1, 0, 0, 5, 0, 0, 4, 0, 0],
    #     [0, 7, 0, 0, 3, 0, 0, 5, 0],
    #     [0, 0, 6, 0, 0, 4, 0, 0, 7],
    #     [0, 0, 8, 0, 0, 5, 0, 0, 6],
    #     [0, 3, 0, 0, 7, 0, 0, 4, 0],
    #     [2, 0, 0, 3, 0, 0, 9, 0, 0],
    # ]

    # # 6 

    test = [
        [0, 8, 0, 0, 0, 0, 0, 9, 0],  # https://sudoku.com/expert/
        [0, 1, 0, 0, 8, 6, 3, 0, 2],
        [0, 0, 0, 3, 1, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [0, 0, 0, 2, 6, 1, 0, 0, 4],
        [0, 0, 0, 5, 4, 0, 0, 0, 6],
        [3, 0, 9, 0, 0, 0, 8, 0, 0],
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    cnf = sudoku_board_to_sat_formula(test)
    # # for i,val in enumerate(cnf):
    # #     if len(val)==1:
    # #         print(i)
    # # updatetest = [[('c',False),('b',True)],[('c',True)]]
    # # c = update_formula(updatetest,('c',False))
    cnf = simplify(cnf)
    # # print(len(cnf))
    # print(cnf[:100])
    solution = satisfying_assignment(cnf)
    print(assignments_to_sudoku_board(solution,9))
    # print(get_constraint_coords((1,4),9))
