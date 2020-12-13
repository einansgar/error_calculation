""" Contain several mathematical functions.

Each provides the following functionality:
- __init__(arg, [arg2]) -- construct a new function of this type with the given value(s)
- __str__() -- convert the function to algebraic representation
- prnt(replacements) -- Return a string with the values inserted (replacements is a dict)
- evaluate(replacements) -- Return a double of the value at the specified values (replacements is a dict)
- derivate(variable) -- Return a function which should be identical to the 1st derivative by variable (variable is a str)
- simplify() -- Return a function which should do the same but in a less complex way.
- contains(variable) -- Return whether the function makes any use of the variable (variable is a str)
"""
from math import log, inf, pi, e, cos, sin


class Sum:

    def __init__(self, summand1, summand2):
        """Create a new sum.
        
        Arguments:
        summand1, summand2 -- function
        """
        self.summand1 = summand1
        self.summand2 = summand2
        
    def evaluate(self, replacements):
        return summand1.evaluate(replacements) + summand2.evaluate(replacements)
        
    def derivate(self, variable):
        if not self.summand1.contains(variable):
            if not self.summand2.contains(variable):
                return Constant(0)
            return summand2.derivate(variable)
        if not self.summand2.contains(variable):
            return summand1.derivate(variable)
        return self
        
    def simplify(self):
        self.summand1 = self.summand1.simplify()
        self.summand2 = self.summand2.simplify()
        if isinstance(self.summand1, Constant):
            if isinstance(self.summand2, Constant):
                return Constant(self.summand1.value + self.summand2.value)
            elif self.summand1.value == 0:
                return self.summand2
        elif isinstance(self.summand2, Constant) and self.summand2.value == 0:
            return self.summand1
        return self
        
    def contains(self, variable):
        return self.summand1.contains(variable) or self.summand2.contains(variable)
        
    def __str__(self):
        return '(' + str(self.summand1) + '+' + str(self.summand2) + ')'
        
    def prnt(self, replacements):
        return '(' + self.summand1.prnt(replacements) + '+' + self.summand2.prnt(replacements) + ')'


class Constant:

    def __init__(self, value: float):
        """Create a new constant with value."""
        self.value = value
        
    def evaluate(self, replacements):
        return self.value
        
    def derivate(self, variable):
        return Constant(0)
        
    def simplify(self):
        return self
        
    def contains(self, variable):
        return False
        
    def __str__(self):
        if 'e' in str(self.value):
            return str(self.value).replace('e', '\\cdot 10^{') + '}'
        return str(self.value)
        
    def prnt(self, replacements):
        if 'e' in str(self.value):
            return str(self.value).replace('e', '\\cdot 10^{') + '}'
        return str(self.value)


class MathConstant:

    def __init__(self, name: str):
        if name == 'math.pi':
            self.value = pi
            self.name = '\\pi'
        elif name == 'math.e':
            self.value = e
            self.name = 'e'
        else:
            self.value = 1 # should not be the case
            self.name = '<unknown constant>'
            
    def evaluate(self, replacements):
        return self.value
        
    def derivate(self, variable):
        return Constant(0)
        
    def simplify(self):
        return self
        
    def contains(self, variable):
        return False
        
    def __str__(self):
        return self.name
        
    def prnt(self, replacements):
        return self.name # should display itself as pi, e, ...


class Negate:

    def __init__(self, entry):
        """ Create a negation of the function in entry. """
        self.entry = entry
        
    def evaluate(self, replacements):
        return -1 * self.entry.evaluate(replacements)
        
    def derivate(self, variable):
        if not self.entry.contains(variable):
            return Constant(0)
        return Negate(self.entry.derivate(variable))
    
    def simplify(self):
        self.entry = self.entry.simplify()
        if isinstance(self.entry, Constant):
            return Constant(-self.entry.value)
        if isinstance(self.entry, Negate):
            return self.entry.entry
        return self
        
    def contains(self, variable):
        return self.entry.contains(variable)
        
    def __str__(self):
        return '(-' + str(self.entry) + ')'
        
    def prnt(self, replacements):
        return '(-' + self.entry.prnt(replacements) + ')'
        
        
class Difference:

    def __init__(self, minuend, subtrahend):
        """ Create a difference of the functions minuend, subtrahend. """
        self.minuend = minuend
        self.subtrahend = subtrahend
        
    def evaluate(self, replacements):
        return self.minuend.evaluate(replacements) - self.subtrahend.evaluate(replacements)
        
    def derivate(self, variable):
        return Difference(self.minuend.derivate(variable), self.subtrahend.derivate(variable))
        
    def simplify(self):
        self.minuend = self.minuend.simplify()
        self.subtrahend = self.subtrahend.simplify()
        if isinstance(self.minuend, Constant):
            if isinstance(self.subtrahend, Constant):
                return Constant(self.minuend.value - self.subtrahend.value)
            elif self.minuend.value == 0:
                return Negate(self.subtrahend)
        elif isinstance(self.subtrahend, Constant) and self.subtrahend.value == 0:
            return self.minuend
        return self
        
    def contains(self, variable):
        return self.minuend.contains(variable) or self.subtrahend.contains(variable)
        
    def __str__(self):
        return '(' + str(self.minuend) + '-' + str(self.subtrahend) + ')'
        
    def prnt(self, replacements):
        return '(' + self.minuend.prnt(replacements) + '-' + self.subtrahend.prnt(replacements) + ')'


class Product:

    def __init__(self, factor1, factor2):
        """ Create a product with the functions factor1, factor2. """
        self.factor1 = factor1
        self.factor2 = factor2
        
    def evaluate(self, replacements):
        return self.factor1.evaluate(replacements)*self.factor2.evaluate(replacements)
        
    def derivate(self, variable):
        if not self.factor1.contains(variable):
            if not self.factor2.contains(variable):
                return Constant(0)
            return Product(self.factor1, self.factor2.derivate(variable))
        if not self.factor2.contains(variable):
            return Product(self.factor1.derivate(variable), self.factor2)            
        return Sum(Product(self.factor1, self.factor2.derivate(variable)), Product(self.factor1.derivate(variable), self.factor2))
        
    def simplify(self):
        self.factor1 = self.factor1.simplify()
        self.factor2 = self.factor2.simplify()
        if isinstance(self.factor1, Constant):
            if isinstance(self.factor2, Constant):
                return Constant(self.factor1.value * self.factor2.value)
            if self.factor1.value == 0:
                return self.factor2
            elif self.factor1.value == 1:
                return self.factor2
            elif self.factor1.value == -1:
                return Negate(self.factor2)
        elif isinstance(self.factor2, Constant):
            if self.factor2.value == 0:
                return self.factor1
            elif self.factor2.value == 1:
                return self.factor1
            elif self.factor2.value == -1:
                return Negate(self.factor1)
        return self
        
    def contains(self, variable):
        return self.factor1.contains(variable) or self.factor2.contains(variable)
        
    def __str__(self):
        return str(self.factor1) + '\\cdot ' + str(self.factor2)
        
    def prnt(self, replacements):
        return self.factor1.prnt(replacements) + '\\cdot ' + self.factor2.prnt(replacements)
        
        
class Variable:
    def __init__(self, name: str):
        self.name = name
        
    def evaluate(self, replacements):
        return replacements[self.name]
        
    def derivate(self, variable):
        if variable == self.name:
            return Constant(1)
        return Constant(0)
        
    def simplify(self):
        return self
        
    def contains(self, variable):
        return self.name == variable
        
    def __str__(self):
        return self.name
        
    def prnt(self, replacements):
        s = str(replacements[self.name])
        if 'e' in s:
            return s.replace('e', '\\cdot 10^{') + '}'
        return s


class Cosine:
    def __init__(self, entry):
        """ Create the Cosine of the entry function. """
        self.entry = entry
        
    def evaluate(self, replacements):
        return cos(self.entry.evaluate(replacements))
        
    def derivate(self, variable):
        if not self.entry.contains(variable):
            return Constant(0)
        return Product(Negate(Sine(self.entry)), self.entry.derivate(variable))
        
    def simplify(self):
        self.entry = self.entry.simplify()
        if isinstance(self.entry, Constant):
            return Constant(cos(self.entry.value))
        return self
        
    def contains(self, variable):
        return self.entry.contains(variable)
        
    def __str__(self):
        return '\\cos{(' + str(self.entry) + ')}'
        
    def prnt(self, replacements):
        return '\\cos{(' + self.entry.prnt(replacements) + ')}'


class Sine:
    def __init__(self, entry):
        """ Create the sine of the entry function. """
        self.entry = entry
        
    def evaluate(self, replacements):
        return sin(self.entry.evaluate(replacements))
        
    def derivate(self, variable):
        if not self.entry.contains(variable):
            return Constant(0)
        return Product(Cosine(self.entry), self.entry.derivate(variable))
        
    def simplify(self):
        self.entry = self.entry.simplify()
        if isinstance(self.entry, Constant):
            return Constant(sin(self.entry.value))
        return self
        
    def contains(self, variable):
        return self.entry.contains(variable)
        
    def __str__(self):
        return '\\sin{(' + str(self.entry) + ')}'
        
    def prnt(self, replacements):
        return '\\sin{(' + self.entry.prnt(replacements) + ')}'
    

class PowConstant:
    def __init__(self, base, exponent: float):
        """ Create a pow function with a constant exponent and a function as base. """
        self.base = base
        if exponent - int(exponent) == 0:
            exponent = int(exponent)
        self.exponent = exponent # has to be a number
        
    def evaluate(self, replacements):        
        return self.base.evaluate(replacements) ** self.exponent
        
    def derivate(self, variable):
        if self.exponent == 0:
            return Constant(0)
        elif not self.base.contains(variable):
            return Constant(0)
        elif self.exponent == 1:
            return self.base.derivate(variable)
        return Product(Product(Constant(self.exponent), PowConstant(self.base, self.exponent-1)), self.base.derivate(variable))
        
    def simplify(self):
        self.base = self.base.simplify()
        if self.exponent == 0:
            return Constant(1)
        elif isinstance(self.base, PowConstant):
            return PowConstant(self.base.base, self.exponent + self.base.exponent)
        elif self.exponent == 1:
            return self.base
        elif isinstance(self.base, Constant):
            return Constant(self.base.value ** self.exponent)
        return self
            
    def contains(self, variable):
        return self.base.contains(variable)
        
    def __str__(self):
        return '(' + str(self.base) + ')^{' + str(self.exponent) + '}'
        
    def prnt(self, replacements):
        return '(' + self.base.prnt(replacements) + ')^{' + str(self.exponent) + '}'


class Pow:
    def __init__(self, base, exponent):
        """ Create the pow function of functions base, exponent (base ^ exponent)."""
        self.base = base
        self.exponent = exponent
        
    def evaluate(self, replacements):
        return self.base.evaluate(replacements) ** self.exponent.evaluate(replacements)
        
    def derivate(self, variable):
        if (isinstance(self.base.simplify(), MathConstant) 
                and self.base.simplify().name == 'e'):
            return Product(self, self.exponent.derivate(variable))
        if not self.base.contains(variable):
            if not self.exponent.contains(variable):
                return Constant(0)
            return Product(Product(self, self.exponent.derivate(variable)), Logarithm(self.base))
        if not self.exponent.contains(variable):
            return Product(Pow(self.base, Difference(self.exponent, Constant(1))), Product(self.exponent, self.base.derivate(variable)))
        return Product(Pow(self.base, Difference(self.exponent, Constant(1))), 
                        Sum(Product(self.exponent, self.base.derivate(variable)), 
                        Product(Product(self.base, self.exponent.derivate(variable)),
                        Logarithm(self.base))))
                        
    def simplify(self):
        self.exponent = self.exponent.simplify()
        self.base = self.base.simplify()
        if isinstance(self.exponent, Constant):
            return PowConstant(self.base, self.exponent.value).simplify()
        if isinstance(self.base, Constant):
            if self.base.value == 0:
                return Constant(0)
            elif self.base.value == 1:
                return Constant(1)
        if isinstance(self.exponent, Logarithm):
            return self.exponent.entry
        return self
        
    def contains(self, vaiable):
        return self.exponent.contains(variable) or self.base.contains(variable)
        
    def __str__(self):
        return '(' + str(self.base) + ')^{' + str(self.exponent) + '}'
        
    def prnt(self, replacements):
        return '(' + self.base.prnt(replacements) + ')^{' + self.exponent.prnt(replacements) + '}'
        
        
class Quotient:
    def __init__(self, dividend, divisor):
        """ Create a quotient of functions dividend, divisor. """
        self.dividend = dividend
        self.divisor = divisor
        
    def evaluate(self, replacements):
        return self.dividend.evaluate(replacements)/self.divisor.evaluate(replacements)
        
    def derivate(self, variable):
        if not self.divisor.contains(variable):
            return Quotient(self.dividend.derivate(variable), self.divisor)
        elif not self.dividend.contains(variable):
            return Negate(Quotient(Product(self.dividend, self.divisor.derivate(variable)), PowConstant(self.divisor, 2)))
        return Quotient(Difference(Product(self.dividend.derivate(variable), self.divisor), Product(self.dividend, self.divisor.derivate(variable))), PowConstant(self.divisor, 2))
        
    def simplify(self):
        self.divisor = self.divisor.simplify()
        self.dividend = self.dividend.simplify()
        if isinstance(self.divisor, Constant) and self.divisor.value == 0:
            return Constant(inf) # mathematically incorrect, nvm
        elif isinstance(self.dividend, Constant):
            if self.dividend.value == 0:
                return Constant(0)
            elif isinstance(self.divisor, Constant):
                return Constant(self.dividend.value / self.divisor.value)
            elif self.dividend.value == 1:
                return PowConstant(self.divisor, -1)
            elif self.dividend.value == -1:
                return Negate(PowConstant(self.divisor, -1))
        elif isinstance(self.divisor, Constant):
            if self.divisor.simplify().value == 1:
                return self.dividend
            elif self.divisor.value == -1:
                return Negate(self.dividend)
        return self
        
    def contains(self, variable):
        return self.dividend.contains(variable) or self.divisor.contains(variable)
        
    def __str__(self):
        return "\\frac{" + str(self.dividend) + '}{' + str(self.divisor) + '}'
        
    def prnt(self, replacements):
        return "\\frac{" + self.dividend.prnt(replacements) + '}{' + self.divisor.prnt(replacements) + '}'


# not supported
class Logarithm:

    def __init__(self, entry):
        """ Create the Logarithm of the entry function. """
        self.entry = entry
        
    def evaluate(self, replacements):
        return log(self.entry.evaluate(replacements))
        
    def derivate(self, variable):
        return Quotient(self.entry.derivate(variable), self.entry)
        
    def simplify(self):
        self.entry = self.entry.simplify()
        if isinstance(self.entry, Constant):
            if self.entry.value > 0:
                return Constant(log(self.entry.value))
        if isinstance(self.entry, Pow) and isinstance(self.entry.base, MathConstant) and self.entry.base.name == 'e':
            return self.entry.exponent        
        return self
        
    def contains(self, variable):
        return self.entry.contains(variable)
        
    def __str__(self):
        return '\\log{' + str(self.entry) + '}'
        
    def prnt(self, replacements):
        return '\\log{' + self.entry.prnt(replacements) + '}'


        
