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