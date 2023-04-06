import numpy as np
import matplotlib.pyplot as plt
import pickle
import ugradio as ug

def chiSq(model, params,x, data, err):
    predicted = model(x,params)
    error = [((data[i] - predicted[i])**2 / (err[i]**2)) for i in range(len(data))]
    return np.sum(error)

def fringeFrequencies(x, params):
    return params[0]*np.cos(x) - params[1]*np.sin(x)

data = []
times = []
accCnt = []
oldData = []
oldTimes = []
oldAccCnt = []
filepath = "./lab3data/12hrSun_new/dat{0}.pkl"
for i in range(1,11862):
    with open(filepath.format(i), "rb") as file:
        tempData = pickle.load(file)
        oldData.append(tempData["corr01"][500:800])
        oldTimes.append(tempData["time"]) ##I think this is in seconds
        oldAccCnt.append(tempData["acc_cnt"])

indecies = np.argsort(oldTimes)
for i in indecies:
    data.append(oldData[i])
    times.append(oldTimes[i])
    accCnt.append(oldAccCnt[i])


spectralFrequencies = np.fft.fftfreq(1024, 500e6)[500:800] + 10.5e9

avgData = np.mean(data, axis = 0)
for i in range(len(data)):
    data[i] = data[i] - avgData

numCorrelations = len(data)
numChunks = 32
chunkLength = int(numCorrelations/numChunks)

freqData = np.transpose(data)[150]
spectralFrequency = spectralFrequencies[150]
timeStep = np.mean(np.diff(times))


fringeFreq = []
fringeTimes = []
err = []

fig, ax = plt.subplots(1,1)

for i in range(numChunks):
    transformedData = np.abs(np.fft.fft(freqData[i*chunkLength:(i+1)*chunkLength]))
    maxIndex = np.where(transformedData == np.max(transformedData[5:]))[0]
    frequencies = np.fft.fftfreq(len(transformedData),timeStep)
    fringeFreq.append(frequencies[maxIndex][0])
    fringeTimes.append(np.mean(times[i*chunkLength:(i+1)*chunkLength]))
    #print(i, fringeTimes[-1])
    error = 0
    ax.plot(frequencies, np.abs(transformedData))
    err.append(np.diff(frequencies)[0])

fig.savefig("./images/fringeFT.png")

jdTimes = ug.timing.julian_date(fringeTimes)
lst = ug.timing.lst(jdTimes)
ra, dec = ug.coord.sunpos(jdTimes[0])
ra = ra*np.pi/180
hourAngle = lst - ra
for i in range(len(hourAngle)):
    if hourAngle[i] < -4:
        hourAngle[i] += 2*np.pi

#err = 0.01*np.ones(len(fringeFreq))
##TODO: Brute force fit using fringeFreq, hourAngle, using the fringeFrequencies function

aParams = np.linspace(0.03, 0.04, 1500)
bParams = np.linspace(-0.02,0.02,1500)

grads = np.zeros([1500,1500])


for i in range(len(aParams)):
    for j in range(len(bParams)):
        grads[i][j] = chiSq(fringeFrequencies, [aParams[i],bParams[j]], hourAngle, fringeFreq, err)/(len(fringeFreq)-2)

minIndex = np.where(grads == np.min(grads))

optA = aParams[minIndex[0][0]]
optB = bParams[minIndex[1][0]]

waveLength = 3e8/spectralFrequency
earthRotRate = 2*np.pi/(86164.0905)

baselineEW = (optA*waveLength)/(np.cos(dec*np.pi/180)*earthRotRate)
baselineNS = (optB*waveLength)/(np.cos(dec*np.pi/180)*np.sin(ug.nch.lat*np.pi/180)*earthRotRate)
print(optA, optB)
#print(chiSq(fringeFrequencies, [0.04,0], hourAngle, fringeFreq, err))

##True Baseline Values: b_ew = 14.91973 m, b_ns = 1.11181 m

fig, ax = plt.subplots(1,1)
ax.errorbar(hourAngle, fringeFreq, yerr = err, marker = "o", ls = "")
ax.plot(hourAngle, fringeFrequencies(hourAngle, [optA, optB]))
plt.savefig("./images/fringeFrequencies.png")


fig, ax = plt.subplots(1,1)
imshow = ax.imshow(grads, cmap = "cividis_r", vmax = 50)
fig.colorbar(imshow, ax = ax)
plt.savefig("./images/gradientDescent.png")







    


