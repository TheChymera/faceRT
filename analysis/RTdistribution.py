#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from os import listdir
from data_functions import get_config_file, get_and_filter_results

def main(experiment=False, source=False, prepixelation=False, num_bins=False, keep_scrambling=False):
    data_all = get_and_filter_results(experiment, source, prepixelation)
    config = get_config_file()
    
    #IMPORT VARIABLES
    if num_bins:
	pass
    else: num_bins = config.getint('RTdistribution', 'num_bins')
    if keep_scrambling:
	pass
    else: keep_scrambling = [int(i) for i in config.get('RTdistribution', 'keep_scrambling').split(',')]
    #END IMPORT VARIABLES
    
    data_filtered = pd.DataFrame()
    for scrambling in keep_scrambling:
	data_scrambling = data_all[(data_all['scrambling'] == scrambling)]
	data_filtered = pd.concat([data_filtered, data_scrambling], ignore_index=True)
    
    fig = figure(figsize=(data_filtered['RT'].max()*4, 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
    # the histogram of the data
    n, bins, patches = plt.hist(data_filtered['RT'], num_bins, normed=True, facecolor='green', alpha=0.5)
    # add a 'best fit' line
    mu = data_filtered['RT'].mean()
    sigma = np.std(data_filtered['RT'])
    y = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, y, 'm')
    plt.xlabel('RT [s]')
    plt.ylabel('Probability')
    keep_scrambling = [str(i) for i in keep_scrambling]
    plt.title('Histogram of RTs for scrambling = '+ ', '.join(keep_scrambling)+ r'		$\mu\approx$'+str(np.around(mu, decimals=2))+r' s, $\sigma\approx$'+str(np.around(sigma, decimals=2))+' s')
    plt.subplots_adjust(left=0.15)# Tweak spacing to prevent clipping of ylabel

if __name__ == '__main__':
	main()
	show()
