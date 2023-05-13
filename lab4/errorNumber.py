import numpy as np

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

temperature = np.delete(temperature,fails)
speeds = np.delete(speeds,fails)
metadata = np.delete(metadata,fails, axis = 0)
sigma = np.delete(sigma, fails)
chiSq = np.delete(chiSq, fails)

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

print(np.mean(newTemps), np.std(newTemps))
print(np.mean(newSpeeds), np.std(newSpeeds))
print(np.mean(newSigmas), np.std(newSigmas))
print(np.mean(chiSq), np.std(chiSq))

i = np.argmax(newTemps)
print(metadata[i])