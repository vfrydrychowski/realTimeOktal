from pyAmakCore.classes.amas import Amas
from clusterEnv import clusterEnv
from clusterAgent import clusterAgent
import numpy as np
import matplotlib.pyplot as plt
from dataAgent import dataAgent
class clusterAmas(Amas):

    def __init__(self, environment: clusterEnv) -> None:
        self.clusterTab = []
        super().__init__(environment)

    def get_agent(self, id):
        l = [x for x in self.get_agents() if x.get_id() == id]
        return l[0]

    def on_initialization(self) -> None:
        return super().on_initialization()
    
    def on_initial_agents_creation(self) -> None:
        #add cluster agents
        c0 = clusterAgent(self, np.array([0,0]), 'k')
        c1 = clusterAgent(self, np.array([1,1]), 'r')
        c2 = clusterAgent(self, np.array([1,0]), 'g')
        c3 = clusterAgent(self, np.array([0,1]), 'b')
        clist = [c0,c1,c2,c3]
        self.clusterTab = clist
        for cluster in clist:
            self.add_agent(cluster)
            cluster.clusterTab = clist

        #add the first data agent
        self.addDataAgent()

    def addDataAgent(self):
        data = self.get_environment().getData()
        if data != []:
            self.add_agent(dataAgent(self, data, self.clusterTab,100000000, 0))

    def on_cycle_end(self) -> None:
        #add a data to the system
        self.addDataAgent()

        #plot image of system state
        self.plotSystemState()

    def plotSystemState(self):
        clusters = np.array([])
        clustersColor = []
        datas = np.array([])
        datasColor = []
        
        for agent in self.get_agents():
            if type(agent) == clusterAgent:
                if clusters.size == 0:
                    clusters = np.array([agent.pos])
                    clustersColor = [agent.color]
                else:
                    clusters = np.append(clusters, np.array([agent.pos]), axis = 0)
                    clustersColor.append(agent.color)
            else : 
                if datas.size == 0:
                    datas = np.array([agent.pos])
                else:
                    datas = np.append(datas, np.array([agent.pos]), axis = 0)
                if agent.cluster == None:
                    datasColor.append('tab:gray')
                else:
                    datasColor.append(agent.cluster.color)

        f = plt.figure()
        plt.scatter(clusters[:,0], clusters[:,1], c = clustersColor, marker='s')
        plt.scatter(datas[:,0], datas[:,1], c = datasColor)
        plt.show()