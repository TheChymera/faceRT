#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from get_and_filter import get_and_filter_results

# Variables
num_bins = 100 # number of bins to divide the times into
# END Variables

data_all = get_and_filter_results()
data_all = data_all[(data_all['scrambling'] == 0) | (data_all['scrambling'] == 6) | (data_all['scrambling'] == 14)]

fig = figure(figsize=(data_all['RT'].max()*4, 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
# the histogram of the data
n, bins, patches = plt.hist(data_all['RT'], num_bins, normed=True, facecolor='green', alpha=0.5)
# add a 'best fit' line
mu = data_all['RT'].mean()
sigma = np.std(data_all['RT'])
y = mlab.normpdf(bins, mu, sigma)
plt.plot(bins, y, 'm')
plt.xlabel('RT [s]')
plt.ylabel('Probability')
plt.title(r'Histogram of RTs: $\mu\approx$'+str(np.around(mu, decimals=2))+r' s, $\sigma\approx$'+str(np.around(sigma, decimals=2))+' s')
plt.subplots_adjust(left=0.15)# Tweak spacing to prevent clipping of ylabel
plt.show()
