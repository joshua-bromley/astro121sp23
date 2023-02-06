import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib import rcParams
from ugradio import dft

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

data = np.loadtxt("./lab1data/data_noise_1blocks_16384samples_10MHzLPfilter_32e5HzRate.csv", delimiter = ",")
bigData = np.loadtxt("./lab1data/data_noise_200blocks_2048samples_10MHzLPfilter_32e5HzRate.csv", delimiter = ",")

mean = np.mean(data)
stdDev = np.std(data)

x = np.linspace(-1,1,100)
y = (1/(stdDev*np.sqrt(2*np.pi)))*np.exp(-0.5*((x-mean)/stdDev)**2)

maxY = np.max(y)

fig, ax = plt.subplots(1,1, figsize = (6,4))

histogram = ax.hist(data, bins = 50, color = "#0d265c")
maxVal = np.max(histogram[0])

ax.plot(x,y*maxVal/maxY,color = "#ffa600")

ax.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

ax.set_xlabel("Voltage (V)", fontsize = axesLabelSize)
ax.set_ylabel("Count", fontsize = axesLabelSize)

plt.tight_layout()
plt.savefig("./images/noiseHist.png")
