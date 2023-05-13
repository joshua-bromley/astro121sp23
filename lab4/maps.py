import numpy as np
import ugradio as ug
from astropy.io import fits
import emcee
import scipy.optimize as opt
from tqdm import tqdm

def readData(filenames):
    """
    Reads the data out of fits files. Averages per polarization over every fits file and returns all the data.
    Error is determined by fourier filtering away the lowest 1/4 of the frequencies of the spectra and taking the standard deviation

    Parameters
    -------------
    filenames: list(string) list of filenames to read data from

    Returns
    ------------
    pol0Spectra: list(list(double)) List of spectra from polarization 0
    pol1Spectra: list(list(double)) List of spectra from polarization 1
    pol0Error: list(list(double)) List of errors for spectra from polarization 0
    pol1Error: list(list(double)) List of errors for spectra from polarization 1
    metadata: list((double, double, double)) JD, Galactic Coordinate l, b of the observation
    frequencies: list(double) List of frequencies associated with the frequency channels
    """
    pol0Spectra = []
    pol1Spectra = []
    metadata = []
    pol0Error = []
    pol1Error = []
    sampRate = 0
    numChannels = 0

    
    for filename in filenames:
        try:
            with fits.open(filename) as dataLoad:
                tempPol0Spectra = []
                tempPol1Spectra = []
                for i in range(1,len(dataLoad)):
                    tempPol0Spectra.append(dataLoad[i].data["auto0_real"])
                    tempPol1Spectra.append(dataLoad[i].data["auto1_real"])
                pol0Spectra.append(np.mean(tempPol0Spectra, axis = 0))##Average over the spectra taken
                pol1Spectra.append(np.mean(tempPol1Spectra, axis = 0))
                pol0Error.append(np.ones(len(pol0Spectra[-1]))*np.std(fourierFilter(pol0Spectra[-1],freqMin = 1000)))##Set error by fourier filtering
                pol1Error.append(np.ones(len(pol1Spectra[-1]))*np.std(fourierFilter(pol1Spectra[-1],freqMin = 1000)))
                l = dataLoad[0].header["L"]
                b = dataLoad[0].header["B"]
                time = dataLoad[0].header["JD"]
                metadata.append((time,l,b)) #TODO: Make into a dictionary
                #sampRate = float(dataLoad[0].header["SAMPRATE"])
                #numChannels = int(dataLoad[0].header["NCHAN"])
        except(FileNotFoundError):
            print(filename + " not found")
        
    frequencies = np.linspace(144e6,156e6,8192) + 2*635.25e6 #TODO: Add frequqency offset
    return pol0Spectra, pol1Spectra, pol0Error, pol1Error, metadata, frequencies

def gain(onSpec, offSpec, deltaT):
    """
    Calculates the gain of the telescope

    Parameters
    ----------
    onSpec: list(double) Warmer calibration spectra
    offSpec: list(double) Cooler calibration spectra
    deltaT: double, Change in temperature between the spectra

    Returns
    ---------
    gain: double
    """
    diff = onSpec - offSpec
    gain = deltaT/(np.mean(diff))

    return gain

def fourierFilter(data, freqMin = 0, freqMax = -1):
    """
    Fourier filters the data by fourier transforming, keeping only data within the given frequency range and inverse fourier transforming

    Parameters
    ----------
    data: list(double) Data to filter
    freqMin: int, index of the minimum channel to keep, default = 0
    freqMax: int, index of the maximum channel to keep, default = len(data)/2-1

    Returns
    ---------
    filteredData: list(double), fitlered data
    """
    if freqMax == -1:
        freqMax = int(len(data)/2)-1
    transformedData = np.fft.fft(data)
    for i in range(len(transformedData)):
        if i < freqMin:
            transformedData[i] = 0
        elif i > freqMax and i < (len(transformedData) - freqMax):
            transformedData[i] = 0
        elif i > (len(transformedData) - freqMin):
            transformedData[i] = 0
    filteredData = np.abs(np.fft.ifft(transformedData))
    return filteredData

def polyDetrend(data, frequencies, error):
    median = np.median(data)
    baseline = []
    baselineFreqs = []
    baselineErr = []
    for i in range(len(data)):
        if data[i] <= median:
            baseline.append(data[i])
            baselineFreqs.append(frequencies[i])
            baselineErr.append(error[i])
    params,_ = opt.curve_fit(quadratic, baselineFreqs, baseline)
    detrendedData = data - quadratic(frequencies, *params)
    return detrendedData

def quadratic(x, a,b,c):
    return a*(x-b)**2 + c

def chiSq(x,y,err, model, params):
    predicted = model(x,*params)
    error = [((y[i] - predicted[i])**2 / (err[i]**2)) for i in range(len(y))]
    return np.sum(error)

def logProbability(theta, x, y, err, model):
    lnl = -chiSq(x,y,err,model,theta)
    return lnl

def mcmcFit(x, y, err, model, params, nwalkers, nsteps):
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
    nsteps: int, number of steps

    Returns
    -------
    results: list(tuple(double)): list of the results for each param in params. Each entry contains the value and then the error. The error is determined to be 1SD of the walker positions 
    """
    ndim = len(params)
    pos = params*np.ones([nwalkers,ndim]) + params*((np.random.random([nwalkers,ndim])-0.5)/5)
    sampler = emcee.EnsembleSampler(nwalkers, ndim, logProbability, args = (x,y,err,model))
    sampler.run_mcmc(pos, nsteps, progress = False)
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

def deconvolve(data, freqs, centralF, debug = False):
    mask = np.where(np.abs(freqs - centralF) < 0.3e6, 0, 1)
    minIdx = 0
    maxIdx = 0
    for i in range(1,len(mask)-1):
        if mask[i] == 0 and mask[i-1] == 1:
            minIdx = i
        if mask[i] == 0 and mask[i+1] ==1:
            maxIdx = i
    mask[0:300] = 0
    mask[-2500:] = 0
    dataFT = np.fft.rfft(data*mask)
    modelFT = np.zeros_like(dataFT)
    maskFT = np.fft.rfft(mask)
    model = np.ones(len(data))
    idx = np.argmax(np.abs(dataFT))
    stdDev = np.std(mask*data)
    counter = 0
    while np.std(mask*(data-model)) > 0.001*stdDev and counter < 5000:
        idx = np.argmax(np.abs(dataFT))
        modelFT[idx] += dataFT[idx] / (maskFT[0]/mask.size)
        model = np.fft.irfft(modelFT)
        dataFT = np.fft.rfft((data-model)*mask)
        counter += 1
    
    if debug == True:
        return data, model, mask
    else:
        return (data - model)[minIdx:maxIdx], freqs[minIdx:maxIdx]


def getProminence(data):
    prominence = []
    for i in range(len(data)):
        leftProminence = 1420e6
        rightProminence = 1420e6
        for j in np.flip(range(0,i)):
            if data[j] >= data[i]:
                leftProminence = data[i] - np.min(data[j:i+1])
                break
        for j in range(i+1,len(data)):
            if data[j] >= data[i]:
                rightProminence = data[i] - np.min(data[i:j])
                break
        if leftProminence == 1420e6 and rightProminence == 1420e6:
            prominence.append((data[i] - np.min(data))**2)
        elif leftProminence < rightProminence:
            prominence.append(leftProminence*np.sqrt(data[i] - np.min(data)))
        else:
            prominence.append(rightProminence*np.sqrt(data[i] - np.min(data)))
    return prominence/np.max(prominence)

def freqToVelocity(frequencies, metadata):
    velocities = []
    ra,dec = ga2eq(metadata[1],metadata[2])
    v = ug.doppler.get_projected_velocity(ra,dec,metadata[0]).value
    for i in range(len(frequencies)):

        velocities.append(v + 3e8*(1420.405e6 - frequencies[i])/1420.405e6)
    return velocities

def getVelocity(data, velocity, p0, error):
    params, cov = opt.curve_fit(doubleGaussian, velocity, data, p0 = p0, bounds = [[0,-np.inf,0,0,-np.inf,0],[np.inf,np.inf,np.inf,np.inf,np.inf,np.inf]])
    T1,mu1,sigma1,T2,mu2,sigma2 = params
    err= np.sqrt(np.diag(cov))
    T1Err, mu1Err, sigma1Err, T2Err,mu2Err, sigma2Err = err
    prominence = np.sort(getProminence(doubleGaussian(velocity,*params)))
    chiSquared = chiSq(velocity,data,error,doubleGaussian,params)/(len(data) - 6)
    #if np.abs(T1 - T2) > 20 or np.abs(maxVal - max(T1,T2)) > 0.5*maxVal or np.abs(mu1-mu2) < 2000:
    if chiSquared > 10:
        return [[None,None,None,None,None,None], None]
    if prominence[-2] == 0:
        idx = np.argmax(doubleGaussian(velocity,*params))
        mu = velocity[idx]
        T = doubleGaussian(mu,*params)
        muErr = np.max([mu1Err,mu2Err])
        TErr = np.max([T1Err,T2Err])
        if np.abs(mu1 - mu) < np.abs(mu2 - mu):
            sigma = sigma1
            sigmaErr = sigma1Err
        else:
            sigma = sigma2
            sigmaErr = sigma2Err
        if T > 7 and T < 200 and np.abs(mu) < 50000 and sigma > 750 and sigma < 19000:
            return [[T,mu,sigma, TErr, muErr, sigmaErr], chiSquared]
        else:
            return [[None,None,None,None,None,None], None]
    if T1 < 7 or T1 > 150 or mu1 > 20000 or mu1 < -50000 or sigma1 < 750 or sigma1 > 19000:
        if T2 < 7 or T2 > 150 or mu2 > 20000 or mu2 < -50000 or sigma2 < 750 or sigma2 > 19000:
            return [[None,None,None,None,None,None], None]
        else:
            return [[T2,mu2,sigma2,T2Err, mu2Err, sigma2Err], chiSquared]
    elif T2 < 7 or T2 > 150 or mu2 > 20000 or mu2 < -50000 or sigma2 < 750 or sigma2 > 19000:
        return [[T1,mu1,sigma1, T1Err, mu1Err, sigma1Err], chiSquared]
    else:
        if mu1 > mu2:
            return [[T2,mu2,sigma2,T2Err,mu2Err,sigma2Err],[T1,mu1,sigma1, T1Err, mu1Err, sigma1Err], chiSquared]
        else:
            return [[T1,mu1,sigma1, T1Err, mu1Err, sigma1Err],[T2,mu2,sigma2,T2Err,mu2Err, sigma2Err], chiSquared]



        
        
    
    
    

def doubleGaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1*np.exp(-0.5*((x-mu1)/sigma1)**2)+A2*np.exp(-0.5*((x-mu2)/sigma2)**2)

def gaussian(x, A1, mu1, sigma1):
    return A1*np.exp(-0.5*((x-mu1)/sigma1)**2)

def ga2eq(l,b):
    l = np.deg2rad(l)
    b = np.deg2rad(b)
    lNCP = np.deg2rad(122.93314)
    raNGP = np.deg2rad(192.9)
    decNGP = np.deg2rad(27.13)
    dec = np.arcsin(np.sin(decNGP)*np.sin(b)+np.cos(decNGP)*np.cos(b)*np.cos(lNCP-l))
    ra = np.arcsin(np.cos(b)*np.sin(lNCP-l)/np.cos(dec)) + raNGP
    ra = np.rad2deg(ra)
    dec = np.rad2deg(dec)
    return ra, dec

def interpolate(data, l, b, lmin, lmax, bmin, bmax, dl, db):
    dataGrid = np.full([int((bmax-bmin)/db)+1,int((lmax-lmin)/dl)+1], np.pi)
    for i in range(len(data)):
        x = int((l[i]-lmin)/dl)
        y = int((b[i]-bmin)/db)
        dataGrid[y][x] = data[i]

    interpGrid = np.zeros_like(dataGrid)
    
    for i in tqdm(range(len(dataGrid))):
        for j in range((len(dataGrid[0]))):
            if dataGrid[i][j] != np.pi:
                interpGrid[i][j] = dataGrid[i][j]
            else:
                total = 0
                length = 0
                for di in range(max(0,i-int(10/dl)),min(i+int(10/dl),len(dataGrid))):
                    for dj in range(max(0,j-int(10/db)),min(j+int(10/db),len(dataGrid[i]))):
                        distance = (db*db*((i-di)**2 + (j-dj)**2))
                        if distance == 0:
                            distance = 0.05*db*db
                        if dataGrid[di][dj] != np.pi:
                            total += dataGrid[di][dj]/distance
                            length += 1/distance
                if total == 0:
                    interpGrid[i][j] = 0
                else:
                    interpGrid[i][j] = total/length
    
    return interpGrid


    


