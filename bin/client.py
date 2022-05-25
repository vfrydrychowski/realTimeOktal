import numpy as np
import pandas as pd
import socket
import time

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

# test value 
df = pd.read_csv("data/simulation.csv", delim_whitespace=True, index_col='time')
nump = df[['[00].VehicleUpdate-speed.001', '[00].VehicleUpdate-speed.002',
       '[00].VehicleUpdate-speed.003', '[00].VehicleUpdate-accel.001', '[00].VehicleUpdate-accel.002',
       '[00].VehicleUpdate-accel.003', '[00].VehicleUpdate-consumption', '[00].VehicleUpdate-accelerator',
       '[00].VehicleUpdate-brake']].fillna(value=0).to_numpy().T

def recup():
        """
        process of retrieval of simulated values
        """
        for i in range(nump.shape[1]):

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(nump[:,i].tobytes())  
            
            print("recup" + str(i))
            time.sleep(1)

if __name__ == '__main__':
    print("début de transmission")
    recup()
    print("fin de transmission")
            