from msilib import add_data
from pyAmakCore.classes.amas import Amas
from bin.clusterEnv import clusterEnv
from bin.clusterAgent import clusterAgent
import numpy as np

from bin.dataAgent import dataAgent
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
        c0 = self.add_agent(clusterAgent(self, np.array([0,0])))
        c1 = self.add_agent(clusterAgent(self, np.array([1,1])))
        c2 = self.add_agent(clusterAgent(self, np.array([1,0])))
        c3 = self.add_agent(clusterAgent(self, np.array([0,1])))
        clist = [c0,c1,c2,c3]
        self.clusterTab = clist
        for cluster in clist:
            cluster.clusterTab = clist

        #add the first data agent
        self.add_agent()

    def addDataAgent(self):
        data = self.get_environment.getData()
        if data != []:
            self.add_agent(dataAgent(self, data, self.clusterTab,100000000, 0))

    def on_cycle_end(self) -> None:
        #add a data to the system
        self.addDataAgent()