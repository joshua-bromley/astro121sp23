import numpy as np
import matplotlib.pyplot as plt
import maps

filenames = []

for i in range(30):
    for j in range(30):
        filenames.append("./lab4data/new_april22/gridPoint_{0}b_{1}l.fits".format(i,j))

print(filenames[102])

pol0, pol1, pol0Err, pol1Err,_, frequencies = maps.readData(filenames)

for i in range(len(pol0)):
    pol0[i] = maps.polyDetrend(pol0[i],frequencies,pol0Err[i])



fig, ax = plt.subplots(1,1)
for i in range(7):
    ax.plot(frequencies, pol0[100*i])
#ax.plot(frequencies, pol0[500])
#ax.plot(frequencies, pol0Baseline)

fig.savefig("./images/baseline.png")

prominence = maps.getProminence(pol0[0])

fig1, ax1 = plt.subplots(1,1)
ax1.plot(pol0[0]/np.max(pol0[0]))
ax1.plot(prominence)
fig1.savefig("./images/prominence.png")

