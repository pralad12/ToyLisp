
class assignVar:

  def __init__(self):
    
    self.operators = {
      'set': self.set,
      'let': self.let
    }

  #Add to stack 
  def set(self, args, parser):
    # print("ARGS OF ZERO", args[0])
    # print("ARGS OF ONE", args[1])
    parser.stack[-1][args[0]] = parser.execute(args[1])
    return True

  #Let - uses set for binding
  def let(self, args, parser):
    namespace = {}
    binds = args[0]

    parser.stack.append(namespace)

    for binding in binds:
      # print("BINDINGS", binding)
      self.set(binding, parser)

    return_val = parser.execute(args[1])
    #Get rid of the local namespace once we're done utilizing the variables for let
    parser.stack.pop()
    return return_val