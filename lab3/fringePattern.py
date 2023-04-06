import numpy as np
import matplotlib.pyplot as plt
import pickle
##import ugradio
import interferometry as intf

data = []
times = []
accCnt = []
filepath = "./lab3data/12hrSun_new/dat{0}.pkl"

data, times, _ , accCnt = intf.readData(filepath, 11862, 500, 800)



transformedData = np.fft.fftshift(np.fft.fft(data, axis = 0))
transformedDataTwo = np.fft.fftshift(np.fft.fft(data, axis = 1))
fig, ax = plt.subplots(1,3)
ax[0].imshow(np.abs(data)[0:1000],  cmap = "cividis")
ax[1].imshow(np.abs(transformedData)[0:1000],  cmap = "cividis")
ax[2].imshow(np.abs(transformedDataTwo)[0:1000],  cmap = "cividis")

plt.savefig("./images/fringePatternTest.png")

print(len(data))

fig1, ax1 = plt.subplots(1,1)
ax1.plot(np.real(np.transpose(data))[200][-2000:-1])
ax1.plot(np.imag(np.transpose(data))[200][-2000:-1])
ax1.plot(np.abs(np.transpose(data))[200][-2000:-1])
plt.savefig("./images/singleFrequency.png")

