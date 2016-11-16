'''
Created on Jul 26, 2015

@author: joro
'''
import numpy as np
from Evaluation import calcAveragePrecisionAtK

if __name__ == "__main__":
    relevances = np.array([1, 0, 1, 0, 1])
    K = 1
    cardinality = 5
    aveP = calcAveragePrecisionAtK(relevances, K, cardinality)
    print aveP