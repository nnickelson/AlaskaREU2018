# RK Estimator method for CO2 emissions and costs
# Estimator based on method by Dr. Vladimir Alexeev
# GUI by Nathan Nickelson

# Class RK Methlod File

import numpy as np
import random as rn

class RKMethod(object):

    def __init__(self):
        # parameters
        
        self.NP = 0                                                 # self.NP = number of players
        self.NT = 4000                                                # self.NT = number of time steps
        self.pde = 0.68
        
        self.alam = np.zeros((self.NP))
        self.beta = 1.0
        
        self.plotX = []
        self.plotCost = []

        self.payoff = [[self.pde,self.pde] for x in range(self.NP)]
        self.strategy = [[0.68] for x in range(self.NP)]
        self.lastStrategy = [["C"] for x in range(self.NP)]

    def resetVariables(self):
        # Reset Button to default value Variables
        self.beta = 1.0
        self.RKPlotsVariables()


    def RKPlotsVariables(self):
        # arrays initialized from the parameters
        #####################################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        self.x = np.full((self.NP, self.NT), 1.0 )           # concentration of a pollutant
        self.aij = np.full((self.NP, self.NP), 1.0)
        self.xi = np.zeros((self.NP))
        self.asum = np.zeros((self.NP))
        self.co2 = np.full((self.NP), 1.0)   
        self.cost = np.zeros((self.NP, self.NT))            #-------unused matrix
        self.costn = np.zeros((self.NP, self.NT))
        self.un = np.zeros((self.NP, self.NT))              # strategy
        self.u = np.full((self.NP, self.NT), self.pde)

        self.costTotals = np.zeros((self.NP))               # an array used to sum the column totals of costn 
        for i in range(self.NP):
            self.x[i][0] = self.randStart[i]
    ################################################################################################################!!!!!
    ## RK ESTIMATOR FUNCTION                                                                ########################!!!!!
    ##  pcalculates the plot data for each of the categories on the graph                   ########################!!!!!  
    ################################################################################################################!!!!!                      
    def RKPlots(self):
        self.RKPlotsVariables()
        print("line 61, RK, Lambdas = {}".format(self.alam))
        self.populateUtility()
    
        # Matrix self.aij
        for i in range(self.NP):
            self.aij[i][i] = 0.0

        # Time Step
        dt = 0.01

        # Iterative Process
        for n in range(1, self.NT):

            # Matrix of interaction with other countries
            # 1st RK step
            for i in range(self.NP):
                ss = 0.0
                for j in range(self.NP):
                    ss = ss + self.aij[i][j]*(1.0 - self.u[j][n]) * self.x[j][n]
                self.asum[i] = ss

        # Choosing the 'Optimal' Strategy
            self.un = self.u 
            ##### commented out for update #############################################################################
            #self.un[:, n] = self.beta * (self.x[:, n-1] + self.asum[:]) / (2.0 * self.beta * self.x[:, n-1] - self.alam)
    
            #for i in range(self.NP):
            #    if self.un[i][n] < 0.0:
            #        self.un[i][n] = 0.0
            #    if self.un[i][n] > 1.0:
            #        self.un[i][n] = 1.0

        # First step of Runge-Kutta
            self.xi[:] = self.x[:, n-1] + 0.5 * dt * (self.co2[:] + (1.0 - 2.0 * self.un[:, n-1]) * self.x[:, n-1] + self.asum[:])

        # Matrix interaction with other countries
            for i in range(self.NP):
                ss = 0.0
                for j in range(self.NP):
                    ss = ss + self.aij[i][j] * (1.0 - self.un[j][n]) * self.xi[j]
                    continue
                self.asum[i] = ss

        # Second step of Runge-Kutta
            self.x[:, n] = self.x[:, n-1] + dt * (self.co2[:] + (1.0 - 2.0 * self.un[:, n]) * self.x[:, n-1] + self.asum[:])
            self.costn[:, n] = self.beta * (self.x[:, n] - self.x[:, n-1]) + self.alam[:] * self.un[:, n]

        self.costTotals = np.sum(self.costn, axis = 1) 

        return (self.x, self.costn)
    
    def setStrategy(self, player, strat):
        print("player = {} ..... strategy Text = {}".format(player, strat))
        if strat == "":
            self.strategy[player] = [0.6]
            return
        tempStrat = []
        for i in range(len(strat)):
            if strat[i] == 'c' or strat[i] == 'C':
                tempStrat.append(self.payoff[player][0])
            if strat[i] == 'd' or strat[i] == 'D':
                tempStrat.append(self.payoff[player][1])
        print(tempStrat)
        self.strategy[player] = tempStrat
    
    def populateUtility(self):
        for i in range(self.NT):
            for j in range(self.NP):
                k = i % len(self.strategy[j])
                self.u[j][i] = self.strategy[j][k]
            #print("strategy j/k = {}".format(self.strategy[j][k])) 
            #print(self.u[:,i])
            #imput = input("pause")


    def changeNumPlayers(self, num):
        self.NP = num
        self.randStart = []
        for i in range(self.NP):
            self.randStart.append(rn.random())
        self.alam = np.zeros((self.NP))
        self.payoff = [[self.pde,self.pde] for x in range(self.NP)]
        self.strategy = [[0.68] for x in range(self.NP)] 
        self.lastStrategy = [["C"] for x in range(self.NP)]
        self.RKPlotsVariables()