#!/usr/bin/env python
from __future__ import division
__author__ = 'Horea Christian'
from scipy.stats import sem
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
from pylab import figure, show, errorbar, setp, legend
from matplotlib import axis
from data_functions import get_and_filter_results, categories_of_interest

def main(experiment=False, source=False, prepixelation='not specified', elinewidth=2, ecolor='0.3', make_tight=True):
	data_all = get_and_filter_results(experiment=experiment, source=source, prepixelation=prepixelation, make_CoI=True)
	
	ids = sorted(list(set(data_all['ID'])))
	pos_ids = np.arange(len(ids))
	
	fig = figure(figsize=(pos_ids.max()*4, 5), dpi=300,facecolor='#eeeeee', tight_layout=make_tight)
	ax=fig.add_subplot(1,1,1)
	width = 0.1
	ax.yaxis.grid(True, linestyle='-', which='major', color='#dddddd',alpha=0.6, zorder = 0)
	ax.set_axisbelow(True)
	scrambling_list = set(data_all['scrambling'])
	
	errors_index = range(len(set(data_all['ID'])))
	errors_columns = ['ID', 'correct', 'incorrect']
		
	total_errors_index = range(len(set(data_all['ID']))*(len(scrambling_list)+1)) # number of error entries - per ID: one for each scrambling step, and TWO for 0
	total_errors_columns = ['ID', 'ER', 'scrambling', 'intensity', 'CoI']
	total_errors = pd.DataFrame(index=total_errors_index, columns=total_errors_columns) # empty container frame for concatenating input from multiple files
	
	
	for id_ix, le_id in enumerate(set(data_all['ID'])):
		id_ix = id_ix*(len(scrambling_list)+1) # number of errors per ID: one for each scrambling step, and TWO for 0
		
		data_for_id = data_all[data_all['ID'] == le_id]
		
		strong_em_errors = len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['correct answer'] != data_for_id['keypress']) & (data_for_id['intensity'] == 100)].index)/len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['intensity'] == 100)].index)
		weak_em_errors = len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['correct answer'] != data_for_id['keypress']) & (data_for_id['intensity'] == 40)].index)/len(data_for_id[(data_for_id['scrambling'] == list(scrambling_list)[0]) & (data_for_id['intensity'] == 40)].index)
		
		total_errors.ix[id_ix]['ID'] = le_id
		total_errors.ix[id_ix]['ER'] = strong_em_errors
		total_errors.ix[id_ix]['scrambling'] = list(scrambling_list)[0]
		total_errors.ix[id_ix]['intensity'] = 100
		total_errors.ix[id_ix+1]['ID'] = le_id
		total_errors.ix[id_ix+1]['ER'] = weak_em_errors
		total_errors.ix[id_ix+1]['scrambling'] = list(scrambling_list)[0]
		total_errors.ix[id_ix+1]['intensity'] = 40

		
		for scrambling_id, scrambling in enumerate(list(scrambling_list)[1:]): #all scrambling steps except 0
			errors = len(data_for_id[(data_for_id['scrambling'] == scrambling) & (data_for_id['correct answer'] != data_for_id['keypress'])].index)/len(data_for_id[(data_for_id['scrambling'] == scrambling)].index)
			
			total_errors.ix[id_ix+2+scrambling_id]['ID'] = le_id
			total_errors.ix[id_ix+2+scrambling_id]['ER'] = errors
			total_errors.ix[id_ix+2+scrambling_id]['scrambling'] = scrambling
			total_errors.ix[id_ix+2+scrambling_id]['intensity'] = 100
			
	total_errors = categories_of_interest(total_errors, scrambling_list) #make categories of interest
	total_errors_just_for_plotting = total_errors.copy() 	# please DO NOT USE THE DATA FROM THIS NEW VARIABLE for anything BUT plotting
	total_errors_just_for_plotting.ix[(total_errors_just_for_plotting['ER'] == 0), 'ER'] = 0.002 # this is a hack to make 0-height bins visible when plotting
	
	
	#START DRAWING GRAPHIC ELEMENTS
	for scrambling_id, scrambling in enumerate(set(total_errors_just_for_plotting['scrambling'])):
		if scrambling == 0:
			#below this: per-participant graphs
			plot_em_strong = plt.bar(pos_ids-width, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 100)]['ER'], width ,color='m', alpha=0.7, zorder = 1, linewidth=0)
			plot_em_weak = plt.bar(pos_ids, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 40)]['ER'], width ,color='m', alpha=0.4, zorder = 1, linewidth=0)
			#below this: total graphs
			tot_plot_em_strong = plt.bar(pos_ids[-1]+1-width, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 100)]['ER'].mean(), width ,color='m', alpha=0.7, zorder = 1, linewidth=0)
			tot_err_em_strong = errorbar(pos_ids[-1]+1-(width/2), total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 100)]['ER'].mean(), yerr=sem(total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 100)]['ER']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
			tot_plot_em_weak = plt.bar(pos_ids[-1]+1, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 40)]['ER'].mean(), width ,color='m', alpha=0.4, zorder = 1, linewidth=0)
			tot_err_em_weak = errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 40)]['ER'].mean(), yerr=sem(total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling) & (total_errors_just_for_plotting['intensity'] == 40)]['ER']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
		else:
			#below this: per-participant graphs
			errors_part_n0 = total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling)]['ER']
			plot_sc = plt.bar(pos_ids+width*scrambling_id, total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling)]['ER'], width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1, linewidth=0)
			#below this: total graphs
			errors_total_n0 = total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling)]['ER'].mean()
			plot_sc = plt.bar(pos_ids[-1]+1+width*scrambling_id, errors_total_n0, width ,color='g', alpha=0.2+0.12*scrambling_id, zorder = 1,linewidth=0)
			errorbar(pos_ids[-1]+1+(width/2)+width*scrambling_id, errors_total_n0, yerr=sem(total_errors_just_for_plotting[(total_errors_just_for_plotting['scrambling'] == scrambling)]['ER']), ecolor=ecolor, elinewidth=elinewidth, capsize=0, linestyle='None', zorder = 2)
	
	width_multiplier = 15/np.shape(data_all[(data_all['scrambling'] == scrambling)].groupby('ID')['RT'].mean())[0]
	plt.axvline(pos_ids[-1]+1-width*width_multiplier, color='0.2')
	
	ids=ids+['ALL']
	pos_ids = np.arange(len(ids))
	ax.set_xlim(0, pos_ids[-1]+width*5)
	ax.set_ylim(0, total_errors_just_for_plotting['ER'].max()*1.2)
	ax.set_ylabel(r'$\mathsf{\Sigma_{wrong} / \Sigma_{all}}$', fontsize=13)
	ax.set_xlabel('Participant', fontsize=11)
	ax.set_xticks(pos_ids + width*3)
	ax.set_xticklabels(ids,fontsize=9) # add rotation=30 if labels are too long and need rotating
	for tick in ax.axes.get_xticklines():
		tick.set_visible(False)
	axis.Axis.zoom(ax.xaxis, -0.5)
	scrambling_list = [str(i) for i in scrambling_list if i != 0]
	legend((plot_em_strong,plot_em_weak, plot_sc),('Strong Emotion','Weak Emotion', 'Scrambled '+', '.join(scrambling_list)),loc='upper center', bbox_to_anchor=(0.5, 1.065), ncol=3, fancybox=False, shadow=False,prop= FontProperties(size='9'))
	#END DRAWING GRAPHIC ELEMENTS
	
	total_errors['ER'] = total_errors['ER'].astype(float) # apparently some other scripts (using R linear models) cannot deal with the output unless we do this.
	return total_errors

if __name__ == '__main__':
	main(source='local')
	show()
