import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import functions
import colors

rcParams["axes.linewidth"] = 2

rcParams["ytick.right"] = True
rcParams["ytick.direction"] = "in"
rcParams["ytick.minor.visible"] = True
rcParams["ytick.major.left"] = True
rcParams["ytick.major.right"] = True
rcParams["ytick.minor.left"] = True
rcParams["ytick.minor.right"] = True
rcParams["ytick.major.size"] = 8
rcParams["ytick.minor.size"] = 4



rcParams["xtick.top"] = True
rcParams["xtick.direction"] = "in"
rcParams["xtick.minor.visible"] = True
rcParams["xtick.major.top"] = True
rcParams["xtick.major.bottom"] = True
rcParams["xtick.minor.top"] = True
rcParams["xtick.minor.bottom"] = True
rcParams["xtick.major.size"] = 8
rcParams["xtick.minor.size"] = 4

axesLabelSize = 16
tickLabelSize = 12
textSize = 12

gain = 145.37886765112168

lowParams = [1.15345261e7, -2.42777878e-4,  1.43194993e2]
highParams = [8.36720714e6, 4.27338249e-4, 1.44137243e2]

dataLow = np.loadtxt("./lab2data/LO1419.gz")
dataHigh = np.loadtxt("./lab2data/LO1420.gz")

signalLow = dataLow[1][0:1024]
calLow = np.flip(dataLow[1][1024:])

velocitiesLow = dataLow[0][0:1024]

signalLowFlat = np.divide(signalLow, calLow)*gain
lowFlat = signalLowFlat - functions.polyModel(lowParams, velocitiesLow)

signalHigh = dataHigh[1][1024:]
calHigh = np.flip(dataHigh[1][0:1024])
signalHighFlat = np.divide(signalHigh, calHigh)*gain

velocitiesHigh = dataHigh[0][1024:]
highFlat = signalHighFlat - functions.polyModel(highParams, velocitiesHigh) 

fig, ax = plt.subplots(2,1, figsize = (6,8))
ax[0].plot(velocitiesLow*100, signalLowFlat, color = colors.blue)
ax[0].plot(velocitiesLow*100, functions.polyModel(lowParams, velocitiesLow), color = colors.yellow, lw = 2, ls = "--")

ax[1].plot(velocitiesHigh*100, signalHighFlat, color = colors.blue)
ax[1].plot(velocitiesHigh*100, functions.polyModel(highParams, velocitiesHigh), color = colors.yellow, lw = 2, ls = "--")

for axis in ax:
    axis.set_ylabel("Temperature (K)", fontsize = axesLabelSize)
    axis.set_xlabel("Velocity (0.01c)", fontsize = axesLabelSize)
    axis.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

yTicks = np.arange(130,200.1,10)
xTicksLow = np.arange(-0.1,0.041, 0.02)
xTicksHigh = np.arange(-0.06,0.081, 0.02)

ax[0].text(-0.09,190, "LO: 1419.906 MHz", fontsize = textSize)
ax[1].text(0.025,190, "LO: 1420.906 MHz", fontsize = textSize)

ax[0].set_ylim(130,200)
ax[0].set_yticks(yTicks)
ax[0].set_xlim(-0.1,0.04)
ax[0].set_xticks(xTicksLow)
ax[1].set_ylim(130,200)
ax[1].set_yticks(yTicks)
ax[1].set_xlim(-0.06,0.08)
ax[1].set_xticks(xTicksHigh)

plt.tight_layout()
plt.savefig("./images/fig4.png")
plt.savefig("./images/pdfs/fig4.pdf")