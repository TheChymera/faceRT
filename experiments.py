# -*- coding: utf-8 -*-
__author__ = 'Horea Christian'
from psychopy import visual, data, event, core

def em_faces(win, expInfo, fixation, fixationtime, trialClock, local_dir, ratingfilename=None):
	from numpy.random import permutation, choice, sample
	from lefunctions import save_csv
	import numpy as np
	import pandas as pd
	
	
	#EXPERIMENT VARIABLES
	
	#Files:
	em_faces_stimuli_file = local_dir + 'metadata/em_faces_stim.csv'
	img_path = local_dir + 'img/'
	
	#Demo Stimuli
	demo_emo = [1,3]
	demo_scrambled = [2,4,6,8]
	
	#Times (in [s]):
	att_time = 5
	process_paddingtime = 1
	
	#Runtime Parameters
	just_preprocessing = False
	
	#END EXPERIMENT VARIABLES
	
	wmfilename = local_dir + 'results/' + expInfo['Identifier'] + '.csv'
	wmwriter,wmfile = save_csv(wmfilename, ['emotion','intensity','scrambling','gender','top face','left face','right face','correct answer','keypress','RT','session'])
	
	#CREATE STIMULUS LIST
	em_faces_stimuli = pd.DataFrame
	em_faces_stimuli = em_faces_stimuli.from_csv(em_faces_stimuli_file, index_col=False)
	em_faces_stimuli = em_faces_stimuli.reindex(np.random.permutation(em_faces_stimuli.index))
	em_faces_stimuli = em_faces_stimuli.set_index('block')
	blocks = np.array(list(set(em_faces_stimuli.index))) # non-randomized list of blocks
	em_faces_stimuli = pd.concat([em_faces_stimuli.ix[i] for i in blocks]).reset_index()
	random_trials_for_demo = [choice(np.arange(len(em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_emo))]))),choice(np.arange(len(em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_scrambled))])))]
	demo_faces = pd.concat([em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_emo))].reset_index().ix[[random_trials_for_demo[0]]], em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_scrambled))].reset_index().ix[[random_trials_for_demo[1]]]]).reset_index()
	#~print demo_faces, demo_emo, demo_scrambled, random_trials_for_demo, em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_emo))], em_faces_stimuli[(em_faces_stimuli['block'] == choice(demo_scrambled))]
	   
	harari_stimuli = [{'emotion': x[1],'intensity': x[2],'scrambling': x[3],'gender': x[4],'top face':x[5],'left face':x[6],'right face':x[7],'correct answer': x[8]} for x in np.array(em_faces_stimuli)]
	#END CREATE STIMULUS LIST
	
	#stimuli:
	circle_top = visual.Circle(win, pos=[0,8], radius=7, edges=500, lineColor=(1,0,0), interpolate=True)
	circle_down = visual.Circle(win, radius=7, edges=500, lineColor=(1,0,0), interpolate=True)
	message3 = visual.TextStim(win, pos=[0,2],color=[1,1,1],text=u'Im Folgenden werden Ihnen unterschiedliche Gesichter mit verschiedenen Emotionen gezeigt. Bitte ordnen Sie immer das\
								obenstehende Gesicht entsprechend einem der untenstehenden Gesichter zu. \n\nSie haben jeweils zwei Gesichter zur Auswahl. Bestätigen Sie das passende Gesicht\
								jeweils mit der linken oder der rechten Pfeiltaste. Anschließend werden Ihnen in Kacheln unterteilte und unkenntlich gemachte Gesichter gezeigt, von denen Sie die\ Identischen Bilder ebenso zuordnen sollen.\
								\n\nFortfahren zu den Beispielen mit beliebiger Taste.',wrapWidth=20.0)
	message_demo1 = visual.TextStim(win, pos=[0,-15],color=[1,1,1],text=u'Fortfahren mit der entsprechenden Pfeiltaste.',wrapWidth=20.0)
	message_demo2 = visual.TextStim(win, pos=[0,-15],color=[1,1,1],text=u'Fortfahren und Beenden der Demonstration mit der entsprechenden Pfeiltaste.\
								\nDas Experiment fängt gleich im Anschluss an.',wrapWidth=20.0)
	image_l = visual.ImageStim(win, pos=[-16,-8], size=[12,16], interpolate=False)
	image_r = visual.ImageStim(win, pos=[16,-8], size=[12,16], interpolate=False)
	image_t = visual.ImageStim(win, pos=[0,8], size=[12,16], interpolate=True)
	core.wait(process_paddingtime,process_paddingtime)
	
	# new loops
	harari_loop = data.TrialHandler(harari_stimuli, 1, method="sequential")
	
	if just_preprocessing:
		raise NameError('HiThere')
	
	#INTERACTING W/ PARTICIPANT
	message3.draw()
	win.flip()
	event.waitKeys()#pause until there's a keypress
	image_t.setImage(img_path + demo_faces.ix[0]['top face']+'.jpg')
	image_l.setImage(img_path + demo_faces.ix[0]['left face']+'.jpg')
	image_r.setImage(img_path + demo_faces.ix[0]['right face']+'.jpg')
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
	
	print demo_faces.ix[1]['top face']
	
	image_t.setImage(img_path + demo_faces.ix[1]['top face']+'.jpg')
	image_l.setImage(img_path + demo_faces.ix[1]['left face']+'.jpg')
	image_r.setImage(img_path + demo_faces.ix[1]['right face']+'.jpg')
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
	
	for ix, harari_stimuli_val in enumerate(harari_stimuli):
		image_t.setImage(img_path + harari_stimuli_val['top face']+'.jpg')
		image_l.setImage(img_path + harari_stimuli_val['left face']+'.jpg')
		image_r.setImage(img_path + harari_stimuli_val['right face']+'.jpg')
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
		wmwriter.writerow([harari_stimuli_val['emotion'],harari_stimuli_val['intensity'],harari_stimuli_val['scrambling'],harari_stimuli_val['gender'],
		harari_stimuli_val['top face'],harari_stimuli_val['left face'],harari_stimuli_val['right face'],harari_stimuli_val['correct answer'],
		keypress[0][0], keypress[0][1], ix])
	wmfile.close()
	#END INTERACTING W/ PARTICIPANT
