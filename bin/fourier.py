import numpy as np


def spectrogramme(data: np.array) -> np.array:
    """
    create the 'spectrogram' of data, one fourier transformation for each signal
    Args:
        data : (nb_sample) np.array
    """
    spec = np.array([np.fft.fftshift(np.fft.fft(data[x,:])) for x in range(data.shape[0])])
    return spec

if __name__ == '__main__':
    import clientTest
    import matplotlib.pyplot as plt
    data = np.log(np.abs(spectrogramme(clientTest.nump)))
    plt.imshow(data[:,:50], interpolation='nearest', cmap='magma')
    plt.savefig("im.png", dpi=1200)
    plt.show()