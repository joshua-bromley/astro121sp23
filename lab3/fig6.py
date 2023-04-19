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
err = intf.fourierFilter(envelope, 150,300)


#envelope,times = intf.getEnvelope(np.real(np.transpose(data)[150]), times, 15)
#envelope, _ = intf.rollingAverage(envelope, 2)
#times = times[0:-1]
#filteredEnvelope = intf.fourierFilter(envelope, 100,512)
#err = np.std(filteredEnvelope)*np.ones(len(envelope))


hourAngle = intf.uTimeToHrAngle(times)

baselineEW = 15.23
wavelength = 3e8/frequencies[150]
_, dec = ug.coord.sunpos(ug.timing.julian_date(times[0]))
dec = np.deg2rad(dec)
u = (baselineEW/wavelength)*np.cos(hourAngle)*np.cos(dec)

envelope = envelope[-2000:]
u = u[-2000:]

print(ug.timing.local_time(times[0]),ug.timing.local_time(times[-1]))
print(np.mean(np.diff(times)))
print(frequencies[0],frequencies[150],frequencies[-1])
print(len(u[1300:-1]))

minOneIdx = np.argmin(envelope)
minOne = envelope[minOneIdx]
minTwoIdx = np.argmin(envelope[-250:])+len(envelope)-250
minTwo = envelope[minTwoIdx]


for i in range(len(envelope)):
    envelope[i] = envelope[i] - (minOne + (i-minOneIdx)*(minOne - minTwo)/(minOneIdx-minTwoIdx))




rParams = np.linspace(1e-3, 1e-2, 50)
tParams = np.linspace(5,50,50)
params = []
for r in rParams:
    for t in tParams:
        params.append([r,t])

optR, optT = intf.bruteForceFit(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, params, grid = False)

#err = np.ones(len(u))*np.std(envelope[1300:-1] - solarRadius(u[1300:-1],(optR, optT)))

results = intf.mcmcFit(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, (optR, optT), 8)
mcmcR = results[0]
mcmcT = results[1]

print(optR, optT)
print(np.rad2deg(mcmcR[0]), np.rad2deg(mcmcR[1]))
print(mcmcT[0], mcmcT[1])
print(results[2],results[2]/len(u[1300:-1]-2))
print(results[3])

print(intf.chiSq(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, (mcmcR[0],mcmcT[0])))




fig, ax = plt.subplots(1,1, figsize = (6,4))
ax.plot(u,envelope, marker = ".", color = colors.berkeley_blue, alpha = 0.5)
ax.plot(u, solarRadius(u, [mcmcR[0],mcmcT[0]]), color = colors.california_gold, ls = "-")

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)
ax.set_xlabel("$u$ (Dimensionless)", fontsize = axesLabelSize)


plt.tight_layout()
plt.savefig("./figures/pngs/fig6.png")
plt.savefig("./figures/pdfs/fig6.pdf")