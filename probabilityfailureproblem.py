'''
Created on May 1, 2013

@author: ivihernandez
'''
#standard imports
import copy
import random
import sys
#non standard imports
import inspyred
#ivan's imports
import facilitylocationproblem
import parameterreader
import myutils

"""
class DistanceProblem:
    def __init__(self, demandCenters, distributionCenters):
        self.demandCenters = demandCenters
        self.distributionCenters = distributionCenters
    def getTotalDistance(self, workingFacilities):
"""
class ProbabilityFailureProblem:
    """
        The objective of this class is to calculate the probability
        that the the distance  of a facility 
        location solution increases
        by delta. 
        
        It is assumed that all facilities have the same
        failure probability. 
    """
    def __init__(self, demandCentersFilePath, distributionCentersFilePath, pareto, configurationFilePath, failureProbability=0.9):
        """
            @param demandCenters: weight and coordinates of the demand centers
            @param distributionCenters: coordinates of the distribution centers
            @param paretoDistributionCentersIDs: IDs  
            @param configurationFilePath: file containing the description of the experiment that was performed (how they were runned) 
            @param failureProbability: probability with which each open facility will fail 
        """
        self.failureProbability = failureProbability
        seed = 98213487
        random.seed(seed)
        self.prng = random.random()
        
        
        """
        print "len(demandCenters)",len(demandCenters)
        print "len(distributionCenters)",len(distributionCenters)
        print "len(pareto)", len(pareto)
        """
        #[open, distance, failed, distance after failure]
        #create instance of facility location problem
        datasetList = [distributionCentersFilePath, demandCentersFilePath]
        parameterReader = parameterreader.ParameterReader(configurationFilePath)
        facilityLocationProblem = facilitylocationproblem.UncapacitatedFacilityLocationProblem(inputs=datasetList,
                                                                                  prng=None,
                                                                                  parameterReader=parameterReader,
                                                                                  resultsFolder="results",
                                                                                  embeddedEA=None)
        THRESHOLD = 11
        MAX_POP_SIZE = 1000
        self.population = []
        for solution in pareto:
            indices = [i for i, elem in enumerate(solution.candidate) if elem==1]
            
            if len(indices) <= 1:
                continue
            
            distanceBeforeFailure = solution.fitness[1]
            if len(indices) < THRESHOLD:
                popSize = len(indices)
            else:
                popSize = MAX_POP_SIZE
            
            for i in range(popSize):
                #randomly select how many will fail
                numberToFail = random.randint(1, len(indices) - 1)
                #randomly select which ones will fail
                indicesToFail = random.sample(indices, numberToFail)
                #turn off the bits
                
                
                failedChromosome = [x for x in solution.candidate]#copy.deepcopy(solution.candidate)
                for index in indicesToFail:
                    failedChromosome[index] = 0
                distanceAfterFailure = facilityLocationProblem.get_total_distance(failedChromosome)
                newFitness = []
                
                newFitness.append(len(indices))
                newFitness.append(distanceBeforeFailure)
                newFitness.append(distanceAfterFailure)
                newFitness.append(numberToFail)
                
                ind = inspyred.ec.Individual(failedChromosome)
                
                ind.fitness = newFitness
                
                #fit = inspyred.ec.emo.Pareto(newFitness, [False,False, False, True])
                #ind.fitness = fit
                
                
                self.population.append(ind)
                
                
        #let us show the solutions
        #print "len(pop)", len(self.population)
        self.archive = []
        myset = set()
        for individual in self.population:
            #print individual
            elem = (tuple(individual.candidate), tuple(individual.fitness))
            if not elem in myset:
                myset.add(elem)
                self.archive.append(individual)
        
        #myset = set(self.population)
        fileName = "results.txt"
        file = open(fileName, "w")
        print "len(self.archive)", len(self.archive)
        for sol in self.archive:
            print sol
            file.write(str(sol) + "\n")
        file.close()