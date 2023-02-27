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

filename = "./lab2data/flattenedSignal.gz"
data = np.loadtxt(filename)
velocities = data[0]
signal = data[1]

gaussParams = [-3.50913783e-5,  3.21491712e-5,  3.62617252e-3, -1.75673198e-4,
  6.25805193e-5,  4.49589864e-3]

fig, ax = plt.subplots(1,1, figsize = (6,4))
ax.plot(velocities*100, signal, color = colors.blue)
ax.plot(velocities*100, functions.doubleGaussModel(gaussParams, velocities), color = colors.yellow, lw = 2)

ax.set_xlabel("Velocity (0.1c)", fontsize = axesLabelSize)
ax.set_ylabel("Relative Temperature (K)", fontsize = axesLabelSize)

ax.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

yTicks = np.arange(-10,61,10)
xTicks = np.arange(-0.04,0.021,0.01)
ax.set_ylim(-10,60)
ax.set_yticks(yTicks)
ax.set_xlim(-0.04,0.02)
ax.set_xticks(xTicks)

plt.tight_layout()
plt.savefig("./images/fig5.png")
plt.savefig("./images/pdfs/fig5.pdf")

residuals = signal - functions.doubleGaussModel(gaussParams, velocities)

fig1, ax1 = plt.subplots(1,1, figsize = (6,4))
histogram = ax1.hist(residuals, bins = 40, density= True, color = colors.blue)

ax1.set_ylabel("Density", fontsize = axesLabelSize)
ax1.set_xlabel("Residual (K)", fontsize = axesLabelSize)

ax1.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

yTicks = np.arange(0,0.21,0.025)
xTicks = np.arange(-7.5,10.1,2.5)
ax1.set_ylim(0,0.2)
ax1.set_yticks(yTicks)
ax1.set_xlim(-7.5,10)
ax1.set_xticks(xTicks)

plt.tight_layout()
plt.savefig("./images/fig6.png")
plt.savefig("./images/pdfs/fig6.pdf")

