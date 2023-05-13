import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import maps
import cartopy.crs as ccrs

npz = np.load("./lab4data/processedSpectra.npz", allow_pickle=True)


temperature = npz["tempErr"]
speeds = npz["vErr"]
metadata = npz["coord"]
sigma = npz["sigmaErr"]
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


tempGrid = maps.interpolate(newTemps,l,b,160,221,-70,-12,0.25,0.25)
vGrid = maps.interpolate(newSpeeds,l,b,160,221,-70,-12,0.25,0.25)
sigmaGrid = maps.interpolate(newSigmas,l,b,160,221,-70,-12,0.25,0.25)
chiSqGrid = maps.interpolate(chiSq,l,b,160,221,-70,-12,0.25,0.25)
 

#farVGrid = maps.interpolate(farV,l,b,160,221,-70,-12,0.5,0.5)







#tempGrid = (tempGrid-np.min(tempGrid))/(2*(np.max(tempGrid)-np.min(tempGrid))) + 0.5
#nearVGrid = (nearVGrid-np.min(nearVGrid))/(2*(np.max(nearVGrid)-np.min(nearVGrid)))
#farVGrid = (farVGrid-np.min(farVGrid))/(2*(np.max(farVGrid)-np.min(farVGrid)))

#imgGrid = np.zeros([len(farVGrid),len(farVGrid[0]),4])
#for i in range(len(imgGrid)):
#    for j in range(len(imgGrid[0])):
#        imgGrid[i][j] = [nearVGrid[i][j],0,farVGrid[i][j],tempGrid[i][j]]

fig = plt.figure(figsize = (11,11))

ax = fig.add_subplot(2,2,1,projection = ccrs.Mollweide(central_longitude=180))
img = ax.imshow(tempGrid, cmap = "jet", extent = [160,221,-70,-12], transform = ccrs.PlateCarree(), origin = "lower", vmax = 20)
ax.set_extent([160,221,-70,-12], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
cbar = fig.colorbar(img)
cbar.set_label("Temperature (K)", fontsize = 14)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)


ax = fig.add_subplot(2,2,2,projection = ccrs.Mollweide(central_longitude=180))
img = ax.imshow(vGrid*1e-3, cmap = "jet", extent = [160,221,-70,-12], transform = ccrs.PlateCarree(), origin = "lower", vmax = 60)
ax.set_extent([160,221,-70,-12], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
cbar = fig.colorbar(img)
cbar.set_label("Velocity (km/s)", fontsize = 14)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)


ax = fig.add_subplot(2,2,3,projection = ccrs.Mollweide(central_longitude=180))
img = ax.imshow(sigmaGrid*1e-3, cmap = "jet", extent = [160,221,-70,-12], transform = ccrs.PlateCarree(), origin = "lower", vmax = 5)
ax.set_extent([160,221,-70,-12], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
cbar = fig.colorbar(img)
cbar.set_label("Signal Width (km/s)", fontsize = 14)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)

ax = fig.add_subplot(2,2,4,projection = ccrs.Mollweide(central_longitude=180))
img = ax.imshow(chiSqGrid, cmap = "jet", extent = [160,221,-70,-12], transform = ccrs.PlateCarree(), origin = "lower")
ax.set_extent([160,221,-70,-12], crs = ccrs.PlateCarree())
ax.gridlines( draw_labels = True, x_inline = False, y_inline = False)
ax.set_xlabel("$\ell$", fontsize = 25)
ax.set_ylabel("$b$", fontsize = 25)
cbar = fig.colorbar(img)
cbar.set_label("Reduced Chi Squared", fontsize = 14)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = 10, pad = 10)
cbar.ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = 10, pad = 10)

fig.savefig("./images/errorMap.png")
fig.savefig("./figures/errorMap.pdf")

'''
deltaV = []
twoSpeed = 0
for i in range(len(speeds)):
    if len(speeds[i]) == 2:
        twoSpeed += 1
        deltaV.append(speeds[i][-1] - speeds[i][0])
        if speeds[i][-1] - speeds[i][0] > 30000:
            print(i)
    else:
        deltaV.append(0)

print(twoSpeed)

deltaVGrid = maps.interpolate(deltaV,l,b,160,221,-70,-12,0.5,0.5)


ax1 = plt.axes(projection = ccrs.Mollweide(central_longitude=180))
img = ax1.imshow(deltaVGrid, cmap = "jet", extent = [160,221,-70,-12], vmax = 30000, transform = ccrs.PlateCarree())
ax1.set_extent([140,240,-90,00], crs = ccrs.PlateCarree())
ax1.gridlines(draw_labels = True)
plt.colorbar(img)
plt.savefig("./images/dvMap.png")
'''



