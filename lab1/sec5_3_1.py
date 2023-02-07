import numpy as np 
import matplotlib.pyplot as plt
import scipy
from matplotlib import rcParams

##Adjust plotting defaults
rcParams["axes.linewidth"] = 3.5

rcParams["ytick.right"] = True
rcParams["ytick.direction"] = "in"
rcParams["ytick.minor.visible"] = True
rcParams["ytick.major.left"] = True
rcParams["ytick.major.right"] = True
rcParams["ytick.minor.left"] = True
rcParams["ytick.minor.right"] = True
rcParams["ytick.major.size"] = 16
rcParams["ytick.minor.size"] = 8



rcParams["xtick.top"] = True
rcParams["xtick.direction"] = "in"
rcParams["xtick.minor.visible"] = True
rcParams["xtick.major.top"] = True
rcParams["xtick.major.bottom"] = True
rcParams["xtick.minor.top"] = True
rcParams["xtick.minor.bottom"] = True
rcParams["xtick.major.size"] = 16
rcParams["xtick.minor.size"] = 8 

axesLabelSize = 34
tickLabelSize = 26
textSize = 26

filename ="data_noise_1blocks_16384samples_10MHzLPfilter_32e5HzRate.csv"


signalRate = 0.5e6 #Signal Rate in HZ
sampleRate = 3.2e6 #Sample rates in Hz

data = np.loadtxt("./lab1data/"+filename, delimiter = ",")
timeStep = 1/sampleRate
voltageSpectrum = np.fft.fft(data, n = 2*len(data)-1)
magSpectrum = np.abs(voltageSpectrum)
powerSpectrum = np.multiply(magSpectrum,magSpectrum)

fig, ax = plt.subplots(2,2, figsize = (24,16))
fig.subplots_adjust(hspace = 0, wspace = 0)

invPowerSpectrum = np.fft.ifft(powerSpectrum)
iftTimes = np.linspace(-len(data)*timeStep*1e3,len(data)*timeStep*1e3, 2*len(data))
npACF = np.correlate(data, data, mode = "full")
acTimes = np.linspace(-len(data)*timeStep*1e3,len(data)*timeStep*1e3, 2*len(data)-1)

ax[0][0].plot(acTimes,np.fft.fftshift(invPowerSpectrum), label = "IFT", ls = "", marker= ".")
ax[0][1].plot(acTimes, np.fft.fftshift(invPowerSpectrum)-npACF, ls = "", marker = ".")
#ax[0][1].plot(iftTimes[8192-200:8192+200],np.fft.fftshift(invPowerSpectrum)[8192-200:8192+200], label = "IFT", ls = "-", marker = "o")
ax[1][0].plot(acTimes,npACF, label = "numpy", ls = "", marker = ".", color = "tab:green")
#ax[1][1].plot(acTimes[16384-400:16384+400],npACF[16384-400:16384+400], label = "numpy", ls = "-", marker = "o", color = "tab:green")

ax[0][0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = True, labelbottom = False)
ax[0][0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0][0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labelleft = True, labelright = False)
ax[0][0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0][1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = True, labelbottom = False)
ax[0][1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0][1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labelleft = False, labelright = True)
ax[0][1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1][0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = False, labelbottom = True)
ax[1][0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1][0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labelleft = True, labelright = False)
ax[1][0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1][1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = False, labelbottom = True)
ax[1][1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1][1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labelleft = False, labelright = True)
ax[1][1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)


ax[0][0].set_ylabel("Correlation ($V^2$)", fontsize = axesLabelSize)
ax[1][0].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)
ax[1][0].set_ylabel("Correlation ($V^2$)", fontsize = axesLabelSize)
ax[1][1].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)

'''
for axes in ax:
    for axis in axes:
        axis.set_ylim(-15,15)
        axis.set_yticks([-10,-5,0,5,10])

ax[0][0].set_xlim(-0.8,0.8)
ax[0][0].set_xticks([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])
ax[1][0].set_xlim(-0.8,0.8)
ax[1][0].set_xticks([-0.6,-0.4,-0.2,0,0.2,0.4,0.6])

ax[0][1].set_xlim(-0.02,0.02)
ax[0][1].set_xticks([-0.015,-0.005,0.005,0.015])
ax[1][1].set_xlim(-0.02,0.02)
ax[1][1].set_xticks([-0.015,-0.005,0.005,0.015])

ax[0][0].text(-0.7,10, "IFT", fontsize = textSize)
ax[1][0].text(-0.7,10, "np.correlate", fontsize = textSize)
'''

plt.savefig("./images/noiseAutoCorrelate.png")
plt.savefig("../images/pdfs/noiseAutoCorrelate.pdf")
