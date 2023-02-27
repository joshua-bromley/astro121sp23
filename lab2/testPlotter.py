import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import functions

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

data = np.loadtxt("./lab2data/cassie_1419_906MHzLO_signalRF_maxSamp.gz", dtype = complex)

voltSpec = np.abs(np.fft.fft(data[0:2]))
powSpec = np.multiply(voltSpec,voltSpec)
sampleRate = 3.2e6
timeStep = 1/sampleRate

diff = (powSpec[0]-powSpec[1])
variance = np.mean(diff**2)

frequencies = np.fft.fftfreq(len(powSpec[0]), timeStep)

fig,ax = plt.subplots(1,1,figsize = (6,4))
ax.plot(frequencies, diff**2)
#ax[1].plot(frequencies[-450:-80], np.flip(powSpec[80:450]))


plt.savefig("./images/rawdata.png")

print(variance)

