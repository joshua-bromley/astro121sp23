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

filename ="data_noise_1blocks_16384samples_10MHzLPfilter_32e5HzRate.csv"


signalRate = 0.5e6 #Signal Rate in HZ
sampleRate = 3.2e6 #Sample rates in Hz

data = np.loadtxt("../lab1data/"+filename, delimiter = ",")
timeStep = 1/sampleRate
voltageSpectrum = np.fft.fft(data, n = 2*len(data)-1)
magSpectrum = np.abs(voltageSpectrum)
powerSpectrum = np.multiply(magSpectrum,magSpectrum)

fig, ax = plt.subplots(2,1, figsize = (6,8))
fig.subplots_adjust(hspace = 0, wspace = 0)

invPowerSpectrum = np.fft.ifft(powerSpectrum)
iftTimes = np.linspace(-len(data)*timeStep*1e3,len(data)*timeStep*1e3, 2*len(data))
npACF = np.correlate(data, data, mode = "full")
acTimes = np.linspace(-len(data)*timeStep*1e3,len(data)*timeStep*1e3, 2*len(data)-1)

ax[0].plot(acTimes,np.fft.fftshift(invPowerSpectrum), label = "IFT", ls = "", marker= ".", color = "#0d265c")
ax[0].plot(acTimes,npACF+100, label = "numpy", ls = "", marker = ".", color = "#ffa600")

ax[1].plot(acTimes[16384-100:16384+100],np.fft.fftshift(invPowerSpectrum)[16384-100:16384+100], label = "IFT", ls = "-", marker= ".", color = "#0d265c")
ax[1].plot(acTimes[16384-100:16384+100],npACF[16384-100:16384+100], label = "numpy", ls = "-", marker = ".", color = "#ffa600")


ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)



ax[0].set_ylabel("Correlation ($V^2$)", fontsize = axesLabelSize)
ax[0].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)
ax[1].set_ylabel("Correlation ($V^2$)", fontsize = axesLabelSize)
ax[1].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)

ax[0].set_xlim(-6,6)
ax[0].set_xticks(np.arange(-6,6.1,2))
ax[0].set_ylim(-200,1000)
ax[0].set_yticks(np.arange(-200,1001,200))

ax[1].set_xlim(-0.03,0.03)
ax[1].set_xticks(np.arange(-0.03,0.031,0.01))
ax[1].set_ylim(-50,50)
ax[1].set_yticks(np.arange(-40,41,20))


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
plt.tight_layout()
plt.savefig("../images/noiseAutoCorrelate.png")
plt.savefig("../images/pdfs/noiseAutoCorrelate.pdf")