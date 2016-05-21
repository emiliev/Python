import collections


class Base:
    def __add__(self, other):
        op = Operator('+', lambda lhs, rhs: lhs + rhs)
        return Expression((self, op, other))

    __radd__ = __add__

    def __mul__(self, other):
        op = Operator('*', lambda lhs, rhs: lhs * rhs)
        return Expression((self, op, other))

    __rmul__ = __mul__

    def __sub__(self, other):
        op = Operator('-', lambda lhs, rhs: lhs - rhs)
        return Expression((self, op, other))

    def __rsub__(self, other):
        op = Operator('-', lambda lhs, rhs: rhs - lhs)
        return Expression((self, op, other))

    def __truediv__(self, other):
        op = Operator('/', lambda lhs, rhs: lhs / rhs)
        return Expression((self, op, other))

    def __rtruediv__(self, other):
        op = Operator('/', lambda lhs, rhs: rhs / lhs)
        return Expression((self, op, other))

    def __floordiv__(self, other):
        op = Operator('//', lambda lhs, rhs: lhs // rhs)
        return Expression((self, op, other))

    def __rfloordiv__(self, other):
        op = Operator('//', lambda lhs, rhs: rhs // lhs)
        return Expression((self, op, other))

    def __mod__(self, other):
        op = Operator("%", lambda lhs, rhs: lhs % rhs)
        return Expression((self, op, other))

    def __rmod__(self, other):
        op = Operator('%', lambda lhs, rhs: rhs % lhs)
        return Expression((self, op, other))

    def __lshif__(self, other):
        op = Operator('<<', lambda lhs, rhs: lhs << rhs)
        return Expression((self, op, other))

    def __rshift__(self, other):
        op = Operator('>>', lambda lhs, rhs: lhs >> rhs)
        return Expression((self, op, other))

    def __and__(self, other):
        op = Operator('&', lambda lhs, rhs: lhs ^ rhs)
        return Expression((self, op, other))

    def __xor__(self, other):
        op = Operator('^', lambda lhs, rhs: lhs ^ rhs)
        return Expression(self, op, other)

    def __or__(self, other):
        op = Operator('|', lambda lhs, rhs: lhs | rhs)
        return Expression(self, op, other)

    def __pow__(self, other):
        op = Operator("**", lambda lhs, rhs: lhs ** rhs)
        return Expression((self, op, other))

    def __rpow__(self, other):
        op = Operator("**", lambda lhs, rhs: rhs ** lhs)
        return Expression((self, op, other))


class Constant(Base):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def evaluate(self, **value):
        return self.value


class Variable(Base):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)

    def evaluate(self, **value):
        if self.name in value:
            return value[self.name]


class Operator:

    def __init__(self, symbol, function):
        self.symbol = symbol
        self.function = function

    def __str__(self):
        return str(self.symbol)

    def __repr__(self):
        return str(self.symbol)


class Expression(Base):

    def __init__(self, expression_structure):
        self.variable_names = {}
        self.init_variable_names(expression_structure)
        self.exp = expression_structure

    def init_variable_names(self, expression):
        for item in expression:
            if (isinstance(item, Variable)):
                self.variable_names.update({item.name: []})
            elif(isinstance(item, collections.Iterable)):
                self.init_variable_names(item)

    def evaluate(self, **variables):
        for key in variables:
            if key in self.variable_names:
                self.variable_names[key] = variables[key]

        return(self.calculate(self.exp))

    def calculate(self, expr):

        operand = self.check_collection(expr[0])
        if(isinstance(operand, Variable) and
                operand.name in self.variable_names):
            operand = self.variable_names[operand.name]
        if isinstance(operand, Constant):
            operand = operand.value
        if isinstance(operand, Expression):
            operand = operand.evaluate((operand.variable_names))
        operator = expr[1]
        operand1 = self.check_collection(expr[2])
        if (isinstance(operand1, Variable) and
                operand1.name in self.variable_names):
            operand1 = self.variable_names[operand1.name]
        if isinstance(operand1, Constant):
            operand1 = operand1.value
        if isinstance(operand1, Expression):
            operand1 = self.calculate(operand1.exp)
        return operator.function(operand, operand1)

    def check_collection(self, operand):
        if isinstance(operand, collections.Iterable):
            return self.calculate(operand)
        return operand

    def show(self):
        exp_string = "("
        exp_string += self.private_show(self.exp)
        exp_string += ")"
        return exp_string

    def private_show(self, expr):
        result = ""
        for item in expr:
            if(isinstance(item, collections.Iterable)):
                result += "("
                result += self.private_show(item)
                result += ")"
            elif (isinstance(item, Variable)):
                result += item.name
            else:
                result += " " + str(item) + " "
        return result

    def __str__(self):
        return str(self.show())


def create_constant(value):
    return Constant(value)


def create_variable(name):
    return Variable(name)


def create_operator(symbol, function):

    return Operator(symbol, function)


def create_expression(expression_structure):
    return Expression(expression_structure)
