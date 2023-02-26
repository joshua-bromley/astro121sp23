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

axesLabelSize = 17
tickLabelSize = 13
textSize = 13

filenamesCold = [["./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp2.gz"],["./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp3.gz"]]
filenamesHot = [["./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp2.gz"],["./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp3.gz"]]



coldLow = functions.fileToPowerSpec(filenamesCold[0])
coldHigh = functions.fileToPowerSpec(filenamesCold[1])

hotLow = functions.fileToPowerSpec(filenamesHot[0])
hotHigh = functions.fileToPowerSpec(filenamesHot[1])

sampleRate = 3.2e6
timeStep = 1/sampleRate

freqsLow = np.fft.fftfreq(len(coldLow), timeStep) + 1419.906e6
freqsHigh = np.fft.fftfreq(len(coldLow), timeStep) + 1420.906e6

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(np.fft.fftshift(freqsLow)*1e-6, np.fft.fftshift(coldLow), label = "Cold Sky", color = colors.blue)
ax[0].plot(np.fft.fftshift(freqsLow)*1e-6, np.fft.fftshift(hotLow), label = "Humans", color = colors.yellow)

ax[0].set_xlabel("Frequencies (MHz)", fontsize = axesLabelSize)
ax[0].set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)
ax[0].legend(frameon = False, fontsize = textSize)

ax[1].plot(np.fft.fftshift(freqsHigh)*1e-6, np.fft.fftshift(coldHigh), label = "Cold Sky", color = colors.blue)
ax[1].plot(np.fft.fftshift(freqsHigh)*1e-6, np.fft.fftshift(hotHigh), label = "Humans", color = colors.yellow)

ax[1].set_xlabel("Frequencies (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)
ax[1].legend(frameon = False, fontsize = textSize)

ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

yTicks = np.arange(0,41,10)
xTicksLow = np.arange(1418,1422.1)
xTicksHigh = np.arange(1419, 1423.1)

ax[0].set_ylim(-2,42)
ax[0].set_yticks(yTicks)
ax[0].set_xlim(1418,1422)
ax[0].set_xticks(xTicksLow)

ax[1].set_ylim(-2,42)
ax[1].set_yticks(yTicks)
ax[1].set_xlim(1419,1423)
ax[1].set_xticks(xTicksHigh)


plt.tight_layout()

plt.savefig("./images/fig2.png")
plt.savefig("./images/pdfs/fig2.pdf")

#gain = functions.calcGain(filenamesCold, filenamesHot)
#print(gain)
