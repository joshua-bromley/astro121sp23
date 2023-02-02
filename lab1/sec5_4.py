import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rcParams
import  ugradio as ug

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
frequencies = np.arange(-sampleRate/2,sampleRate/2,sampleRate/len(data))

frequencies, voltageSpectrum = ug.dft.dft(data, times, frequencies)
powerSpectrum = np.multiply(np.abs(voltageSpectrum), np.abs(voltageSpectrum))

leakedFrequencies = np.arange(-sampleRate/2,sampleRate/2,0.001*sampleRate/len(data))
leakedFrequencies, leakedVoltageSpectrum = ug.dft.dft(data, times, frequencies, vsamp =1)
leakedPowerSpectrum = np.multiply(np.abs(leakedVoltageSpectrum), np.abs(leakedVoltageSpectrum))

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(leakedFrequencies*1e-6,leakedPowerSpectrum*1e-6)
ax[0].plot(frequencies*1e-6, powerSpectrum*1e-6, ls = ":")
ax[0].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[0].set_ylabel("Power (mV)", fontsize = axesLabelSize)

ax[0].set_yscale("log")

ax[1].plot(leakedFrequencies*1e-6, leakedPowerSpectrum*1e-6)
ax[1].plot(frequencies*1e-6, powerSpectrum*1e-6, ls = ":")
ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (mV)", fontsize = axesLabelSize)

ax[1].set_xlim(0.6,0.7)
#ax[1].set_ylim(0,1)

ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.savefig("./images/spectralLeakage.jpg")
