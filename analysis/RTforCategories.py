#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import ttest_ind, sem
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from get_and_filter import get_and_filter_results

# Variables
spacing = 1 #for plotting
# END Variables

data_all = get_and_filter_results()

ids = sorted(list(set(data_all['ID'])))
pos_ids = np.arange(len(ids))

fig = figure(figsize=(pos_ids.max()*4, 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.1
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
scrambling_list = set(data_all['scrambling'])
scrambling_list = [str(i) for i in scrambling_list if i != 0]


for scrambling_id, scrambling in enumerate(set(data_all['scrambling'])):
	if scrambling == 0:
		#below this: per-participant graphs
		plot_em_strong = plt.bar(pos_ids-width, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean(), width ,color='m', alpha=0.4, zorder = 1)
		errorbar(pos_ids-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
		plot_em_weak = plt.bar(pos_ids, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean(), width ,color='m', alpha=0.7, zorder = 1)
		errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
		#below this: total graphs
		plt.bar(pos_ids[-1]+spacing+1-width, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), width ,color='m', alpha=0.4, zorder = 1)
		errorbar(pos_ids[-1]+spacing+1-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
		plt.bar(pos_ids[-1]+spacing+1, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), width ,color='m', alpha=0.7, zorder = 1)
		errorbar(pos_ids[-1]+spacing+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
	else:
		#below this: per-participant graphs
		plot_sc = plt.bar(pos_ids+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1)
		errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
		#below this: total graphs
		plot_sc = plt.bar(pos_ids[-1]+spacing+1+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1)
		errorbar(pos_ids[-1]+spacing+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

plt.axvline(pos_ids[-1]+spacing+width*3, color='0.2')

ids=ids+['']+['TOTAL']
pos_ids = np.arange(len(ids))
ax.set_xlim(0, pos_ids.max()+width*6)
ax.set_ylabel(r'$\mathsf{\overline{RT}}$ [s]', fontsize=13)
ax.set_xlabel('Participant')
ax.set_xticks(pos_ids + width*3)
ax.set_xticklabels(ids,fontsize=9,rotation=30)
for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
axis.Axis.zoom(ax.xaxis, -0.5)
legend((plot_em_strong,plot_em_weak, plot_sc),('Strong Emotion','Weak Emotion', 'Scrambled '+', '.join(scrambling_list)), 'upper right', shadow=False, frameon=False, prop= FontProperties(size='11'))
show()
