import maps
import numpy as np
import matplotlib.pyplot as plt

filenames = ["./lab4data/calib.fits", "./lab4data/calib_noise.fits"]

pol0, pol1, _, _ = maps.readData(filenames)

pol0Gain = maps.gain(pol0[1],pol0[0],79)
pol1Gain = maps.gain(pol1[1],pol1[0],58)

print(np.mean(pol0Gain),np.mean(pol1Gain))

fig, ax = plt.subplots(1,1)
ax.plot(pol0[0])
ax.plot(pol0[1])
ax.set_yscale("log")

plt.savefig("./images/gain.png")