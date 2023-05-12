import numpy as np
import maps
from matplotlib import pyplot as plt


gainFilenames = ["./lab4data/calib.fits", "./lab4data/calib_noise.fits"]

pol0G, pol1G, _, _, _,_ = maps.readData(gainFilenames)

gain0 = maps.gain(pol0G[1],pol0G[0],79)
gain1 = maps.gain(pol1G[1],pol1G[0],58)

print(gain0, gain1)

filenames = []

for i in range(30):
    for j in range(30):
        filenames.append("./lab4data/new_april22/gridPoint_{0}b_{1}l.fits".format(i,j))

filenames = ["./lab4data/new_april22/gridPoint_3b_13l.fits"]

pol0, pol1, pol0Err, pol1Err, metadata, freqs = maps.readData(filenames)

for i in range(len(pol0)):
    pol0[i],_ = maps.deconvolve(pol0[i],freqs)
    pol1[i],_ = maps.deconvolve(pol1[i],freqs)

_,freqs = maps.deconvolve(pol0G[0],freqs)

pol0 = np.multiply(pol0, gain0)
pol1 = np.multiply(pol1, gain1)

velocities = []
for i in range(len(metadata)):
    velocities.append(maps.freqToVelocity(freqs,metadata[i]))

temperatures = []
speeds = []
spreads = []




for i in range(len(pol0)):
    data = []
    if np.mean(pol0[i]) > 0 and np.mean(pol1[i]) > 0:
        data = (pol0[i]+pol1[i])/2
    elif np.mean(pol0[i]) <= 0:
        data = pol1[i]
    elif np.mean(pol1[i]) <= 0:
        data = pol0[i]
    else:
        data = np.zeros_like(pol0[i])
    prominence = maps.getProminence(data)
    indecies = np.argsort(prominence)
    p0 = [data[indecies[-1]],velocities[i][indecies[-1]],10000,data[indecies[-2]],velocities[i][indecies[-2]],10000]
    try:
        params = maps.getVelocity(data, velocities[i], p0)
    except(RuntimeError):
        print("Velocities could not be Found")
        params = [[None,None,None]]
    if len(params) == 2:
        temperatures.append([params[0][0],params[1][0]])
        speeds.append([params[0][1],params[1][1]])
        spreads.append([params[0][2],params[1][2]])
    else:
        temperatures.append([params[0][0]])
        speeds.append([params[0][1]])
        spreads.append([params[0][2]]) 
    print(i)
    

'''
fig,ax = plt.subplots(1,1)
ax.plot(velocities[0], (pol0[0] + pol1[0])/2)
#ax.plot(velocities[0], pol1[0])
if len(temperatures[i]) == 1:
    ax.plot(velocities[0],maps.gaussian(velocities[0],temperatures[i][0],speeds[i][0],spreads[i][0]))
else:
    ax.plot(velocities[0],maps.doubleGaussian(velocities[0],temperatures[i][0],speeds[i][0],spreads[i][0], temperatures[i][1],speeds[i][1],spreads[i][1]))
'''




#fig.savefig("./images/testData.png")


#np.savez("./lab4data/processedSpectra", temp = temperatures, speed = speeds,coord = metadata,sigma =spreads)


