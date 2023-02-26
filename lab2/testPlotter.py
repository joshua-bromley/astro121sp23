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

data = np.loadtxt("./lab2data/flattenedSignal.gz")
'''
powSpec = functions.fileToPowerSpec(filenamesLow)
sampleRate = 3.2e6
timeStep = 1/sampleRate

frequencies = np.fft.fftfreq(len(powSpec), timeStep)
'''
fig,ax = plt.subplots(1,1,figsize = (6,4))
ax.plot(data[0],data[1])
#ax[1].plot(frequencies[-450:-80], np.flip(powSpec[80:450]))


plt.savefig("./images/newHLineData.png")

