import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rcParams

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

filename = "../lab1data/150MHzLO_149MHzRF_maxSamp_SDR_10by2048_AliOff"

data = np.loadtxt(filename, dtype = complex)
data = np.delete(data, np.arange(1800,2048,1), axis = 1)
sampleRate = 3.2e6
timeStep = 1/sampleRate
times = np.arange(0,(len(data[2]))*timeStep,timeStep)

voltageSpectrum = np.abs(np.fft.fft(data[2]))
powerSpectrum = np.multiply(voltageSpectrum, voltageSpectrum)
frequencies = np.fft.fftfreq(len(data[2]), timeStep)

filenameTwo = "../lab1data/150MHzLO_151MHzRF_maxSamp_SDR_10by2048_AliOff"

dataTwo = np.loadtxt(filenameTwo, dtype = complex)
dataTwo = np.delete(dataTwo, np.arange(1800,2048,1), axis = 1)
sampleRate = 3.2e6
timeStep = 1/sampleRate
times = np.arange(0,(len(data[2]))*timeStep,timeStep)

voltageSpectrumTwo = np.abs(np.fft.fft(dataTwo[2]))
powerSpectrumTwo = np.multiply(voltageSpectrumTwo, voltageSpectrumTwo)
frequenciesTwo = np.fft.fftfreq(len(dataTwo[2]), timeStep)

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(times[100:200]*1e6, data[2][100:200], marker = 'o', color = "#0d265c")
ax[0].plot(times[100:200]*1e6, dataTwo[2][100:200], marker = 'o', color = "#ffa600")
#ax[0].plot(x,y,color = "black", ls = ":")

ax[1].plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6, color = "#0d265c", ls = "--", label = "149 MHz")
ax[1].plot(np.fft.fftshift(frequenciesTwo)*1e-6, np.fft.fftshift(powerSpectrumTwo)*1e-6, color = "#ffa600", ls = ":", label = "151 MHz")

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

ax[0].set_xlim(30,65)
ax[0].set_xticks(np.arange(30,65.1,5))
ax[0].set_ylim(-0.32,0.32)
ax[0].set_yticks(np.arange(-0.3,0.31,0.1))

ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)

ax[1].legend(frameon = False, fontsize = textSize)

ax[1].set_xlim(-1.6,1.6)
ax[1].set_xticks(np.arange(-1.6,1.61,0.4))
ax[1].set_ylim(-0.005,0.14)
ax[1].set_yticks(np.arange(0,0.141,0.02))


plt.tight_layout()

plt.savefig("../images/mixerSDRTimeSeries.png")
plt.savefig("../images/pdfs/mixerSDRTimeSeries.pdf")

for i in range(len(frequencies)):
    if powerSpectrum[i]*1e-6 > 0.05:
        print(frequencies[i])

for i in range(len(frequenciesTwo)):
    if powerSpectrumTwo[i]*1e-6 > 0.08:
        print(frequenciesTwo[i])