__author__ = 'Horea Christian'
from psychopy import visual, data, event, core

def em_faces(win, expInfo, fixation, fixationtime, trialClock, local_dir, ratingfilename=None):
    from numpy.random import permutation
    from lefunctions import save_csv
    import numpy as np
    import pandas as pd
    
    
    #EXPERIMENT VARIABLES
    
    #Files:
    em_faces_stimuli_file = local_dir + 'metadata/em_faces_stim.csv'
    img_path = local_dir + 'img/'
    
    #Times (in [s]):
    att_time = 5
    process_paddingtime = 1
    
    #END EXPERIMENT VARIABLES
    
    wmfilename = local_dir + 'results/' + expInfo['Identifier'] + '.csv'
    wmwriter,wmfile = save_csv(wmfilename, ['emotion','intensity','scrambling','gender','top face','left face','right face','correct answer','keypress','RT','session'])
    
    #CREATE STIMULUS LIST
    em_faces_stimuli = pd.DataFrame
    em_faces_stimuli = em_faces_stimuli.from_csv(em_faces_stimuli_file, index_col=False)
    em_faces_stimuli = em_faces_stimuli.reindex(np.random.permutation(em_faces_stimuli.index))
    em_faces_stimuli = em_faces_stimuli.set_index('block')
    blocks = np.array(list(set(em_faces_stimuli.index))) # non-randomized list of blocks
    #~ blocks = np.random.permutation(np.array(list(set(em_faces_stimuli.index)))) # sets can't be turned directly into arrays, so we do this via a list
    em_faces_stimuli = pd.concat([em_faces_stimuli.ix[i] for i in blocks])
    
    tb_pictures = [{'emotion': x[0],'intensity': x[1],'scrambling': x[2],'gender': x[3],'top face':x[4],'left face':x[5],'right face':x[6],'correct answer': x[7]} for x in np.array(em_faces_stimuli)]
    #END CREATE STIMULUS LIST
    
    #stimuli:
    message3 = visual.TextStim(win, pos=[0,2],color=[1,1,1],text='Waehlen Sie bei jeder erneuten Bildanzeige die Seite (links/rechts) auf der in der Unteren Zeile die Emotion des oberen\
                                Bildes abgeblidet wird. \n\nFuer Anzeigen mit in Kacheln unterteilten und vermischten Bildern waehlen Sie bitte die Seite auf der das obere Bild wiederholt wird. \
                                \n\nBenutzen Sie fuer die Auswahl die links/rechts Pfeiltasten. \
                                \n\nFortfahren mit beliebiger Taste.',wrapWidth=20.0)
    image_l = visual.ImageStim(win, pos=[-16,-8], size=[12,16], interpolate=False)
    image_r = visual.ImageStim(win, pos=[16,-8], size=[12,16], interpolate=False)
    image_t = visual.ImageStim(win, pos=[0,8], size=[12,16], interpolate=True)
    core.wait(process_paddingtime,process_paddingtime)
    
    # new loops
    attwm_loop = data.TrialHandler(tb_pictures, 1, method="sequential")
    
    #INTERACTING W/ PARTICIPANT
    message3.draw()
    win.flip()
    event.waitKeys()#pause until there's a keypress
    
    for ix, attwm_loop_val in enumerate(attwm_loop):
        image_t.setImage(img_path + attwm_loop_val['top face']+'.jpg')
        image_l.setImage(img_path + attwm_loop_val['left face']+'.jpg')
        image_r.setImage(img_path + attwm_loop_val['right face']+'.jpg')
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
            keypress = np.array([['none',2]])
        elif keypress != []:
            keypress = np.array(keypress)
        keypress = keypress[np.in1d(keypress[:, 0], ['left', 'right', 'none'])]#remove any other keys except left, right, none
        if len(keypress) == 0:
            keypress = np.array(['none',2])
        wmwriter.writerow([attwm_loop_val['emotion'],attwm_loop_val['intensity'],attwm_loop_val['scrambling'],attwm_loop_val['gender'],
        attwm_loop_val['top face'],attwm_loop_val['left face'],attwm_loop_val['right face'],attwm_loop_val['correct answer'],
        keypress[0][0], keypress[0][1], ix])
    wmfile.close()
    #END INTERACTING W/ PARTICIPANT
