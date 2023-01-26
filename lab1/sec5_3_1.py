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

filename ="data_500kHzFreq_3000kHzSamp2.gz"

signalRate = 0.5e6 #Signal Rate in HZ
sampleRate = 3e6 #Sample rates in Hz

data = np.loadtxt("./lab1data/"+filename)*0.1
timeStep = 1/sampleRate
voltageSpectrum = np.fft.fft(data)
magSpectrum = np.abs(voltageSpectrum)
powerSpectrum = np.multiply(magSpectrum,magSpectrum)

fig, ax = plt.subplots(2,2, figsize = (24,16))
fig.subplots_adjust(hspace = 0, wspace = 0)

invPowerSpectrum = np.fft.ifft(powerSpectrum)
iftTimes = np.linspace(-2048*timeStep*1e3,2048*timeStep*1e3, 2048)
npACF = np.correlate(data, data, mode = "full")
acTimes = np.linspace(-2047*timeStep*1e3,2047*timeStep*1e3, 4095)

ax[0][0].plot(iftTimes,np.fft.fftshift(invPowerSpectrum), label = "IFT", ls = "", marker= ".")
ax[0][1].plot(iftTimes[1024-25:1025+25],np.fft.fftshift(invPowerSpectrum)[1024-25:1024+26], label = "IFT", ls = "-", marker = "o")
ax[1][0].plot(acTimes,npACF, label = "numpy", ls = "", marker = ".", color = "tab:green")
ax[1][1].plot(acTimes[2048-50:2048+50],npACF[2048-50:2048+50], label = "numpy", ls = "-", marker = "o", color = "tab:green")

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


plt.savefig("./images/autoCorrelate2"+".jpg")
plt.savefig("./images/pdfs/autoCorrelate2"+".pdf")

