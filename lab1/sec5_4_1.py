import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rcParams
import  ugradio as ug

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

filename ="data_500kHzFreq_3000kHzSamp2.gz"

data = np.loadtxt("./lab1data/"+filename)

sampleRate = 3e6
timeStep = 1/sampleRate



voltageSpectrum = np.fft.fft(data)
powerSpectrum = np.multiply(np.abs(voltageSpectrum), np.abs(voltageSpectrum))
frequencies = np.fft.fftfreq(len(powerSpectrum), timeStep)

leakedVoltageSpectrum = np.fft.fft(data, 100*len(data))
leakedPowerSpectrum = np.multiply(np.abs(leakedVoltageSpectrum), np.abs(leakedVoltageSpectrum))
leakedFrequencies = np.fft.fftfreq(len(leakedPowerSpectrum), timeStep)

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(np.fft.fftshift(leakedFrequencies)*1e-6,np.fft.fftshift(leakedPowerSpectrum)*1e-6)
ax[0].plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6, ls = ":")
ax[0].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[0].set_ylabel("Power (mV)", fontsize = axesLabelSize)

ax[0].set_yscale("log")

ax[1].plot(np.fft.fftshift(leakedFrequencies)*1e-6,np.fft.fftshift(leakedPowerSpectrum)*1e-6)
ax[1].plot(np.fft.fftshift(frequencies)*1e-6, np.fft.fftshift(powerSpectrum)*1e-6, ls = ":")
ax[1].set_xlabel("Frequency (MHz)", fontsize = axesLabelSize)
ax[1].set_ylabel("Power (mV)", fontsize = axesLabelSize)

ax[1].set_xlim(0.66,0.7)
ax[1].set_ylim(0,0.2)

ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.savefig("./images/spectralLeakagenp.jpg")
