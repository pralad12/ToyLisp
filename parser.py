import abc
from enum import Enum
class ParserException( Exception ):
  pass
class Binding( Enum ):
  DEEP = 1
  SHALLOW = 2
  ADHOC = 3
class Parser( metaclass = abc.ABCMeta ):
  @abc.abstractmethod
  def evaluate( self, input ):
    '''return the result of parsing the given input'''
    return
  @abc.abstractmethod
  def set_binding( self, binding ):
    '''change the variable binding semantics'''
    return
