import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import emcee
import corner
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

filename = "./lab2data/flattenedSignal.gz"

data = np.loadtxt(filename)
velocities = data[0]
signal = data[1]
err = np.ones(len(signal))*2.5563

initialGuess = [-0.00003,0.000035, 50, -0.00019, 0.00005, 50]

pos = initialGuess*np.ones([16,6]) + initialGuess*((np.random.random([16,6])-0.5)/50)

nwalkers, ndim = pos.shape


sampler = emcee.EnsembleSampler(nwalkers, ndim, functions.logProbability, args = (velocities, signal, err, functions.doubleGaussModel))
sampler.run_mcmc(pos,10000, progress = True)
flatSamples = sampler.get_chain(discard = 500, thin = 5, flat = True)
logProb = sampler.get_log_prob()
redChiSq = np.mean(-logProb[-1]/(439))

gaussParams = np.ones(ndim)
for i in range(ndim):
    gaussParams[i] = np.percentile(flatSamples[:,i],50)

residuals = signal - functions.doubleGaussModel(gaussParams, velocities)
stdDev = np.std(residuals)
print(stdDev)

for i in range(ndim):
    mcmc = np.percentile(flatSamples[:,i],[16,50,84])
    q = np.diff(mcmc)
    stdDev = np.mean(q)
    print(mcmc[1], stdDev)

fig, ax = plt.subplots(1,1, figsize = (6,4))
ax.plot(velocities, signal)
ax.plot(velocities, functions.doubleGaussModel(gaussParams, velocities))

plt.savefig("./images/doubleGaussFit.png")

fig1 = corner.corner(flatSamples, labels = ["$\mu_1$", "$\sigma_1$", "$A_1$", "$\mu_2$", "$\sigma_2$", "$A_2$"])
plt.savefig("./images/doubleGaussCorner.png")
print(gaussParams)
print(redChiSq)
