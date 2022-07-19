"""
Data agent
"""

from pyAmakCore.classes.communicating_agent import CommunicatingAgent

import numpy as np
from bin.clusterAmas import clusterAmas

from bin.dataAgent import dataAgent


class clusterAgent(CommunicatingAgent):

    def __init__(self,
                 amas : clusterAmas,
                 pos : np.ndarray
                 ) -> None:
        super().__init__(amas)
        self.pos : np.array= pos
        self.clusterTab : list= []
        self.response = []
        self.attResponse : bool= False
        self.dataTab : list = []
        self.posDataTab : np.array = None
        self.dataToAppend : list = []

    def addData(self, data : dataAgent):
        self.dataTab.append(data)
        np.append(self.posDataTab, data.pos)

    def removeData(self, data : dataAgent):
        self.posDataTab = np.delete(self.posDataTab, self.dataTab.index(data), 0)
        self.dataTab.remove(data)
        

    def read_mail(self, mail: 'Mail') -> None:
        if type(mail) == int:
            self.dataToAppend.append()

    def on_perceive(self) -> None:
        #update position of in datas cluster 
        self.posDataTab = np.array([data.pos for data in self.posDataTab])
        # update self position
        self.pos = np.mean(self.posDataTab, axis = 0)

    def validData(message):
        """
            validation function of a data adhesion
        """
        return True

    def on_act(self) -> None:
        #add datas to cluster
        for id in self.dataToAppend:
            data = self.__amas.get_agent(id)
            if self.validData(data):
                self.addData(data)
        pass
