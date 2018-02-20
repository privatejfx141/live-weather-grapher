from numpy import *
from math import *
import matplotlib.pyplot as plt


xvals = linspace(-10,10,200)

yvals = []
for x in xvals:
    y = cos(x)
    yvals.append(y)

plt.plot(xvals,yvals)
plt.xticks([-3*pi -2*pi -pi 0pi 2*pi 3*pi])
plt.show()
