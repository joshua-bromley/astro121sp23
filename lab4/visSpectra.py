from matplotlib import pyplot as plt
import numpy as np


npz = np.load("./lab4data/deconvolvedSpectra.npz", allow_pickle=True)


pol0 = npz["pol0"]
metadata = npz["metadata"]
v = npz["v"]

npz = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)


temperature = npz["tempErr"]
speeds = npz["speed"]
metadata1 = npz["coord"]
sigma = npz["sigma"]
chiSq = npz["chiSq"]


fails = []
for i in range(len(temperature)):
    if temperature[i][0] == None or temperature[i][0] > 200:
        fails.append(i)


        

temperature = np.delete(temperature,fails)
speeds = np.delete(speeds,fails)
metadata = np.delete(metadata,fails, axis = 0)
metadata1 = np.delete(metadata1,fails, axis = 0)
sigma = np.delete(sigma, fails)
chiSq = np.delete(chiSq, fails)
pol0 = np.delete(pol0, fails, axis = 0)
v = np.delete(v, fails, axis = 0)


i = np.argmax(temperature)

print(metadata[i],metadata1[i])
print(temperature[i])

print(fails, i)

fig, ax = plt.subplots(1,1, figsize = (6,8))
ax.plot(v[i]*1e-3,pol0[i])
ax.set_xlim(np.max(v[i]*1e-3),np.min(v[i]*1e-3))

fig.savefig("./images/spectra.png")