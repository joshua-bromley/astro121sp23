import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from ugradio import dft
import scipy

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



filename = "../lab1data/data_noise_200blocks_2048samples_10MHzLPfilter_32e5HzRate.csv"

data = np.loadtxt(filename, delimiter = ",")
sampleRate = 3.2e6
timeStep = 1/sampleRate

times = np.arange(0,(len(data[1])+1)*timeStep,timeStep)

oneBlock = data[34]
eightBlocks = 0.125*(np.sum(data[8:16], axis = 0))
allBlocks = (1/200)*(np.sum(data, axis = 0))

oneVoltageSpectrum = np.abs(np.fft.fft(oneBlock))
onePowerSpectrum = np.multiply(oneVoltageSpectrum, oneVoltageSpectrum)
eightVoltageSpectrum = np.abs(np.fft.fft(eightBlocks))
eightPowerSpectrum = np.multiply(eightVoltageSpectrum, eightVoltageSpectrum)
totalVoltageSpectrum = np.abs(np.fft.fft(allBlocks))
totalPowerSpectrum = np.multiply(totalVoltageSpectrum,totalVoltageSpectrum)

frequencies = np.fft.fftfreq(len(oneBlock), timeStep)

fig,ax = plt.subplots(3,1, figsize = (6,12))

histogramOne = ax[0].hist(oneBlock, bins = 40, range = (-0.3,0.3), density = True, color = "#0d265c", zorder = 1)
histogramEight = ax[0].hist(eightBlocks, bins = 40, range = (-0.3,0.3), density = True,color = "#c4346b", alpha = 0.8, zorder = 2)
histogramAll = ax[0].hist(allBlocks, bins = 40, range = (-0.3,0.3), density = True,color = "#ffa600", alpha = 0.7, zorder = 3)

binCenters = np.zeros(len(histogramOne[0]))
for i in range(len(histogramOne[1])-1):
    binCenters[i] = (0.5*histogramOne[1][i] + histogramOne[1][i+1])

paramsOne = scipy.optimize.curve_fit(scipy.stats.norm.pdf, binCenters,histogramOne[0], [np.mean(oneBlock), np.std(oneBlock)])
paramsEight = scipy.optimize.curve_fit(scipy.stats.norm.pdf, binCenters,histogramEight[0], [np.mean(oneBlock), np.std(oneBlock)])
paramsAll = scipy.optimize.curve_fit(scipy.stats.norm.pdf, binCenters,histogramAll[0], [np.mean(oneBlock), np.std(oneBlock)])

x = np.linspace(-0.3,0.3,200)


ax[0].plot(x,scipy.stats.norm.pdf(x,paramsOne[0][0],paramsOne[0][1]), color = "#0d265c", zorder = 1)
ax[0].plot(x,scipy.stats.norm.pdf(x,paramsEight[0][0],paramsEight[0][1]), color = "#c4346b", zorder = 2)
ax[0].plot(x,scipy.stats.norm.pdf(x,paramsAll[0][0],paramsAll[0][1]), color = "#ffa600", zorder = 3)


ax[1].plot(times[100:315]*1e6,oneBlock[100:315], color = "#0d265c", marker = ".")
ax[1].plot(times[100:315]*1e6,eightBlocks[100:315],color = "#c4346b", marker = ".")
ax[1].plot(times[100:315]*1e6, allBlocks[100:315], color = "#ffa600", marker = ".")

shiftedFreqs = np.fft.fftshift(frequencies)*1e-6

ax[2].plot(shiftedFreqs, np.fft.fftshift(onePowerSpectrum), color = "#0d265c", label = "1 Blocks")
ax[2].plot(shiftedFreqs, np.fft.fftshift(eightPowerSpectrum),color = "#c4346b", alpha = 0.8, label = "8 Blocks")
ax[2].plot(shiftedFreqs, np.fft.fftshift(totalPowerSpectrum),color = "#ffa600", alpha = 0.7, label = "200 Blocks")

ax[0].set_xlabel("Voltage (Arbitrary)", fontsize = axesLabelSize)
ax[0].set_ylabel("Magnitude", fontsize = axesLabelSize)

ax[1].set_xlabel("Time (ms)", fontsize = axesLabelSize)
ax[1].set_ylabel("Voltage (Arbitrary)", fontsize = axesLabelSize)

ax[2].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[2].set_ylabel("Power (Aribtrary)", fontsize = axesLabelSize)

ax[2].legend(frameon = False, fontsize = textSize)

ax[0].set_xlim(-0.3,0.3)
ax[0].set_xticks(np.arange(-0.3,0.31,0.1))
ax[0].set_ylim(0,40)
ax[0].set_yticks(np.arange(0,41,10))

ax[1].set_xlim(30,100)
ax[1].set_xticks(np.arange(30,101,10))
ax[1].set_ylim(-0.4,0.4)
ax[1].set_yticks(np.arange(-0.4,0.41,0.2))

ax[2].set_xlim(-1.6,1.6)
ax[2].set_xticks(np.arange(-1.6,1.61,0.4))
ax[2].set_ylim(-20,620)
ax[2].set_yticks(np.arange(0,601,100))


for axis in ax:
    axis.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.tight_layout()
plt.savefig("../images/noisePlot.png")
plt.savefig("../images/pdfs/noisePlot.pdf")

print(paramsOne[0], np.sqrt(np.diag(paramsOne[1])))
print(paramsEight[0], np.sqrt(np.diag(paramsEight[1])))
print(paramsAll[0], np.sqrt(np.diag(paramsAll[1])))

