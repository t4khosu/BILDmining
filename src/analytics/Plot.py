import matplotlib.pyplot as plt
from abc import ABC, abstractmethod

class Plot(ABC):
    def __init__(self, nrows, ncols, figsize):
        self.fig = plt.figure(figsize=figsize)
        self.nrows = nrows
        self.ncols = ncols
        self.data = None
        super().__init__()

    @abstractmethod
    def collectData(self, db):
        pass

    @abstractmethod
    def createPlot(self):
        pass

    def show(self):
        plt.show()

