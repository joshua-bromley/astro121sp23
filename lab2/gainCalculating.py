import numpy as np 
import matplotlib.pyplot as plt
import ugradio
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

filenameCal = "./lab2data/hornHuman_1419MHzLO_signalRF_maxSamp"
filenameOn = "./lab2data/hornCold_1419MHzLO_signalRF_maxSamp"
filenameOff = "./lab2data/hornTest_1409MHzLO_1410MHzRF_maxSamp"

dataOn = np.loadtxt(filenameOn, dtype = complex)
dataOff = np.loadtxt(filenameOff, dtype = complex)
dataCal = np.loadtxt(filenameCal, dtype = complex)
sampleRate = 3.2e6
timeStep = 1/sampleRate

voltSpecOn = np.abs(np.fft.fft(dataOn))
powSpecOn = np.multiply(voltSpecOn,voltSpecOn)
avgPowSpecOn = np.mean(powSpecOn, axis = 0)

voltSpecOff = np.abs(np.fft.fft(dataOff))
powSpecOff = np.multiply(voltSpecOff, voltSpecOff)
avgPowSpecOff = np.mean(powSpecOff, axis = 0)

voltSpecCal = np.abs(np.fft.fft(dataCal))
powSpecCal = np.multiply(voltSpecCal, voltSpecCal)
avgPowSpecCal = np.mean(powSpecCal, axis = 0)

deltaT = 10

gain = deltaT*np.divide(avgPowSpecOn,(avgPowSpecCal-avgPowSpecOn))

normPowerSpec = np.divide(avgPowSpecOn,avgPowSpecOff)

gainPowerSpec = np.multiply(gain, normPowerSpec)

print(np.mean(gain))


freqs = np.fft.fftfreq(len(avgPowSpecOn), timeStep)
velocities = -(freqs)/1420e6

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(freqs*1e-6, gainPowerSpec)
ax[1].plot(velocities*1e2, gainPowerSpec)

ax[0].set_xlabel("Frequency MHz", fontsize = axesLabelSize)
ax[1].set_xlabel("Target Velocity (percent of c)", fontsize = axesLabelSize)



plt.savefig("./images/avgPowerSpectrum.png")
