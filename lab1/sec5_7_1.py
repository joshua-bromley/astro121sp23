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

data = np.loadtxt("./lab1data/data_noise_200blocks_2048samples_10MHzLPfilter_32e5HzRate.csv", delimiter = ",")
sampleRate = 3e6
timeStep = 1/sampleRate

oneBlock = data[34]
twoBlocks = 0.5*(data[1]+data[2])
fourBlocks = 0.25*(np.sum(data[3:7], axis = 0))
eightBlocks = 0.125*(np.sum(data[8:16], axis = 0))
sixteenBlocks = 0.0625*(np.sum(data[17:33], axis = 0))
allBlocks = (1/200)*(np.sum(data, axis = 0))

oneVoltageSpectrum = np.abs(np.fft.fft(oneBlock))
onePowerSpectrum = np.multiply(oneVoltageSpectrum, oneVoltageSpectrum)
twoVoltageSpectrum = np.abs(np.fft.fft(twoBlocks))
twoPowerSpectrum = np.multiply(twoVoltageSpectrum, twoVoltageSpectrum)
fourVoltageSpectrum = np.abs(np.fft.fft(fourBlocks))
fourPowerSpectrum = np.multiply(fourVoltageSpectrum, fourVoltageSpectrum)
eightVoltageSpectrum = np.abs(np.fft.fft(eightBlocks))
eightPowerSpectrum = np.multiply(eightVoltageSpectrum, eightVoltageSpectrum)
sixteenVoltageSpectrum = np.abs(np.fft.fft(sixteenBlocks))
sixteenPowerSpectrum = np.multiply(sixteenVoltageSpectrum, sixteenVoltageSpectrum)
totalVoltageSpectrum = np.abs(np.fft.fft(allBlocks))
totalPowerSpectrum = np.multiply(totalVoltageSpectrum,totalVoltageSpectrum)

frequencies = np.fft.fftfreq(len(oneBlock), timeStep)

fig,ax = plt.subplots(3,2, figsize = (12,12))

ax[0][0].plot(np.fft.fftshift(frequencies),np.fft.fftshift(onePowerSpectrum), color = "#0d265c")
ax[0][1].plot(np.fft.fftshift(frequencies),np.fft.fftshift(twoPowerSpectrum), color = "#0d265c")
ax[1][0].plot(np.fft.fftshift(frequencies),np.fft.fftshift(fourPowerSpectrum), color = "#0d265c")
ax[1][1].plot(np.fft.fftshift(frequencies),np.fft.fftshift(eightPowerSpectrum), color = "#0d265c")
ax[2][0].plot(np.fft.fftshift(frequencies),np.fft.fftshift(sixteenPowerSpectrum), color = "#0d265c")
ax[2][1].plot(np.fft.fftshift(frequencies),np.fft.fftshift(totalPowerSpectrum), color = "#0d265c")

for axes in ax:
    for axis in axes:
        axis.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
        axis.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
        axis.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
        axis.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.tight_layout()
plt.savefig("./images/noisePowerSpectrum")



