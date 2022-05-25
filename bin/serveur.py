from multiprocessing import Process,Lock, Condition, Value,SimpleQueue
from multiprocessing.dummy import Array
import numpy as np
import socket
import DOP

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


class process:
    def __init__(self):
        self.lock = Lock() #semaphore
        self.database = np.array([[0]]*9) #databased to be fill
        self.dopLect = Value('i', lock=False)
        self.attLecture = Condition(self.lock)
        self.q = SimpleQueue()

    def constrIm(self):
        """
        fetch data and contruct DOP
        """
        with self.lock:
            while(self.dopLect.value != 0):
                self.attLecture.wait()
            self.dopLect.value += 1
            data = self.q.get() #ERROR wait too long
            print(data)
            print(data.shape)
            self.dopLect.value -= 1
            self.attLecture.notify()
        

    
    def lect(self, taillIm):
        """
        process reading values from recup proccess
        """       
        #initiate proces number waiting for reading data in q
        with self.lock:
            self.dopLect.value = 0

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
                if i%taillIm == 0 and taillIm != 0: 
                    print(">>>>launch dop construction")
                    #start the process of DOP creation
                    Process(target=process().constrIm).start()
                    #send requierd data through q
                    with self.lock:
                        self.q.put(self.database[:,-taillIm:])


if __name__ == '__main__':
    p = process()
    p.lect(10)