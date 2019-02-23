import json, argparse, sys, numpy as np
from components.DatabaseManager import DatabaseManager
from sql.ArticleTypeSQL import *
import matplotlib.pyplot as plt
from analytics.ArticleNumberLengthCorrelation import ArticleNumberLengthCorrelation

if __name__ == '__main__':
    with open("parameters.json") as fIn:
	    parameters = json.load(fIn)
    
    databaseManager = DatabaseManager(parameters, None)

    analytics1 = ArticleNumberLengthCorrelation((15, 4))
    analytics1.collectData(databaseManager)
    analytics1.createPlot()
    analytics1.show()