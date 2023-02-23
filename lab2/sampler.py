import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
#import ugradio
import emcee
import corner
import samplerFunctions

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

data = np.loadtxt("./lab2data/signal.gz")

velocities = data[0]
powSpec = data[1]
powSpecCal = data[2]
err = np.ones(len(powSpec))

pos = [4.5e9,-0.0004,43]*np.ones([16,3]) + [1.5e8,-0.0002,43]*((np.random.random([16,3])-0.5)/5)

nwalkers, ndim = pos.shape

sampler = emcee.EnsembleSampler(nwalkers, ndim, samplerFunctions.logProbability, args = (velocities, powSpecCal, err , samplerFunctions.polyModel))
sampler.run_mcmc(pos,5000, progress = True)

flatSamples = sampler.get_chain(discard = 100, thin = 15, flat = True)

polyParams = np.ones(3)
for i in range(ndim):
    polyParams[i] = np.percentile(flatSamples[:,i],50)

flatPowSpec = powSpec - samplerFunctions.polyModel(polyParams, velocities)

fig, ax = plt.subplots(2,1,figsize = (6,8))

ax[0].plot(velocities, powSpec)
ax[0].plot(velocities,samplerFunctions.polyModel(polyParams,velocities))

ax[1].plot(velocities, flatPowSpec)

plt.savefig("./images/polyfit.png")

print(polyParams)

pos = [-0.0001,0.00005,0.01875]*np.ones([16,3]) + [-0.0001,0.00005,0.01875]*((np.random.random([16,3])-0.5)/50)

nwalkers, ndim = pos.shape

sampler = emcee.EnsembleSampler(nwalkers, ndim, samplerFunctions.logProbability, args = (velocities, flatPowSpec, err , samplerFunctions.gaussModel))
sampler.run_mcmc(pos,5000, progress = True)
flatSamples = sampler.get_chain(discard = 100, thin = 5, flat = True)

gaussParams = np.ones(ndim)
for i in range(ndim):
    gaussParams[i] = np.percentile(flatSamples[:,i],50)

fig1, ax1 = plt.subplots(1,1,figsize = (6,4))
ax1.plot(velocities, flatPowSpec)
ax1.plot(velocities, samplerFunctions.gaussModel(gaussParams, velocities))
ax1.set_xlabel("Velocity (c)", fontsize = axesLabelSize)
ax1.set_ylabel("Relative Temperature (K)", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./images/gaussfit.png")

print(gaussParams)

fig3 = corner.corner(flatSamples, labels = ["$\mu$", "$\sigma$", "A"])

plt.savefig("./images/corner.png")




