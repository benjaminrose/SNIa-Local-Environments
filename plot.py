""" plot.py -- make all of my plots

Benjamin Rose
brose3@nd.edu
benjamin.rose@me.com
University of Notre Dame
2017-04-03
Python 3.6
"""

import numpy as np
import matplotlib.pyplot as plt
from astropy.table import Table
import corner
# import seaborn

import pandas as pd

def plotCorner(SN):
    # data = Table.read(f'resources/SN{SN}_chain-2017-04-13.tsv', 
                      # format='ascii.commented_header', delimiter='\t')
    # data = Table.read(f'resources/SN{SN}_chain.tsv', 
                      # format='ascii.commented_header', delimiter='\t')
    # data = Table.read(f'resources/long-CRC-run/SN{SN}_chain.tsv', 
    #                   format='ascii.commented_header', delimiter='\t')
    # data = Table.read(f'resources/2017-05-11 correct age calcuation/SN{SN}_chain.tsv', 
    #                   format='ascii.commented_header', delimiter='\t')
    data = Table.read(f'resources/global/SN{SN}_chain.tsv', 
                      format='ascii.commented_header', delimiter='\t')

    #clean data -- needed for SN10028 on 2017-04-18
    data = data.to_pandas()
    data.dropna(inplace=True)

    # data['age'] = data['age'] - data['tStart']
    fig = corner.corner(data, show_titles=True, use_math_text=True,
                        quantiles=[0.16, 0.5, 0.84], smooth=0.5, 
                        plot_datapoints=False,
                        labels=["$logZsol$", "$dust_2$", r"$\tau$", 
                                "$t_{start}$", "$t_{trans}$", 'sf slope', 
                                'c', 'Age']
                        )

    # plt.show()
    fig.savefig(f'figures/global_05-11run_SN{SN}.pdf')
    # fig.savefig("figures/SF_Age_triangle.pdf")

if __name__ == '__main__':
    # plotCorner(10028) #Original tests
    plotCorner(18749) #from long run on crc