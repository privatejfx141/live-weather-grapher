from numpy import *
from math import *
import matplotlib.pyplot as plt


xvals = linspace(-10,10,200)

yvals = []
for x in xvals:
    y = cos(x)
    yvals.append(y)

if __name__ == "__main__":
    plt.plot(xvals,yvals)
    plt.xticks([-3*pi -2*pi -pi 0 pi 2*pi 3*pi])
    plt.show()
