from multiprocessing import Process,Lock, Condition, Value,SimpleQueue
from multiprocessing.dummy import Array
import time
import pandas as pd
import numpy as np
import socket

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class process:
    def __init__(self):
        self.lock = Lock()
        self.data = np.array([[0]]*9)
        self.nb_att = Value('i', lock=False)

            
    
    def lect(self):
        """
        process reading values from recup proccess
        """       

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            for i in range(100):
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)
                    if not data:
                        break
                    datanump = np.frombuffer(data, dtype=np.float64)
                    self.data = np.append(self.data, datanump.reshape((datanump.shape[0],1)), axis = 1)
                    print(self.data[:,:])
            

if __name__ == '__main__':
    p = process()
    p.lect()