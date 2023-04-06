import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import ugradio as ug
import pickle
import interferometry as intf
import colors

def localFringeFrequency(x, params):
    return params[0]*np.cos(x) - params[1]*np.sin(x)

filepath = "./lab3data/12hrSun_new/dat{0}.pkl"
data, times, frequencies, _ = intf.readData(filepath, 11862, 500, 800)


fringeFrequencies, hourAngle, err = intf.getFringeFrequencies(np.transpose(data)[0], times, 40)
fringeFreqs = [fringeFrequencies]

for i in range(1,300):
    fringeFrequencies, _ , _ = intf.getFringeFrequencies(np.transpose(data)[i], times, 40)
    fringeFreqs.append(fringeFrequencies)

wavelengths  = 3e8/frequencies

fringeSpeed = []
for i in range(len(fringeFreqs)):
    fringeSpeed.append(np.multiply(fringeFreqs[i],wavelengths[i]))
print(wavelengths[0])


avgFringeSpeed = np.mean(fringeSpeed, axis = 0)
err = np.std(fringeSpeed, axis = 0)
#err = err/np.sqrt(300)


aParams = np.linspace(0.0006,0.0012,500)
bParams = np.linspace(0.00001,0.0006,500)
params = []

for a in aParams:
    for b in bParams:
        params.append((a,b))

optA, optB = intf.bruteForceFit(hourAngle, avgFringeSpeed, err, localFringeFrequency, params)

earthRotRate = 2*np.pi/(86164.0905)
_, dec = ug.coord.sunpos(ug.timing.julian_date(times[0]))
dec = np.deg2rad(dec)



mcmcA, mcmcB = intf.mcmcFit(hourAngle, avgFringeSpeed, err, localFringeFrequency, [optA,optB], 32)

baselineEW = (mcmcA[0])/(np.cos(dec)*earthRotRate)
baselineNS = (mcmcB[0])/(np.cos(dec)*np.sin(np.deg2rad(ug.nch.lat))*earthRotRate)
ewErr = (mcmcA[1])/(np.cos(dec)*earthRotRate)
nsErr = (mcmcB[1])/(np.cos(dec)*np.sin(np.deg2rad(ug.nch.lat))*earthRotRate)
print(baselineEW, ewErr)
print(baselineNS, nsErr)

fig, ax = plt.subplots(1,1)
ax.errorbar(hourAngle, avgFringeSpeed, yerr = err, marker = ".", ls = "", color = colors.berkeley_blue)
#for i in range(300):
#    ax.plot(hourAngle, fringeSpeed[i], ls = "", marker = ".")
ax.plot(hourAngle, localFringeFrequency(hourAngle, [mcmcA[0], mcmcB[0]]), color = colors.california_gold)
plt.savefig("./images/fringeFrequencies.png")
