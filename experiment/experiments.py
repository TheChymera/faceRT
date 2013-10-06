# -*- coding: utf-8 -*-
__author__ = 'Horea Christian'
from psychopy import visual, data, event, core

def em_faces(win, expInfo, fixation, fixationtime, trialClock, u, local_dir):
	from numpy.random import permutation, choice, sample
	from lefunctions import save_csv
	from os import listdir, path
	import numpy as np
	import pandas as pd
	import ConfigParser
	
	#GET CONFIG FILE
	cfg_file = filter(lambda x: x.endswith('.cfg'), listdir(local_dir))
	if len(cfg_file) > 1:
	    raise InputError('There are multiple *.cfg files in your experiment\'s rot directory (commonly .../faceRT/experiment) - Please delete all but one (whichever you prefer). The script will not run until then.')
	config = ConfigParser.ConfigParser()
	config.read(cfg_file)
	#END GET CONFIG FILE
	
	#IMPORT VARIABLES
	block_presentation = config.get('Stimuli', 'block_presentation')
	prepixelation = config.get('Stimuli', 'prepixelation')
	stimulus_list = config.get('Stimuli', 'stimulus_list')
	trial_time = config.get('Times', 'trial_time')
	just_preprocessing = config.getboolean('Runtime', 'just_preprocessing')
	#END IMPORT VARIABLES

	scrambling_subdirectory = 'px' + str(prepixelation)
	img_path = local_dir + 'img/' + scrambling_subdirectory + '/'
	stimlist = local_dir + 'metadata/' + stimulus_list
			
	results_filename = path.dirname(local_dir) + 'results/' + scrambling_subdirectory + '/' + expInfo['Identifier'] + '.csv'
	results_writer,results_file = save_csv(results_filename, ['emotion','intensity','scrambling','gender','top face','left face','right face','correct answer','keypress','RT','session'])
	
	#PREPARE STIMULUS LIST	
	faces_stimuli = pd.DataFrame
	faces_stimuli = faces_stimuli.from_csv(stimlist, index_col=False)
	faces_stimuli = faces_stimuli.reindex(np.random.permutation(faces_stimuli.index)) # randomize stimulus order
	if block_presentation:
		faces_stimuli = faces_stimuli.set_index('block')
		blocks = np.array(np.random.permutation(list(set(faces_stimuli.index)))) # randomized block order
		faces_stimuli = pd.concat([faces_stimuli.ix[i] for i in blocks]).reset_index() # randomizes blocks
	random_trials_for_demo = [choice(np.arange(len(faces_stimuli[(faces_stimuli['emotion intensity'] == 100) & (faces_stimuli['scrambling'] == 0)]))),choice(np.arange(len(faces_stimuli[(faces_stimuli['scrambling'] != 0)])))]
	demo_faces = pd.concat([faces_stimuli[(faces_stimuli['emotion intensity'] == 100) & (faces_stimuli['scrambling'] == 0)].reset_index().ix[[random_trials_for_demo[0]]], faces_stimuli[(faces_stimuli['scrambling'] != 0)].reset_index().ix[[random_trials_for_demo[1]]]]).reset_index()
	
	harari_stimuli = [dict(row) for idx, row in faces_stimuli.iterrows()] # turn dataframe into list of dicts
	#PREPARE STIMULUS LIST
	
	#stimuli:
	circle_top = visual.Circle(win, pos=[0,u/2], radius=u/2*0.95, edges=500, lineColor=(1,0,0), interpolate=True)
	circle_down = visual.Circle(win, radius=u/2*0.95, edges=500, lineColor=(1,0,0), interpolate=True)
	message3 = visual.TextStim(win, pos=[0,u/6],color=[1,1,1],text=u'Im Folgenden werden Ihnen per Bildschirmanzeige jeweils drei Gesichtsbilder präsentiert. Bitte ordnen Sie immer eins der unterstehenden Gesichter der angezeigten Emotion nach dem oberstehenden Gesicht zu. \n\nSelektieren Sie das passende Gesicht jeweils mit der linken oder der rechten Pfeiltaste. \n\nIhnen werden separat auch in Kacheln unterteilte und unkenntlich gemachte Gesichter gezeigt. In diesen Bildschirmanzeigen müssen Sie das mit dem oberen Bild identische untere Bilder ebenso zuordnen. \n\nFortfahren zu den Beispielen mit beliebiger Taste.',wrapWidth=4*u, height=u/10)
	message_demo1 = visual.TextStim(win, pos=[0,-1.4*u],color=[1,1,1],text=u'Fortfahren mit der entsprechenden Pfeiltaste.',wrapWidth=3*u, height=u/10)
	message_demo2 = visual.TextStim(win, pos=[0,-1.4*u],color=[1,1,1],text=u'Fortfahren und Beenden der Demonstration mit der entsprechenden Pfeiltaste. \nDas Experiment fängt gleich im Anschluss an.',wrapWidth=3*u, height=u/10)
	image_l = visual.ImageStim(win, pos=[-u,-u/2], size=[u*3/4,u], interpolate=True)
	image_r = visual.ImageStim(win, pos=[u,-u/2], size=[u*3/4,u], interpolate=True)
	image_t = visual.ImageStim(win, pos=[0,u/2], size=[u*3/4,u], interpolate=True)
	
	# new loops
	harari_loop = data.TrialHandler(harari_stimuli, 1, method='random')
	
	if just_preprocessing:
		raise NameError('Hi there! This is here because you selected just_processinf = True in .../experiments.py')
	
	#INTERACTING W/ PARTICIPANT
	message3.draw()
	win.flip()
	event.waitKeys()#pause until there's a keypress
	image_t.setImage(img_path + demo_faces.ix[0]['top face'])
	image_l.setImage(img_path + demo_faces.ix[0]['left face'])
	image_r.setImage(img_path + demo_faces.ix[0]['right face'])
	if demo_faces.ix[0]['correct answer'] == 'left':
		circle_down.setPos((-u,-u/2))
	elif demo_faces.ix[0]['correct answer'] == 'right':
		circle_down.setPos((u,-u/2))
	else:
		raise NameError('!!!ERROR: \"correct answer\" field in the stimulus metadata file has a value which is neither \"left\" nor \"right\"')
	message_demo1.draw(win)
	image_t.draw(win)
	image_l.draw(win)
	image_r.draw(win)
	circle_top.draw(win)
	circle_down.draw(win)
	win.flip()
	event.waitKeys(keyList=[demo_faces.ix[0]['correct answer']])
	
	image_t.setImage(img_path + demo_faces.ix[1]['top face'])
	image_l.setImage(img_path + demo_faces.ix[1]['left face'])
	image_r.setImage(img_path + demo_faces.ix[1]['right face'])
	if demo_faces.ix[1]['correct answer'] == 'left':
		circle_down.setPos((-u,-u/2))
	elif demo_faces.ix[1]['correct answer'] == 'right':
		circle_down.setPos((u,-u/2))
	else:
		raise NameError('!!!ERROR: \"correct answer\" field in the stimulus metadata file has a value which is neither \"left\" nor \"right\"')
	message_demo2.draw(win)
	image_t.draw(win)
	image_l.draw(win)
	image_r.draw(win)
	circle_top.draw(win)
	circle_down.draw(win)
	win.flip()
	event.waitKeys(keyList=[demo_faces.ix[1]['correct answer']])
	
	for ix, harari_stimuli_val in enumerate(harari_loop):
		image_t.setImage(img_path + harari_stimuli_val['top face'])
		image_l.setImage(img_path + harari_stimuli_val['left face'])
		image_r.setImage(img_path + harari_stimuli_val['right face'])
		#Fixation
		fixation.draw(win)
		win.flip()
		core.wait(fixationtime,fixationtime)
		#Targets
		image_t.draw(win)
		image_l.draw(win)
		image_r.draw(win)
		win.flip()
		trialClock.reset() #Put this after the fixation win.flip if you want to count fixation as part of the trial.
		core.wait(trial_time,trial_time)
		if len(event.getKeys(['escape'])): core.quit() # quit via escape
		keypress = event.getKeys(keyList=None,timeStamped=trialClock)
		if keypress == []:
			keypress = np.array([['none',5]])
		elif keypress != []:
			keypress = np.array(keypress)
		keypress = keypress[np.in1d(keypress[:, 0], ['left', 'right', 'none'])]#remove any other keys except left, right, none
		if len(keypress) == 0:
			keypress = np.array(['none',5])
		results_writer.writerow([harari_stimuli_val['emotion'],harari_stimuli_val['emotion intensity'],harari_stimuli_val['scrambling'],harari_stimuli_val['gender'],
		harari_stimuli_val['top face'],harari_stimuli_val['left face'],harari_stimuli_val['right face'],harari_stimuli_val['correct answer'],
		keypress[0][0], keypress[0][1], ix])
	results_file.close()
	#END INTERACTING W/ PARTICIPANT
