'''
Created on Apr 30, 2013

@author: ivihernandez
'''
#standard imports
import sys
import xml.etree.ElementTree as ET
import os
#non standard imports
import networkx as nx
#ivan's imports
import myutils
import probabilityfailureproblem

class CalculateProbabilityFailure:
    """
        The objective of this class is to obtain a set of results
        for a bi-objective facility location problem 
        (minimize distance and minimize # of facilities)
        and determine the probability that the distance will increase by
        Delta percent, assuming that each open facility of a given solution
        in the Pareto set has a specific probability of failing. 
    """
    def __init__(self, configurationFilePath, paretoFilePath):
        """
            @param configurationFilePath: path to the file that has information
            about how the experiment was runned: 1) demand center, 
            2) distribution center, 3) objective functions
            
            @param paretoFilePath: path to the file containing the Pareto set.
            This file also has information about the objective function types 
            The pareto was created by running the program facility-location using
            the configurationFilePath  
        """
        self.configurationFilePath = configurationFilePath
        self.paretoFilePath = paretoFilePath
        configurationFile = open(self.configurationFilePath, 'r')
        paretoFile = open(self.paretoFilePath, 'r')
        
        print 'configuration file', self.configurationFilePath
        print 'pareto file', self.paretoFilePath
        tree = ET.parse(self.configurationFilePath)
        #obtain the file path of the distribution centers
        for elem in tree.iter(tag='distributionCenters'):
            self.distributionCentersFilePath = elem.text
        #obtain the file path of the demand centers
        for elem in tree.iter(tag='demandCenters'):
            self.demandCentersFilePath = elem.text
        
        
        os.path.normpath(self.distributionCentersFilePath)
        os.path.normpath(self.demandCentersFilePath)
        
        #load the demand and distribution centers as s
        distributionCenters = nx.read_graphml(self.distributionCentersFilePath, node_type=int)
        demandCenters = nx.read_graphml(self.demandCentersFilePath, node_type=int)
        
        #load the ids of the distribution centers of the pareto set
        os.path.normpath(self.paretoFilePath)
        pareto = myutils.load_pareto(self.paretoFilePath)
        """
        probabilityFailureProblem = probabilityfailureproblem.ProbabilityFailureProblem(demandCenters=demandCenters,
                                                                                        distributionCenters=distributionCenters,
                                                                                        pareto=pareto
                                                                                        )
        """
        probabilityFailureProblem = probabilityfailureproblem.ProbabilityFailureProblem(demandCentersFilePath=self.demandCentersFilePath,
                                                                                        distributionCentersFilePath=self.distributionCentersFilePath,
                                                                                        pareto=pareto,
                                                                                        configurationFilePath=configurationFilePath
                                                                                        )
if __name__ == '__main__':
    print 'program started'
    configurationFilePath = r'C:\Users\ivihernandez\Documents\PhD-systems-engineering\projects\articles\facility-location\robust-facilities-ivan-12-17-2012\results-paper-robust-facilities\results Sun 03 Feb 2013 22 22 45-swain-updatedpath\a-experiment-swain-total-distance-interdiction.xml'
    
    paretoFilePath = r'C:\Users\ivihernandez\Documents\PhD-systems-engineering\projects\articles\facility-location\robust-facilities-ivan-12-17-2012\results-paper-robust-facilities\results Sun 03 Feb 2013 22 22 45-swain-updatedpath\combined-pareto-1.xml'
    calculateProbabilityFailure = CalculateProbabilityFailure(configurationFilePath=configurationFilePath,
                                                              paretoFilePath=paretoFilePath)
    print 'program finished'
