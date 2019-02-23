import numpy as np
from analytics.Plot import Plot
from sql.ArticleTypeSQL import *
from scipy.stats.stats import pearsonr
import matplotlib.pyplot as plt

class ArticleNumberLengthCorrelation(Plot):
    def __init__(self, figsize):
        super().__init__(1, 3, figsize)

    def collectData(self, db):
        db.startConnection()
        avgArticleLengths = countAverageArticleLengths(db, premium=False)
        articleTypeCount = countArticlesByType(db)
        db.closeConnection()

        articleTypesList = [a[0] for a in avgArticleLengths]
        avgArticleLengthsList = [int(v[1]) for v in avgArticleLengths]

        articleTypeCountList = {a:-1 for a in articleTypesList}
        for var in articleTypeCount:
            articleTypeCountList[var[0]] = var[1]
        articleTypeCountList = list(articleTypeCountList.values())

        self.data = [articleTypesList, avgArticleLengthsList, articleTypeCountList]

    def createPlot(self):
        self.fig.subplots_adjust(bottom=0.3, wspace=0.4) 
        ax1 = self.fig.add_subplot(self.nrows, self.ncols, 1)
        ax2 = self.fig.add_subplot(self.nrows, self.ncols, 2)
        ax3 = self.fig.add_subplot(self.nrows, self.ncols, 3)
        axes = [ax1, ax2, ax3]

        N = len(self.data[0])
        barWidth = 0.8
        barColor = '#AAAAAA'
        ind = np.arange(N)

        for c, ax in enumerate(axes[:2]):
            ax.bar(ind, self.data[c+1], barWidth, color=barColor)
            ax.set_xticks(ind)
            xtickNames = ax.set_xticklabels(self.data[0])
            plt.setp(xtickNames, rotation=90, fontsize=8)
            ax.set_xlabel('Art. Types')
            ax.wspance = 0.2

        ax1.set_ylabel('Avg. Art. Length / Chars')
        ax1.set_title('Avg. Art. Lengths / Art. Types')

        ax2.set_ylabel('#Art.')
        ax2.set_title('Count Art./Types')

        ax3.set_ylabel('Norm Count')
        ax3.set_xlabel('Norm Avg. lenghts')
        ax3.set_title('Pearson Visualization')

        pearson = pearsonr(self.data[1], self.data[2])[0]
        norm1 = [float(i)/sum(self.data[1]) for i in self.data[1]]
        norm2 = [float(i)/sum(self.data[2]) for i in self.data[2]]

        maxValue = max(norm1 + norm2)
        maxValue += (1/10) * maxValue
        minValue = min(norm1 + norm2)
        minValue -= (1/10) * minValue

        ax3.set_xlim([minValue, maxValue])  
        ax3.set_ylim([minValue, maxValue])

        avg1 = sum(norm1) / len(norm1)
        avg2 = sum(norm2) / len(norm2)
        n = avg2 - pearson * avg1

        x = np.array([minValue, maxValue])
        ax3.plot(x, x * pearson + n)
        ax3.plot(norm1, norm2, 'o')