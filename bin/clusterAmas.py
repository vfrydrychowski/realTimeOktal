from pyAmakCore.classes.amas import Amas

class clusterAmas(Amas):

    def get_agent(self, id):
        l = [x for x in self.get_agents() if x.get_id() == id]
        return l[0]
