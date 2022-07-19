from pyAmakCore.classes.environment import Environment
import matplotlib.pyplot as plt


class clusterEnv(Environment):

    def __init__(self, dataList):
        self.dataList = dataList
        super().__init__()
    
    def getData(self):
        try:
            d = self.dataList.pop(0)
        except IndexError:
            d = []
        return d
