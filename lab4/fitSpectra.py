import maps
import numpy as np
from tqdm import tqdm

npz = np.load("./lab4data/deconvolvedSpectra.npz", allow_pickle=True)

pol0 = npz["pol0"]
pol1 = npz["pol1"]
metadata = npz["metadata"]
velocities = npz["v"]
pol0Err = npz["pol0Err"]
pol1Err = npz["pol1Err"]


temperatures = []
speeds = []
spreads = []
tempErr = []
speedsErr = []
spreadsErr = []
chiSq = []



badData = []
for i in tqdm(range(len(pol0))):
    data = []
    err = []
    if np.mean(pol0[i]) > 0 and np.mean(pol1[i]) > 0:
        data = (pol0[i]+pol1[i])/2
        err = (np.abs(pol0Err[i])+np.abs(pol1Err[i]))/2
    elif np.mean(pol0[i]) <= 0 and np.mean(pol1[i]) > 0:
        data = pol1[i]
        err = pol1Err[i]
    elif np.mean(pol1[i]) <= 0 and np.mean(pol0[i]) > 0:
        data = pol0[i]
        err = pol0Err[i]

    else:
        data = np.zeros_like(pol0[i])
        err = np.ones_like(pol0[i])
        badData.append(i)
    prominence = maps.getProminence(data)
    indecies = np.argsort(prominence)
    if np.abs(velocities[i][indecies[-1]] - velocities[i][indecies[-2]]) > 10000:
        p0 = [np.abs(data[indecies[-1]]),velocities[i][indecies[-1]],10000,np.abs(data[indecies[-2]]),velocities[i][indecies[-2]],10000]
    else:
        p0 = [data[indecies[-1]]/2,velocities[i][indecies[-1]],10000,data[indecies[-2]]/2,velocities[i][indecies[-2]],10000]
    try:
        params = maps.getVelocity(data, velocities[i], p0, err)
    except(RuntimeError):
        print("Velocities could not be Found", i)
        params = [[None,None,None,None,None,None],None]
    if len(params) == 2:
        temperatures.append([params[0][0]])
        speeds.append([params[0][1]])
        spreads.append([params[0][2]]) 
        tempErr.append([params[0][3]])
        speedsErr.append([params[0][4]])
        spreadsErr.append([params[0][5]])
        chiSq.append(params[-1])
    else:
        temperatures.append([params[0][0],params[1][0]])
        speeds.append([params[0][1],params[1][1]])
        spreads.append([params[0][2],params[1][2]])
        tempErr.append([params[0][3],params[1][3]])
        speedsErr.append([params[0][4],params[1][4]])
        spreadsErr.append([params[0][5],params[1][5]])
        chiSq.append(params[-1])


np.savez("./lab4data/processedSpectra", temp = temperatures, speed = speeds,coord = metadata,sigma =spreads, tempErr = tempErr, vErr = speedsErr, sigmaErr = spreadsErr, chiSq = chiSq)
print(badData)