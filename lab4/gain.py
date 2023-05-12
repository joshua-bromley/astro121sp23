import maps
import numpy as np
import matplotlib.pyplot as plt

filenames = ["./lab4data/calib.fits", "./lab4data/calib_noise.fits"]

pol0, pol1, _, _, _ , _ = maps.readData(filenames)

pol0Gain = maps.gain(pol0[1],pol0[0],79)
pol1Gain = maps.gain(pol1[1],pol1[0],58)

print(pol0Gain,pol1Gain)

pol0 = np.multiply(pol0, pol0Gain)
pol1 = np.multiply(pol1, pol1Gain)

pol0Diff = pol0[1]-pol0[0]
pol1Diff = pol1[1]-pol1[0]

#ax.set_yscale("log")

plt.tight_layout()
plt.savefig("./images/gain.png")

filename = "./lab4data/april21_orion/gridPoint_24b_17l.fits"

dataPol0 = maps.readData([filename])

dataPol0 = np.multiply(dataPol0[0], pol0Gain)


fig,ax = plt.subplots(1,1)
ax.plot(dataPol0[0])
ax.plot(pol0[0])


plt.savefig("./images/testData.png")

