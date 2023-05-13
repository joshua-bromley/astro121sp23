import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import maps
import cartopy.crs as ccrs

npz = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)


temperature = npz["temp"]
speeds = npz["speed"]
metadata = npz["coord"]
sigma = npz["sigma"]
chiSq = npz["chiSq"]

fails = []


for i in range(len(temperature)):
    if temperature[i][0] == None or temperature[i][0] > 200:
        fails.append(i)

print(len(fails))

        

temperature = np.delete(temperature,fails)
speeds = np.delete(speeds,fails)
metadata = np.delete(metadata,fails, axis = 0)
sigma = np.delete(sigma, fails)
chiSq = np.delete(chiSq, fails)


time = []
l = []
b = []
for i in range(len(metadata)):
    time.append(metadata[i][0])
    l.append(metadata[i][1])
    b.append(metadata[i][2])


frontSpeed = []
frontL = []
frontB = []
for i in range(len(speeds)):
    if len(speeds[i]) == 2:
        frontSpeed.append(speeds[i][-1])
        frontL.append(l[i])
        frontB.append(b[i])

frontVGrid = maps.interpolate(frontSpeed,frontL,frontB,160,221,-70,-12,0.25,0.25)
frontVGrid[0][0] = -np.min(frontVGrid)

fig = plt.figure(figsize = (5,5))

ax = fig.add_subplot(1,1,1,projection = ccrs.Mollweide(central_longitude=180))
img = ax.imshow(frontVGrid*1e-3, cmap = "RdBu_r", extent = [160,221,-70,-12], transform = ccrs.PlateCarree(), origin = "lower")
ax.set_extent([150,231,-75,1], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
cbar = fig.colorbar(img)
cbar.set_label("Velocity (km/s)", fontsize = 14)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)
ax.plot(230,0, zorder = 1, marker = "*", color = "r", transform = ccrs.PlateCarree())


fig.savefig("./images/frontVMap.png")
fig.savefig("./figures/frontVMap.pdf")
