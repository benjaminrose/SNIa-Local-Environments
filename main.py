""" main.py -- Looking for correlations between HR and local environments/ages

Benjamin Rose
brose3@nd.edu
benjamin.rose@me.com
University of Notre Dame
2017-01-19
Python 3
"""
from sys import argv

import numpy as np
import fsps
import logging

#initiate logger
logger = logging.getLogger("localEnvironments")
logger.setLevel(logging.INFO)
#create handler object to be able to change settings.
try:
    #if a command line argument is given, this is from a job-array on the crc
    #http://wiki.crc.nd.edu/wiki/index.php/Submitting_an_array_Job_to_SGE
    #use log associated with this job array.
    fh = logging.FileHandler("logs/localEnvironments_{}.log".format(argv[1]))
except IndexError:
    fh = logging.FileHandler("logs/localEnvironments.log")
#update logging formating
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add handler to logger object
logger.addHandler(fh)
logger.info('Starting')

"""
# Background

"""

"""
# Goals

"""

"""
# Data Selection

"""

"""
# FSPS Parameters

FSPS has a large number of parameters, many have clear choices, but few need investigation.

## add_igm_absorption

I am going to leave IGM off.

## zcontinuous

We want to use `logzsol` and  let the metallicity of the sample vary a bit (`pmetals`), so we set `zcontinuous = 2`

## cloudy_dust

`True`, dust matters!

## sfh

Looking at Simha 2014, we select the 4 parameter lin-exp + late time linear model. This get around the systematically over estimate of age of that basic tau-model. (`sfh = 5`)

## compute_vega_mags

The default is `False`, but the examples explicitly set it. Verified below and the default is `False` as expected and desired!

## add_neb_emission

How important is this? I think it is very important for hosts with large positive r-i (> 1). Yes it is.

## dust

Does dust type influence the extinction curve, and `dust1`, `dust2`, `dust_tesc` account for attenuation? Note young stars get both `dust1` **&** `dust2`. 
"""
# import fspsParameters 

# print(fspsParameters.test_compute_vega_mags())
# fspsParameters.test_neg_ri_color()
# fspsParameters.test_add_neb_emission()

"""
# Get MCMC running and be able to calculate an age with uncertainties.
"""

import calculateAge
#####
#unit tests
#####
# runFSPS()
# - should return a list with 5 arguments
# sp = fsps.StellarPopulation(zcontinuous=2, logzsol=0, dust1=1.0, dust2=0.5,
        # cloudy_dust=True, sfh=4)
# redshift = 0.084
logzsol = 0.0
dust2 = 0.1
tau = 1
tStart = 1
sfTrans = 10
sfSlope = 1
# results = calculateAge.runFSPS(sp, redshift, logzsol, dust2, tau, tStart, sfTrans, sfSlope)
# print('runFSPS(): ', results)
# currently succeeds! We get a list with 5 parameters

#lnlike() 
# - should return a float
#[logzsol, dust2, tau, tStart, sfTrans, sfSlope, c]`.
c = -20
theta = [logzsol, dust2, tau, tStart, sfTrans, sfSlope, c]
#from SN12781, or 2006er just using the values in the file
# SED = np.array([24.41, 23.92, 23.08, 22.68, 22.01])
# SEDerr = np.array([0.49, 0.10, 0.05, 0.05, 0.10])
# redshift = 0.084
#from SN10028, or ? just using the values in the file
SNID=10028
SED = np.array([21.22, 19.45, 18.64, 18.27, 17.98])
SEDerr = np.array([0.041, 0.004, 0.019, 0.012, 0.004])
redshift = 0.065
#from SN15776 (global) that should be red and dead, but on 2017-05-11 was young and dusty
SNID=15776
SED = np.array([23.14426, 21.00639, 19.41827, 18.82437, 18.46391 ])
SEDerr = np.array([0.8009404, 0.04814964, 0.01899451, 0.01771959, 0.04554904])
redshift = 0.305
# results = calculateAge.lnlike(theta, SED, SEDerr, redshift, sp)
# print('lnlike(): ')
# print(type(results))
# print(results)
# print('where is this X < 0 coming from?')

#calculateSFH()
# sp = fsps.StellarPopulation(zcontinuous=2, logzsol=0, dust1=1.0, dust2=0.5,
        # cloudy_dust=True, sfh=4)
# SED = np.array([24.41, 23.92, 23.08, 22.68, 22.01])
# SEDerr = np.array([0.49, 0.10, 0.05, 0.05, 0.10])
# redshift = 0.084
# results = calculateAge.calculateSFH(SED, SEDerr, redshift, 10028)#, sp=sp)
# print('calculateSFH(): ', results)
## results = calculateAge.calculateAge(redshift, SED, SEDerr, SNID)
# results = calculateAge.calculateAge(redshift, SED, SEDerr, SNID=10028, debug=True)
# print('calculateAge(): ', results)
# Currently Fails!!


#from SN12781, or 2006er just using the values in the file
# SED = np.array([24.41, 23.92, 23.08, 22.68, 22.01])
# SEDerr = np.array([0.49, 0.10, 0.05, 0.05, 0.10])
# redshift = 0.084
# results = calculateAge.calculateAge(redshift, SED, SEDerr)
# print('calcualteAge()')

"""
# Test on global SED's

We want to redo what Gupta did to make sure we can actually do something before we analyze on new data. 
"""
import redoGupta

redoGupta.redoGupta(argv[1], lenJobs=10, debug=True, useGupta=False)
# redoGupta.redoGupta(argv[1])

logger.info('Done')