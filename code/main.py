from math import sqrt, pi
from os import linesep

from functions import *
from parser import parse, parse_variable


def calculateValue(function, replacements):
    print("Your function is")
    print('Algebraic representation: $' + str(function) + '$ \\\\')
    print('With numbers: $' + function.prnt(replacements) + '$ \\\\')
    return function.evaluate(replacements)
    
    
def calculateError(function, replacements, error_replacements):
    print("Error calculations")
    variables = replacements.keys()
    s = 0
    c = list()
    d = list()
    for variable in variables:
        s += (function.derivate(variable).evaluate(replacements)*error_replacements[variable])**2
        d.append('(' + str(function.derivate(variable).simplify().simplify()) + '\\cdot\\Delta ' + str(variable) + ')^2')
        cv = str(function.derivate(variable).evaluate(replacements))
        if 'e' in cv:
            cv = cv.replace('e', '\\cdot 10^{') + '}'
        cv2 = str(error_replacements[variable])
        if 'e' in cv2:
            cv2 = cv2.replace('e', '\\cdot 10^{') + '}'
        c.append('(' + cv + '\\cdot ' + cv2 + ')^2')
        print("$\\frac{\\partial}{\\partial "+ variable +"} = " + str(function.derivate(variable).simplify().simplify())+"$\\\\")
    print('Algebraic representation: \\\\ $\sqrt{\\begin{aligned}' + ' \\\\ + '.join(d) + '\\end{aligned}}$ \\\\')
    print('With numbers: \\\\ $\sqrt{\\begin{aligned}' + ' \\\\ + '.join(c) + '\\end{aligned}}$ \\\\')
    return sqrt(s)


def main_menu():
    replacements = {}
    error_replacements = {}
    while True:
        print("Enter function (command =) or define variable (command :) or quit (command q)")
        i = input()
        if i == '=':
            print("Enter your function. Seperate arguments by brackets or spaces. Operators are + - * / ^ (only for constant exponents) sin cos log. Mathematical constants: math.pi, math.e")
            s = input()
            function, replacements, error_replacements = parse(s, replacements, error_replacements)
            function = function.simplify().simplify()
            print("Mean: "  + '$' + str(calculateValue(function, replacements)) + '$\\\\')
            print("Error: " + '$' + str(calculateError(function, replacements, error_replacements)) + '$\\\\')
            print("Have fun at removing useless parts and cleaning formatting!")
        elif i == ':':
            print("What is the identifier of your variable?", end=' ')
            li = input()
            replacements, error_replacements = parse_variable(li, replacements, error_replacements)
        elif i == 'q':
            print("quit.")
            return None
        else:
            print("Unrecognized command, try again.")


if __name__=="__main__":
    
    main_menu()
    


