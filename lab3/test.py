import ugradio as ug
import numpy as np

filename = "./lab3data/403_dataBatch{0}.npz"


data = np.zeros(1024)
times = []

npz = np.load("./lab3data/moonData.npz", allow_pickle=True)
print(npz['vis'][5])



'''
for i in range(0,10):
    npz = np.load(filename.format(i), allow_pickle=True)
    for j in range(20):
        data = np.vstack((data, npz["arr_0"][j]['corr01']))
        times.append(npz["arr_0"][j]["time"])
    print(i)

print(data.shape)
print(times)
'''

    