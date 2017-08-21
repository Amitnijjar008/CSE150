#Amit Nijjar
#A11489111

#imports
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

mdp = MDP()
mdp.dF = 0.99
mdp.a.append('NORTH')
mdp.a.append('SOUTH')
mdp.a.append('EAST')
mdp.a.append('WEST')

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
def value_iteration(mdp, e):
	val = []
	val2 = []
	
	for s in mdp.s:
		val.append(0)
		val2.append(0)
	
	while 1:
		for i in range(0, len(val2)):
			val[i] = val2[i]
		maxC = 0
		
		for s in mdp.s:
			listPval = []
			
			for action in mdp.a:
				Pval = 0
				
				for (s2, prob) in mdp.tF[(s, action)]:
					Pval = Pval + prob*val[s2-1]
				listPval.append(Pval)
			val2[s-1] = mdp.r[s] + mdp.dF*max(listPval)
			
			if abs(val2[s-1] - val[s-1]) > maxC:
				maxC = abs(val2[s-1] - val[s-1])

		if(maxC == 0):
			break
	return val

val = value_iteration(mdp,0.1)
policyIteration = {}

for s in mdp.s:
	maxPval = float("-inf")
	maxA = None
	for action in mdp.a:
		Pval = 0

		for (s2, prob) in mdp.tF[(s, action)]:
			Pval = Pval + prob*val[s2-1]

		if Pval > maxPval:
			maxPval = Pval
			maxA = action
	policyIteration[s] = maxA
queue = []

for i in range (1, 81):
	if val[i-1] > 0:
		queue.append((i, val[i-1], policyIteration[i]))

for element in queue:
	print element
