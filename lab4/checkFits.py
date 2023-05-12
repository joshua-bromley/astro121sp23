import maps
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rcParams
from scipy import optimize as opt
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

npz = np.load("./lab4data/deconvolvedSpectra.npz", allow_pickle=True)

pol0 = npz["pol0"]
pol1 = npz["pol1"]
metadata = npz["metadata"]
v = npz["v"]

npz1 = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)


temperature = npz1["temp"]
speeds = npz1["speed"]
sigma = npz1["sigma"]


i = 199
print(len(pol0))

data = []
if np.mean(pol0[i]) > 0 and np.mean(pol1[i]) > 0:
    data = (pol0[i]+pol1[i])/2
elif np.mean(pol0[i]) <= 0:
    data = pol1[i]
elif np.mean(pol1[i]) <= 0:
    data = pol0[i]
else:
    data = np.zeros_like(pol0[i])
    print("Data bad")


fig, ax = plt.subplots(3,1, figsize = (6,12))

ax[2].plot(v[i]*1e-3,data, color = colors.berkeley_blue)

if len(temperature[i]) == 2:
    ax[2].plot(v[i]*1e-3,maps.doubleGaussian(v[i],temperature[i][0],speeds[i][0],sigma[i][0],temperature[i][1],speeds[i][1],sigma[i][1]), color = colors.california_gold, alpha = 0.8)
else:
    if temperature[i][0] != None:
        ax[2].plot(v[i]*1e-3,maps.gaussian(v[i],temperature[i][0],speeds[i][0],sigma[i][0]), color = colors.california_gold, alpha = 0.8)

ax[2].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[2].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[2].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[2].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax[2].set_xlabel("Velocity km/s", fontsize = axesLabelSize)
ax[2].set_ylabel("Temperature (K)", fontsize = axesLabelSize)

i = 538
data = []
if np.mean(pol0[i]) > 0 and np.mean(pol1[i]) > 0:
    data = (pol0[i]+pol1[i])/2
elif np.mean(pol0[i]) <= 0:
    data = pol1[i]
elif np.mean(pol1[i]) <= 0:
    data = pol0[i]
else:
    data = np.zeros_like(pol0[i])
    print("Data bad")

prominence = maps.getProminence(data)
indecies = np.argsort(prominence)
if np.abs(v[i][indecies[-1]] - v[i][indecies[-2]]) > 10000:
    p0 = [np.abs(data[indecies[-1]]),v[i][indecies[-1]],10000,np.abs(data[indecies[-2]]),v[i][indecies[-2]],10000]
else:
    p0 = [data[indecies[-1]]/2,v[i][indecies[-1]],10000,data[indecies[-2]]/2,v[i][indecies[-2]],10000]
params, cov = opt.curve_fit(maps.doubleGaussian, v[i], data, p0 = p0, bounds = [[0,-np.inf,0,0,-np.inf,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
ax[1].plot(v[i]*1e-3,data, color = colors.berkeley_blue)
ax[1].plot(v[i]*1e-3, maps.doubleGaussian(v[i],*params), color = colors.california_gold, alpha = 0.8)

ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[1].set_xlabel("Velocity km/s", fontsize = axesLabelSize)
ax[1].set_ylabel("Temperature (K)", fontsize = axesLabelSize)

i = 300
print(temperature[i][0])
data = []
if np.mean(pol0[i]) > 0 and np.mean(pol1[i]) > 0:
    data = (pol0[i]+pol1[i])/2
elif np.mean(pol0[i]) <= 0:
    data = pol1[i]
elif np.mean(pol1[i]) <= 0:
    data = pol0[i]
else:
    data = np.zeros_like(pol0[i])
    print("Data bad")

prominence = maps.getProminence(data)
indecies = np.argsort(prominence)
if np.abs(v[i][indecies[-1]] - v[i][indecies[-2]]) > 10000:
    p0 = [np.abs(data[indecies[-1]]),v[i][indecies[-1]],10000,np.abs(data[indecies[-2]]),v[i][indecies[-2]],10000]
else:
    p0 = [data[indecies[-1]]/2,v[i][indecies[-1]],10000,data[indecies[-2]]/2,v[i][indecies[-2]],10000]
params, cov = opt.curve_fit(maps.doubleGaussian, v[i], data, p0 = p0, bounds = [[0,-np.inf,0,0,-np.inf,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
ax[0].plot(v[i]*1e-3,data, color = colors.berkeley_blue)
ax[0].plot(v[i]*1e-3, maps.doubleGaussian(v[i],*params), color = colors.california_gold, alpha = 0.8)

ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax[0].set_xlabel("Velocity km/s", fontsize = axesLabelSize)
ax[0].set_ylabel("Temperature (K)", fontsize = axesLabelSize)



plt.tight_layout()


fig.savefig("./images/fitCheck.png")
fig.savefig("./figures/fitting.pdf")