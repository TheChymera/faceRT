#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pandas as pd
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from os import listdir, path
from data_functions import get_and_filter_results
from chr_helpers import get_config_file

def main(experiment=False, source=False, prepixelation='not specified', num_bins=False, keep_scrambling=False, make_tight=True, print_title = True, linewidth=0.5, fontscale=1):
    data_all = get_and_filter_results(experiment, source, prepixelation, remove='no-response')
    localpath = path.dirname(path.realpath(__file__)) + '/'
    config = get_config_file(localpath)
    
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
    
    fig = figure(figsize=(data_filtered['RT'].max()*4, 5),  dpi=300,facecolor='#eeeeee', tight_layout=make_tight)
    ax=fig.add_subplot(1,1,1)
    ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.6, zorder = 0)
    ax.set_axisbelow(True)
    # the histogram of the data
    n, bins, patches = plt.hist(data_filtered['RT'], num_bins, normed=True, facecolor='green', alpha=0.5, linewidth=linewidth)
    # add a 'best fit' line
    mu = data_filtered['RT'].mean()
    sigma = np.std(data_filtered['RT'])
    norm_fit = mlab.normpdf(bins, mu, sigma)
    plt.plot(bins, norm_fit, 'm')
    plt.xlabel('RT [s]')
    plt.ylabel('Probability')
    keep_scrambling = [str(i) for i in keep_scrambling]
    if print_title:
        plt.title('Histogram of RTs for scrambling = '+ ', '.join(keep_scrambling)+ r'		$\mu\approx$'+str(np.around(mu, decimals=2))+r' s, $\sigma\approx$'+str(np.around(sigma, decimals=2))+' s')
    plt.subplots_adjust(left=0.15)# Tweak spacing to prevent clipping of ylabel
    axis.Axis.zoom(ax.yaxis, -0.5) # sets y margins further apart from the content proportional to its length
    ax.set_ylim(bottom=0) # after scaling to disregard padding unerneath zero.
    legend(('Fitted normal distribution', 'RT bins'), loc='upper center', bbox_to_anchor=(0.5, 1.065), ncol=3, fancybox=False, shadow=False, prop=FontProperties(size=str(int(9*fontscale))))
    
    return data_filtered

if __name__ == '__main__':
	main()
	show()
