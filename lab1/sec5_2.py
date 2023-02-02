import numpy as np 
import matplotlib.pyplot as plt
from matplotlib import rcParams

##Adjust plotting defaults
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

data = []
filenames = ["data_500kHzFreq_1000kHzSamp.txt","data_500kHzFreq_1500kHzSamp.txt","data_500kHzFreq_2000kHzSamp.txt","data_500kHzFreq_2500kHzSamp.txt","data_500kHzFreq_3000kHzSamp.txt"]

signalRate = 1e6 #Signal Rate in HZ
sampleRates = [1e6, 1.5e6, 2e6, 2.5e6, 3e6] #Sample rates in Hz

for name in filenames:
    data.append(np.loadtxt("./lab1data/"+name))

for i in range(5):
    fig, ax = plt.subplots(2,1, figsize = (6,8))
    sampleRate = sampleRates[i]
    timeStep = 1/sampleRate
    times = np.arange(0,200*timeStep*1e3,timeStep*1e3)

    ax[0].plot(times, data[i][0:200], color = "black")

    powerSpectrum = np.fft.fft(data[i])
    powerSpectrum = np.abs(powerSpectrum)
    powerSpectrum = np.multiply(powerSpectrum,powerSpectrum)

    frequencies = np.fft.fftfreq(len(powerSpectrum), timeStep)

    ax[1].plot(np.fft.fftshift(frequencies)*1e-3, np.fft.fftshift(powerSpectrum), color = "black")

    
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

    ax[1].set_xlabel("Frequency (kHz)", fontsize = axesLabelSize)
    ax[1].set_ylabel("Power", fontsize = axesLabelSize)

    plt.tight_layout()
    plt.savefig("./images/plot"+str(i)+".jpg")
    plt.savefig("./images/pdfs/plot"+str(i)+".pdf")





