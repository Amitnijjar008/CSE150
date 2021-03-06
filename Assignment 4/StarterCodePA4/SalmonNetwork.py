#!/usr/bin/env python

from BayesianNetwork import *
#
#   * Creates and tests the alarm network as given in the book.
#
class SalmonNetwork(object):
    """ generated source for class SalmonNetwork """
    @classmethod
    def main(cls, args):
        """ generated source for method main """
        salmon_run = BayesianNetwork()
        #  Add variables to network
        asia = RandomVariable("asia")
        smoker = RandomVariable("smoker")
        tb = RandomVariable("tb")
        lung_cancer = RandomVariable("lung_cancer")
        tb_or_cancer = RandomVariable("tb_or_cancer")
        bronchitis = RandomVariable("bronchitis")
        xray = RandomVariable("xray")
        dispnea = RandomVariable("dispnea")

        salmon_run.addVariable(tb)
        salmon_run.addVariable(asia)
        salmon_run.addVariable(smoker)
        salmon_run.addVariable(lung_cancer)
        salmon_run.addVariable(tb_or_cancer)
        salmon_run.addVariable(bronchitis)
        salmon_run.addVariable(xray)
        salmon_run.addVariable(dispnea)
        #  Add edges to network
        salmon_run.addEdge(asia, tb)
        salmon_run.addEdge(smoker, lung_cancer)
        salmon_run.addEdge(smoker, bronchitis)
        salmon_run.addEdge(tb, tb_or_cancer)
        salmon_run.addEdge(lung_cancer, tb_or_cancer)
        salmon_run.addEdge(tb_or_cancer, dispnea)
        salmon_run.addEdge(bronchitis, dispnea)
        salmon_run.addEdge(tb_or_cancer, xray)
        #  Initialize probability tables
        asiaProbs = [.01]
        smokerProbs = [.5]
        tbProbs = [.05, .01]
        lungProbs = [.1, .01]
        bronchitisProbs = [.6,.3]
        tb_or_cancerProbs = [1, 1, 1, 0]
        xrayProbs = [.98, .05]
        dispneaProbs = [.9, .7, .8, .1]

        salmon_run.setProbabilities(asia, asiaProbs)
        salmon_run.setProbabilities(smoker, smokerProbs)
        salmon_run.setProbabilities(tb, tbProbs)
        salmon_run.setProbabilities(lung_cancer, lungProbs)
        salmon_run.setProbabilities(bronchitis, bronchitisProbs)
        salmon_run.setProbabilities(tb_or_cancer, tb_or_cancerProbs)
        salmon_run.setProbabilities(xray, xrayProbs)
        salmon_run.setProbabilities(dispnea, dispneaProbs)

        #  Perform sampling tests
        #  ----------------------
        print("Test 1")
        given1 = {}
        given1[asia]= True
        given1[smoker]=False
        given1[xray]=True
        given1[dispnea]=False

        print("rejection sampling: " +str(salmon_run.performRejectionSampling(tb, given1, 999999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(tb, given1, 99999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(tb, given1, 99999)))

        print("Test 2")
        given2 = {}
        given2[asia] = True
        given2[smoker] = False
        given2[bronchitis] = True

        print("rejection sampling: " + str(salmon_run.performRejectionSampling(dispnea, given2, 999999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(dispnea, given2, 99999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(dispnea, given2, 99999)))

        print("Test 3")
        given3 = {}
        given3[asia] = True
        given3[smoker] = True
        given3[tb_or_cancer] =False
        given3[bronchitis] =True

        print("rejection sampling: " + str(salmon_run.performRejectionSampling(tb, given3, 999999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(tb, given3, 99999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(tb, given3, 99999)))

        print("Test 4")
        given4 = {}
        given4[asia] = True
        given4[smoker] = False
        given4[xray] = True
        given4[dispnea] = False
        given4[bronchitis] =True
        given4[tb] =False


        print("rejection sampling: " + str(salmon_run.performRejectionSampling(dispnea, given4, 999999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(dispnea, given4, 99999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(dispnea, given4, 99999)))

        print("Test 5")
        given5 = {}
        given5[asia] = True
        given5[smoker] = False
        given5[bronchitis] = True

        print("rejection sampling: " + str(salmon_run.performRejectionSampling(xray, given5, 999999)))
        print("weighted sampling: " + str(salmon_run.performWeightedSampling(xray, given5, 99999)))
        print("gibbs sampling: " + str(salmon_run.performGibbsSampling(xray, given5, 99999)))




if __name__ == '__main__':
    import sys
    SalmonNetwork.main(sys.argv)
import sys
SalmonNetwork.main(sys.argv)
