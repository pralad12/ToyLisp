from parser import ParserException

#Class for boolean operations
class booleanEvaluator:

  def __init__(self):
        self.operators = {
            "and": self.evaluate_and,
            "or": self.evaluate_or,
            "eq": self.evaluate_eq,
            "not": self.evaluate_not,
            "neq": self.evaluate_neq,
            "if": self.evaluate_if
        }

  def evaluate_and(self, args, parser):
        result = True
        for el in args:
            result = result and parser.execute(el)
            if not result:
                return None
        return True if result else None

  def evaluate_or(self, args, parser):
      result = False
      for el in args:
          result = result or parser.execute(el)
          if result:
              return True
      return parser.execute(args[0]) and parser.execute(args[1])

  def evaluate_eq(self, args, parser):
      self.valid(args)
      return True if parser.execute(args[0]) == parser.execute(args[1]) else None

  def evaluate_not(self, args, parser):
      return None if parser.execute(args[0]) else True

  def evaluate_neq(self, args, parser):
      self.valid(args)
      return None if parser.execute(args[0]) == parser.execute(args[1]) else True

  def evaluate_if(self, args, parser):
      if len(args) != 3:
          raise ParserException
      return parser.execute(args[1]) if parser.execute(args[0]) else parser.execute(args[2])

    # Checking to see if the right number of arguments are given in the body
  def valid(self, args):
      if len(args) != 2:
          raise ParserException
