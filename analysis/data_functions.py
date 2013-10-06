#!/usr/bin/env python
__author__ = 'Horea Christian'

def get_config_file():
	from os import listdir, path
	import ConfigParser
	#GET CONFIG FILE
	cfg_file = filter(lambda x: x.endswith('.cfg'), listdir(path.dirname(path.realpath(__file__))))
	if len(cfg_file) > 1:
	    raise InputError('There are multiple *.cfg files in your experiment\'s rot directory (commonly .../faceRT/experiment) - Please delete all but one (whichever you prefer). The script will not run until then.')
	config = ConfigParser.ConfigParser()
	config.read(cfg_file)
	return config
	#END GET CONFIG FILE


def get_and_filter_results(experiment=False, source=False, prepixelation=False, remove_incorrect=True):
	import pandas as pd
	from os import listdir, path
	
	config = get_config_file()
	
	#IMPORT VARIABLES
	if prepixelation:
		pass
	else: prepixelation = config.getint('Data', 'prepixelation')
	if experiment:
		pass
	else: experiment = config.get('Data', 'experiment')
	if source:
		pass
	else: source = config.get('Source', 'source')
	data_path = config.get('Addresses', source)
	ignore_filename = config.get('Data', 'ignore_filename')
	#END IMPORT VARIABLES
	
	if source == 'live':
		results_dir = path.dirname(path.dirname(path.realpath(__file__))) + data_path + prepixelation + '/'
	else:
		results_dir = data_path + experiment + '/px' + str(prepixelation) + '/' 
	results_dir = path.expanduser(results_dir)
	
	print('Loading data from '+results_dir)
	
	
	files = [lefile for lefile in listdir(results_dir) if lefile.endswith('.csv') and not lefile.endswith(ignore_filename+'.csv')]
	data_all = pd.DataFrame([]) # empty container frame for concatenating input from multiple files
	for lefile in files:
		data_lefile = pd.DataFrame.from_csv(results_dir+lefile)
		data_lefile['ID'] = path.splitext(lefile)[0]
		data_lefile = data_lefile[data_lefile['RT'] >=0] # remove entries with instant RTs here
		if remove_incorrect:
			data_lefile = data_lefile[data_lefile['correct answer'] == data_lefile['keypress']] # remove entries with incorrect answers here
		data_all = pd.concat([data_all, data_lefile], ignore_index=True)
	return data_all
	
