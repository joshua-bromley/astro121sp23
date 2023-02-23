import numpy as np

def polyModel(params,x):
    return params[0]*(x-params[1])**2 + params[2]

def gaussModel(params,x):
    return (params[2]/(params[1]*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-params[0])/params[1])**2)

def doubleGaussModel(params, x):
     return (params[2]/(params[1]*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-params[0])/params[1])**2) + (params[5]/(params[4]*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-params[3])/params[4])**2) 

def logLikelihood(theta, x, y, err, model):
    predicted = model(theta,x)
    error = [((y[i] - predicted[i])**2 / (2*err[i]**2)) for i in range(len(y))]
    lnl = -np.sum(error)
    return lnl

def logPrior(theta):
    for param in theta:
        if np.abs(param) > 1e15:
            return -np.inf
    return 0

def logProbability(theta, x, y, err, model):
    lp = logPrior(theta)
    lnl = logLikelihood(theta, x, y, err, model)
    return lp + lnl