import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import ugradio as ug
import pickle
import interferometry as intf
import colors

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


avgFringeSpeed = np.mean(fringeSpeed, axis = 0)
for i in range(len(fringeSpeed)):
    for j in range(len(fringeSpeed[i])):
        if fringeSpeed[i][j] < avgFringeSpeed[j]/2:
            fringeSpeed[i][j] = avgFringeSpeed[j]

avgFringeSpeed = np.mean(fringeSpeed, axis = 0)
#err = np.std(fringeSpeed, axis = 0)
#err = err/np.sqrt(300)
err = err*np.mean(wavelengths)

aParams = np.linspace(0.0008,0.0013,500)
bParams = np.linspace(0.00001,0.0003,500)

params = []

for a in aParams:
    for b in bParams:
        params.append((a,b))

opt, chiSqArr = intf.bruteForceFit(hourAngle, avgFringeSpeed, err, localFringeFrequency, params, grid = True)
print(err[0])


earthRotRate = 2*np.pi/(86164.0905)
_, dec = ug.coord.sunpos(ug.timing.julian_date(times[0]))
dec = np.deg2rad(dec)

minEW = (0.0008)/(np.cos(dec)*earthRotRate)
maxEW = (0.0013)/(np.cos(dec)*earthRotRate)
minNS =(0.00001)/(np.cos(dec)*np.sin(np.deg2rad(ug.nch.lat))*earthRotRate)
maxNS = (0.0003)/(np.cos(dec)*np.sin(np.deg2rad(ug.nch.lat))*earthRotRate)

optEW = (opt[0])/(np.cos(dec)*earthRotRate)
optNS = (opt[1])/(np.cos(dec)*np.sin(np.deg2rad(ug.nch.lat))*earthRotRate)

fig, ax = plt.subplots(1,1, figsize = (6,6))
image = ax.imshow(chiSqArr, cmap = "terrain_r", aspect = "auto", extent = [minNS, maxNS, maxEW, minEW])
cbar = fig.colorbar(image)
print(opt[0],opt[1])
print(optEW, optNS)

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_ylabel("Baseline East-West (m)", fontsize = axesLabelSize)
ax.set_xlabel("Baseline North-South (m)", fontsize = axesLabelSize)

cbar.set_label("Chi Squared", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./figures/pngs/fig3.png")
plt.savefig("./figures/pdfs/fig3.pdf")