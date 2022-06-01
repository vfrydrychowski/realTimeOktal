from multiprocessing import Process,Lock, Condition, Value,SimpleQueue
from multiprocessing.dummy import Array
import numpy as np
import socket
import DOP
import time
import matplotlib.pyplot as plt

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class process:
    def __init__(self):
        self.database = np.array([[0]]*9) #databased to be fill

    def constrIm(self, data):
        """
        fetch data and construct DOP
        """

        start = time.time()
        im = DOP.image(data, 20, 7)
        end = time.time()
        print(">> duree dop : " + str(end-start))
        plt.imshow(im, interpolation='nearest')
        plt.show()

        

    
    def lect(self, taillIm, recouvrement):
        """
        process reading values from recup proccess
        """

        #initiate tcp connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() #serveur listening to clints requests
            i = 0
            while(1): #subjectiv numbre of connection allowed for this process
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
                    self.database= np.append(self.database, datanump.reshape((datanump.shape[0],1)), axis = 1)
                    #print(self.data[:,:])
                
                #when there is enough data, a DOP is created
                if i%(taillIm//recouvrement) == 0 and i >= taillIm: 
                    print(">>>>launch dop construction")
                    #start the process of DOP creation
                    
                    imData = np.copy(self.database[:,-taillIm:])

                    Process(target=p.constrIm, args=(imData,)).start()                    
                   #print(imData.shape)
                    print("send data")
                i += 1


if __name__ == '__main__':
    p = process()
    p.lect(200, 1)