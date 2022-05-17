from multiprocessing import Process,Lock, Condition, Value,SimpleQueue
from multiprocessing.dummy import Array
import time
import pandas as pd
import numpy as np

# test value 
df = pd.read_csv("../data/simulation.csv", delim_whitespace=True, index_col='time')
nump = df[['[00].VehicleUpdate-speed.001', '[00].VehicleUpdate-speed.002',
       '[00].VehicleUpdate-speed.003', '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002',
       '[00].VehicleUpdate-accel.003', '[00].VehicleUpdate-consumption', '[00].VehicleUpdate-accelerator',
       '[00].VehicleUpdate-brake']].fillna(value=0).to_numpy().T

class process:
    def __init__(self):
        self.lock = Lock()
        self.data = np.array([[0]]*9)
        self.attLecture = Condition(self.lock)
        self.q = SimpleQueue()
        self.nb_att = Value('i', lock=False)


    def recup(self):
        """
        process of retrieval of simulated values
        """
        for i in range(nump.shape[1]):
            with self.lock:
                self.q.put(np.resize(nump[:,i], (nump.shape[0], 1)))
                self.nb_att.value += 1
                print("recup" + str(i))
                self.attLecture.notify()
            time.sleep(1)
            
    
    def lect(self):
        """
        process reading values from recup proccess
        """       
        for i in range(nump.shape[1]):
            with self.lock:
                #tant que le buffer est vide
                while(self.nb_att.value == 0):
                    self.attLecture.wait()
                self.data = np.append(self.data, self.q.get(), axis = 1)
                self.nb_att.value -= 1
                print(self.data[:,:])

if __name__ == '__main__':
    p = process()
    simu = Process(target=p.recup)
    simu.start()
    lect = Process(target=p.lect)
    lect.start()