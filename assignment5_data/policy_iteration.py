#Amit Nijjar
#A11489111

#imports
import random
import numpy
from collections import defaultdict

class MDP(object):

	dF = None
	tF = None
	s = None
	a = None
	r = None

	def __init__(self):
		self.s = []
		self.a = []
		self.r = {}
		self.tF = defaultdict(list)

	def setR(self, state, reward):
		self.r[int(state)] = float(reward)

	def addS(self, state):
		self.s.append(int(state));

	def addT(self, s2, s, action, prob):
		self.tF[(int(s), action)].append((int(s2), float(prob)));

#set up mdp
mdp = MDP()
mdp.dF = 0.99
mdp.a.append('EAST')
mdp.a.append('WEST')
mdp.a.append('SOUTH')
mdp.a.append('NORTH')

#add states and set rewards
f = open("rewards.txt")
i = 1
for line in f:
	mdp.addS(i)
	mdp.setR(i, line[:-1])
	i = i+1
f.close()

#add transition
f = open("prob_north.txt")
for line in f:
	list = line.split()
	mdp.addT(list[1], list[0], 'NORTH', list[2])
f.close()

#add transition
f = open("prob_south.txt")
for line in f:
	list = line.split()
	mdp.addT(list[1], list[0], 'SOUTH', list[2])
f.close()

#add transition
f = open("prob_east.txt")
for line in f:
	list = line.split()
	mdp.addT(list[1], list[0], 'EAST', list[2])
f.close()

#add transition
f = open("prob_west.txt")
for line in f:
	list = line.split()
	mdp.addT(list[1], list[0], 'WEST', list[2])
f.close()

#evaluate MDP
def policy_iteration(mdp):
	pi = {}
    
	for i in range(1, len(mdp.s)+1):
		pi[i] = mdp.a[random.randint(0, 3)]
	val = []
	
	while 1:
		val = policy_evaluation(pi, mdp)
		unchanged = True
        
		for s in mdp.s:
			mProbUnchanged = float("-inf")
			mAction = None
            
			for action in mdp.a:
				probUnchanged = 0
                
				for (s2, prob) in mdp.tF[(s, action)]:

					probUnchanged = probUnchanged + prob*val[s2-1]
                    
				if probUnchanged > mProbUnchanged:

					mProbUnchanged = probUnchanged
					mAction = action
			
			probUnchanged = 0
			for (s2, prob) in mdp.tF[(s, pi[s])]:
				probUnchanged = probUnchanged + prob*val[s2-1]

			if mProbUnchanged > probUnchanged:
				pi[s] = mAction
				unchanged = False

		if unchanged == True:
			break
	return (pi, val)

def policy_evaluation(pi, mdp):

	grid = numpy.zeros((len(mdp.s),len(mdp.s)))
	left = numpy.zeros((len(mdp.s), 1))

	for i in range(1, len(mdp.s)+1):
		grid[i-1][i-1] = 1

		for (s2, prob) in mdp.tF[(i, pi[i])]:
			grid[i-1][s2-1] = grid[i-1][s2-1] - mdp.dF*prob
		left[i-1][0] = mdp.r[i]

	mati = numpy.mat(grid)
	matLeft = numpy.mat(left)

	result = numpy.linalg.solve(mati, matLeft)
	arrResult = result.getA()
	var2 = []

	for i in range (len(mdp.s)):
		var2.append(arrResult[i][0])
	return var2


#print out data
polIter, val = policy_iteration(mdp)
queue = []

for i in range(1, 81):
	if val[i-1] > 0:
		queue.append((i, polIter[i]))

for val in queue:
	print val