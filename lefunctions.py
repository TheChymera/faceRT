from __future__ import division
__author__ = 'Horea Christian'
import numpy as np

def open_csv(filename):
	import csv
	contents = []
	lefile = open(filename + '.csv', 'r')
	readfile = csv.reader(lefile, delimiter =',')
	for row in readfile:
		contents.append(row)
	lefile.close()
	return contents

def save_csv(filename, firstline=['this line caused by save_csv in lefunctions']):
    from os import path, makedirs
    from shutil import move
    from datetime import date, datetime
    import csv
    jzt=datetime.now()
    time = str(date.today())+'_'+str(jzt.hour)+str(jzt.minute)+str(jzt.second)
    if path.isfile(filename):
        if path.isdir(path.dirname(filename)+'/.backup'):
            pass
        else: makedirs(path.dirname(filename)+'/.backup')        
        newname = path.dirname(filename)+'/.backup/'+path.splitext(path.basename(filename))[0]+'_'+time+path.splitext(path.basename(filename))[1]
        move(filename, newname)
        print 'moved pre-existing data file '+ filename +' to backup location ('+newname+')'
    else: pass
    datafile = open(filename, 'a')
    datawriter = csv.writer(datafile, delimiter=',')
    #print first line
    datawriter.writerow(firstline)
    return datawriter, datafile	
