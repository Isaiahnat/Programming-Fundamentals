"""
6.1010 Spring '23 Lab 10: Symbolic Algebra
"""

import doctest


# NO ADDITIONAL IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.


class Symbol:
    """Parent Class"""
    precedence = 0
    right_parens = False
    left_parens = False

    def __add__(self, exp):
        return Add(self, exp)
    
    def __radd__(self, exp):
        return Add(exp, self)
    
    def __sub__(self, exp):
        return Sub(self, exp)
    
    def __rsub__(self, exp):
        return Sub(exp, self)
    
    def __mul__(self, exp):
        return Mul(self, exp)
    
    def __rmul__(self, exp):
        return Mul(exp, self)
    
    def __truediv__(self, exp):
        return Div(self, exp)
    
    def __rtruediv__(self, exp):
        return Div(exp, self)
    
    def __pow__(self,exp):
        return Pow(self, exp)
    
    def __rpow__(self,exp):
        return Pow(exp, self)
    
    def eval(self,mapping):
        return self.evaluate(mapping)

    def simplify(self):
        return self

class Var(Symbol):
    """Class in which instances represent variables"""
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n

    def copy(self):
        return Var(self.name)
    
    def get_attribute(self):
        return self.name

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Var('{self.name}')"
    
    def evaluate(self, mapping):
        if self.name not in mapping:
            raise NameError
        return mapping[self.name]

    def __eq__(self, other):
        
        return  bool(isinstance(other,Var) and self.name == other.name)
        # if type(other)==Var and self.name == other.name:
        #     return True
        # else:
        #     return False
    
    def deriv(self, respect):
        if respect == self.name:
            return Num(1)
        else:
            return Num(0)
        

class Num(Symbol):
    """Class in which instances represent numbers"""
    
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n
    def get_attribute(self):
        return self.n
    
    def copy(self):
        return Num(self.n)
    
    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return f"Num({self.n})"
    
    def evaluate(self,mapping):
        return self.n
    
    def __eq__(self, other):
        return bool(isinstance(other,Num) and self.n==other.n)
        # if type(other)==Num and self.n == other.n:
        #     return True
        # else:
        #     return False
        
    def deriv(self,respect):
        return Num(0)
    
    
class BinOp(Symbol):
    """Class in which instances represent the result of binary operators"""
    name = {"+":"Add","-":"Sub","*":"Mul","/":"Div", "**":"Pow"}
    pre = {"+":3,"-":3,"*":2,"/":2,"**":1}
    

    def __init__(self, left, right):
        self.left = None
        self.right = None
        if isinstance(left, (int,float)):
            self.left = Num(left)
        elif isinstance(left, str):
            self.left = Var(left)
        else:
            self.left = left

        if isinstance(right, int) or isinstance(right, float):
            self.right = Num(right)
        elif isinstance(right, str):
            self.right = Var(right)
        else:
            self.right = right

    def get_attribute(self):
        return (self.left,self.right)
    
    def __repr__(self):
        return f"{BinOp.name[self.operator]}({repr(self.left)}, {repr(self.right)})"
    
    def __str__(self):
        leftstr = None
        rightstr = None
        if self.left_parens and self.left.precedence>=BinOp.pre[self.operator]:
            leftstr = f"({str(self.left)})"
        elif self.left.precedence>BinOp.pre[self.operator]:
            leftstr = f"({str(self.left)})"
        else:
            leftstr = str(self.left)
        if self.right_parens and self.right.precedence==BinOp.pre[self.operator]:
            rightstr =f"({str(self.right)})"
        elif self.right.precedence>BinOp.pre[self.operator]:
            
            rightstr = f"({str(self.right)})"
        else:
            rightstr = str(self.right)
        
        return f"{leftstr} {self.operator} {rightstr}"
    
    def __eq__(self, other):
        return bool(type(other)==type(self) and self.left == other.left and self.right==other.right)
        
        

class Add(BinOp):
    """Class in which instances represent the result of addition"""
    precedence = 3
    operator = "+"
    right_parens = False

    def evaluate(self, mapping):
        return self.left.evaluate(mapping)+self.right.evaluate(mapping)
    
    def copy(self):
        return Add(self.left,self.right)
    
    def deriv(self, respect):
        return self.left.deriv(respect)+self.right.deriv(respect)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left,Num) and isinstance(right,Num):
            return Num(left.get_attribute()+right.get_attribute())
        elif left.get_attribute()==0:
            return right.copy()
        elif right.get_attribute()==0:
            return left.copy()
        else:
            return Add(left.copy(),right.copy())




class Sub(BinOp):
    """Class in which instances represent the result of subtraction"""
    precedence = 3
    operator = "-"
    right_parens = True

    def evaluate(self, mapping):
        return self.left.evaluate(mapping)- self.right.evaluate(mapping)
    
    def deriv(self, respect):
        return self.left.deriv(respect)-self.right.deriv(respect)
    
    def copy(self):
        return Sub(self.left,self.right)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left,Num) and isinstance(right,Num):
            return Num(left.get_attribute()-right.get_attribute())
        elif right.get_attribute()==0:
            return left.copy()
        else:
            return Sub(left.copy(),right.copy())
    
class Mul(BinOp):
    """Class in which instances represent the result of multiplication"""
    precedence = 2
    operator = "*"
    right_parens = False

    def evaluate(self, mapping):
        return self.left.evaluate(mapping)*self.right.evaluate(mapping)
    
    def deriv(self, respect):
        return self.left*self.right.deriv(respect)+self.right*self.left.deriv(respect)
    
    def copy(self):
        return Mul(self.left,self.right)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left,Num) and isinstance(right,Num):
            return Num(left.get_attribute()*right.get_attribute())
        elif left.get_attribute()==0:
            return Num(0)
        elif right.get_attribute()==0:
            return Num(0)
        elif left.get_attribute()==1:
            return right.copy()
        elif right.get_attribute()==1:
            return left.copy()
        else:
            return Mul(left.copy(),right.copy())


class Div(BinOp):
    """Class in which instances represent the result of division"""
    precedence = 2
    operator = "/"
    right_parens = True

    def evaluate(self, mapping):
        return self.left.evaluate(mapping)/self.right.evaluate(mapping)
    
    def deriv(self, respect):
        return (self.right*self.left.deriv(respect)-self.left*self.right.deriv(respect))/(self.right*self.right)

    def copy(self):
        return Div(self.left,self.right)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left,Num) and isinstance(right,Num):
            return Num(left.get_attribute()/right.get_attribute())
        elif left.get_attribute()==0:
            return Num(0)
        elif right.get_attribute()==1:
            return left.copy()
        else:
            return Div(left.copy(),right.copy())
        
class Pow(BinOp):
    """Class in which instances represent the result of a power"""

    precedence = 1
    operator = "**"
    right_parens = False
    left_parens = True

    def evaluate(self, mapping):
        return self.left.evaluate(mapping)**self.right.evaluate(mapping)
    
    def deriv(self, respect):
        if type(self.right) != Num:
            raise TypeError
        return self.right*(self.left**Sub(self.right.get_attribute(),1))*self.left.deriv(respect)

    def copy(self):
        return Pow(self.left,self.right)
    
    def simplify(self):
        left = self.left.simplify()
        right = self.right.simplify()
        
        if isinstance(left,Num) and isinstance(right,Num):
            return Num(left.get_attribute()**right.get_attribute())
        elif left.get_attribute()==0:
            return Num(0)
        elif right.get_attribute()==1:
            return left.copy()
        elif right.get_attribute()==0:
            return Num(1)
        else:
            return Pow(left.copy(),right.copy())

        
def expression(string):
    """
    takes in a string representing an algebraic expression and
    converts it two an instance of a child of the symbol class
    """
    tokens = tokenize(string)
    return parse(tokens)
        
def tokenize(exp):
    """
    Takes in an expression in string format and returns the 
    corresponding symbolic representation

    Parameters:
        Expression - String representing expression to be converted

    Returns:
        instance of a Child of class Symbol
    """

    newstring = exp.replace("(","( ").replace(")"," )")
    return newstring.split(" ")
    


def parse(tokens):
    """
    Helper function that parses a given token list and
    returns the symbol representaiton
    """
    operands = {"+","-", "*","/","**"}
    parens = {"(",")"}
    classes = {"+":Add,"-":Sub,"*":Mul,"/":Div, "**":Pow}

    def parse_expression(index):
        try:
            num = float(tokens[index])
            return (Num(num),index+1)
        except:
            val = tokens[index]
            if val not in operands and val not in parens:
                return(Var(val),index+1)
            elif val==")":
                return parse_expression(index+1)
            else:
                left = parse_expression(index+1)
                # operand = tokens[left[1]]
                # print(f"left: {left} operand: {operand}")
                # add = 0
                # if operand not in operands:
                #     operand = tokens[left[1]+1]
                #     add = 1
                index = left[1] 
                while tokens[index] not in operands: 
                    index+=1
                operand = tokens[index]
                sym = classes[operand]
                right = parse_expression(index+1)
                return (sym(left[0],right[0]),right[1])
            
    parsed_expression, next_index = parse_expression(0)
    return parsed_expression

if __name__ == "__main__":
    doctest.testmod()
    # z = Add(Var('x'), Sub(Var('y'), Num(2)))
    # y = repr(z)  # notice that this result, if fed back into Python, produces an equivalent object.
    # print(y)
    # #"Add(Var('x'), Sub(Var('y'), Num(2)))"
    # print(str(z))  # this result cannot necessarily be fed back into Python, but it looks nicer.
    # print(repr(Var("y")))
    # # 'x + y - 2'
    # print(Mul(Var('x'), Add(Var('y'), Var('z'))))
    # print(Add(Num(0),Mul(Var('y'),Num(2))))

    # thing = Div(2,3)
    # print(thing.right_parens)
    # Div.right_parens = False
    # print(thing.right_parens)
    # test = Mul(Var('z'), Div(Num(0), Var('x')))
    # print(test)

    # z = Add(Var('x'), Sub(Var('y'), Mul(Var('z'), Num(2))))
    # print(z.eval({'x': 3, 'y': 10, 'z': 2}))

    # print(Add(Num(4), Var('x')) == Add(Num(4), Var('x')))
    # x = Var('x')
    # y = Var('y')
    # z = 2*x - x*y + 3*y
    # print(z.deriv('x'))  # unsimplified, but the following gives us (2 - y)
    # 2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
    # print(z.deriv('y'))  # unsimplified, but the following gives us (-x + 3)
    # 2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0
    # w = Div(x, y)
    # print(w.deriv('x'))
    # (y * 1 - x * 0) / (y * y)
    # print(repr(w.deriv('x')))  # deriv always returns a new Symbol object
    # Div(Sub(Mul(Var('y'), Num(1)), Mul(Var('x'), Num(0))), Mul(Var('y'), Var('y')))
    y = Var("y")
    x = Var("x")
    z = 2*x - x*y + 3*y
    print(z.simplify())
    # 2 * x - x * y + 3 * y
    print(z.deriv('x'))
    # 2 * 1 + x * 0 - (x * 0 + y * 1) + 3 * 0 + y * 0
    print(z.deriv('x').simplify())
    # 2 - y
    # print(z.deriv('y'))
    # 2 * 0 + x * 0 - (x * 1 + y * 0) + 3 * 1 + y * 0
    # print(z.deriv('y').simplify())
    # 0 - x + 3
    # print(Add(Add(Num(2), Num(-2)), Add(Var('x'), Num(0))).simplify())
    # Var('x')
    # test = '(x * (-2.333 + 3.23) - 5)'
    # print(tokenize(test))
    # tokens = tokenize("(x * (2 + 3))")
    # print(repr(expression("(x * (2 + 3))")))
    # Mul(Var('x'), Add(Num(2), Num(3)))
    # print(repr(2 ** Var('x')))
    # Pow(Num(2), Var('x'))
    # x = expression('(x ** 2)')
    # print(repr(x.deriv('x')))
    # Mul(Mul(Num(2), Pow(Var('x'), Sub(Num(2), Num(1)))), Num(1))
    # print(x.deriv('x').simplify())
    # 2 * x
    # print(Pow(Add(Var('x'), Var('y')), Num(1)))
    # (x + y) ** 1
    # print(Pow(Add(Var('x'), Var('y')), Num(1)).simplify())
    # x + y
    # test = Pow(Num(0),Var("x"))
    # print(test.simplify())
    # exp = Pow(Add(Var('x'), Var('y')), Num(4))
    # print(exp.deriv("x"))
        