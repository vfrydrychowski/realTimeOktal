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
        self.lock = Lock() #semaphore
        self.data = np.array([[0]]*9) #databased to be fill

            
    
    def lect(self):
        """
        process reading values from recup proccess
        """       
        #initiate tcp connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() #serveur listening to clints requests

            for i in range(100): #subjectiv numbre of connection allowed for this process
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    data = conn.recv(1024)

                    #TODO better error case for corrupted data
                    if not data: 
                        break

                    #transform bit object to numpy array
                    datanump = np.frombuffer(data, dtype=np.float64) 
                    #append collected data to database
                    self.data = np.append(self.data, datanump.reshape((datanump.shape[0],1)), axis = 1)
                    #print(self.data[:,:]) 
            

if __name__ == '__main__':
    p = process()
    p.lect()