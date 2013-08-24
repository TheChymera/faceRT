#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, monitors
from os import path
from experiments import em_faces
import time

#EXPERIMENT VARIABLES
#General:
local_dir = path.dirname(path.realpath(__file__)) + '/'


#Experiments:
call_experiment = True

#Times (in [s]):
fixationtime = 1
end_pause = 5

#Monitor specs:
if call_experiment:
    mymon = monitors.Monitor('testMonitor', width=51, distance=53)
    resolution = [1920, 1080]
#END EXPERIMENT VARIABLES

#INTERACTING W/ PARTICIPANT

    expInfo = {'Identifier':''}
    dlg = gui.DlgFromDict(expInfo, title='Experiment1')
    if dlg.OK == False: core.quit()  # user pressed cancel
#END INTERACTING W/ PARTICIPANT

#windows:
    win = visual.Window(resolution, color=[-0.043,-0.043,-0.043],fullscr=True,allowGUI=False,monitor=mymon, screen=0, units="deg")
    win.setRecordFrameIntervals(False)

#stimuli:
    fixation = visual.Circle(win, radius=0.15, edges=64, lineColor=(1,1,1), fillColor=(1,1,1), interpolate=True)
    fin_message = visual.TextStim(win, pos=[0,2],color=[1,1,1],text=u'Vielen Dank für Ihre Teilnahme - bitte melden Sie sich beim Versuchsleiter.'
                           ,wrapWidth=20.0)
    wait_message = visual.TextStim(win, pos=[0,2],color=[1,1,1],text=u'Bitte warten.', wrapWidth=20.0)
 
#clocks:
    globalClock = core.Clock()
    trialClock = core.Clock()




if call_experiment:
	wait_message.draw()
	win.flip()
	em_faces(win, expInfo, fixation, fixationtime, trialClock, local_dir)
	fin_message.draw()
	win.flip()
	time.sleep(end_pause)
	win.close()
