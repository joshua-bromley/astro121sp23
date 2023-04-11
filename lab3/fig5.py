import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import interferometry as intf
import colors

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

hourAngle = intf.uTimeToHrAngle(times)

frequencies = frequencies*1e-9

fringePattern = np.transpose(data)[150][9000:]

hourAngle = hourAngle[9000:]

fig, ax = plt.subplots(1,1, figsize = (12,4))
ax.plot(hourAngle, np.real(fringePattern), color = colors.berkeley_blue, alpha = 0.8, label = "Real")
ax.plot(hourAngle, np.imag(fringePattern), color = colors.lap_lane, alpha = 0.8, label = "Imaginary")
ax.plot(hourAngle, np.abs(fringePattern), color = colors.california_gold, alpha = 0.8, label = "Absolute Value") 
ax.legend(frameon = False, fontsize = textSize)

ax.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_ylabel("Power (Arbitrary)", fontsize = axesLabelSize)
ax.set_xlabel("Hour Angle (Radians)", fontsize = axesLabelSize)


plt.tight_layout()
plt.savefig("./figures/pngs/fig5.png")
plt.savefig("./figures/pdfs/fig5.pdf")