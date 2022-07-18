"""
Data agent
"""

from pyAmakCore.classes.communicating_agent import CommunicatingAgent

import numpy as np

from bin.dataAgent import dataAgent


class clusterAgent(CommunicatingAgent):

    def __init__(self,
                 amas,
                 pos : np.ndarray,
                 clusterTab : list
                 ) -> None:
        super().__init__(amas)
        self.pos : np.array= pos
        self.clusterTab : list= clusterTab
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
        
    def validData(message):
        """
            validation function of a data adhesion
        """
        return True

    def on_act(self) -> None:
        for data in self.dataToAppend:
            if self.validData():
                
        pass
