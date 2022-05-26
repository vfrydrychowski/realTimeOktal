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
        self.lock = Lock() #semaphore
        self.database = np.array([[0]]*9) #databased to be fill
        self.dataAtt = Value('i', lock=False)
        self.isReading = Value('i', lock=False)
        self.attLecture = Condition(self.lock)
        self.q = SimpleQueue()

    def constrIm(self):
        """
        fetch data and construct DOP
        """
        with self.lock:
            while(self.dataAtt.value == 0 or self.isReading.value > 0):
                #someone is reading or there is no data waiting
                self.attLecture.wait()
            self.isReading.value += 1 #begin reading
            data = self.q.get()
            print(data)
            print(data.shape)
            self.dataAtt.value -= 1 #one data fetch
            self.isReading.value -= 1 #end reading
            self.attLecture.notify()
        start = time.time()
        im = DOP.image(data, 20, 7)
        end = time.time()
        print(">> duree dop : " + str(end-start))
        plt.imshow(im, interpolation='nearest')
        plt.show()
        time.sleep(2)

        

    
    def lect(self, taillIm):
        """
        process reading values from recup proccess
        """       
        #initiate proces number waiting for reading data in q
        with self.lock:
            self.dataAtt.value = 0
            self.isReading.value = 0
        p = process()

        #initiate tcp connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen() #serveur listening to clints requests

            for i in range(1469): #subjectiv numbre of connection allowed for this process
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
                if i%taillIm == 0 and i != 0: 
                    print(">>>>launch dop construction")
                    #start the process of DOP creation
                    Process(target=p.constrIm).start()
                    #send requierd data through q
                    imData = np.copy(self.database[:,-taillIm:])
                    with p.lock:
                        #print(imData.shape)
                        p.q.put(imData)
                        p.dataAtt.value += 1
                        print("send data")
                        p.attLecture.notify()


if __name__ == '__main__':
    p = process()
    p.lect(600)