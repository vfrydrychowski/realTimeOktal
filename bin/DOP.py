import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def featureCalc(signal):
    """
    Compute the mean, min, max, median, 0.25 quantile, 0.75 quantile and standard deviation.
    It is compute on the whole signal length.
    Args:
        signal: a 1-D numpy array of non-null data.
    Returns:
        numpy array : (7,) array of statistics listed above.
    """
    moy = np.mean(signal)
    min = np.min(signal)
    max = np.max(signal)
    median = np.median(signal)
    quart1 = np.quantile(signal, 0.25)
    quart3 = np.quantile(signal, 0.75)
    std = np.std(signal)
    return np.array([moy, min, max, median, quart1, quart3, std])

def pixel(data, nb_feature):
    """
    Compute the statiscal value for each signals in data.
    Args:
        data: (signals,lenght) numpy array
        nb_feature: number of statistical features to be compute
    Returns:
        pix : (signals*nb_feature,) numpy array.
    """
    pix = np.zeros((data.shape[0]*nb_feature))
    for i in range(data.shape[0]):
        pix[i*nb_feature:i*nb_feature+nb_feature] = featureCalc(data[i, :])
    return pix

def image(data, nb_samples, nb_feature):
    #TODO if nb_sample>datasize error
    """
    Compute the DOP of the data
    Args:
        data: (signals,lenght) numpy array
        nb_samples: number of samples to merge in one pixel
        nb_feature: number of statistical features to be compute
    Returns:
        pix : (signals*nb_feature,) numpy array.
    """
    im = np.zeros((data.shape[0]*nb_feature, data.shape[1]//nb_samples))
    for i in range(im.shape[1]):
        im[:,i] = pixel(data[:,nb_samples*i:nb_samples*i+nb_samples], nb_feature)
        #no normalisation for the moment
        #normIm = np.linalg.norm(im, axis=0)
        #im = im/normIm
    return im
    