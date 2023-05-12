import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import emcee

npz = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)

v = npz["speed"]
vErr = npz["vErr"]
metadata = npz["coord"]

fails = []
for i in range(len(v)):
    if v[i][0] == None:
        fails.append(i)

print(fails)

centerL = 230
centerB = 0
        

vErr = np.delete(vErr,fails)
v = np.delete(v,fails)
metadata = np.delete(metadata,fails, axis = 0)

time = []
l = []
b = []
for i in range(len(metadata)):
    time.append(metadata[i][0])
    l.append(metadata[i][1])
    b.append(metadata[i][2])


deltaV = []

for i in range(len(v)):
    if len(v[i]) == 2:
        deltaV.append((v[i][-1]+v[i][0])/2)

bulkV = np.mean(deltaV)
bulkVErr = np.std(deltaV)

newV = []
newVErr = []
for i in range(len(v)):
    if v[i][0] < v[i][-1]:
        newV.append(v[i][0] - bulkV)
        newVErr.append(vErr[i][0] + bulkVErr)
    else:
        newV.append(v[i][-1] - bulkV)
        newVErr.append(vErr[i][-1] + bulkVErr)


outBubble = []
for i in range(len(newV)):
    if newV[i] > 0:
        outBubble.append(i)

v = np.delete(newV, outBubble)
vErr = np.delete(newVErr, outBubble)
l = np.delete(l, outBubble)
b = np.delete(b, outBubble)

v = np.abs(v)

angle = []
for i in range(len(l)):
    radL = np.deg2rad(np.abs(l[i]- centerL))
    radB = np.deg2rad(np.abs(b[i]-centerB))
    angle.append(np.arcsin(0.5*np.sqrt(np.sin(radL)**2 + np.sin(radB)**2)))
    if np.isnan(angle[-1]):
        print(0.5*np.sqrt(np.sin(radL)**2 + np.sin(radB)**2))


def model(theta, params):
    v = params[2]*np.cos(np.pi-np.arcsin(np.sin(theta*params[0]/params[1])))
    return v

def chiSq(x,y,err, model, params):
    predicted = []
    for i in range(len(x)):
        predicted.append(model(x[i],params))
    error = [0.5*((y[i] - predicted[i])**2 / (err[i]**2)) for i in range(len(y))]
    
    return np.sum(error)

def logProbability(theta, x, y, err, model):
    lnl = -chiSq(x,y,err,model,theta)
    lp = logPrior(theta)
    return lnl + lp

def logPrior(theta):
    d0 = theta[0]*3.240756e-17
    d1 = theta[0]*3.240756e-17
    if np.sum(theta) == np.inf:
        return -np.inf

    lp0 = -0.5*((788-d0)**2 / (200)**2)
    lp1 = -0.5*((220-d1)**2 / (70)**2)
    lp2 = -0.5*((10000-theta[2])**2 / (3000)**2)
    return lp0+lp1+lp2

params = [2.4e19,6.9e18,np.max(v)]
nwalkers = 16
ndim = 3
pos = params*np.ones([nwalkers,ndim]) + params*((np.random.random([nwalkers,ndim])-0.5)/5)
sampler = emcee.EnsembleSampler(nwalkers, ndim, logProbability, args = (angle,v,vErr,model))
sampler.run_mcmc(pos, 10000, progress = True)
flatSamples = sampler.get_chain(discard = 100, thin = 15, flat = True)
results = []
for i in range(ndim):
    mcmc = np.percentile(flatSamples[:,i],[2.5,50,97.5])
    q = np.diff(mcmc)
    stdDev = np.mean(q)
    results.append((mcmc[1], stdDev))

print(results)              