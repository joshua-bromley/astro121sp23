import numpy as np
import ugradio as ug
import matplotlib.pyplot as plt
import interferometry as intf
from scipy import special as sp
from matplotlib import rcParams
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

def solarRadius(u, params):
    x = 2*np.pi*u*params[0]
    return np.abs(sp.j1(x)/x)*params[1]


filepath = "./lab3data/12hrSun_new/dat{0}.pkl"
data, times, frequencies, _ = intf.readData(filepath, 11862, 500, 800)

envelope, err = intf.rollingAverage(np.abs(np.transpose(data)[150]), 20)
times = times[0:-1]


#envelope,times = intf.getEnvelope(np.real(np.transpose(data)[150]), times, 15)
#envelope, _ = intf.rollingAverage(envelope, 2)
#times = times[0:-1]
#filteredEnvelope = intf.fourierFilter(envelope, 100,512)
#err = np.std(filteredEnvelope)*np.ones(len(envelope))


hourAngle = intf.uTimeToHrAngle(times)

baselineEW = 14.91973
wavelength = 3e8/frequencies[100]
_, dec = ug.coord.sunpos(ug.timing.julian_date(times[0]))
dec = np.deg2rad(dec)
u = (baselineEW/wavelength)*np.cos(hourAngle)*np.cos(dec)

envelope = envelope[-2000:]
u = u[-2000:]

minOneIdx = np.argmin(envelope)
minOne = envelope[minOneIdx]
minTwoIdx = np.argmin(envelope[-250:])+len(envelope)-250
minTwo = envelope[minTwoIdx]


for i in range(len(envelope)):
    envelope[i] = envelope[i] - (minOne + (i-minOneIdx)*(minOne - minTwo)/(minOneIdx-minTwoIdx))




rParams = np.linspace(1e-3, 1e-2, 100)
tParams = np.linspace(5,50,100)
params = []
for r in rParams:
    for t in tParams:
        params.append([r,t])

opt, chiSqArr = intf.bruteForceFit(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, params, grid = True)
print(opt)

fig, ax = plt.subplots(1,1, figsize = (6,6))
image = ax.imshow(chiSqArr, cmap = "terrain_r", aspect = "auto", extent = [tParams[0],tParams[-1],np.rad2deg(rParams[0]), np.rad2deg(rParams[-1])], vmax = 1000)
cbar = fig.colorbar(image)

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_ylabel("Solar Radius (degrees)", fontsize = axesLabelSize)
ax.set_xlabel("Power (Arbitrary)", fontsize = axesLabelSize)

cbar.set_label("Chi Squared", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./figures/pngs/fig7.png")
plt.savefig("./figures/pdfs/fig7.pdf")