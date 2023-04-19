import numpy as np
import ugradio as ug
from astropy.io import fits

def readData(filenames):
    pol0Spectra = []
    pol1Spectra = []
    metadata = []
    pol0Error = []
    pol1Error = []
    sampRate = 0
    numChannels = 0

    
    for filename in filenames:
        with fits.open(filename) as dataLoad:
            tempPol0Spectra = []
            tempPol1Spectra = []
            for i in range(1,len(dataLoad)):
                tempPol0Spectra.append(dataLoad[i].data["auto0_real"])
                tempPol1Spectra.append(dataLoad[i].data["auto1_real"])
            pol0Spectra.append(np.mean(tempPol0Spectra, axis = 0))
            pol1Spectra.append(np.mean(tempPol1Spectra, axis = 0))
            pol0Error.append(np.ones(len(pol0Spectra[-1]))*np.std(fourierFilter(pol0Spectra[-1],1000,numChannels/2)))
            pol1Error.append(np.ones(len(pol1Spectra[-1]))*np.std(fourierFilter(pol1Spectra[-1],1000,numChannels/2)))
            l = dataLoad[0].header["L"]
            b = dataLoad[0].header["B"]
            time = dataLoad[0].header["JD"]
            metadata.append((time,l,b))
            sampRate = float(dataLoad[0].header["SAMPRATE"])
            numChannels = int(dataLoad[0].header["NCHAN"])
        
    frequencies = np.fft.fftfreq(numChannels, 1/sampRate)
    return pol0Spectra, pol1Spectra, pol0Error, pol1Error, metadata, frequencies

def gain(onSpec, offSpec, deltaT):
    gain = []
    for i in range(len(onSpec)):
        if onSpec[i] == offSpec[i]:
            gain.append(0)
        else:
            gain.append(deltaT/(onSpec[i]-offSpec[i]))
    
    return gain

def fourierFilter(data, freqMin, freqMax):
    transformedData = np.fft.fft(data)
    for i in range(len(transformedData)):
        if i < freqMin:
            transformedData[i] = 0
        elif i > freqMax and i < (len(transformedData) - freqMax):
            transformedData[i] = 0
        elif i > (len(transformedData) - freqMin):
            transformedData[i] = 0
    filteredData = np.fft.ifft(transformedData)
    return filteredData

