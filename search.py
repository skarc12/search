# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called 
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
  """
  This class outlines the structure of a search problem, but doesn't implement
  any of the methods (in object-oriented terminology: an abstract class).
  
  You do not need to change anything in this class, ever.
  """
  
  def getStartState(self):
     """
     Returns the start state for the search problem 
     """
     util.raiseNotDefined()
    
  def isGoalState(self, state):
     """
       state: Search state
    
     Returns True if and only if the state is a valid goal state
     """
     util.raiseNotDefined()

  def getSuccessors(self, state):
     """
       state: Search state
     
     For a given state, this should return a list of triples, 
     (successor, action, stepCost), where 'successor' is a 
     successor to the current state, 'action' is the action
     required to get there, and 'stepCost' is the incremental 
     cost of expanding to that successor
     """
     util.raiseNotDefined()

  def getCostOfActions(self, actions):
     """
      actions: A list of actions to take
 
     This method returns the total cost of a particular sequence of actions.  The sequence must
     be composed of legal moves
     """
     util.raiseNotDefined()
           

def tinyMazeSearch(problem):
  """
  Returns a sequence of moves that solves tinyMaze.  For any other
  maze, the sequence of moves will be incorrect, so only use this for tinyMaze
  """
  from game import Directions
  s = Directions.SOUTH
  w = Directions.WEST
  return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
  """
  Search the deepest nodes in the search tree first [p 85].
  
  Your search algorithm needs to return a list of actions that reaches
  the goal.  Make sure to implement a graph search algorithm [Fig. 3.7].
  
  To get started, you might want to try some of these simple commands to
  understand the search problem that is being passed in:
  
  print "Start:", problem.getStartState()
  print "Is the start a goal?", problem.isGoalState(problem.getStartState())
  print "Start's successors:", problem.getSuccessors(problem.getStartState())
  """
  "*** YOUR CODE HERE ***"

  stack = util.Stack()
  for i in problem.getSuccessors(problem.getStartState()):
    stack.push(i)

  moves = []
  visited = []
  visited.append(problem.getStartState())

  while not stack.isEmpty():
    current = stack.pop()
    moves.append(current)

    count = 0
    visited.append(current[0])
    for i in problem.getSuccessors(current[0]):
      if(visited.count(i[0]) == 0):
        stack.push(i)
        count = count + 1

    if problem.isGoalState(current[0]):
      break

    while count == 0 and not len(moves) == 0:
      back = moves.pop()
      for i in problem.getSuccessors(back[0]):
        if(visited.count(i[0]) == 0):
          count = count + 1
      if count > 0:
        moves.append(back)
        break

  length = 0
  for i in moves:
    length = length + 1

  iterations = 0
  while not iterations == (length):
    i = moves[0]
    moves.append(i[1])
    moves.pop(0)
    iterations = iterations + 1


  return moves

def breadthFirstSearch(problem):
  "Search the shallowest nodes in the search tree first. [p 81]"
  "*** YOUR CODE HERE ***"
  myQ = util.Queue();
  
  start = problem.getStartState()
  visited = []
  visited.append(start[0])
  goal = start
  for i in problem.getSuccessors(start):
    movesList = [i[1]]
    myQ.push((i, movesList))
    visited.append(i[0])

  while not myQ.isEmpty():	
    #print myQ.pop()
    curr = myQ.pop()
    
    if problem.isGoalState(curr[0][0]):
       goal = curr
       break
    
    for i in problem.getSuccessors(curr[0][0]):
      if i[0] not in visited:
        visited.append(i[0])
        newList = []
        newList.extend(curr[1])
        newList.append(i[1])
        myQ.push((i, newList))
  return goal[1]

def uniformCostSearch(problem):
  "Search the node of least total cost first. "
    
  frontier = util.PriorityQueue() # queue which stores objects with form (state, path, cost)
  frontierList = []               # holds just the (x,y) tuple of the frontier's objects
  visited = []                    # holds the locations we've visited before

  'print "Start: ", problem.getStartState()'

  for i in problem.getSuccessors(problem.getStartState()): # initialize frontier
    frontier.push((i, [i[1]] , i[2]), i[2])
    frontierList.append(i[0])
    'print "Add ", i, "to frontier with cost ", i[2]'

  visited.append(problem.getStartState())

  while not frontier.isEmpty(): #expand frontier until a goal state is found
    current = frontier.pop()
    frontierList.remove(current[0][0])
    'print "Lowest cost node: ", current[0][0], " with cost ", current[0][2]'
    'print "Location: " , current[0][0]'
    'print "Path to location: ", current[1]'
    if problem.isGoalState(current[0][0]):
       return current[1]
    visited.append(current[0][0])
    for i in problem.getSuccessors(current[0][0]):
       if i[0] not in visited:
          if i[0] not in frontierList:
             templist = []
             templist.extend(current[1])
             templist.append(i[1])
             cost = current[2] + i[2]
             frontier.push((i, templist , cost),  cost)
             frontierList.append(i[0])
             'print "Add ", i , " and ", i[1], " to frontier with cost ", cost'
          
  print "if this printed, something went wrong in ucs"
  util.raiseNotDefined()

def nullHeuristic(state, problem=None):
  """
  A heuristic function estimates the cost from the current state to the nearest
  goal in the provided SearchProblem.  This heuristic is trivial.
  """
  return 0

def aStarSearch(problem, heuristic=nullHeuristic):
  "Search the node that has the lowest combined cost and heuristic first."
    
  frontier = util.PriorityQueue() # queue which stores objects with form (state, path, cost)
  frontierList = []               # holds just the (x,y) tuple of the frontier's objects
  visited = []                    # holds the locations we've visited before

  'print "Start: ", problem.getStartState()'

  for i in problem.getSuccessors(problem.getStartState()): # initialize frontier
    cost = i[2] + heuristic(i[0], problem)
    node = (i, [i[1]], cost)
    frontier.push(node, cost)
    frontierList.append(i[0])
    'print "Add ", i, "to frontier with cost ", i[2]'

  visited.append(problem.getStartState())

  while not frontier.isEmpty(): #expand the frontier until finished
    current = frontier.pop()
    frontierList.remove(current[0][0])
    'print "Lowest cost node: ", current[0][0], " with cost ", current[0][2]'
    'print "Location: " , current[0][0]'
    'print "Path to location: ", current[1]'
    if problem.isGoalState(current[0][0]):
       return current[1]
    visited.append(current[0][0])
    for i in problem.getSuccessors(current[0][0]):
       if i[0] not in visited:
          if i[0] not in frontierList:
             templist = []
             templist.extend(current[1])
             templist.append(i[1])
             cost = current[2] + i[2] + heuristic(i[0], problem)
             frontier.push((i, templist , cost),  cost)
             frontierList.append(i[0])
             'print "Add ", i , " and ", i[1], " to frontier with cost ", cost'
          
  print "if this printed, something went wrong in astar"
  util.raiseNotDefined()
    
  
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
