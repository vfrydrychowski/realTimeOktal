"""
Data agent
"""

from dis import distb
from pyAmakCore.classes.communicating_agent import CommunicatingAgent
from clusterAgent import clusterAgent

import numpy as np
import time


class dataAgent(CommunicatingAgent):

    def __init__(self,
                 amas,
                 pos : np.ndarray,
                 clusterTab : list,
                 ageLimit,
                 ) -> None:
        super().__init__(amas)
        self.pos = pos
        self.cluster = None
        self.bestC = None
        self.clusterTab = clusterTab
        self.response = []
        self.attResponse = False
        self.silhouette = None
        self.age = time.time()
        self.ageLimit = ageLimit


    def read_mail(self, mail: 'Mail') -> None:
        if type(mail) == bool:
            if self.attResponse:
                self.response.append(mail)

    def a(self,cluster : clusterAgent):
        """
            Calcule de distance entre le self et tout les points appartenant à cluster
        """
        if cluster == self.cluster:
            #on exclue la data que l'on veut observer
            dataTab = np.delete(cluster.posDataTab, cluster.clusterTab.index(self), 0)
        #distance euclidienne
        distTab = np.abs(np.sum(self.pos - dataTab, axis=0))

        return np.mean(distTab)
        

    def on_perceive(self) -> None:
        #Si on a pas de cluster associé, on regarde le plus proche
        if self.cluster == None:
            posTab = np.array([x.pos for x in self.clusterTab])
            idMinCluster = np.argmin(np.abs(posTab-self.pos))
            self.bestC = self.clusterTab[idMinCluster]
        else:
            #sinon, on regarde si la data se sent "bien" dans le cluster
             a = a(self.cluster)
             clusterTab = np.delete(self.clusterTab, self.clusterTab.index(self.cluster), 0)
             b = np.min([a(x) for x in clusterTab])
             self.silhouette = (b - a)/(np.max(a,b))

    def destroy(self):
        """
            supprime l'agent
        """
        if self.cluster != None:
            self.cluster.removeData(self)
        self.remove_agent()

    def on_act(self) -> None:
        #si la donnee est trop vielle, on la supprime.
        if time.time() - self.age > self.ageLimit:
            self.destroy()
        pass
