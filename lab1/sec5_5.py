import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

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

filename = "doubleSin_samp3MHz_ob1500kHz_ob2501kHz.gz"

data = np.loadtxt("./lab1data/"+filename)

sampleRate = 3e6
timeStep = 1/sampleRate

voltageSpectrum = np.abs(np.fft.fft(data, len(data)*1000))
powerSpectrum = np.multiply(voltageSpectrum,voltageSpectrum)
frequencies = np.fft.fftfreq(len(powerSpectrum), timeStep)

fig,ax = plt.subplots(1,1, figsize = (6,4))

ax.plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6)

ax.set_xlabel("Frequency (mHz)")
ax.set_ylabel("Power ($mV^2$)")

ax.set_xlim(0.6,0.8)

plt.savefig("./images/frequencyResolution.jpg")
