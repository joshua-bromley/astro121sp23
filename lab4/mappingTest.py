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

print(min(l),max(l))
print(min(b),max(b))

newTemps = []
newSpeeds = []
newSigmas = []
for i in range(len(temperature)):
    if speeds[i][0] < speeds[i][-1]:
        newTemps.append(temperature[i][0])
        newSpeeds.append(speeds[i][0])
        newSigmas.append(sigma[i][0])
    else:
        newTemps.append(temperature[i][-1])
        newSpeeds.append(speeds[i][-1])
        newSigmas.append(sigma[i][-1])
    if newSpeeds[-1] > 15000:
        print(i)

vGrid = maps.interpolate(newSpeeds,l,b,160,221,-70,-12,1,1)

fig = plt.figure(figsize = (5,5))

cmap = cm.get_cmap("jet")
newTemps = (newTemps - np.min(newTemps))/(np.max(newTemps) - np.min(newTemps))
colors = cmap(newTemps)

ax = fig.add_subplot(1,1,1,projection = ccrs.Mollweide(central_longitude=180))
#img = ax.imshow(vGrid, cmap = "jet", extent = [221,160,-70,-12], transform = ccrs.PlateCarree())
ax.scatter(l,b,transform = ccrs.PlateCarree(), color = colors)
ax.set_extent([140,240,-80,5], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
#cbar = fig.colorbar(img)
#cbar.set_label("Temperature (K)", fontsize = 14)
#cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
#cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)

ax.plot(230,0, zorder = 1, marker = "*", color = "r", transform = ccrs.PlateCarree())

plt.tight_layout()
plt.savefig("./images/mapTest.png")
plt.show()

print(l[150],b[150])