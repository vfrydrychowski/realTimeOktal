import scaner.sim
import socket
import time
import numpy as np




class Script:
    def __init__(self):
        # this is called once per scenario execution, during the SCANeR load phase

        ## An input/output variable must be declared between the corresponding labels. 
        ## Example of variable declaration:
        # self.my_simple_variable = 10
        # self.my_complex_variable = scaner.sim.get_vehicles()["MY_VEHICLE"] # type: scaner.sim.Vehicle
        ## see the documentation for more details on input/output variable declaration

        # BEGIN SCANeR script inputs
        # END SCANeR script inputs

        # BEGIN SCANeR script outputs
        # END SCANeR script outputs

        self.HOST = "127.0.0.1"  # The server's hostname or IP address
        self.PORT = 65432  # The port used by the server
        self.carName = 'SmallFamilyCar'
        pass
    
    def recup(self): 
        """
        retrieve infos from simulation with scanner.sim

        Returns:
            pix : numpy array of instant info.
        """
        #retrieve all info of vehicle carName
        out = scaner.sim.get_vehicles()[self.carName].get_output()
        
        speed = out.speed
        accel = out.accel
        conso = out.consumption
        accelPedal = out.accelerator
        brakePedal = out.brake/400 #max force of a car's brake = 400 N
        return np.array([speed.x, speed.y, speed.z, accel.x, accel.y, accel.z, conso, accelPedal, brakePedal]).reshape((9,1))
    
    def send(self, data):
        """
        send data to the host (HOST variable)
        Args:
            data: (signals,) numpy array
        """
        #initiate a connection to host
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(data.tobytes()) #send all bytes from an column of the array
            print("sending")    

    def run(self):
        # this is called at each scenario step
        self.send(self.recup())
        pass

def main():
    return 0