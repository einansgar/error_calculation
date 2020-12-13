""" Contain some function to convert an input string to usable mathematical constructs. """

from math import sqrt, pi
import sys

from functions import *


class structure:
    """ Element to create the parsing tree."""
    def __init__(self):
        """ Create a new structure with a list of deeper level entries. """
        self.li = list()
        self.counter = -1
    def append(self, item, depth):
        """ Add the new item to this level or pass it to deeper levels if depth > 0.
        
        Arguments:
        item -- str or structure
        depth -- how far the item should be passed into the tree, 0 if to be appended here.
        """
        if isinstance(item, str) and len(item) == 0:
            pass
        elif depth == 0:
            self.counter += 1
            self.li.append(item)
        else:
            self.li[self.counter].append(item, depth-1)
    def return_as_list(self):
        """ Convert self to a nested list and return that. """
        li = list()
        if len(self.li) == 1:
            if isinstance(self.li[0], structure):
                return self.li[0].return_as_list()
        for item in self.li:
            if isinstance(item, structure):
                li.append(item.return_as_list())
            else:
                li.append(item)
        return li
        
  
def parse_variable(li, r, e):
    """ Get value and error of a variable from the input and add it to the dictionaries r and e.
    
    Arguments:
    li -- name of the variable (str)
    r -- dictionary of mean values
    e -- dictionary of error values
    """
    print('Enter value and error of ' + li + ', separated by comma: ', end='')
    mean = None
    error = None
    while mean is None or error is None:
        try:
            i = input()
            s = i.split(',')
            mean = float(s[0])
            error = float(s[1])
        except:
            print("That did not work, try again!")
    r[li] = mean
    e[li] = error
    print(li + ":= " + str(mean) + " +/- " + str(error))
    return r, e
      
        
def get_structure(string):
    """ Take a string and return the related structure if possible (may raise errors). """
    level = structure()
    current_symbol = list()
    current_depth = 0
    for i in range(len(string)):
        if string[i] == '(':
            level.append(''.join(current_symbol), current_depth)
            current_symbol = list()
            level.append(structure(), current_depth)
            current_depth += 1
        elif string[i] == ')':
            level.append(''.join(current_symbol), current_depth)
            current_symbol = list()
            current_depth -= 1
        elif string[i] == ' ':
            level.append(''.join(current_symbol), current_depth)
            current_symbol = list()
        else:
            current_symbol.append(string[i])
    level.append(''.join(current_symbol), current_depth)
    return level.return_as_list()

def get_functions(li, r, e):
    """ Take a nested list and build together the related functions recursively.
    
    Arguments:
    li -- nested list like returned from structure.return_as_list()
    r -- dictionary of means
    e -- dictionary of errors
    """
    if len(li) == 1:
        if isinstance(li, list):
            return get_functions(li[0], r, e)
    if isinstance(li, str) or len(li) == 1:
        if not isinstance(li, str):
            li = li[0]
        try:
            return Constant(float(li)), r, e
        except:
            if li in ('math.e', 'math.pi'):
                return MathConstant(li), r, e
            else:
                if not li in r:
                    r, e = parse_variable(li, r, e)
                return Variable(li), r, e                
    elif li[0] == 'log':
        f, r, e = get_functions(li[1], r, e)
        return Logarithm(f), r, e
    elif li[0] == 'sin':
        f, r, e = get_functions(li[1], r, e)
        return Sine(f), r, e
    elif li[0] == 'cos':
        f, r, e = get_functions(li[1], r, e)
        return Cosine(f), r, e
    elif '+' in li:
        pos = li.index('+')
        f1, r, e = get_functions(li[0:pos], r, e)
        f2, r, e = get_functions(li[pos+1:len(li)], r, e)
        return Sum(f1, f2), r, e
    elif '-' in li:
        pos = li.index('-')
        if pos != 0:
            f1, r, e = get_functions(li[0:pos], r, e)
            f2, r, e = get_functions(li[pos+1:len(li)], r, e)
            return Difference(f1, f2), r, e
        f, r, e = get_functions(li[0:pos], r, e)
        return Negate(f), r, e # ignore the remaining parts
    elif '*' in li:
        pos = li.index('*')
        f1, r, e = get_functions(li[0:pos], r, e)
        f2, r, e = get_functions(li[pos+1:len(li)], r, e)
        return Product(f1, f2), r, e
    elif '/' in li:
        pos = li.index('/')
        f1, r, e = get_functions(li[0:pos], r, e)
        f2, r, e = get_functions(li[pos+1:len(li)], r, e)
        return Quotient(f1, f2), r, e
    elif '^' in li:
        pos = li.index('^')
        f1, r, e = get_functions(li[0:pos], r, e)
        f2, r, e = get_functions(li[pos+1:len(li)], r, e)
        if isinstance(f2.simplify().simplify(), Constant) or isinstance(f2.simplify().simplify(), MathConstant):
            return PowConstant(f1, f2.simplify().simplify().value), r, e
        return Pow(f1, f2), r, e
        
        
def parse(string, replacements, replacements_error):
    """ Take a string and return the related function if there is no error in between. 
    
    Will return Constant(0) at any error, be careful.
    Arguments:
    string -- str of function
    replacements -- dictionary of means
    replacements_error -- dictionary of errors
    """
    try:
        todo_list = get_structure(string)
        return get_functions(todo_list, replacements, replacements_error)
    except ZeroDivisionError:
        print("PARSE ERROR Divison by zero")
    except MathDomainError:
        print("PARSE ERROR MathDomain")
    except:
        print("PARSE ERROR ", sys.exec_info()[0])
        raise
    return Constant(0)

