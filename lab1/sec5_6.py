import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from ugradio import dft

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

filename ="data_500kHzFreq_3000kHzSamp2.gz"

data = np.loadtxt("./lab1data/"+filename)

sampleRate = 3e6
timeStep = 1/sampleRate

times = np.linspace(-len(data)/(2*sampleRate),(len(data)/2 -1)/sampleRate, len(data))
frequencies = np.arange(-4*sampleRate/2,4*sampleRate/2,sampleRate/len(data))

frequencies, voltageSpectrum = dft.dft(data, times, frequencies)
powerSpectrum = np.multiply(np.abs(voltageSpectrum), np.abs(voltageSpectrum))

fig,ax = plt.subplots(1,1, figsize = (6,4))

ax.plot(frequencies*1e-6, powerSpectrum*1e-6)

for i in np.arange(-2*sampleRate,2*sampleRate+1,sampleRate/2):
    ax.vlines(i*1e-6, -0.1,1,color = "tab:red")

ax.set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax.set_ylabel("Power ($mV^2$)", fontsize = axesLabelSize)

fig.savefig("./images/windows.png")