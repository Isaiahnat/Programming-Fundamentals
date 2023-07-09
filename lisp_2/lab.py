"""
6.1010 Spring '23 Lab 12: LISP Interpreter Part 2
"""
#!/usr/bin/env python3
import sys
sys.setrecursionlimit(20_000)

# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH YOUR lab.py FROM
# THE PREVIOUS LAB, WHICH SHOULD BE THE STARTING POINT FOR THIS LAB.


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
    current_frame[key] = value
    

def equality_test(args):
    """
    Built in equality tester
    """

    first = args[0]

    for i in args[1:]:

        if i!=first:
            return False
    
    return True


def greater_than(args):

    previous = args[0]

    for i in args[1:]:

        current = i
        if previous<=current:
            return False
        previous = current
        
    return True


def greater_equal(args):

    previous = args[0]

    for i in args[1:]:

        current = i
        if previous<current:
            return False
        previous = current
        
    return True


def less_than(args):

    previous = args[0]

    for i in args[1:]:

        current = i
        if previous>=current:
            return False
        previous = current
        
    return True


def less_equal(args):

    previous = args[0]

    for i in args[1:]:

        current = i
        if previous>current:
            return False
        previous = current
        
    return True


def not_eval(args):
    
    if not args:
        raise SchemeEvaluationError
    test = None
    try:
        test = args[1]
    except:
        pass

    if test is not None:
        raise SchemeEvaluationError
    
    val = args[0]
    return not val


def cons(args):
    if len(args)!=2:
        raise SchemeEvaluationError
    
    return Pair(args[0],args[1])


def car(args):

    if len(args)!=1 or not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    
    return args[0].get_car()


def cdr(args):

    if len(args)!=1 or not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    
    return args[0].get_cdr()


def list_create(args):

    if not args:
        return None
    
    elif len(args)==1:
        return Pair(args[0],None)
    
    else:
        return Pair(args[0],list_create(args[1:]))


def islist(args):

    if len(args)!=1:
        raise SchemeEvaluationError
    
    head = args[0]

    if head is None:
        return True
    
    elif not isinstance(head, Pair):
        return False

    def help(current):

        if current.get_cdr() is None:
            return True
        
        elif isinstance(current.get_cdr(),Pair):
            return help(current.get_cdr()) 
        
        else:
            return False
        
    return help(head)



def length(args):
    
    if len(args)!=1:
        raise SchemeEvaluationError

    elif not islist(args):
        raise SchemeEvaluationError
    
    def helper(current):

        if current.get_cdr() is None:
            return 1
        else:
            return 1+helper(current.get_cdr())
    
    pair = args[0]
    if pair is None:
        return 0
    return helper(pair)

def ref(args):

    if len(args)!=2:
        raise SchemeEvaluationError
    
    pair = args[0]
    
    if not isinstance(pair, Pair):
        raise SchemeEvaluationError
    
    index = args[1]

    def inner(current, index):

        if not isinstance(current, Pair):
            raise SchemeEvaluationError
        
        elif index==0:
            return current.get_car()
        
        elif current.get_cdr() is None:
            raise SchemeEvaluationError
        
        else:
            new = index -1
            return inner(current.get_cdr(), new)
        
    return inner(pair, index)



def append_method(args):
    
    if len(args)==0:
        return None
    
    head = None
    end_node = None

    for i in args:
        
        if not islist([i]):
            raise SchemeEvaluationError

        if i is None:
            continue
        list_copy = i.copy()

        if head is None:
            head = list_copy


        if end_node is not None:
            end_node.set_cdr(list_copy)

        end_node = get_end_node(list_copy)

    return head

def get_end_node(linked):
    
    if linked.get_cdr() is None:
        
        return linked
    
    else:
        return get_end_node(linked.get_cdr())
    
def map_func(args):
    
    func = args[0]
    head = args[1]
    if head is None:
        return None
    if not islist([head]):
        raise SchemeEvaluationError
    
    def map_helper(node):
        new_car = node.get_car()
        new_car = func([new_car])

        if node.get_cdr() is None:
            return Pair(new_car,None)
        
        else:
            return Pair(new_car,map_helper(node.get_cdr()))
        
    return map_helper(head)

def filter_func(args):
    
    func = args[0]
    head = args[1]
    if head is None:
        return None
    if not islist([head]):
        raise SchemeEvaluationError
    
    def filter_helper(node):
        car = node.get_car()
        check = func([car])

        if node.get_cdr() is None:
            if check:
                return Pair(car,None)
            else:
                return None
        
        else:
            if check:
                return Pair(car,filter_helper(node.get_cdr()))
            else:
                return filter_helper(node.get_cdr())
        
    return filter_helper(head)

def reduce_func(args):
    
    func = args[0]
    head = args[1]
    initial = args[2]

    if head is None:
        return initial
    
    if not islist([head]):
        raise SchemeEvaluationError
    
    def reduce_helper(node,val):
        car = node.get_car()
        new_car = func([val, car])

        if node.get_cdr() is None:
            return new_car
        
        else:
            return reduce_helper(node.get_cdr(),new_car)
        
    return reduce_helper(head,initial)

def begin(args):
    return args[-1]

##############
#  Builtins  #
##############

scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": mul, "/":div,
    "define": define,
    "#t": True,
    "#f": False,
    "equal?": equality_test,
    ">": greater_than,
    ">=": greater_equal,
    "<": less_than,
    "<=": less_equal,
    "not": not_eval,
    "cons": cons,
    "car": car,
    "cdr": cdr,
    "nil": None,
    "list": list_create,
    "list?": islist,
    "length": length,
    "list-ref": ref,
    "append": append_method,
    "map" : map_func,
    "filter": filter_func,
    "reduce": reduce_func,
    "begin":begin
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
        
    def remove(self, key):
        if key in self.vars:
            return self.vars.pop(key)
        else:
            raise SchemeNameError
       
    def get(self):
        return self.vars
    
    def set_val(self, var, expr):

        if var in self.vars:
            self.vars[var] = expr
        
        elif var not in self.vars and self.parent is None:
            raise SchemeNameError
        
        else:
            self.parent.set_val(var, expr)
        
    
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
        
        if len(arguments)!=len(self.parameters):
            raise SchemeEvaluationError
        

        skeleton = ["define", None, None]
        new_frame = Frame(self.frame)

        
        for i, val in enumerate(arguments):
            skeleton[1] = self.parameters[i]
            skeleton[2] = val
           
            evaluate(skeleton, new_frame)

        return evaluate(self.expr, new_frame)
    
##############
#   Pairs    #
##############

class Pair():

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr
    
    def get_car(self):
        return self.car
    
    def get_cdr(self):
        return self.cdr
    
    def copy(self):
        if self.cdr is None:
            return Pair(self.car,self.cdr)
        else:
            return Pair(self.car, self.cdr.copy())
    
    def set_cdr(self, val):
        self.cdr = val
        

##############
#  File Eval #
##############

def evaluate_file(file_name, frame=None):

    with open(file_name, 'r') as data:
        line = data.read()
        return evaluate(parse(tokenize(line)),frame)

##############
# Evaluation #
##############


def define_eval(tree, current_frame):
    """
    evaluation branch for define
    """
    
    if isinstance(tree[1],list):
        translated = ["define", tree[1][0], ["lambda",tree[1][1:],tree[2]]]
        return evaluate(translated, current_frame)

    new_definition = [tree[1], evaluate(tree[2],current_frame)]
    define(new_definition,current_frame)
    return current_frame[new_definition[0]]

def and_eval(tree, current_frame):
    """
    evaluation branch for and operator
    """
    
    for i in tree[1:]:

        if not evaluate(i, current_frame):
            return False
    
    return True

def or_eval(tree, current_frame):
    """
    evaluation branch for and operator
    """
    
    for i in tree[1:]:

        if evaluate(i, current_frame):
            return True
        
    return False

def if_eval(tree, current_frame):

    boolean = evaluate(tree[1],current_frame)
    
    if boolean:
        return evaluate(tree[2], current_frame)
    else:
        return evaluate(tree[3],current_frame)
    
def let_eval(tree, current_frame):
    values = []

    for i in tree[1]:
        values.append((i[0],evaluate(i[1],current_frame)))
    
    skeleton = ["define", None, None]

    new_frame = Frame(current_frame)
    for vals in values:
        skeleton[1] = vals[0]
        skeleton[2] = vals[1]

        evaluate(skeleton,new_frame)
    
    return evaluate(tree[-1],new_frame)

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

    if tree ==[]:
        raise SchemeEvaluationError
    
    elif tree is None:
        return None
    
    elif isinstance(tree,(int,float,Function,Pair)):
        return tree

    elif isinstance(tree,str):
        return current_frame[tree]
    
    elif callable(tree):
        return tree
    
    operator = tree[0]
    

    if operator =="define":
        return define_eval(tree, current_frame)
    
    
    elif operator == "lambda":
        return Function(tree[1],tree[2], current_frame)
    
    elif operator == "and":
        return and_eval(tree, current_frame)
    
    elif operator == "or":
        return or_eval(tree, current_frame)
    
    elif operator == "if":
        return if_eval(tree, current_frame)
    
    elif operator =="del":
        return current_frame.remove(tree[1])
    
    elif operator == "let":
        return let_eval(tree,current_frame)
    
    elif operator == "set!":
        expr = evaluate(tree[2],current_frame)
        current_frame.set_val(tree[1],expr)
        return expr
        
    else:
        operator = evaluate(operator, current_frame)

        if not callable(operator):
            raise SchemeEvaluationError
        
        new_tree = []
        for val in tree[1:]:
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
    for data_name in sys.argv[1:]:
        evaluate_file(data_name,frame)

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
    





