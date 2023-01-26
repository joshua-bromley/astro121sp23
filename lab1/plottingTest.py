import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0,5)

fig, ax = plt.subplots(2,1)

ax[0].plot(x,x)
ax[1].plot(x,x, color = "xkcd:neon red")

plt.savefig("./images/test.png")