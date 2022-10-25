from parser import ParserException, Parser, Binding
import parser_impl
import assign
import copy

class functionImpl:

  def __init__(self):
    self.operations = {
      "lambda": self.setfunc
    }

  def setfunc(self, args, parser):
    
    if len(args) != 2:

      raise ParserException

    #Dictionary to place on the stack (namespace)
    func_contents = {}
    
    #Set binding logic - if shallow, only copy top of the stack
    if parser.binding == Binding.DEEP:
      closure = copy.deepcopy(parser.stack)
    else:
      closure = copy.deepcopy(parser.stack[-1:])

    #Store the lambda info into a dictionary
    func_contents["params"] = args[0]
    func_contents["body"] = args[1]
    func_contents["closure"] = closure

    return func_contents


   #When I get a function object (dictionary), I want to execute it:
  def executefunc(self, dictionary, args, parser):
    assign_instance = assign.assignVar()
    #Make a copy of the stack for resolution later, and unpack values - need deepcopy because .copy() was not working
    stack_copy = copy.deepcopy(parser.stack)
    params, body, closure = dictionary["params"], dictionary["body"], dictionary["closure"]
    print("CHOSURE", closure)
    parser.stack = closure

    #office hrs: WE NEED TO BIND VARIABLES BEFORE EXECUTING FUNC!! - 
    #this is the spot to bind variables and place on top of stack - Scoping with let is giving out wrong answer, not sure why
    bindings = []
    if params:
      for i in range(len(params)):
        binding = [params[i], args[i]]
        bindings.append(binding)
        
    args = [bindings, body]
    res = assign_instance.let(args, parser)

    # Doing it the way Will said during class - resolving variables using another temp namespace and putting it on top of the 
    # stack so that the values using eager evaluation is found first

    # temp_dict = {}
    # if params:
    #   for i in range(len(params)):
    #     temp_dict[params[i]] = parser.execute(args[i])

    # if parser.binding == Binding.DEEP:
    #   parser.stack = closure
    # else:
    #   parser.stack = parser.stack + closure

    #This sets the values on top of the stack to the most recent values
    #parser.stack.append(temp_dict)
    #We now execute the body since the stack has the newer bindings on top
    #return_val = parser.execute(body)

    parser.stack = copy.deepcopy(stack_copy)

    return res 


     



    






