# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]




def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    "*** YOUR CODE HERE ***"
    #import what we will need
    from util import Stack


    #function variables
    pStack = Stack()
    route = []
    tbd = {}

    #get root
    root = problem.getStartState()
    pStack.push((root, root, 'END'))

    #dfs algorithm
    while not pStack.isEmpty():
        node = pStack.pop()

        #checks out popped node
        if problem.isGoalState(node[0]):
            while node[2] != 'END':
                route.append(node[2])
                node = tbd[node[1]]
            route.reverse()
            return route
        tbd[node[0]] = node

        children = problem.getSuccessors(node[0])

        for child in children:
            if child[0] not in tbd:
                pStack.push((child[0], node[0], child[1]))

    return None






def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    #import waht we will need
    from util import Queue

    cState = problem.getStartState()
    done = set([cState])
    route = []
    nStack = Queue()
    counter = 0

    while not problem.isGoalState(cState):
        for successor in problem.getSuccessors(cState):
            if successor[0] not in done:
                done.add(successor[0])
                nStack.push((successor[0], route + [successor[1]]))
        cState = nStack.pop()
        route = cState[1]
        cState = cState[0]
        counter += 1
    return route

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    #saw this solution on piazza for the class
    #instructor endorsed this answer
    return aStarSearch(problem, nullHeuristic)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    #get root
    root = problem.getStartState()

    #start algorithm
    done = set()

    aQueue = util.PriorityQueue()
    aQueue.push((root, [], 0), 0)

    #loop for algorithm
    while not aQueue.isEmpty():
        spot, path, cost = aQueue.pop()

        #achieved goal
        if problem.isGoalState(spot):
            return path
        #continue loop
        if spot not in done:
            done.add(spot)
            for a, b, c in problem.getSuccessors(spot):
                if a not in done:
                    bCost = c + cost
                    fCost = heuristic(a, problem)
                    tCost = bCost + fCost
                    aQueue.push((a, path + [b], bCost), tCost)
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
