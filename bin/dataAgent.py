"""
Data agent
"""

from pyAmakCore.classes.communicating_agent import CommunicatingAgent
from pyAmakCore.classes.communicating_agent import Mail

import numpy as np
import time


class dataAgent(CommunicatingAgent):

    def __init__(self,
                 amas,
                 pos : np.ndarray,
                 clusterTab : list,
                 ageLimit,
                 silouhetteThreshold : int
                 ) -> None:
        super().__init__(amas)
        self.pos : np.ndarray = pos
        self.cluster  = None
        self.bestC  = None
        self.clusterTab = clusterTab
        #self.response = []
        #self.attResponse = False
        self.silhouette = None
        self.age = time.time()
        self.ageLimit = ageLimit
        self.silouhetteThreshold = silouhetteThreshold


    def read_mail(self, mail: Mail) -> None:
        #si on est accepté dans le cluster, on s'assigne au cluster
        if mail.get_message():
            self.cluster = self.get_amas().get_agent(mail.get_id_sender())
            

    def a(self,cluster ):
        """
            Calcule de distance entre le self et tout les points appartenant à cluster
        """
        if cluster.dataTab == []:
            return np.float64(0)
        if cluster == self.cluster:
            #on exclue la data que l'on veut observer
            dataindex = cluster.dataTab.index(self)
            dTab = np.delete(cluster.posDataTab, dataindex, 0)
        else:
            dTab = cluster.posDataTab
        if dTab.size == 0:
            return np.float64(0)
        #distance euclidienne
        distTab = np.abs(np.sum( np.array(self.pos) - dTab))

        return np.mean(distTab)
        
    def findClosestCluster(self):
        posTab = np.array([x.pos for x in self.clusterTab])
        idMinCluster = np.argmin(np.sum(np.abs(posTab-self.pos), axis = 1))
        self.bestC = self.clusterTab[idMinCluster]

    def on_perceive(self) -> None:
        #Si on a pas de cluster associé, on regarde le plus proche
        if self.cluster == None:
            self.findClosestCluster()
        else:
            #sinon, on regarde si la data se sent "bien" dans le cluster
            A = self.a(self.cluster)
            clusterTab = np.delete(self.clusterTab, self.clusterTab.index(self.cluster), 0)
            B = np.min([self.a(x) for x in clusterTab])
            max = np.maximum(A,B)
            if max != 0:
                self.silhouette = (B - A)/(max)
            else:
                self.silhouette = (B - A)

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
        #si la données n'a pas de cluster, on envois un mess au cluster leplus proche
        if self.cluster == None:
            self.send_message(self.get_id, self.bestC.get_id())
        #sinon on verifie la cohérence des données
        elif self.silhouette < self.silouhetteThreshold:
            self.cluster.removeData(self)
            self.cluster = None
            #on envois un message au cluster le plus proche
            self.bestC = self.findClosestCluster()
            self.send_message(self.get_id(), self.bestC.get_id())
        
