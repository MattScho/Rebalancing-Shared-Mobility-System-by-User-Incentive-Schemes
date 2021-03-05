import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

'''

:author: Matthew Schofield
:version: 1.10.2021
'''
class MatrixCreator:

    def __init__(self):
        pass

    def makeGaussianMatrix(self, systemSize, std):
        """
        Returns a 2D Gaussian Matrix
        """
        # Create vector distributed as a Gaussian distribution
        gaussVector = signal.gaussian(systemSize, std=std).reshape(systemSize, 1)

        # Outer multiply of vector to create a Matrix
        gaussMatrix = np.outer(gaussVector, gaussVector)

        return gaussMatrix

    def makeInvGaussianMatrix(self, systemSize, std):
        '''
        Returns an inverse 2D Gaussian Matrix

        :param systemSize:
        :param std:
        :return:
        '''
        # Create inverse Gaussian matrix
        return np.subtract(np.ones((systemSize, systemSize)), self.makeGaussianMatrix(systemSize, std))

    def makeUniformMatrix(self, systemSize):
        '''
        Build a square matrix to represent a Uniform distribution

        :param systemSize: length of matrix sides
        :return: matrix representing a uniform distribution
        '''
        return np.full((systemSize, systemSize), fill_value=1)

    def normalizeMatrix(self, systemSize, matrix):
        '''
        Normalize a matrix such that all elements sum to 1.0,
        this allows the matrix to be used as a probability distribution

        :param systemSize: length of matrix sides
        :param matrix: matrix to normalize
        :return: normalized matrix
        '''
        # Flatten matrix
        matrixFlattened = matrix.reshape((systemSize ** 2))

        # Normalize flattened matrix then reshape to matrix again
        matrixNormalized = np.true_divide(matrixFlattened, sum(matrixFlattened)).reshape((systemSize, systemSize))

        return matrixNormalized

    def flatten(self, systemSize, matrix):
        return matrix.reshape((systemSize ** 2))

    '''
    Visualizations to confirm
    '''
    def showDistribution(self, matrix, title):
        '''
        Show a distribution matrix using pyplot

        :param matrix: matrix to display
        :param title: title of display
        '''
        plt.title(title)
        plt.imshow(matrix, cmap='Greens')
        plt.show()
