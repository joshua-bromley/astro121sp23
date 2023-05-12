from matplotlib import pyplot as plt
import numpy as np


npz = np.load("./lab4data/deconvolvedSpectra.npz", allow_pickle=True)

pol0 = npz["pol0"]
metadata = npz["metadata"]
v = npz["v"]

indecies = np.argsort(metadata[:,2])

print(len(pol0))

sortedPol0 = pol0[indecies]
i = 261
fig, ax = plt.subplots(2,1, figsize = (6,8))
ax[0].imshow(pol0, aspect = "auto")
ax[1].plot(v[i]*1e-3,pol0[i])
ax[1].set_xlim(np.max(v[i]*1e-3),np.min(v[i]*1e-3))

fig.savefig("./images/spectra.png")