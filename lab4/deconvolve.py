'''
import maps
import matplotlib.pyplot as plt

pol0, pol1, pol0err, pol1err, metadata, freqs = maps.readData(["./lab4data/new_april22/gridPoint_7b_12l.fits"])

data, model, mask = maps.deconvolve(pol1[0],freqs, debug = True)

fig,ax = plt.subplots(1,1, figsize = (8,4))
ax.plot((data*mask)[3000:5000])
ax.plot(model[3000:5000])
fig.savefig("./images/deconvolution.png")
'''
import numpy as np
import maps
from matplotlib import pyplot as plt
from tqdm import tqdm


gainFilenames = ["./lab4data/calib.fits", "./lab4data/calib_noise.fits"]

pol0G, pol1G, _, _, _,_ = maps.readData(gainFilenames)

gain0 = maps.gain(pol0G[1],pol0G[0],79)
gain1 = maps.gain(pol1G[1],pol1G[0],58)

print(gain0, gain1)

filenames = []

for i in range(30):
    for j in range(30):
        filenames.append("./lab4data/new_april22/gridPoint_{0}b_{1}l.fits".format(i,j))

#filenames = ["./lab4data/new_april22/gridPoint_3b_13l.fits"]

pol0, pol1, pol0Err, pol1Err, metadata, freqs = maps.readData(filenames)

freqsList = []

velocities = []
for i in range(len(metadata)):
    velocities.append(maps.freqToVelocity(freqs,metadata[i]))

for i in range(len(pol0)):
    centralF = freqs[np.argmin(np.abs(velocities[i]))]
    pol0[i],tempFreqs = maps.deconvolve(pol0[i],freqs, centralF)
    pol1[i],_ = maps.deconvolve(pol1[i],freqs, centralF)
    velocities[i] = maps.freqToVelocity(tempFreqs,metadata[i])
    print(i)




pol0 = np.multiply(pol0, gain0)
pol1 = np.multiply(pol1, gain1)
pol0Err = np.multiply(pol0Err, gain0)
pol1Err = np.multiply(pol1Err, gain1)




np.savez("./lab4data/deconvolvedSpectra", pol0 = pol0, pol1 = pol1, pol0Err = pol0Err, pol1Err = pol1Err, metadata = metadata, v = velocities)