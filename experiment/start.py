#!/usr/bin/env python
 # -*- coding: utf-8 -*-
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
__author__ = 'Horea Christian'
from psychopy import core, visual, gui, monitors
from os import path, listdir
from experiments import em_faces
import time
import ConfigParser

#General variables:
local_dir = path.dirname(path.realpath(__file__)) + '/' # navigates to the folder containing the "analysis" folder

#GET CONFIG FILE
cfg_file = filter(lambda x: x.endswith('.cfg'), listdir(local_dir))
if len(cfg_file) > 1:
    raise InputError('There are multiple *.cfg files in your experiment\'s rot directory (commonly .../faceRT/experiment) - Please delete all but one (whichever you prefer). The script will not run until then.')
config = ConfigParser.ConfigParser()
config.read(cfg_file)
#END GET CONFIG FILE

#IMPORT VARIABLES
fixationtime = config.getint('Times', 'fixationtime')
end_pause = config.getint('Times', 'end_pause')
monitor_width = config.getint('Monitor', 'width')
monitor_distance = config.getint('Monitor', 'distance')
monitor_resolution = [config.getint('Monitor', 'x_resolution'), config.getint('Monitor', 'y_resolution')]
#END IMPORT VARIABLES


#Monitor specs:
mymon = monitors.Monitor('testMonitor', width=monitor_width, distance=monitor_distance) # psychopy actually wants half the width
resolution = monitor_resolution

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

#call experiment:
wait_message.draw()
win.flip()
em_faces(win, expInfo, fixation, fixationtime, trialClock, local_dir)
fin_message.draw()
win.flip()
time.sleep(end_pause)
win.close()
