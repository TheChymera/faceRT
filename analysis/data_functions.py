__author__ = 'Horea Christian'

def get_and_filter_results(experiment=False, source=False, prepixelation=False, remove_incorrect=True):
	import pandas as pd
	from os import path
	import sys
	from chr_helpers import get_config_file

	config = get_config_file(localpath=path.dirname(path.realpath(__file__))+'/')
	
	#IMPORT VARIABLES
	if not prepixelation:
		prepixelation = config.getint('Data', 'prepixelation')
	if not experiment:
		experiment = config.get('Data', 'experiment')
	if not source:
		source = config.get('Source', 'source')
	data_path = config.get('Addresses', source)
	ignore_filename = config.get('Data', 'ignore_filename')
	#END IMPORT VARIABLES
	
	if source == 'server':
		from HTMLParser import HTMLParser
		import urllib
		class ChrParser(HTMLParser):
			def handle_starttag(self, tag, attrs):
				if tag =='a':
					for key, value in attrs:
						if key == 'href' and value.endswith('.csv'):
							pre_fileslist.append(value)
		results_dir = data_path+experiment+'/px'+str(prepixelation)+'/'
		print results_dir
		data_url = urllib.urlopen(results_dir).read()
		parser = ChrParser()
		pre_fileslist = []
		parser.feed(data_url) # pre_fileslist gets populated here
	elif source == 'live':
		from os import listdir
		results_dir = path.dirname(path.dirname(path.realpath(__file__))) + data_path + str(prepixelation) + '/'
		results_dir = path.expanduser(results_dir)
		pre_fileslist = listdir(results_dir)
	elif source == 'local':
		from os import listdir
		results_dir = data_path + experiment + '/px' + str(prepixelation) + '/'
		results_dir = path.expanduser(results_dir)
		pre_fileslist = listdir(results_dir)
		
	print('Loading data from '+results_dir)
		
	if pre_fileslist == []:
		raise InputError('For some reason the list of results files could not be populated.')
	files = [lefile for lefile in pre_fileslist if lefile.endswith('.csv') and not lefile.endswith(ignore_filename+'.csv')]
	data_all = pd.DataFrame([]) # empty container frame for concatenating input from multiple files
	for lefile in files:
		data_lefile = pd.DataFrame.from_csv(results_dir+lefile)
		data_lefile['ID'] = path.splitext(lefile)[0]
		data_lefile = data_lefile[data_lefile['RT'] >=0] # remove entries with instant RTs here
		if remove_incorrect:
			data_lefile = data_lefile[data_lefile['correct answer'] == data_lefile['keypress']] # remove entries with incorrect answers here
		data_all = pd.concat([data_all, data_lefile], ignore_index=True)
	return data_all
	
