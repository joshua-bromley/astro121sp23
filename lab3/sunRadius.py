import numpy as np
import ugradio as ug
import matplotlib.pyplot as plt
import interferometry as intf
from scipy import special as sp

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




rParams = np.linspace(1e-3, 1e-2, 50)
tParams = np.linspace(5,50,50)
params = []
for r in rParams:
    for t in tParams:
        params.append([r,t])

optR, optT = intf.bruteForceFit(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, params)

mcmcR, mcmcT = intf.mcmcFit(u[1300:-1], envelope[1300:-1], err[1300:-1], solarRadius, (optR, optT), 16)

print(np.rad2deg(mcmcR[0]), np.rad2deg(mcmcR[1]))
print(mcmcT[0], mcmcT[1])




fig, ax = plt.subplots(1,1)
ax.plot(u,envelope, marker = ".")
ax.plot(u, solarRadius(u, [mcmcR[0],mcmcT[0]]))
fig.savefig("./images/bessel.png")