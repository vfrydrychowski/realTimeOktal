import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

class CNN(nn.Module):
    def __init__(self, nb_feature = 7, nb_sign = 9,hidden= 832, kWidth = 5, width = 600):
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(in_channels=1,out_channels=32,kernel_size=(nb_feature*nb_sign,kWidth))
        self.conv2 = nn.Conv2d(in_channels=32,out_channels=64,kernel_size=(1,2))

        self.pool = nn.MaxPool2d(1, 2)

        conv1sizex , conv1sizey = (nb_feature*nb_sign, width-kWidth//2*2)
        pool1sizex, pool1sizey = (conv1sizex, conv1sizey//2)
        conv2sizex , conv2sizey = (pool1sizex, pool1sizey-2)
        pool2sizex, pool2sizey = (conv2sizex, conv2sizey//2)
        self.pool2size = 64*(pool2sizex*pool2sizey)

        self.fc1 = nn.Linear(self.pool2size, hidden)
        self.fc2 = nn.Linear(hidden, 2)

        self.norm0 = nn.BatchNorm2d(1)
        self.normc1 = nn.BatchNorm2d(32)
        self.normc2 = nn.BatchNorm2d(64)

        self.normH = nn.BatchNorm1d(hidden)


    def forward(self, x):
        
        #x = self.norm0(x)

        x = self.conv1(x)
        #x = self.normc1(x)
        x = nn.functional.relu(x)
        x = self.pool(x)

        x = self.conv2(x)
        #x = self.normc2(x)
        x = nn.functional.relu(x)
        x = self.pool(x)

        x = x.view(-1, self.pool2size) # flatten

        x = self.fc1(x)
        #self.normH(x)
        x = nn.functional.relu(x)
        x = self.fc2(x)

        return x 

if __name__ == '__main__':
    import DOP
    import simulator

    data = simulator.nump[:,:300]
    dop = DOP.image(data, 10, 7)#issue in image builder (length = 1)
    dopTensor = ((torch.from_numpy(dop)).unsqueeze(0)).unsqueeze(0)
    plt.imshow(dop, interpolation='nearest')
    plt.savefig("im.png", dpi=1200)
    plt.show()
    cnn = CNN(width=300)
    print(cnn(dopTensor))
