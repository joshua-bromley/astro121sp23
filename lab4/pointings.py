import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import cartopy.crs as ccrs
import colors

npz = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)


temperature = npz["temp"]
metadata = npz["coord"]

fails = []


for i in range(len(temperature)):
    if temperature[i][0] == None or temperature[i][0] > 200:
        fails.append(i)

time = []
l = []
b = []
for i in range(len(metadata)):
    time.append(metadata[i][0])
    l.append(metadata[i][1])
    b.append(metadata[i][2])

fig = plt.figure(figsize = (6,6))
ax = fig.add_subplot(1,1,1,projection = ccrs.Mollweide(central_longitude=180))
for i in range(len(l)):
    if i in fails:
        ax.plot(l[i],b[i], marker = "o", ls = "", color = colors.berkeley_blue, alpha = 0.25, transform = ccrs.PlateCarree())
    else:
        ax.plot(l[i],b[i], marker = "o", ls = "", color = colors.berkeley_blue, alpha =1, transform = ccrs.PlateCarree())

ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)

plt.tight_layout()
fig.savefig("./images/pointings.png")
fig.savefig("./figures/pointings.pdf")