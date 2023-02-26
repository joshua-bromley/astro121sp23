import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import rcParams
import ugradio
import functions

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



filenamesLow = ["./lab2data/cassie_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/cassie_1419_906MHzLO_signalRF_maxSamp2.gz"]
filenamesHigh = ["./lab2data/cassie_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/cassie_1420_906MHzLO_signalRF_maxSamp2.gz"]

powSpecLow = functions.fileToPowerSpec(filenamesLow)
powSpecHigh = functions.fileToPowerSpec(filenamesHigh)


for i in range(len(powSpecLow)-1):
    if powSpecLow[i] > powSpecLow[i+1]+1:
        powSpecLow[i] = powSpecLow[i+1]

for i in range(len(powSpecHigh)-1):
    if powSpecHigh[i] > powSpecHigh[i+1]+1:
        powSpecHigh[i] = powSpecHigh[i+1]

sampleRate = 3.2e6
timeStep = 1/sampleRate

powSpecLow = powSpecLow
powSpecHigh = powSpecHigh

avgPowSpec = np.mean((powSpecLow,powSpecHigh), axis = 0)

freqsLow = np.fft.fftfreq(len(powSpecLow), timeStep) + 1419.906e6
freqsHigh = np.fft.fftfreq(len(powSpecLow), timeStep) + 1420.906e6

nu = 1420.40575e6
ra = 6.45088448
dec = 62.72554931
jd =  2459998.633030077
v = ugradio.doppler.get_projected_velocity(ra, dec, jd).value/3e8

velocitiesLow = v-((freqsLow- nu)/nu)
velocitiesHigh = v-((freqsHigh -nu)/nu)

np.savetxt("./lab2data/LO1419.gz",[velocitiesLow, powSpecLow])
np.savetxt("./lab2data/LO1420.gz",[velocitiesHigh, powSpecHigh])

fig, ax = plt.subplots(2,1, figsize = (6,8))

ax[0].plot(velocitiesLow, powSpecLow)
ax[1].plot(velocitiesHigh, powSpecHigh)

plt.savefig("./images/HLineVelo.png")

'''
powSpecFlat = np.divide(powSpecLow,powSpecHigh)

fig, ax = plt.subplots(2,1, figsize = (6,8))
 
ax[0].plot(freqs, powSpecLow)
ax[1].plot(freqs, np.flip(powSpecHigh))

plt.savefig("./images/HlineAvgPowerSpectrum.png")

fig1, ax1 = plt.subplots(1,1, figsize = (6,4))

ax1.plot(freqs, powSpecFlat)

plt.savefig("./images/HLineFlatPowerSpectrum.png")

fig2, ax2 = plt.subplots(1,1, figsize = (6,4))
ax2.plot(velocities[50:600], powSpecLow[50:600])
plt.savefig("./images/HLineVelo.png")

clippedVelocities = velocities[200:450]
clippedPowSpec = avgPowSpec[200:450]

clippedPowSpecCal = np.flip(avgPowSpec[-450:-200])

np.savetxt("./lab2data/signal.gz", [clippedVelocities, clippedPowSpec, clippedPowSpecCal])
'''



