import numpy as np
import matplotlib.pyplot as plt

filename = "doubleSin_samp3MHz_ob1500kHz_ob2501kHz.gz"

data = np.loadtxt("./lab1data/"+filename)
sampleRate = 3e6
timeStep = 1/sampleRate
times = np.linspace(0,len(data)*timeStep,len(data))

voltageSpectrum = np.abs(np.fft.fft(data))
powerSpectrum = np.multiply(voltageSpectrum,voltageSpectrum)
frequencies = np.fft.fftfreq(len(powerSpectrum), timeStep)

fig, ax = plt.subplots(2,1)

ax[0].plot(times[0:200],data[0:200])
ax[1].plot(np.fft.fftshift(frequencies),np.fft.fftshift(powerSpectrum))

plt.savefig("./images/test.png")