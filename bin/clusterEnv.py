from pyAmakCore.classes.environment import Environment
import matplotlib.pyplot as plt


class clusterEnv(Environment):

    def __init__(self, dataList : list):
        self.dataList : list = dataList
        super().__init__()
    
    def getData(self):
        if self.dataList == []:
            d = []
        else:
            d = self.dataList.pop(0)
        return d
