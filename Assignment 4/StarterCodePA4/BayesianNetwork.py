#!/usr/bin/env python
""" generated source for module BayesianNetwork """
from Assignment4 import *


import random


#
#  * A bayesian network
#  * @author Panqu
#
class BayesianNetwork(object):
    """ generated source for class BayesianNetwork """
    #
    #     * Mapping of random variables to nodes in the network
    #
    varMap = None

    #
    #     * Edges in this network
    #
    edges = None

    #
    #     * Nodes in the network with no parents
    #
    rootNodes = None

    #
    #     * Default constructor initializes empty network
    #
    def __init__(self):
        """ generated source for method __init__ """
        self.varMap = {}
        self.edges = []
        self.rootNodes = []

    #
    #     * Add a random variable to this network
    #     * @param variable Variable to add
    #
    def addVariable(self, variable):
        """ generated source for method addVariable """
        node = Node(variable)
        self.varMap[variable]=node
        self.rootNodes.append(node)

    #
    #     * Add a new edge between two random variables already in this network
    #     * @param cause Parent/source node
    #     * @param effect Child/destination node
    #
    def addEdge(self, cause, effect):
        """ generated source for method addEdge """
        source = self.varMap.get(cause)
        dest = self.varMap.get(effect)
        self.edges.append(Edge(source, dest))
        source.addChild(dest)
        dest.addParent(source)
        if dest in self.rootNodes:
            self.rootNodes.remove(dest)

    #
    #     * Sets the CPT variable in the bayesian network (probability of
    #     * this variable given its parents)
    #     * @param variable Variable whose CPT we are setting
    #     * @param probabilities List of probabilities P(V=true|P1,P2...), that must be ordered as follows.
    #       Write out the cpt by hand, with each column representing one of the parents (in alphabetical order).
    #       Then assign these parent variables true/false based on the following order: ...tt, ...tf, ...ft, ...ff.
    #       The assignments in the right most column, P(V=true|P1,P2,...), will be the values you should pass in as probabilities here.
    #
    def setProbabilities(self, variable, probabilities):
        """ generated source for method setProbabilities """
        probList = []
        for probability in probabilities:
            probList.append(probability)
        self.varMap.get(variable).setProbabilities(probList)

    #
    #     * Returns an estimate of P(queryVal=true|givenVars) using rejection sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of rejection samples to perform
    #
    def performRejectionSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performRejectionSampling """
        #  TODO

        q1 = 0
        q2 = 0

        for x in range(1, numSamples):
            y = self.pSample()

            for z in givenVars:

                if y[z.getName()] == givenVars[z]:

                    if y[queryVar.getName()]:
                        q1 = q1 + 1

                    else:
                        q2 = q2 + 1

        return self.Normalize([q1, q2])

    #
    #     * Returns an estimate of P(queryVal=true|givenVars) using weighted sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numSamples Number of weighted samples to perform
    #
    def performWeightedSampling(self, queryVar, givenVars, numSamples):
        """ generated source for method performWeightedSampling """
        #  TODO

        q1 = 0
        q2 = 0

        for x in range(1, numSamples):
            (y, z) = self.wSample(givenVars)

            if y[queryVar.getName()]:
                q1 = q1 + z

            else:
                q2 = q2 + z

        return self.Normalize([q1, q2])


    #     * Returns an estimate of P(queryVal=true|givenVars) using Gibbs sampling
    #     * @param queryVar Query variable in probability query
    #     * @param givenVars A list of assignments to variables that represent our given evidence variables
    #     * @param numTrials Number of Gibbs trials to perform, where a single trial consists of assignments to ALL
    #       non-evidence variables (ie. not a single state change, but a state change of all non-evidence variables)
    #
    def performGibbsSampling(self, queryVar, givenVars, numTrials):
        """ generated source for method performGibbsSampling """
        #  TODO

        q1 = 0.0
        q2 = 0.0

        sortedVars = sorted(givenVars)
        nEvent, event = self.sEvent(sortedVars, givenVars)

        for x in range(1, numTrials):
            for y in nEvent:
                markov = self.MarkovB(self.varMap[y])
                cEvent = {}

                for node in markov:
                    cEvent[node.getVariable().getName()] = event[node.getVariable().getName()]

                pTrue = self.getNewProb(True, cEvent, y)
                pFalse = self.getNewProb(False, cEvent, y)
                prob = pFalse + pTrue

                if prob == 0:
                    value = 0
                else:
                    value = 1.0 / prob

                value = value * pTrue

                rand = random.random()

                if value >= rand:
                    event[self.varMap[y].getVariable().getName()] = True
                else:
                    event[self.varMap[y].getVariable().getName()] = False

                if event[queryVar.getName()]:
                    q1 = q1 + 1.0

                else:
                    q2 = q2 + 1.0

        return self.Normalize([q1, q2])




# helper functions

    def pSample(self):
        x = {}

        for y in sorted(self.varMap):
            z = random.random()

            if z <= self.varMap.get(y).getProbability(x, True):
                x[y.getName()] = True

            else:
                x[y.getName()] = False

        return x


    def Normalize(self, input):
        x = 0
        for y in input:
            x += y

        if x == 0:
            return 0, 0

        else:
            return float(input[0])/x


    def wSample(self, gVars):
        x = 1
        y = Sample()

        for gVar in gVars:
            y.setAssignment(gVar.getName(), gVars[gVar])

        for sVar in sorted(self.varMap.keys()):
            z = random.random()

            if y.getValue(sVar.getName()) is not None:
                x = y.getWeight() * self.varMap.get(sVar).getProbability(y.assignments, y.assignments.get(sVar.getName()))
                y.setWeight(x)

            else:
                if z <= self.varMap.get(sVar).getProbability(y.assignments, True):
                    y.assignments[sVar.getName()] = True

                else:
                    y.assignments[sVar.getName()] = False

        return y.assignments,y.getWeight()


    def sEvent(self, sG, unsG):
        nEvent = []
        event = {}

        for x in self.varMap.keys():

            if x not in sG:
                nEvent.append(x)
                value = True

                if random.random() <= 0.5:
                    value = False

                event[x.getName()] = value

            else:
                event[x.getName()] = unsG[x]

        return nEvent, event


    def getNewProb(self, x, map, y):
        pChild= 1.0
        q1 = {}

        for parent in self.varMap[y].getParents():
            q1[parent.getVariable().getName()] = map[parent.getVariable().getName()]

        pParent = self.varMap[y].getProbability(q1, x)

        for child in self.varMap[y].getChildren():
            parents = {}

            for p in child.getParents():

                if (p.getVariable().equals(self.varMap[y].getVariable())):
                    parents[self.varMap[y].getVariable().getName()] = x

                else:
                    parents[p.getVariable().getName()] = map[p.getVariable().getName()]

            pChild = pChild * child.getProbability(parents, map[child.getVariable().getName()])

        return (pParent * pChild)


    def MarkovB(self, node):
        markov = []

        for parent in node.getParents():
            markov.append(parent)

        for child in node.getChildren():
            if child not in markov:
                markov.append(child)

                for parent2 in child.getParents():
                    if (parent2 != node) and (parent2 not in markov):
                        markov.append(parent2)

        return markov

