import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

filename = "./lab4data/calib.fits"

with fits.open(filename) as dataLoad:
    print(dataLoad[1].data["auto0_real"].shape)
