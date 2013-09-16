# -*- coding: utf-8 -*-
__author__ = 'Horea Christian'
from psychopy import visual, data, event, core

def em_faces(win, expInfo, fixation, fixationtime, trialClock, local_dir):
	from numpy.random import permutation, choice, sample
	from lefunctions import save_csv
	import numpy as np
	import pandas as pd
	
	
	#EXPERIMENT VARIABLES

	block_presentation = True

	# Stimuli pre-pixelation
	prepixelation = 6 #choose from 0, 2, 4, 6
		
	#Stimulus list:
	auto_generated_stimlist = True
	
	#Times (in [s]):
	att_time = 4
	process_paddingtime = 1
	
	#Runtime Parameters
	just_preprocessing = False # set this to True if you want to not run the visual presentation but rather just compute stimuli 
	
	#END EXPERIMENT VARIABLES
	
	scrambling_subdirectory = 'px' + str(prepixelation)
	img_path = local_dir + 'img/' + scrambling_subdirectory + '/'
	
	
	if auto_generated_stimlist:
		stimlist = local_dir + 'metadata/faceRT_blocksize4.csv'
	else:
		stimlist = local_dir + 'metadata/em_faces_stim.csv' # this is the old hand-mase stimfile !!! will be removed in future versions
			
	wmfilename = local_dir + 'results/' + scrambling_subdirectory + '/' + expInfo['Identifier'] + '.csv'
	wmwriter,wmfile = save_csv(wmfilename, ['emotion','intensity','scrambling','gender','top face','left face','right face','correct answer','keypress','RT','session'])
	
	#CREATE STIMULUS LIST
	
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
	#END CREATE STIMULUS LIST
	
	#stimuli:
	circle_top = visual.Circle(win, pos=[0,8], radius=7.5, edges=500, lineColor=(1,0,0), interpolate=True)
	circle_down = visual.Circle(win, radius=7.5, edges=500, lineColor=(1,0,0), interpolate=True)
	message3 = visual.TextStim(win, pos=[0,2],color=[1,1,1],text=u'Im Folgenden werden Ihnen per Bildschirmanzeige jeweils drei Gesichtsbilder präsentiert. Bitte ordnen Sie immer eins der unterstehenden Gesichter der angezeigten Emotion nach dem oberstehenden Gesicht zu. \n\nSelektieren Sie das passende Gesicht jeweils mit der linken oder der rechten Pfeiltaste. \n\nIhnen werden separat auch in Kacheln unterteilte und unkenntlich gemachte Gesichter gezeigt. In diesen Bildschirmanzeigen müssen Sie das mit dem oberen Bild identische untere Bilder ebenso zuordnen. \n\nFortfahren zu den Beispielen mit beliebiger Taste.',wrapWidth=30.0)
	message_demo1 = visual.TextStim(win, pos=[0,-15],color=[1,1,1],text=u'Fortfahren mit der entsprechenden Pfeiltaste.',wrapWidth=20.0)
	message_demo2 = visual.TextStim(win, pos=[0,-15],color=[1,1,1],text=u'Fortfahren und Beenden der Demonstration mit der entsprechenden Pfeiltaste. \nDas Experiment fängt gleich im Anschluss an.',wrapWidth=20.0)
	image_l = visual.ImageStim(win, pos=[-16,-8], size=[12,16], interpolate=False)
	image_r = visual.ImageStim(win, pos=[16,-8], size=[12,16], interpolate=False)
	image_t = visual.ImageStim(win, pos=[0,8], size=[12,16], interpolate=True)
	core.wait(process_paddingtime,process_paddingtime)
	
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
		circle_down.setPos((-16,-8))
	elif demo_faces.ix[0]['correct answer'] == 'right':
		circle_down.setPos((16,-8))
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
		circle_down.setPos((-16,-8))
	elif demo_faces.ix[1]['correct answer'] == 'right':
		circle_down.setPos((16,-8))
	else:
		raise NameError('!!!ERROR: \"correct answer\" field in the stimulus metadata file has a value which is neither \"left\" nor \"right\"')
	message_demo1.draw(win)
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
		core.wait(att_time,att_time)
		if len(event.getKeys(['escape'])): core.quit() # quit via escape
		keypress = event.getKeys(keyList=None,timeStamped=trialClock)
		if keypress == []:
			keypress = np.array([['none',5]])
		elif keypress != []:
			keypress = np.array(keypress)
		keypress = keypress[np.in1d(keypress[:, 0], ['left', 'right', 'none'])]#remove any other keys except left, right, none
		if len(keypress) == 0:
			keypress = np.array(['none',5])
		wmwriter.writerow([harari_stimuli_val['emotion'],harari_stimuli_val['emotion intensity'],harari_stimuli_val['scrambling'],harari_stimuli_val['gender'],
		harari_stimuli_val['top face'],harari_stimuli_val['left face'],harari_stimuli_val['right face'],harari_stimuli_val['correct answer'],
		keypress[0][0], keypress[0][1], ix])
	wmfile.close()
	#END INTERACTING W/ PARTICIPANT
