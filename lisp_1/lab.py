"""
6.1010 Spring '23 Lab 11: LISP Interpreter Part 1
"""
#!/usr/bin/env python3

import sys
import doctest

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    temp = source[:]
    temp = temp.replace("(", " ( ")
    temp = temp.replace(")", " ) ")
    lines = temp.split("\n")
    
    new_string = ""

    for line in lines:
        for char in line:
            if char==";":
                break
            if char == " ":
                try:
                    if new_string[-1]!=" ":
                        new_string+=char
                except:
                    pass
            else:
                new_string+=char
        try:
            if new_string[-1]!=" ":
                new_string+=" "
        except:
            pass

    if new_string[-1]==" ":
        new_string = new_string[:-1]
    return new_string.split(" ")


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    
    
    Helper function that parses a given token list and
    returns the symbol representaiton
    """
    
    length = len(tokens)
    is_valid(tokens, length)
    
    def parse_expression(index):
        i = index
        result = []

        while i<length and tokens[i]!=")":
            token = tokens[i]
            
            
            if token=="(":
                new = parse_expression(i+1)
                result.append(new[0])
                i = new[1]
            else:
                result.append(number_or_symbol(token))
                i+=1

        return (result, i+1)

    return parse_expression(0)[0][0]

def is_valid(tokens, length):
    """
    function to check if the list of tokens is a valid expression
    If not, raises SchemeSyntaxError
    """
    num = 0
    if tokens[0]!="(" and length!=1:
        raise SchemeSyntaxError
    
    for i in tokens:
        if i=="(":
            num+=1
        elif i==")":
            num-=1

        if num<0:
            raise SchemeSyntaxError
        elif num==0 and i !="(" and i!=")" and length!=1:
            raise SchemeSyntaxError
    
    if num!=0:
        raise SchemeSyntaxError
    

        
            


######################
# Built-in Functions #
######################

def mul(nums):
    """
    multiply function
    """
    result = 1
    for i in nums:
        result*=i
    return result

def div(nums):
    """
    division function
    """
    try:
        first = nums[0]
        try:
            test = nums[1]
        except:
            return 1/first
        for i in nums[1:]:
            first/=i
        return first
    except:
        raise Exception
    
def define(args, current_frame):
    key = args[0]
    value = args[1]
    # if isinstance(value, function):
    #     current_frame[key] = value
    # else:
    #     value = number_or_symbol(value)
    #     if type(value) is int or type(value) is float or isinstance(value,function):
    #         current_frame[key] = value
    #     else:
    #         current_frame[key] = current_frame[value]
    current_frame[key] = value
    

# def create_function(parameters, expr, frame):
#     return Function(parameters, expr, frame)
    
scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul, "/":div,
    "define": define,
}


##############
#   Frames   #
##############

class Frame():
    """ class representing frames"""

    def __init__(self, parent, default=None):
        self.parent = parent
        if default is None:
            self.vars ={}
        else:
            self.vars = default

    def __setitem__(self, key, value):
        self.vars[key] = value

    def __getitem__(self, key):

        if isinstance(key,(float,int)):
            raise SchemeEvaluationError
        
        elif key in self.vars:
        
            return self.vars[key]
        elif key not in self.vars and self.parent is None:
            raise SchemeNameError
        else:
            return self.parent.__getitem__(key)
        
    def __contains__(self, key):
        if key in self.vars:
            return True
        elif key not in self.vars and self.parent is None:
            return False
        else:
            return self.parent.__contains__(key)
  
    def get(self):
        return self.vars
    
##############
#  Function  #
##############
class Function():
    """
    Class representing lisp functions
    """
    def __init__(self, parameters, expr, encloseframe):
        self.parameters = parameters
        self.expr = expr
        self.frame = encloseframe

    def __call__(self, arguments):
        # print(f"arguments: {arguments}\nparameters: {self.parameters}")
        if len(arguments)!=len(self.parameters):
            raise SchemeEvaluationError
        
        # print(f"arguments: {arguments}")
        # evaled_args = []
        # for val in arguments:
        #     evaled_args.append(evaluate(val, self.frame))

        skeleton = ["define", None, None]
        new_frame = Frame(self.frame)

        
        for i, val in enumerate(arguments):
            skeleton[1] = self.parameters[i]
            skeleton[2] = val
            # print(f"skeleton: {skeleton}")
            evaluate(skeleton, new_frame)

        # print(f"expression {self.expr}")
        return evaluate(self.expr, new_frame)
        

##############
# Evaluation #
##############

# def single_clause_eval(tree, current_frame):
#     """
#     evaluation frame for single cluased expressions
#     """
#     if type(tree) is int or type(tree) is float:
#         return tree
#     elif type(tree) is list:
#         # if type
#         if tree[0] in current_frame:
#             if isinstance(current_frame[tree[0]],function):
#                 operation = current_frame[tree[0]]
#                 return operation.call([])
            
#             return current_frame[tree[0]]
        
#         else:
#             raise SchemeEvaluationError
#     elif type(tree) is str:
#         # print("here")
#         print("tree")
#         # if tree in scheme_builtins:
#         #     return scheme_builtins[tree[0]]
#         # elif tree in current_frame:
#         #     return current_frame[]
#         # else:
#         #     raise SchemeEvaluationError
#         if isinstance(current_frame[tree],function):
#                 operation = current_frame[tree]
#                 return operation.call([])
#         return current_frame[tree]
    

def define_eval(tree, current_frame):
    """
    evaluation branch for define
    """
    
    if isinstance(tree[1],list):
        translated = ["define", tree[1][0], ["lambda",tree[1][1:],tree[2]]]
        return evaluate(translated, current_frame)

    # for val in tree[1:]:
    #     # print(val)
    #     if type(val) is list:
    #         new_definition.append(evaluate(val,current_frame))
    #     else:
    #         new_definition.append(val)
    # print(f"new def {new_definition}")
    new_definition = [tree[1], evaluate(tree[2],current_frame)]
    define(new_definition,current_frame)
    return current_frame[new_definition[0]]



def evaluate(tree, current_frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """

    if current_frame is None:
        parent = Frame(None,scheme_builtins)
        current_frame =Frame(parent)

    if isinstance(tree,(int,float,Function)):
        return tree
    
    elif isinstance(tree,str):
        # print(f"this is the tree: {tree}")
        return current_frame[tree]
    
    operator = tree[0]

    if operator =="define":
        return define_eval(tree, current_frame)
    
    
    elif operator == "lambda":
        return Function(tree[1],tree[2], current_frame)
    
    # elif type(operator) is list and operator[0]=="define":
    #     print(operator)
    #     operation = function(tree[0][1],tree[0][2],current_frame)
    #     # print("here")
    #     try:
    #         return operation.call(tree[1:])
    #     except:
    #         raise SchemeNameError
    
    # elif type(operator) is list:
    #     operator = evaluate(operator, current_frame)
    #     try:
    #         return operator.call(tree[1:])
    #     except:
    #         raise SchemeNameError

    
    # elif isinstance(current_frame[operator],function):
    #     print(f"this is the tree: {tree}")
    #     operation = current_frame[operator]
    #     return operation.call(tree[1:])
    
    else:
        operator = evaluate(operator, current_frame)

        if not callable(operator):
            raise SchemeEvaluationError
        
        new_tree = []
        for val in tree[1:]:
            # if type(val) is list:
            #     new_frame = frame(current_frame)
            #     new_tree.append(evaluate(val,new_frame))
            # else:
            #     try:
            #         test = float(val)
            #         new_tree.append(val)
                    
            #     except:
            #         new_tree.append(current_frame[val])
            new_tree.append(evaluate(val,current_frame))
        return operator(new_tree)
            

def result_and_frame(tree, current_frame=None):
    if current_frame is None:
        parent = Frame(None, scheme_builtins)
        new_frame = Frame(parent)
        result = evaluate(tree, new_frame)
        return (result, new_frame)
    else:
        result = evaluate(tree, current_frame)
        return (result,current_frame)

def repl(verbose=False):
    """
    Read in a single line of user input, evaluate the expression, and print 
    out the result. Repeat until user inputs "QUIT"
    
    Arguments:
        verbose: optional argument, if True will display tokens and parsed
            expression in addition to more detailed error output.
    """
    import traceback
    _, frame = result_and_frame(["+"])  # make a global frame
    while True:
        input_str = input("in> ")
        if input_str == "QUIT":
            return
        try:
            token_list = tokenize(input_str)
            if verbose:
                print("tokens>", token_list)
            expression = parse(token_list)
            if verbose:
                print("expression>", expression)
            output, frame = result_and_frame(expression, frame)
            print("  out>", output)
        except SchemeError as e:
            if verbose:
                traceback.print_tb(e.__traceback__)
            print("Error>", repr(e))

if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)
    
    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    repl(True)


  
    # test = " (define circle-area (lambda (r) (* 3.14 (* r r)))) "
    # print(tokenize(test))
    # print(parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']))
    # built = frame(None, scheme_builtins)
    # globalframe = frame(built)
    # # globalframe["x"] = 2
    # new_global = frame(built)
    # test = function(["x"],["*", "x", "x"], new_global)
    # print(test.call([2]))
    # evaluate(['define', 'square', ['lambda', ['x'], ['*', 'x', 'x']]],globalframe)
    # print(globalframe.get())
    # evaluate(["square", 2],globalframe)
    
    # ['add7', [['addN', 3], [['addN', 19], 8]]]
    
    # print(evaluate([['define', 'spam', 'x'], 'eggs']))

