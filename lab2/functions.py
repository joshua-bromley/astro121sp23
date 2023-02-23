import numpy as np
import ugradio

def fileToPowerSpec(filenames):
    '''
    Loads data from a bunch of files and returns the average power spectrum
    Parameters: 
        filenames: array of filenames to load data from 
    Returns:
        acgPowerSpectrum: The averaged power spectrum
    '''
    data = np.loadtxt(filenames[0], dtype = complex)
    for i in range(1,len(filenames)):
        newData = np.loadtxt(filenames[i], dtype = complex)
        data = np.concatenate((data, newData))
        
    voltageSpectrum = np.abs(np.fft.fft(data))
    powerSpectrum = np.multiply(voltageSpectrum,voltageSpectrum)
    avgPowerSpectrum = np.mean(powerSpectrum, axis = 0)
    return avgPowerSpectrum

def gain(coldSpec, hotSpec, deltaT):
    '''
    Calculates gain from power spectra
    Parameters:
        coldSpec: Power Spectrum of telescope pointed at the sky
        hotSpec: Power spectrum of telecope pointed at humans
        deltaT: Temperature difference between sky and humans
    Returns:
        gainVal: the gain
    '''
    gainVal = deltaT*np.sum(coldSpec)/np.sum(hotSpec-coldSpec)
    return gainVal

def calcGain(filenamesCold, filenamesHot):
    '''
    Calculates gain based on calibration files
    Parameters:
        filenamesCold: Array of arrays of filenames of the sky data. Each subarray should have the same LO frequency
        filenamesHot: Array of arrays of filenames of the human data. Each subarray should have the same LO frequency
    Returns:
        avgGain: The average gain value over all the LO frequencies
    '''
    gains = []
    for i in range(len(filenamesCold)):
        powerSpecCold = fileToPowerSpec(filenamesCold[i])
        powerSpecHot = fileToPowerSpec(filenamesHot[i])
        gains.append(gain(powerSpecCold,powerSpecHot,300))
    avgGain = np.mean(gains)
    return avgGain

'''
filenamesColdLow = ["./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1419_906MHzLO_signalRF_maxSamp2.gz"]
filenamesHotLow = ["./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1419_906MHzLO_signalRF_maxSamp2.gz"]
filenamesColdHigh = ["./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornCOLD_1420_906MHzLO_signalRF_maxSamp3.gz"]
filenamesHotHigh = ["./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp2.gz","./lab2data/hornHUMAN_1420_906MHzLO_signalRF_maxSamp3.gz"]

powerSpecColdLow = fileToPowerSpec(filenamesColdLow)
powerSpecHotLow = fileToPowerSpec(filenamesHotLow)

powerSpecColdHigh = fileToPowerSpec(filenamesColdHigh)
powerSpecHotHigh = fileToPowerSpec(filenamesHotHigh)


gainValLow = gain(powerSpecColdLow, powerSpecHotLow, 10)
gainValHigh = gain(powerSpecColdHigh, powerSpecHotHigh, 10)

print(gainValLow, gainValHigh)
'''