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

filename = "../lab1data/data_500kHzFreq_3000kHzSamp.txt"

data = np.loadtxt(filename)
sampleRate = 3e6
timeStep = 1/sampleRate
times = np.arange(0,(len(data)+1)*timeStep,timeStep)

voltageSpectrum = np.abs(np.fft.fft(data))
powerSpectrum = np.multiply(voltageSpectrum, voltageSpectrum)
frequencies = np.fft.fftfreq(len(data), timeStep)

x = np.linspace(32,50,200)
y = np.cos((x-34)*np.pi/0.6)

fig, ax = plt.subplots(1,2, figsize = (12,4))

ax[0].plot(times[100:150]*1e6, data[100:150], marker = 'o', color = "black")
#ax[0].plot(x,y,color = "black", ls = ":")

ax[1].plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6, color = "black")

ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax[0].set_xlabel("Time (ms)", fontsize = axesLabelSize)
ax[0].set_ylabel("Voltage (Arbitrary)", fontsize = axesLabelSize)

ax[0].set_xlim(32,50)
ax[0].set_xticks(np.arange(32,50.1,2))
ax[0].set_ylim(-1.1,1.1)
ax[0].set_yticks(np.arange(-1,1.1,0.5))

ax[1].set_xlim(-1.5,1.5)
ax[1].set_xticks(np.arange(-1.5,1.51,0.5))
ax[1].set_ylim(-0.02,0.62)
ax[1].set_yticks(np.arange(0,0.61,0.1))

ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)

plt.tight_layout()

plt.savefig("../images/timeSeries.png")
plt.savefig("../images/pdfs/timeSeries.pdf")

maxPosFreqIndex = np.argmax(powerSpectrum[0:1000])
maxNegFreqIndex = np.argmax(powerSpectrum[-1000:-1]) + len(powerSpectrum)-1000

maxPosFreq = frequencies[maxPosFreqIndex]
maxNegFreq = frequencies[maxNegFreqIndex]

print(maxPosFreq, maxNegFreq)