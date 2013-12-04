#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import ttest_ind, sem
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from data_functions import get_and_filter_results, categories_of_interest
from scipy.stats import ttest_rel, ttest_ind
import pandas.rpy.common as com
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr

def main(experiment=False, source=False, prepixelation='not specified', elinewidth=2, ecolor='0.3', make_tight=True, total='means', make_std=False, make_sem=True):
	data_all = get_and_filter_results(experiment, source, prepixelation, mismeasurement='fix', apply_correct_values=True, make_CoI=True)
	scrambling_list = set(data_all['scrambling'])
	data_all = categories_of_interest(data_all, scrambling_list)
	
	ids = sorted(list(set(data_all['ID'])))
	pos_ids = np.arange(len(ids))
	fig = figure(figsize=(pos_ids.max()*5, 4), dpi=300,facecolor='#eeeeee', tight_layout=make_tight)
	ax=fig.add_subplot(1,1,1)
	ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.6, zorder = 0)
	ax.set_axisbelow(True)
	width = 0.1
	
	for scrambling_id, scrambling in enumerate(set(data_all['scrambling'])):
		if scrambling == 0:
			#below this: per-participant graphs
			plot_em_strong = plt.bar(pos_ids-width, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean(), width ,color='m', alpha=0.7, zorder = 1, linewidth=0)
			plot_em_weak = plt.bar(pos_ids, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean(), width ,color='m', alpha=0.4, zorder = 1, linewidth=0)
			if make_std:
				errorbar(pos_ids-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(np.std), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(np.std), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			if make_sem:
				errorbar(pos_ids-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			#below this: total graphs
			if total == 'all':
				plt.bar(pos_ids[-1]+1-width, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), width ,color='m', alpha=0.7, zorder = 1, linewidth=0)
				plt.bar(pos_ids[-1]+1, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), width ,color='m', alpha=0.4, zorder = 1, linewidth=0)
				if make_std:
					errorbar(pos_ids[-1]+1-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT']), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT']), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				if make_sem:
					errorbar(pos_ids[-1]+1-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			elif total == 'means':
				plt.bar(pos_ids[-1]+1-width, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), width ,color='m', alpha=0.7, zorder = 1, linewidth=0)
				plt.bar(pos_ids[-1]+1, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), width ,color='m', alpha=0.4, zorder = 1, linewidth=0)
				if make_std:
					errorbar(pos_ids[-1]+1-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean()), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean()), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				if make_sem:
					errorbar(pos_ids[-1]+1-(width/2), data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 100)].groupby('ID')['RT'].mean()), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling) & (data_all['intensity'] == 40)].groupby('ID')['RT'].mean()), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)



		else:
			#below this: per-participant graphs
			plot_sc = plt.bar(pos_ids+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1, linewidth=0)
			if make_std:
				errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(np.std), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			if make_sem:
				errorbar(pos_ids+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean(), yerr=data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].aggregate(sem), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			#below this: total graphs
			if total == 'all':
				plot_sc = plt.bar(pos_ids[-1]+1+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1, linewidth=0)
				if make_std:
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				if make_sem:
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)]['RT']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			elif total == 'means':
				plot_sc = plt.bar(pos_ids[-1]+1+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1, linewidth=0)
				if make_std:
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), yerr=np.std(data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean()), ecolor=str(float(ecolor)+0.25), elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
				if make_sem:
					errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, data_all[(data_all['scrambling'] == scrambling)]['RT'].mean(), yerr=sem(data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean()), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)

	
	width_multiplier = 15/np.shape(data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean())[0] #(fine tune) separator positioning  
	plt.axvline(pos_ids[-1]+1-width*width_multiplier, color='0.2') #separator - per-person/total
	scrambling_list = [str(i) for i in scrambling_list if i != 0] #format as string for legend
	
	ids=ids+['ALL']
	pos_ids = np.arange(len(ids))
	ax.set_ylabel(r'$\mathsf{\overline{RT}}$ [s]', fontsize=11)
	ax.set_xlabel('Participant', fontsize=11)
	ax.set_xticks(pos_ids + width*3)
	ax.set_xticklabels(ids,fontsize=9) # add rotation=30 if things get too crowded
	for tick in ax.axes.get_xticklines():
		tick.set_visible(False)
	ax.set_xlim(0, pos_ids[-1]+width*5) # before scaling to add padding in front of zero
	axis.Axis.zoom(ax.xaxis, -0.5) # sets x margins further apart from the content proportional to its length
	axis.Axis.zoom(ax.yaxis, -0.5) # sets y margins further apart from the content proportional to its length
	ax.set_ylim(bottom=0) # after scaling to disregard padding unerneath zero.
	legend((plot_em_strong,plot_em_weak, plot_sc),('Strong Emotion','Weak Emotion', 'Scrambled '+', '.join(scrambling_list)),loc='upper center', bbox_to_anchor=(0.5, 1.065), ncol=3, fancybox=False, shadow=False,prop= FontProperties(size='9'))

	return data_all
	
if __name__ == '__main__':
	main()
	show()
