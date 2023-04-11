import numpy as np
import ugradio as ug
import pickle
import emcee

def readData(filenames, numFiles, freqMin, freqMax):
    '''Returns data extracted from files from the interferometer.

    Parameters
    ----------
    filenames: string, filepath to the data files, where each file is differentiated by a number
    numFiles: int, number of files
    freqMin: int, index of the minimum frequency to keep
    freqMan: int, index of the maximum frequency to keep

    Returns
    ---------
    data: list(list(complex)), list of cross correlations, in power units
    times: list(double), list of times corresponding of axis 0 of data, in unix time
    spectralFrequencies: list(double), list of spectral frquencies corresponding to axis 1 of data, in Hz
    accCnt: list(int), list of accumulation times corresponding to acis 0 of data
    '''
    data, times, accCnt = [],[],[]
    usData, usTimes, usAccCnt = [],[],[]
    for i in range(1,numFiles):
        with open(filenames.format(i), "rb") as file:
            tempData = pickle.load(file)
            usData.append(tempData["corr01"][freqMin:freqMax])
            usTimes.append(tempData["time"])
            usAccCnt.append(tempData["acc_cnt"])
        
    
    indecies = np.argsort(usAccCnt)
    for i in indecies:
        data.append(usData[i])
        times.append(usTimes[i])
        accCnt.append(usAccCnt[i])
    
    avgData = np.mean(data, axis = 0)
    for i in range(len(data)):
        data[i] = data[i] - avgData
    
    spectralFrequencies = np.fft.fftfreq(1024, 1/500e6)[freqMin:freqMax] + 10.29e9

    return data, times, spectralFrequencies, accCnt

def getFringeFrequencies(data, times, numChunks):
    """Returns the fringe frequency vs time for a single frequency channel data stream.

    Parameters
    ---------
    data: list(complex), power over time for a single frequency channel
    times: list(double), times, in unix time, corresponding to the data points in data
    numChuncks: int, number of blocks to break the data into

    Returns
    ---------
    fringeFrequencies: list(double), list of fringe frequencies, in Hz
    hourAngle: list(double), list of times, in hour angle, corresponding to the fringe frequencies
    error: list(double), list of error corresponding to the fringe frequencies
    """
    numCorrelations = len(data)
    chunkLength = int(numCorrelations/numChunks)
    timeStep = np.mean(np.diff(times))

    fringeFrequencies = []
    fringeTimes = []

    for i in range(numChunks):
        transformedData = np.abs(np.fft.fft(data[i*chunkLength:(i+1)*chunkLength]))
        maxIndex = np.argmax(transformedData[5:])+5
        frequencies = np.fft.fftfreq(len(transformedData), timeStep)
        if maxIndex == 5:
            fringeFrequencies.append(None)
        else:
            fringeFrequencies.append(frequencies[maxIndex])
        fringeTimes.append(np.mean(times[i*chunkLength:(i+1)*chunkLength]))
    
    hourAngle = uTimeToHrAngle(fringeTimes)
    
    error = np.ones(len(fringeFrequencies))*np.diff(frequencies)[0]*2

    return fringeFrequencies, hourAngle, error

def uTimeToHrAngle(times):
    """Converts unix time to hour angle for an observer on Campbell Hall

    Parameters
    ---------
    times: list(double), list of unix times

    Returns
    -------
    hourAngle: list(double), list of hour angles
    """
    jdTimes = ug.timing.julian_date(times)
    lst = ug.timing.lst(jdTimes)
    ra, _ = ug.coord.sunpos(jdTimes[0])
    ra = np.deg2rad(ra)
    hourAngle = lst - ra
    for i in range(len(hourAngle)):
        if hourAngle[i] < -np.pi:
            hourAngle[i] += 2*np.pi
        elif hourAngle[i] > np.pi:
            hourAngle -= 2*np.pi
    
    return hourAngle


def bruteForceFit(x, y, err, model, params, grid = False):
    """Performs a brute force fit for the given model over all the params. Selects the best fit by minimizing the chi squared

    Parameters
    ---------
    x: list(double), independent data to fit
    y: list(double), dependent data to fit
    err: list(double), error corresponding to the y points
    model: function(x, params): model to fit on, model must take parameters
        x: list(double), independent data
        params: list(double), all parameters of the function
    params: list(tuple): list of every parameter to test over

    Returns
    -------
    params (tuple): parameters with the lowest least squares for the model
    """
    sideLength = int(np.sqrt(len(params)))
    chiSqArr = []
    for i in params:
        chiSqArr.append(chiSq(x,y,err,model,i))
    minIndex = np.argmin(chiSqArr)

    chiSqGrid = np.reshape(chiSqArr, (sideLength,sideLength))
    
    if grid == True:
        return params[minIndex], chiSqGrid
    else:
        return params[minIndex]

def mcmcFit(x, y, err, model, params, nwalkers):
    """"Performs an mcmc fit for the given model over all params

    Parameters
    ---------
    x: list(double), independent data to fit
    y: list(double), dependent data to fit
    err: list(double), error corresponding to the y points
    model: function(x, params): model to fit on, model must take parameters
        x: list(double), independent data
        params: list(double), all parameters of the function
    params: list(double): list of initial guesses over each parametes. The walkers are randomly distributed within 10% of this value
    nwalkers: int, number of walkers

    Returns
    -------
    results: list(tuple(double)): list of the results for each param in params. Each entry contains the value and then the error. The error is determined to be 1SD of the walker positions 
    """
    ndim = len(params)
    pos = params*np.ones([nwalkers,ndim]) + params*((np.random.random([nwalkers,ndim])-0.5)/5)
    sampler = emcee.EnsembleSampler(nwalkers, ndim, logProbability, args = (x,y,err,model))
    sampler.run_mcmc(pos, 5000, progress = True)
    flatSamples = sampler.get_chain(discard = 100, thin = 15, flat = True)
    results = []
    for i in range(ndim):
        mcmc = np.percentile(flatSamples[:,i],[2.5,50,97.5])
        q = np.diff(mcmc)
        stdDev = np.mean(q)
        results.append((mcmc[1], stdDev))
    
    logProb = sampler.get_log_prob(discard = 100, thin = 15, flat = True)
    chiSquared = -np.mean(logProb)
    autoCorrTime = sampler.get_autocorr_time()
    results.append(chiSquared)
    results.append(autoCorrTime)
    
    return results
    
def chiSq(x,y,err, model, params):
    predicted = model(x,params)
    error = [((y[i] - predicted[i])**2 / (err[i]**2)) for i in range(len(y))]
    return np.sum(error)

def logProbability(theta, x, y, err, model):
    lnl = -chiSq(x,y,err,model,theta)
    return lnl

def getEnvelope(data, times, num):
    """Gets the envelope from a product of oscillating functions by taking only the local maximums

    Parameters
    ----------
    data: list(double), list of data to get envelope from
    times: list(double), list of times corresponding to the data

    Returns
    --------
    envelopeData: list(double), list of the data points that form the envelope
    envelopeTimes: list(double), list of the times corresponding to envelopeData
    """
    envelopeData = []
    envelopeTimes = []
    for i in range(0,len(data)):
        isMax = True
        for j in range(-num,num):
            if i+j < 0 or i+j > len(data)-1:
                j = 0
            if data[i+j] > data[i]:
                isMax = False
        if isMax == True:
            envelopeData.append(data[i])
            envelopeTimes.append(times[i])
    return envelopeData, envelopeTimes

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

def rollingAverage(data, num):
    avgData = []
    err = []
    for i in range(0,len(data)-1):
        if i-num < 0:
            avgData.append(np.mean(data[i:i+num]))
            err.append(np.std(data[i:i+num])) 
        elif i + num > len(data)-1:
            avgData.append(np.mean(data[i-num:i]))
            err.append(np.std(data[i-num:i]))
        else:
            avgData.append(np.mean(data[i-num:i+num]))
            err.append(np.std(data[i-num:i+num]))
    
    return avgData, err

def readMoonData(filename, freqMin, freqMax):
    '''Returns data extracted from files from the interferometer. Specific to the moon data I collected

    Parameters
    ----------
    filenames: string, filepath to the data files, where each file is differentiated by a number
    freqMin: int, index of the minimum frequency to keep
    freqMan: int, index of the maximum frequency to keep

    Returns
    ---------
    data: list(list(complex)), list of cross correlations, in power units
    times: list(double), list of times corresponding of axis 0 of data, in unix time
    spectralFrequencies: list(double), list of spectral frquencies corresponding to axis 1 of data, in Hz
    accCnt: list(int), list of accumulation times corresponding to acis 0 of data
    '''
    npz = np.load(filename, allow_pickle=True)

    data, times = [],[]

    usData = npz["vis"]
    usTimes = npz["times"]
    
        
    
    indecies = np.argsort(usTimes)
    for i in indecies:
        data.append(usData[i])
        times.append(np.real(usTimes[i]))
    
    avgData = np.mean(data, axis = 0)
    for i in range(len(data)):
        data[i] = data[i] - avgData
    
    spectralFrequencies = np.fft.fftfreq(1024, 1/500e6)[freqMin:freqMax] + 10.29e9 

    return data, times, spectralFrequencies

def getFringeFrequenciesTwo(data, times, numChunks):
    """Returns the fringe frequency vs time for a single frequency channel data stream.

    Parameters
    ---------
    data: list(complex), power over time for a single frequency channel
    times: list(double), times, in unix time, corresponding to the data points in data
    numChuncks: int, number of blocks to break the data into

    Returns
    ---------
    fringeFrequencies: list(double), list of fringe frequencies, in Hz
    hourAngle: list(double), list of times, in hour angle, corresponding to the fringe frequencies
    """
    numCorrelations = len(data)
    chunkLength = int(numCorrelations/numChunks)
    timeStep = np.mean(np.diff(times))

    fringeFrequencies = []
    fringeTimes = []

    for i in range(numChunks):
        transformedData = np.abs(np.fft.fft(data[i*chunkLength:(i+1)*chunkLength]))
        fringeFrequencies.append(np.fft.fftshift(transformedData))
        fringeTimes.append(np.mean(times[i*chunkLength:(i+1)*chunkLength]))
    
    hourAngle = uTimeToHrAngle(fringeTimes)
    

    return fringeFrequencies, hourAngle









