import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()


x = np.linspace(0,2*np.pi)


ax = fig.add_subplot(2,1,1)
ax.plot(x,np.sin(x))

ax1 = fig.add_subplot(2,1,2)
ax1.plot(x,np.cos(x))



fig.savefig("./images/test.png")