from functools import reduce

from parser import ParserException


class arithmeticEvaluator:

    def __init__(self):
        self.operators = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide
        }

    def add(self, args, parser):
        self.valid(args)
        return reduce(lambda x, y: parser.execute(x) + parser.execute(y), args)

    def subtract(self, args, parser):
        self.valid(args)
        return reduce(lambda x, y: parser.execute(x) - parser.execute(y), args)

    def multiply(self, args, parser):
        self.valid(args)
        return reduce(lambda x, y: parser.execute(x) * parser.execute(y), args)

    def divide(self, args, parser):
        self.valid(args)
        return reduce(lambda x, y: parser.execute(x) // parser.execute(y), args)

    #Checking to see if the execute method gives an empty string: ex. if ( + ) was inputted
    def valid(self, args):
        if not args:
            raise ParserException
