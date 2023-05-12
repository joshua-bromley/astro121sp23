import maps
import matplotlib.pyplot as plt
import numpy as np

pol0, pol1, pol0err, pol1err, metadata, freqs = maps.readData(["./lab4data/new_april22/gridPoint_7b_12l.fits"])

v = maps.freqToVelocity(freqs, metadata[0])
print(len(v))
centralF = freqs[np.argmin(np.abs(v))]
print(centralF)

data, model, mask = maps.deconvolve(pol1[0],freqs, centralF, debug = True)

fig,ax = plt.subplots(1,1, figsize = (8,4))
ax.plot((mask*data))
ax.plot(model)
fig.savefig("./images/deconvolution.png")