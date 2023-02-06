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

filename = "../lab1data/data_500kHzFreq_3000kHzSamp.txt"

data = np.loadtxt(filename)
sampleRate = 3e6
timeStep = 1/sampleRate

voltageSpectrum = np.abs(np.fft.fft(data))
powerSpectrum = np.multiply(voltageSpectrum, voltageSpectrum)
frequencies = np.fft.fftfreq(len(data), timeStep)

voltageSpectrum10 = np.abs(np.fft.fft(data, 2*len(data)))
powerSpectrum10 = np.multiply(voltageSpectrum10, voltageSpectrum10)
frequencies10 = np.fft.fftfreq(len(data)*2, timeStep)

voltageSpectrum100 = np.abs(np.fft.fft(data, 10*len(data)))
powerSpectrum100 = np.multiply(voltageSpectrum100, voltageSpectrum100)
frequencies100 = np.fft.fftfreq(len(data)*10, timeStep)

fig, ax = plt.subplots(1,1, figsize = (6,4))

ax.plot(frequencies[0:1000]*1e-6,powerSpectrum[0:1000]*1e-6, color = "#0d265c", ls = ":", lw = 2, label = "2048 Bins")
ax.plot(frequencies10[0:2000]*1e-6, powerSpectrum10[0:2000]*1e-6, color = "#c4346b", ls = "--", lw = 2, label = "4096 Bins")
ax.plot(frequencies100[0:10000]*1e-6, powerSpectrum100[0:10000]*1e-6, color = "#ffa600", ls = "-", lw = 2, label = "20480 Bins")

ax.set_xlabel("Frequency (Mhz)", fontsize = axesLabelSize)
ax.set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)

ax.set_xlim(0.58,0.62)
ax.set_ylim(-0.01,0.1)

ax.legend(frameon = False, fontsize = textSize)

plt.tight_layout()
plt.savefig("../images/spectralLeakageFinal.png")
plt.savefig("../images/pdfs/spectralLeakageFinal.pdf")