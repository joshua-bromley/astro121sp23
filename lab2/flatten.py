import numpy as np
import matplotlib.pyplot as plt
import emcee
import functions

filenamesCold = [["./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp2.gz"],["./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp3.gz"]]
filenamesHot = [["./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp2.gz"],["./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp3.gz"]]

gain = functions.calcGain(filenamesCold, filenamesHot)

dataLow = np.loadtxt("./lab2data/LO1419.gz")
dataHigh = np.loadtxt("./lab2data/LO1420.gz")

signalLow = dataLow[1][0:1024]
calLow = np.flip(dataLow[1][1024:])

velocitiesLow = dataLow[0][0:1024]

signalLowFlat = np.divide(signalLow, calLow)*gain

velocitiesLowFit = np.concatenate((velocitiesLow[0:120],velocitiesLow[540:-1]))
signalLowFit = np.concatenate((signalLowFlat[0:120],signalLowFlat[540:-1]))
err = 3.72902*np.ones(len(signalLowFit))

pos = [5e6,-0.0005,140]*np.ones([16,3]) + [5e6,-0.0005,140]*((np.random.random([16,3])-0.5)/5)


nwalkers, ndim = pos.shape

sampler = emcee.EnsembleSampler(nwalkers, ndim, functions.logProbability, args = (velocitiesLowFit, signalLowFit, err, functions.polyModel))
sampler.run_mcmc(pos,5000, progress = True)
flatSamples = sampler.get_chain(discard = 100, thin = 15, flat = True)
logProb = sampler.get_log_prob()

redChiSq = np.mean(-logProb[-1]/(631))
print("Chi Sq Low", redChiSq)



lowParams = np.ones(ndim)
for i in range(ndim):
    lowParams[i] = np.percentile(flatSamples[:,i],50)

lowFlat = signalLowFlat - functions.polyModel(lowParams, velocitiesLow)

residuals = signalLowFit - functions.polyModel(lowParams, velocitiesLowFit)
stdDev = np.std(residuals)
print(stdDev)

signalHigh = dataHigh[1][1024:]
calHigh = np.flip(dataHigh[1][0:1024])
signalHighFlat = np.divide(signalHigh, calHigh)*gain

velocitiesHigh = dataHigh[0][1024:]


velocitiesHighFit = np.concatenate((velocitiesHigh[0:540], velocitiesHigh[-75:]))
signalHighFit = np.concatenate((signalHighFlat[0:540],signalHighFlat[-75:]))
err = 3.46*np.ones(len(signalHighFit))


pos = [5e6,0.0005,140]*np.ones([16,3]) + [5e6,0.0005,140]*((np.random.random([16,3])-0.5)/5)

nwalkers, ndim = pos.shape

sampler = emcee.EnsembleSampler(nwalkers, ndim, functions.logProbability, args = (velocitiesHighFit, signalHighFit, err, functions.polyModel))
sampler.run_mcmc(pos,5000, progress = True)
flatSamples = sampler.get_chain(discard = 100, thin = 15, flat = True)
logProb = sampler.get_log_prob()

redChiSq = np.mean(-logProb[-1]/(612))
print("Chi Sq High", redChiSq)

highParams = np.ones(ndim)
for i in range(ndim):
    highParams[i] = np.percentile(flatSamples[:,i],50)

highFlat = signalHighFlat - functions.polyModel(highParams, velocitiesHigh) 

residuals = signalHighFit - functions.polyModel(highParams, velocitiesHighFit)
stdDev = np.std(residuals)
print(stdDev)


fig, ax = plt.subplots(2,1, figsize = (6,8))
ax[0].plot(velocitiesLow, lowFlat)
ax[1].plot(velocitiesHigh, highFlat)

print(lowParams, highParams)


#Low [120:540]
#High [540:-75]

index = np.where(np.abs(velocitiesHigh -0.000162776529940715) < 0.0000001)




avgSignal = np.mean((lowFlat[120:565], highFlat[504:-75]), axis = 0)

np.savetxt("./lab2data/flattenedSignal.gz", (velocitiesLow[120:565], avgSignal))

print(gain)







