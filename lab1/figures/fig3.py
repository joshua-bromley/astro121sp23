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

filename = "../lab1data/data_500kHzFreq_2000kHzSamp.txt"

data = np.loadtxt(filename)
sampleRate = 2e6
timeStep = 1/sampleRate

filenameTwo = "../lab1data/data_500kHzFreq_1000kHzSamp.txt"
dataTwo = np.loadtxt(filenameTwo)
sampleRateTwo = 1e6 
timeStepTwo = 1/sampleRateTwo

times = np.linspace(-len(data)/(2*sampleRate),(len(data)/2 -1)/sampleRate, len(data))
frequencies = np.arange(-2.5*sampleRate/2,2.5*sampleRate/2,sampleRate/len(data))

frequencies, voltageSpectrum = dft.dft(data, times, frequencies)
powerSpectrum = np.multiply(np.abs(voltageSpectrum), np.abs(voltageSpectrum))
maxPower = np.max(powerSpectrum)
powerSpectrum = powerSpectrum/(maxPower)

timesTwo = np.linspace(-len(dataTwo)/(2*sampleRateTwo),(len(dataTwo)/2 -1)/sampleRateTwo, len(dataTwo))
frequenciesTwo = np.arange(-5*sampleRateTwo/2,5*sampleRateTwo/2,sampleRateTwo/len(dataTwo))

frequenciesTwo, voltageSpectrumTwo = dft.dft(dataTwo, timesTwo, frequenciesTwo)
powerSpectrumTwo = np.multiply(np.abs(voltageSpectrumTwo), np.abs(voltageSpectrumTwo))
maxPowerTwo = np.max(powerSpectrumTwo)
powerSpectrumTwo = powerSpectrumTwo/maxPowerTwo

fig, ax = plt.subplots(2,1, figsize = (6,8))

nyquistZone = int(len(frequencies)/5)
ax[0].plot(frequencies*1e-6,powerSpectrum, color = "#ffa600", zorder = 1)
ax[0].plot(frequencies[int(0.5*nyquistZone):-int(0.5*nyquistZone)]*1e-6,powerSpectrum[int(0.5*nyquistZone):-int(0.5*nyquistZone)], color = "#c4346b", zorder = 2)
ax[0].plot(frequencies[int(1.5*nyquistZone):-int(1.5*nyquistZone)]*1e-6,powerSpectrum[int(1.5*nyquistZone):-int(1.5*nyquistZone)], color = "#0d265c", zorder = 3)

nyquistZone = int(len(frequenciesTwo)/10)
ax[1].plot(frequenciesTwo*1e-6, powerSpectrumTwo, color = "#ffa600", zorder = -1)
ax[1].plot(frequenciesTwo[nyquistZone: -nyquistZone]*1e-6, powerSpectrumTwo[nyquistZone: -nyquistZone], color = "#f76148", zorder = 1)
ax[1].plot(frequenciesTwo[2*nyquistZone: -2*nyquistZone]*1e-6, powerSpectrumTwo[2*nyquistZone: -2*nyquistZone], color = "#c4346b", zorder = 3)
ax[1].plot(frequenciesTwo[3*nyquistZone: -3*nyquistZone]*1e-6, powerSpectrumTwo[3*nyquistZone: -3*nyquistZone], color = "#722e75", zorder = 4)
ax[1].plot(frequenciesTwo[4*nyquistZone: -4*nyquistZone]*1e-6, powerSpectrumTwo[4*nyquistZone: -4*nyquistZone], color = "#0d265c", zorder = 5)



ax[0].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[0].xaxis.set_label_position("top")
ax[0].set_ylabel("Normalized Power", fontsize = axesLabelSize)

ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Normalized Power",fontsize = axesLabelSize)

ax[0].set_xlim(-2.5,2.5)
ax[0].set_xticks(np.arange(-2.5,2.6,0.5))
ax[1].set_xlim(-2.5,2.5)
ax[1].set_xticks(np.arange(-2.5,2.6,0.5))

ax[0].set_ylim(-0.05,1.25)
ax[0].set_yticks(np.arange(0,1.21,0.2))
ax[1].set_ylim(1.25,-0.05)
ax[1].set_yticks(np.arange(0,1.21,0.2))

ax[0].text(-2.25,1.1, "Sample Rate = 2 MHz", fontsize = textSize)
ax[1].text(-2.25,1.15, "Sample Rate = 1 MHz", fontsize = textSize)


ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = True, labelbottom = False)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.tight_layout(h_pad = 0)
plt.savefig("../images/nyquist.png")
plt.savefig("../images/pdfs/nyquist.pdf")

for i in range(len(frequencies)):
    if powerSpectrum[i] > 0.9:
        print("2000 kHz:" + str(frequencies[i]))

for i in range(len(frequenciesTwo)):
    if powerSpectrumTwo[i] > 0.9:
        print("1000 kHz: " + str(frequenciesTwo[i]))

