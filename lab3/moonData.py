import numpy as np


filename = "./lab3data/dataBatch{0}.npz"

data = np.zeros(1024)
times = []

for i in range(1152):
    npz = np.load(filename.format(i), allow_pickle=True)
    for arr in npz["arr_0"]:
        data = np.vstack((data, arr[0]))
        times.append(arr[1][0])
    
data = data[1:]


np.savez("./lab3data/moonData", vis = data, times = times)
