#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import ttest_ind, sem
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from data_functions import get_and_filter_results


data_all = get_and_filter_results(remove_incorrect=False)

ids = sorted(list(set(data_all['ID'])))
pos_ids = np.arange(len(ids))

fig = figure(figsize=(pos_ids.max()*4, 5), dpi=80,facecolor='#eeeeee',tight_layout=True)
ax=fig.add_subplot(1,1,1)
width = 0.1
ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.5, zorder = 1)
scrambling_list = set(data_all['scrambling'])

errors_index = range(len(set(data_all['ID'])))
errors_columns = ['ID', 'correct', 'incorrect']
errors = pd.DataFrame(index=errors_index, columns=errors_columns) # empty container frame for concatenating input from multiple files
	
total_errors_index = range(len(set(data_all['ID']))*(len(scrambling_list)+1)) # number of error entries - per ID: one for each scrambling step, and TWO for 0
total_errors_columns = ['ID', 'error rate', 'scrambling', 'intensity']
total_errors = pd.DataFrame(index=total_errors_index, columns=total_errors_columns) # empty container frame for concatenating input from multiple files


for id_ix, le_id in enumerate(set(data_all['ID'])):
	id_ix = id_ix*(len(scrambling_list)+1) # number of errors per ID: one for each scrambling step, and TWO for 0
	
	data_for_id = data_all[data_all['ID'] == le_id]
	
	strong_em_errors = len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['correct answer'] != data_for_id['keypress']) & (data_for_id['intensity'] == 100)].index)/len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['intensity'] == 100)].index)
	weak_em_errors = len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['correct answer'] != data_for_id['keypress']) & (data_for_id['intensity'] == 40)].index)/len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['intensity'] == 40)].index)
	
	total_errors.ix[id_ix]['ID'] = le_id
	total_errors.ix[id_ix]['error rate'] = strong_em_errors
	total_errors.ix[id_ix]['scrambling'] = list(scrambling_list)[0]
	total_errors.ix[id_ix]['intensity'] = 100
	total_errors.ix[id_ix+1]['ID'] = le_id
	total_errors.ix[id_ix+1]['error rate'] = weak_em_errors
	total_errors.ix[id_ix+1]['scrambling'] = list(scrambling_list)[0]
	total_errors.ix[id_ix+1]['intensity'] = 40
	
	for scrambling_id, scrambling in enumerate(list(scrambling_list)[1:]):
		errors = len(data_for_id[(data_for_id['scrambling'] == scrambling) & (data_for_id['correct answer'] != data_for_id['keypress'])].index)/len(data_for_id[(data_for_id['scrambling'] == scrambling)].index)
		
		total_errors.ix[id_ix+2+scrambling_id]['ID'] = le_id
		total_errors.ix[id_ix+2+scrambling_id]['error rate'] = errors
		total_errors.ix[id_ix+2+scrambling_id]['scrambling'] = scrambling
		total_errors.ix[id_ix+2+scrambling_id]['intensity'] = 100


for scrambling_id, scrambling in enumerate(set(total_errors['scrambling'])):
	if scrambling == 0:
		#below this: per-participant graphs
		plot_em_strong = plt.bar(pos_ids-width, total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 100)]['error rate'], width ,color='m', alpha=0.4, zorder = 1)
		plot_em_weak = plt.bar(pos_ids, total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 40)]['error rate'], width ,color='m', alpha=0.7, zorder = 1)
		#below this: total graphs
		plt.bar(pos_ids[-1]+1-width, total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 100)]['error rate'].mean(), width ,color='m', alpha=0.4, zorder = 1)
		errorbar(pos_ids[-1]+1-(width/2), total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 100)]['error rate'].mean(), yerr=sem(total_errors[(total_errors['scrambling'] == scrambling)]['error rate']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
		plt.bar(pos_ids[-1]+1, total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 40)]['error rate'].mean(), width ,color='m', alpha=0.7, zorder = 1)
		errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, total_errors[(total_errors['scrambling'] == scrambling) & (total_errors['intensity'] == 40)]['error rate'].mean(), yerr=sem(total_errors[(total_errors['scrambling'] == scrambling)]['error rate']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)
	else:
		#below this: per-participant graphs
		plot_sc = plt.bar(pos_ids+width*scrambling_id, total_errors[(total_errors['scrambling'] == scrambling)]['error rate'], width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1)
		#below this: total graphs
		plot_sc = plt.bar(pos_ids[-1]+1+width*scrambling_id, total_errors[(total_errors['scrambling'] == scrambling)]['error rate'].mean(), width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1)
		errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, total_errors[(total_errors['scrambling'] == scrambling)]['error rate'].mean(), yerr=sem(total_errors[(total_errors['scrambling'] == scrambling)]['error rate']), ecolor='0.5', elinewidth='3', capsize=0, linestyle='None', zorder = 2)

plt.axvline(pos_ids[-1]+1-width*2.5, color='0.2')

ids=ids+['TOTAL']
pos_ids = np.arange(len(ids))
ax.set_xlim(0, pos_ids[-1]+width*5)
ax.set_ylim(-0.02, total_errors['error rate'].max()*1.2)
ax.set_ylabel(r'$\mathsf{\Sigma_{wrong} / \Sigma_{all}}$', fontsize=13)
ax.set_xlabel('Participant')
ax.set_xticks(pos_ids + width*3)
ax.set_xticklabels(ids,fontsize=9,rotation=30)
for tick in ax.axes.get_xticklines():
	tick.set_visible(False)
axis.Axis.zoom(ax.xaxis, -0.5)
scrambling_list = [str(i) for i in scrambling_list if i != 0]
legend((plot_em_strong,plot_em_weak, plot_sc),('Strong Emotion','Weak Emotion', 'Scrambled '+', '.join(scrambling_list)), 'upper right', shadow=False, frameon=False, prop= FontProperties(size='11'))
show()
