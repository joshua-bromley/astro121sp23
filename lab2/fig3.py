import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import ugradio
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

def hztoV(x):
    return (-5.7055021676055246e-05-((x*1e6-1420.40575e6)/1420.40575e6))*1e2

def vtoHz(x):
    return (1420.40575e6*(-5.7055021676055246e-05-x*1e-2)+1420.40575e6)/1e6


dataLow = np.loadtxt("./lab2data/LO1419.gz")
dataHigh = np.loadtxt("./lab2data/LO1420.gz")

signalLow = dataLow[1]
signalHigh = dataHigh[1]

freqsLow = dataLow[2]
freqsHigh = dataHigh[2]

fig,ax = plt.subplots(1,1, figsize = (6,4))

ax.plot(np.fft.fftshift(freqsLow)*1e-6, np.fft.fftshift(signalLow), color = colors.blue, label = "LO 1419.906 MHz")
ax.plot(np.fft.fftshift(freqsHigh)*1e-6, np.fft.fftshift(signalHigh), color = colors.yellow, label = "LO 1420.906 MHz")

ax.set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax.set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)

yTicks = np.arange(0,25.1,5)
xTicks = np.arange(1418,1423.1,1)

ax.set_xlim(1418,1423)
ax.set_xticks(xTicks)
ax.set_ylim(-1,26)
ax.set_yticks(yTicks)

ax.legend(frameon = False, fontsize = textSize)

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

secax = ax.secondary_xaxis("top", functions = (hztoV,vtoHz))
secax.set_xlabel("Velocity (0.01c)", fontsize = axesLabelSize)
secax.tick_params(axis = 'x', bottom = False, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
secax.tick_params(axis = 'x', bottom = False, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)



plt.tight_layout()

plt.savefig("./images/fig3.png")
plt.savefig("./images/pdfs/fig3.pdf")