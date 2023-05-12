import maps
import matplotlib.pyplot as plt
import numpy as np

filenames = []

for i in range(30):
    for j in range(30):
        filenames.append("./lab4data/new_april22/gridPoint_{0}b_{1}l.fits".format(i,j))


pol0, pol1, pol0err, pol1err, metadata, freqs = maps.readData(["./lab4data/new_april22/gridPoint_7b_2l.fits"])

data = maps.deconvolve(pol0[0],freqs)

#prominence = maps.getProminence(pol0)

velocities = maps.freqToVelocity(freqs,metadata[0])

data = data[4096-500:4096+500]
velocities = velocities[4096-500:4096+500]
dataErr = pol0err[0][4096-500:4096+500]

results = maps.getVelocity(data, velocities)
print(results)

params = []
for i in results:
    params.append(results[0])

#cloudSpeeds = maps.getVelocity(prominence,velocities)
#print(cloudSpeeds)
#print(metadata[500][1],metadata[500][2])


fig1, ax1 = plt.subplots(1,1)
ax1.plot(velocities, data)
ax1.plot(velocities, maps.doubleGaussian(velocities, *results))
#ax1.plot(velocities, prominence)
fig1.savefig("./images/prominence.png")
