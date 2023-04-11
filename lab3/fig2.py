import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import interferometry as intf

rcParams["axes.linewidth"] = 2

rcParams["ytick.right"] = True
rcParams["ytick.direction"] = "in"
rcParams["ytick.minor.visible"] = True
rcParams["ytick.major.left"] = True
rcParams["ytick.major.right"] = True
rcParams["ytick.minor.left"] = True
rcParams["ytick.minor.right"] = True
rcParams["ytick.major.size"] = 8
rcParams["ytick.minor.size"] = 4



rcParams["xtick.top"] = True
rcParams["xtick.direction"] = "in"
rcParams["xtick.minor.visible"] = True
rcParams["xtick.major.top"] = True
rcParams["xtick.major.bottom"] = True
rcParams["xtick.minor.top"] = True
rcParams["xtick.minor.bottom"] = True
rcParams["xtick.major.size"] = 8
rcParams["xtick.minor.size"] = 4

axesLabelSize = 17
tickLabelSize = 13
textSize = 13

filepath = "./lab3data/12hrSun_new/dat{0}.pkl"
data, times, frequencies, _ = intf.readData(filepath, 11862, 500, 800)

wavelengths = 3e8/frequencies

timeStep = np.mean(np.diff(times))
frequencies = np.fft.fftshift(np.fft.fftfreq(1024, timeStep))

fringePattern, hourAngle = intf.getFringeFrequenciesTwo(np.transpose(data)[150], times, 32)


fig, ax = plt.subplots(1,1, figsize = (6,6))
image = ax.imshow(fringePattern, cmap = "cividis", aspect = "auto", extent = [frequencies[0], frequencies[-1], hourAngle[0],hourAngle[-1]])
cbar = fig.colorbar(image)

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_xlabel("Fringe Frequency (Hz)", fontsize = axesLabelSize)
ax.set_ylabel("Hour Angle (Radians)", fontsize = axesLabelSize)

cbar.set_label("Power (Arbitrary)", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./figures/pngs/fig2.png")
plt.savefig("./figures/pdfs/fig2.pdf")

