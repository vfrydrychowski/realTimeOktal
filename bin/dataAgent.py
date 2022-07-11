"""
Data agent
"""

from pyAmakCore.classes.communicating_agent import CommunicatingAgent

import numpy as np


class CommunicatingAnt(CommunicatingAgent):

    def __init__(self,
                 amas,
                 pos : np.ndarray,
                 clusterTab
                 ) -> None:
        super().__init__(amas)
        self.pos = pos
        self.cluster = None
        self.bestC = None
        self.clusterTab = clusterTab
        self.response = []
        self.attResponse = False


    def read_mail(self, mail: 'Mail') -> None:
        if type(mail) == bool:
            if self.attResponse:
                self.response.append(mail)

    def on_perceive(self) -> None:
        pass

    def on_act(self) -> None:
        pass
