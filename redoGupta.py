""" redoGupta.py -- A file to calculate ages of the whole galaxy, 
like Gupta, with Gupta's galaxies

Benjamin Rose
brose3@nd.edu
benjamin.rose@me.com
University of Notre Dame
2017-03-23
Python 3.5
"""
import logging

import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

import calculateAge

module_logger = logging.getLogger("localEnvironments.redoGupta")

def getPhotometry():
    #this gives annoying warnings, so I moved it here
    from astroquery.sdss import SDSS

    #Get global photometry of objects observed by Gupta
    data = pd.read_csv('data/Gupta11_table2.txt', delimiter='\t', 
                       skiprows=[0,1,2], skipinitialspace=True, 
                       na_values='...', index_col=False)

    #Make a new data table
    HostData = data[['SN ID', 'IAU']]

    for i in range(len(data)):
        Galpos = SkyCoord(ra=data.loc[i, 'RA']*u.deg, 
                         dec=data.loc[i, 'Dec']*u.deg)
        # Galpos = SkyCoord(ra=data.loc[0, 'RA']*u.deg, 
                         # dec=data.loc[0, 'Dec']*u.deg)
        print(data.loc[i, 'SN ID'])
        radius=5*u.arcsec
        results = SDSS.query_region(Galpos, spectro=True, radius=radius, 
                                    specobj_fields=['z'], 
                                    photoobj_fields=['objid', 'ra', 'dec', 
                                                     'PetroRad_r', 'u', 'g', 
                                                     'r', 'i', 'z', 'err_u', 
                                                     'err_g', 'err_r', 'err_i',
                                                     'err_z']
                                     )
        if results is None:
            print('host of SN{} not found with a spectrum'.format(data.loc[i, "SN ID"]))
            #remove spec option
            results = SDSS.query_region(Galpos, radius=3*u.arcsec, 
                                    photoobj_fields=['objid', 'ra', 'dec', 
                                                     'PetroRad_r', 'u', 'g', 
                                                     'r', 'i', 'z', 'err_u', 
                                                     'err_g', 'err_r', 'err_i',
                                                     'err_z']
                                     )
            if results is None:
                print('host of SN{} not found'.format(data.loc[i, "SN ID"]))
                continue
        # import pdb; pdb.set_trace()
        if len(results) == 1:
            # check redshift
            # just save the one result to HostData
            #print the whole Table, no matter how many characters wide
            results.pprint(max_width=-1)
        if len(results) > 1:
            firstID = results[0]['objid']
            isSame = True
            for j in results:
                if firstID != j['objid']:
                    isSame = False
            if isSame:
                print(results[0])#.table.pprint(max_width=-1)
            else:
                print('length:', len(results))
                results.pprint(max_width=-1)


#Run `calculateAge.py` running 15 objects (~5 days on CRC) per job array 
#Gupta has ~210 objects so a complete job array needs 14 objects

def redoGupta(jobID, debug=False):
    """This runs through each broken-up tsv of the global photometry and calling
     calculateAge to save global age calculations.
    
    Parameters
    ----------
    jobID : int
        This is the ID of the global photometry tsv to be used. Should come from
        the crc job-array ID.

    debug : bool
        Flag to have MCMC run incredibly short and in no way accurately. Also 
        does not save resulting chain. Should take around ~12 mins to get a 
        value of one SN.

    Raises
    ------
    
    Notes
    -----
    
    Examples
    --------
    
    """
    logger = logging.getLogger("localEnvironments.redoGupta.redoGupta")

    # Import data file
    logger.info('importing GlobalPhotometry-Gupta-{}.tsv'.format(jobID))
    data = pd.read_csv('data/GlobalPhotometry-Split/GlobalPhotometry-Gupta-{}.tsv'.format(jobID), 
                       delimiter='\t', skiprows=[0,1,2,4],
                       skipinitialspace=True, na_values='...', index_col=False)

    # Iterate over each SN in data file
    i = 0
    #iterate over a zip of SNID, photometry (zipped together), photometry 
    #uncertainty (zipped together), and redshift
    #note http://stackoverflow.com/questions/10729210/iterating-row-by-row-through-a-pandas-dataframe 
    #and http://stackoverflow.com/questions/7837722/what-is-the-most-efficient-way-to-loop-through-dataframes-with-pandas/34311080#34311080
    for sn, photometry, uncertainty, redshift in zip(
                data['SNID'], 
                zip(data['u'], data['g'], data['r'], data['i'], data['g']),
                zip(data['err_u'], data['err_g'], data['err_r'], data['err_i'],
                    data['err_g']),
                data['redshift']
            ):

        # calculate age
        #does this save the data tagged as global?
        logger.info('getting age for SN' + str(sn))
        age = calculateAge.calculateAge(redshift, photometry, uncertainty, 
                                        SNID=sn, debug=debug)
        logger.info("redoGupta's age for SN{}: ".format(sn) + str(age))
        print("redoGupta's age for SN{}: ".format(sn), age)
        

if __name__ == '__main__':
    # getPhotometry()
    redoGupta(1)