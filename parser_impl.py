from array import array
from lib2to3.pgen2.token import tok_name
from parser import Parser, ParserException, Binding
import ply.lex as lex
import ply.yacc as yacc
from functools import reduce
import arithmetic
import boolean
import assign
import function 

# TO_DO:  SUBTRACT, INTEGER DIVISION, EQ, NEG, NOT, AND, OR, UNKNOWN, IF

class Parser_Impl(Parser):

  #Name the token as num - lexical rule. Other rules will be added later
  tokens = [ 'INT', 'LPAREN', 'RPAREN', 'BOOLEAN', 'OP', 'SYMB']

  #Will implement later
  def set_binding( self, binding ):
    pass

  #Regular expression rule 
  t_LPAREN = r'\('
  t_RPAREN = r'\)'
  t_OP = r'[\*\+-\/] | if | and | or | eq | neq | not '
  t_SYMB = r'[a-z][a-z0-9_]*'
  
  #This ignores tabs, spaces, new line, and comments when parsing
  t_ignore = ' \t\n' 
  t_ignore_COMMENT = r'\#.*'

  #Assign integer value to token
  def t_INT(self, t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

  def t_BOOLEAN(self, t):
    r'True|\(\)'
    if t.value == r'()':
      t.value = False
    else:
      t.value = True
    return t
  
  #Error if tokenizer does not encounter a legal character
  def t_error(self, t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

  #Func to calculate return result - NEED TO REFACTOR
  def execute(self, args):
    # print("args", args)
    if type(args) == list:
        if type(args[0]) == list:
          res = self.execute(args[0])
          if type(res) == dict:
            return self.fun.executefunc(res, args[1:], self)
          else:
            for el in args[1:]:
              res = self.execute(el)
          return res
        else:
          for frame in self.stack[::-1]:
              if args[0] in frame:
                if type(frame[args[0]]) == dict:
                  return self.fun.executefunc(frame[args[0]], args[1:], self)
                return frame[args[0]](args[1:], self)
    else:
      #If the return value is not a string (boolean or assignment), return it
      return_val = args
      if type(return_val) != str:
         return return_val
      else:
         #Search the stack
         for namespace in self.stack[::-1]:
            if return_val in namespace:
              return_val = namespace[return_val]
              return return_val
         self.stack.pop()
         raise ParserException(("Unknown Variable"))

  #Function to parse a given string and execute the return list
  def evaluate(self, input):
    input = yacc.parse(input)
    return self.execute(input)

  #Initialize lex and yacc to module itself because it is needed to tokenize and parse
  def __init__(self):
    lex.lex(module = self)
    yacc.yacc(module = self)
    #Operators for other classes
    self.operators = {**arithmetic.arithmeticEvaluator().operators, **boolean.booleanEvaluator().operators, **assign.assignVar().operators, **function.functionImpl().operations}
    self.stack = [self.operators]
    self.binding = Binding.SHALLOW
    self.fun = function.functionImpl()

  #Grammar rules___________________________________________

  #End of recursion
  def p_treetop(self, p):
    ''' treetop : funcs '''
    p[0] = p[1]
    #print("Treetop:", p[0])
    
  def p_funcs_multiple( self, p ):
    ''' funcs : func funcs '''
    p[0] = [p[1], *p[2]]

  def p_funcs_singular( self, p ):
    ''' funcs : func '''
    p[0] = [p[1]]

  def p_func_atoms( self, p ):
    ''' func : LPAREN atoms RPAREN '''
    p[0] = [*p[2]]

  def p_func_empty( self, p ):
    ''' func : LPAREN RPAREN '''
    p[0] = None

  def p_atoms_plural(self, p):
    ''' atoms : atom atoms '''
    p[0] = [p[1], *p[2]]

  def p_atoms_singular(self, p):
    ''' atoms : atom '''
    p[0] = [p[1]]

  def p_atom(self, p):
    ''' atom : func
            | INT
            | BOOLEAN
            | OP
            | SYMB '''
    p[0] = p[1]

  def p_error(self, p):
    print("Syntax error found!")
   


