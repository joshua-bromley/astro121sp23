import numpy as np
import matplotlib.pyplot as plt
import ugradio as ug

filename ="data_500kHzFreq_3000kHzSamp2.gz"

signalRate = 0.5e6 #Signal Rate in HZ
sampleRate = 3e6 #Sample rates in Hz

data = np.loadtxt("./lab1data/"+filename)

frequencies, voltageSpectrum = ug.dft.dft(data)

powerSpectrum = np.multiply(np.abs(voltageSpectrum),np.abs(voltageSpectrum))

fig, ax = plt.subplots(1,1, figsize = (6,4))

ax.plot(frequencies,powerSpectrum)

plt.savefig("./images/ugradioTest.png")