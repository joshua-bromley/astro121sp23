import numpy as np
import ugradio as ug
import time
import threading
import snap_spec

running = True ##Trigger for stopping functions
data = [] ##Temporary list for storing data read from snap_spec
lock = threading.Lock() ##Lock to prevent race conditions

def logData():
    '''
    Reads data from SNAP board and saves it to the data list. Is constantly pinging the SNAP for updates
    '''
    global data
    global running
    acc_cnt = None ##Keep track of the current accumulation
    while running == True: ##Do this loop while running
        jd = ug.timing.julian_date() ##Save the current time
        ##TODO: Change this to get time from SNAP board
        try:
            d = spec.read_data(acc_cnt) ##Read snap data
            acc_cnt = d["acc_cnt"] ##Updata accumulation count
            currentTime = jd*np.ones(len(d["corr01"]))
            lock.acquire() ##Lock the data list
            data.append([d["corr01"],currentTime]) ##Add the data from SNAP to the data list
            ##TODO: Optimize this so I'm not saving a bunch of copies of the same number
            lock.release() ##Release the lock
        except{AssertionError}: ##Catching the error thrown by the SNAP spec if the acc_cnt is out of date
           lock.release() ##Releasing the lock just in case
           print("Data not logged") ##Logging th failure in the termina
           ## acc_cnt = None ##Idk of I should have this reset
        time.sleep(0.001) ##Wait a tiny bit cause I think threading likes it
    return 0

def saveData():
    '''
    Once 20 integrations are acquired, save the data to a file and purge the data list
    '''
    global data
    global running
    counter = 0 ##Counter for naming data files
    while running == True: ##Do this loop while running
        if len(data) >= 20: ##Check if there are at least 20 items in the data list
            lock.acquire() ##Lock the list
            np.savez(filename+str(counter), data) ##Save the data to a file
            counter += 1 
            for i in range(20): ##Empty the list, but maybe I should do data = []
                data.pop(0)
            lock.release() ##Release the lock
        time.sleep(0.001)
    np.savez(filename+str(counter), data) ##When the loop is killed, save all remaining data
    return 0

def pointTelescope():
    '''
    Points the telescope to the target (currently the moon)
    '''
    global running
    while running == True: ##Do this loop while running
        jd = ug.timing.julian_date() ##Get the current time
        ra, dec = ug.coord.moonpos(jd) ##Get the current position of the moon
        ra, dec = ug.coord.precess(ra,dec) ## Precess the equatorial coordinate
        alt, az = ug.coord.get_altaz(ra, dec) ##Conver to Alt-Ax
        ifm.point(alt,az)##Point the telescope
        time.sleep(5)##Do this every 5 seconds
    return 0

spec = snap_spec.snap.UGRadioSnap() ##Initialize the snap_spec object
spec.initialize(mode="corr")
ifm = ug.interf.Interferometer() ##Initialize an iterferometer object

filename = "./joshData/dataBatch" ##Default filename to save data to 

thdLog = threading.Thread(target = logData)##Create a thread for each of the function
thdSave = threading.Thread(target = saveData)
thdPoint = threading.Thread(target = pointTelescope) 

collectTime = 8*3600 ##Lenght of data collection time in seconds

thdLog.start()##Start the threads
thdSave.start()
thdPoint.start()

for i in range(collectTime):##Wait over the whole collection time
    time.sleep(1) ##This is legacy from when I wanted to quickly check if this part of the code is running

running = False ##Tell the functions to stop
print(running) ##Log that I stopped

thdLog.join()##Wait for the functions to stop
thdSave.join()
thdPoint.join()

ifm.stow()##Stow the telescope