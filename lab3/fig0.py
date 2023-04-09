import numpy as np
import matplotlib.pyplot as plt
import colors
from matplotlib import rcParams

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

data = np.zeros([500,500])

for i in range(len(data)):
    for j in range(len(data[i])):
        if (i-250)**2 + (j-250)**2 < 25**2:
            data[i][j] = 1

transformedData = np.fft.fftshift(np.fft.fft2(data))

x = np.linspace(0,0.5)
y = np.zeros(50)

fig,ax = plt.subplots(1,2,figsize = (12,6))
image1 = ax[0].imshow(data, cmap = "cividis", extent = [-1,1,-1,1])
image2 = ax[1].imshow(np.abs(transformedData), cmap = "cividis", extent = [-1,1,-1,1])
ax[1].plot(x,y, color = colors.rose_garden)

for axis in ax:
    axis.tick_params(axis = 'x', bottom = True, top = False, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'x', bottom = True, top = False, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
    axis.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

plt.tight_layout()
plt.savefig("./figures/pngs/fig0.png")
plt.savefig("./figures/pdfs/fig0.pdf")