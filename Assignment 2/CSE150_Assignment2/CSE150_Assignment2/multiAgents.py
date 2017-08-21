# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def __init__(self):
        self.todoArr = []


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        self.todoArr.insert(0, gameState.generatePacmanSuccessor(legalMoves[chosenIndex]).getPacmanPosition())
        if len(self.todoArr) > 5:
            self.todoArr.pop()


        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #variable declaration
        nextFood = 0
        eatGhost = 0
        food = 0
        todo = 0

        #get food distance priority
        if newPos in currentGameState.getFood().asList():
            food = 10

        for index in newFood[newPos[0] - 1:newPos[0] + 2]:
            for row in index[newPos[1] - 1:newPos[1] + 2]:
                if row: nextFood += 1

        #get gost distance priority
        for index in range(len(newGhostStates)):
            dist = util.manhattanDistance(newPos, newGhostStates[index].getPosition())
            if dist == 0: dist = 1e-8

            if dist <= newScaredTimes[index] / 1.5:
                eatGhost += (1. / dist) * 100

            elif dist <= 3:
                eatGhost -= (1. / dist) * 100

        #get waste area priority
        if newPos in self.todoArr:
            todo = -100

        #get cost of path
        return nextFood + eatGhost + todo + food


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        todoArr = self.value(gameState, 0)
        return todoArr[0]

    #function to get the value
    #use minmax to find path
    #min for ghosts, max for pacman
    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxFunc(gameState, depth)
        else:
            return self.minFunc(gameState, depth)

    #min function for ghosts
    def minFunc(self, gameState, depth):
        routes = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, float("inf"))

        for route in routes:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), route)
            todoArr = self.value(succ, depth + 1)

            if todoArr[1] < min_val[1]:
                min_val = (route, todoArr[1])

        return min_val

    #for pacman
    def maxFunc(self, gameState, depth):
        routes = gameState.getLegalActions(0)
        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -float("inf"))
        for route in routes:
            succ = gameState.generateSuccessor(0, route)
            todoArr = self.value(succ, depth + 1)
            if todoArr[1] > max_val[1]:
                max_val = (route, todoArr[1])
        return max_val

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        todoArr = self.value(gameState, 0, -float("inf"), float("inf"))
        return todoArr[0]

    #same as above
    def value(self, gameState, depth, alpha, beta):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxFunc(gameState, depth, alpha, beta)
        else:
            return self.minFunc(gameState, depth, alpha, beta)

    # for ghosts
    def minFunc(self, gameState, depth, alpha, beta):
        routes = gameState.getLegalActions(depth % gameState.getNumAgents())
        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        min_val = (None, float("inf"))
        for route in routes:
            successor = gameState.generateSuccessor(depth % gameState.getNumAgents(), route)
            todoArr = self.value(successor, depth + 1, alpha, beta)

            if todoArr[1] < min_val[1]:
                min_val = (route, todoArr[1])

            if min_val[1] < alpha:
                return min_val

            beta = min(beta, min_val[1])
        return min_val

    # for pacman
    def maxFunc(self, gameState, depth, alpha, beta):
        routes = gameState.getLegalActions(0)
        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -float("inf"))
        for route in routes:
            successor = gameState.generateSuccessor(0, route)
            todoArr = self.value(successor, depth + 1, alpha, beta)

            if todoArr[1] > max_val[1]:
                max_val = (route, todoArr[1])

            if max_val[1] > beta:
                return max_val

            alpha = max(alpha, max_val[1])
        return max_val


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        todoArr = self.value(gameState, 0)
        return todoArr[0]

    #same as previous functions
    def value(self, gameState, depth):
        if depth == self.depth * gameState.getNumAgents() or gameState.isWin() or gameState.isLose():
            return (None, self.evaluationFunction(gameState))
        if depth % gameState.getNumAgents() == 0:
            return self.maxValue(gameState, depth)
        else:
            return self.expValue(gameState, depth)

    # for ghosts
    def expValue(self, gameState, depth):
        routes = gameState.getLegalActions(depth % gameState.getNumAgents())

        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        probability = 1. / len(routes)
        exp_val = 0

        for route in routes:
            succ = gameState.generateSuccessor(depth % gameState.getNumAgents(), route)
            todoArr = self.value(succ, depth + 1)
            exp_val += todoArr[1] * probability
        return (None, exp_val)

    #for pacman
    def maxValue(self, gameState, depth):
        routes = gameState.getLegalActions(0)

        if len(routes) == 0:
            return (None, self.evaluationFunction(gameState))

        max_val = (None, -float("inf"))

        for route in routes:
            succ = gameState.generateSuccessor(0, route)
            todoArr = self.value(succ, depth + 1)

            if todoArr[1] > max_val[1]:
                max_val = (route, todoArr[1])
        return max_val


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #variable definitions
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    metric = util.manhattanDistance
    ghostDistance = [metric(newPos, gh.getPosition()) for gh in newGhostStates]
    score = currentGameState.getScore()
    foodCount = currentGameState.getNumFood()
    nearFoodDist = 100
    nearPeletDist = 100

    #lose the game
    if any([distance == 0 for distance in ghostDistance]):
        return -1

    #victory
    if foodCount == 0:
        return 1000


    for x, item in enumerate(newFood):
        for y, foodItem in enumerate(item):
            nearFoodDist = min(nearFoodDist, metric(newPos, (x, y)) if foodItem else 100)

    ghostDist = lambda d: -20 + d ** 4 if d < 3 else -1.0 / d
    ghostVar = sum(
        [ghostDist(ghostDistance[i]) if newScaredTimes[i] < 1 else 0 for i in range(len(ghostDistance))])

    foodBonus = 1.0 / nearFoodDist
    updateTime = -8 if all((t == 0 for t in newScaredTimes)) else 0

    if all((t > 0 for t in newScaredTimes)):
        ghostVar *= (-1)

    pelets = currentGameState.getCapsules()
    pelets.sort()

    if len(pelets) > 0:
        nearPeletDist = min(nearPeletDist, min([metric(newPos, pelet) for pelet in pelets]))

    peletBonus = 1.0 / nearPeletDist
    peletsRemaining = len(pelets)
    score = score + foodBonus + 2 * ghostVar + 10 * peletBonus + -1.5 * foodCount + peletsRemaining * updateTime
    return score


# Abbreviation
better = betterEvaluationFunction

