import numpy as np 
import matplotlib.pyplot as plt
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

data = []
filenames = ["datasig1sam1.gz","datasig1sam15.gz","datasig1sam2.gz","datasig1sam25.gz","datasig1sam3.gz"]

signalRate = 1e6 #Signal Rate in HZ
sampleRates = [1e6, 1.5e6, 2e6, 2.5e6, 3e6] #Sample rates in Hz

for name in filenames:
    data.append(np.loadtxt("./lab1data/"+name))

for i in range(5):
    fig, ax = plt.subplots(2,1, figsize = (12,16))
    sampleRate = sampleRates[i]
    timeStep = 1/sampleRate
    times = np.arange(0,200*timeStep*1e-3,timeStep*1e-3)

    ax[0].plot(times, data[i][0:200], color = "black")

    powerSpectrum = np.fft.fft(data[i])
    powerSpectrum = np.abs(powerSpectrum)
    powerSpectrum = np.multiply(powerSpectrum,powerSpectrum)

    frequencies = np.fft.fftfreq(len(powerSpectrum), timeStep)

    ax[1].plot(np.fft.fftshift(frequencies), np.fft.fftshift(powerSpectrum), color = "black")

    
    ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

    ax[0].set_xlabel("Time (ms)", fontsize = axesLabelSize)
    ax[0].set_ylabel("Voltage", fontsize = axesLabelSize)

    ax[1].set_xlabel("Frequency", fontsize = axesLabelSize)
    ax[1].set_ylabel("Power", fontsize = axesLabelSize)

    plt.tight_layout()
    plt.savefig("./images/plot"+str(i)+".jpg")
    plt.savefig("./images/pdfs/plot"+str(i)+".pdf")





