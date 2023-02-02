import numpy as np 
import matplotlib.pyplot as plt
import scipy
from matplotlib import rcParams

##Adjust plotting defaults
rcParams["axes.linewidth"] = 3.5

rcParams["ytick.right"] = True
rcParams["ytick.direction"] = "in"
rcParams["ytick.minor.visible"] = True
rcParams["ytick.major.left"] = True
rcParams["ytick.major.right"] = True
rcParams["ytick.minor.left"] = True
rcParams["ytick.minor.right"] = True
rcParams["ytick.major.size"] = 16
rcParams["ytick.minor.size"] = 8



rcParams["xtick.top"] = True
rcParams["xtick.direction"] = "in"
rcParams["xtick.minor.visible"] = True
rcParams["xtick.major.top"] = True
rcParams["xtick.major.bottom"] = True
rcParams["xtick.minor.top"] = True
rcParams["xtick.minor.bottom"] = True
rcParams["xtick.major.size"] = 16
rcParams["xtick.minor.size"] = 8 

axesLabelSize = 34
tickLabelSize = 26
textSize = 26


filename ="data_500kHzFreq_3000kHzSamp2.gz"

signalRate = 0.5e6 #Signal Rate in HZ
sampleRate = 3e6 #Sample rates in Hz

data = np.loadtxt("./lab1data/"+filename)


fig, ax = plt.subplots(1,1, figsize = (12,8))
timeStep = 1/sampleRate
times = np.arange(0,200*timeStep*1e-3,timeStep*1e-3)


voltageSpectrum = np.fft.fft(data)
frequencies = np.fft.fftfreq(len(voltageSpectrum), timeStep)

realSpectrum = np.real(voltageSpectrum)
imaginarySpectrum = np.imag(voltageSpectrum)
magSpectrum = np.abs(voltageSpectrum)
powerSpectrum = np.multiply(magSpectrum,magSpectrum)

ax.plot(np.fft.fftshift(frequencies),np.fft.fftshift(realSpectrum), ls = "-",lw = 1, alpha = 0.6, label = "Real")
ax.plot(np.fft.fftshift(frequencies),np.fft.fftshift(imaginarySpectrum), ls = "-", lw = 1, alpha = 0.6, label = "Imaginary")
# ax.plot(np.fft.fftshift(frequencies), np.fft.fftshift(magSpectrum), ls = "-", lw = 1, alpha = 0.6, label = "Power")

ax.legend(loc = "upper left", frameon = False, fontsize = textSize)



    
ax.tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax.tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)


plt.tight_layout()
plt.savefig("./images/voltageSpectrum"+".jpg")
plt.savefig("./images/pdfs/voltageSpectrum"+".pdf")

fig1, ax1 = plt.subplots(3,1,figsize = (14,24))
fig1.subplots_adjust(hspace = 0)

invPowerSpectrum = np.fft.ifft(powerSpectrum)
npACF = np.correlate(data, data, mode = "full")
spACF = scipy.signal.correlate(data, data)

acTimes = np.linspace(-2047*timeStep*1e3,2047*timeStep*1e3, 4095)
iftTimes = np.linspace(-2048*timeStep*1e3,2048*timeStep*1e3, 2048)

ax1[0].plot(iftTimes,np.fft.fftshift(invPowerSpectrum), label = "IFT", ls = "-", marker = ".")
ax1[1].plot(acTimes,npACF, label = "numpy", ls = "-", marker = ".")
ax1[2].plot(acTimes,spACF, label = "scipy", ls = "-", marker = ".")

ax1[0].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)
ax1[0].xaxis.set_label_position("top")
ax1[2].set_xlabel("Time Difference (ms)", fontsize = axesLabelSize)
ax1[1].set_ylabel("Correlartion ", fontsize = axesLabelSize)


#ax1.legend(loc = "upper left", frameon = False, fontsize = textSize)
ax1[0].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = True, labelbottom = False)
ax1[0].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[0].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[0].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[1].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10, labeltop = False, labelbottom = False)
ax1[1].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[1].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[1].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[2].tick_params(axis = 'x', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[2].tick_params(axis = 'x', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[2].tick_params(axis = 'y', bottom = True, top = True, which = "major", direction = "in", labelsize = tickLabelSize, pad = 10)
ax1[2].tick_params(axis = 'y', bottom = True, top = True, which = "minor", direction = "in", labelsize = tickLabelSize, pad = 10)

#plt.tight_layout(pad = 0)
plt.savefig("./images/autoCorrelate"+".jpg")
plt.savefig("./images/pdfs/autoCorrelate"+".pdf")









