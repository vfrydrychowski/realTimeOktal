"""
Data agent
"""

from pyAmakCore.classes.communicating_agent import CommunicatingAgent
from pyAmakCore.classes.communicating_agent import Mail

import numpy as np


import dataAgent


class clusterAgent(CommunicatingAgent):

    def __init__(self,
                 amas,
                 pos : np.ndarray,
                 color : str
                 ) -> None:
        super().__init__(amas)
        self.pos : np.array= pos
        self.clusterTab : list= []
        self.response = []
        self.attResponse : bool= False
        self.dataTab : list = []
        self.posDataTab : np.array = None
        self.dataToAppend : list = []
        self.color : str = color

    def addData(self, data : dataAgent):
        if self.dataTab == []:
            self.dataTab = [data]
            self.posDataTab = np.array([data.pos])
        else:
            self.dataTab.append(data)
            self.posDataTab = np.append(self.posDataTab, np.array([data.pos]), axis = 0)

    def removeData(self, data : dataAgent):
        self.posDataTab = np.delete(self.posDataTab, self.dataTab.index(data), 0)
        self.dataTab.remove(data)
        

    def read_mail(self, mail: Mail) -> None:
        self.dataToAppend.append(mail.get_id_sender())

    def on_perceive(self) -> None:
        if self.dataTab != []:
            #update position of in datas cluster
            self.posDataTab = np.array([data.pos for data in self.dataTab])
            # update self position
            self.pos = np.mean(self.posDataTab, axis = 0)

    def validData(self, d : CommunicatingAgent):
        """
            validation function of a data adhesion
        """
        self.send_message(True, d.get_id())
        return True

    def on_act(self) -> None:
        #add datas to cluster
        for id in self.dataToAppend:
            data = self.get_amas().get_agent(id)
            if self.validData(data) and data not in self.dataTab:
                self.addData(data)
        self.dataToAppend = []
