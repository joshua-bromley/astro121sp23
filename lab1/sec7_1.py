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

block = 0

filename = "./lab1data/zad1Mixer_700kHzLO_665kHzRF_DSB_10by2048"

data = np.loadtxt(filename)
data = np.delete(data, np.arange(1800,2048,1), axis = 1)
sampleRate = 3e6
timeStep = 1/sampleRate
times = np.arange(0,(len(data[block]))*timeStep,timeStep)

voltageSpectrum = np.abs(np.fft.fft(data[block]))
powerSpectrum = np.multiply(voltageSpectrum, voltageSpectrum)
frequencies = np.fft.fftfreq(len(data[block]), timeStep)

filenameTwo = "./lab1data/zad1Mixer_700kHzLO_735kHzRF_DSB_10by2048"

dataTwo = np.loadtxt(filenameTwo)
dataTwo = np.delete(dataTwo, np.arange(1800,2048,1), axis = 1)
sampleRate = 3e6
timeStep = 1/sampleRate
times = np.arange(0,(len(data[block]))*timeStep,timeStep)

voltageSpectrumTwo = np.abs(np.fft.fft(dataTwo[block]))
powerSpectrumTwo = np.multiply(voltageSpectrumTwo, voltageSpectrumTwo)
frequenciesTwo = np.fft.fftfreq(len(dataTwo[block]), timeStep)

fig, ax = plt.subplots(1,2, figsize = (12,4))

ax[0].plot(times[100:500]*1e6, data[block][100:500], marker = 'o', color = "#0d265c")
ax[0].plot(times[100:500]*1e6, dataTwo[block][100:500], marker = 'o', color = "#ffa600")
#ax[0].plot(x,y,color = "black", ls = ":")

ax[1].plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6, color = "#0d265c", ls = "--")
ax[1].plot(np.fft.fftshift(frequenciesTwo)*1e-6, np.fft.fftshift(powerSpectrumTwo)*1e-6, color = "#ffa600", ls = ":")

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

ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)


plt.tight_layout()

plt.savefig("./images/mixerTimeSeries.png")
#plt.savefig("../images/pdfs/timeSeries.pdf")

fig2, ax2 = plt.subplots(1,1, figsize = (6,4))
voltageSpectrum = np.fft.fft(data[5])

ax2.plot(np.fft.fftshift(frequencies)*1e-6,np.fft.fftshift(np.real(voltageSpectrum))*1e-6, color= "#0d265c")
ax2.plot(np.fft.fftshift(frequencies)*1e-6,np.fft.fftshift(np.imag(voltageSpectrum))*1e-6, color = "#ffa600")

ax2.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax2.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax2.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax2.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax2.set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax2.set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./images/mixerVoltageSpectrum.png")