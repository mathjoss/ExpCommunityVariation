# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 19:36:04 2023

@author: Mathilde JOSSERAND
"""

# --------------------- #
# ---- Preliminary ---- #
 
import sys
import pandas as pd
import cv2
import numpy as np
import tkinter
import tkinter.ttk
from tkinter import filedialog
import shutil
import os
import math
from psychopy import core, visual, gui, data, event, monitors
import random
import itertools
import collections

path = "C:/Users/Mathilde JOSSERAND/Documents/VanGogh/Experiment/"
path = 'C:/Users/expnoteuser/Documents/Experiment/'
sys.path.append(path)



# ------------------------------------- #
# ---- Ask participant Information ---- #

expInfo = {'Group':'1', 'Participant':'1', 'GroupType':['HT', 'HM']}
expInfo['dateStr'] = data.getDateStr()
dictDlg = gui.DlgFromDict(dictionary=expInfo,
        title='TestExperiment', fixed=['ExpVersion'])
if dictDlg.OK:
    print(expInfo)
else:
    print('User Cancelled')
    core.quit()  # the user hit cancel so exit

part_id = expInfo["Participant"]
group_num = int(expInfo["Group"])
group_type = expInfo["GroupType"]



# --------------------------- #
# ---- Write output file ---- #

# name of the file (participant and date)
fileName = "Group" + str(group_num) + "_Participant" + str(part_id) + '_Date' + data.getDateStr()

# open file, a simple text file with 'comma-separated-values'    
dataFile = open(path + 'Results/'+ fileName + '.csv', 'w')  
dataFile.write('GroupNum, GroupType, TypeTest, PartID, Partner, Round, Shape, KeyPressed, PositionItem, ChosenItem, GoodItem, ACC, Word, ID_CG\n')

# open file, a simple text file with 'comma-separated-values' for saving the results of prosociality scale   
dataFile_ps = open(path + 'Results/PS_file_'+ fileName + '.csv', 'w')  
dataFile_ps.write('ItemNum, Answer\n')

# open file, a simple text file with 'comma-separated-values' for saving the results of taskswitching task   
dataFile_ts = open(path + 'Results/TS_file_'+ fileName + '.csv', 'w')  
dataFile_ts.write('BlockName, StimPos, tasktype, letterstim, numberstim, switch, acc, time\n')


# ----------------------------- #
# ---- Experiment settings ---- #
    
mon = monitors.Monitor('testMonitor') 
mon.setDistance(50) #
mon.setWidth(50)
mon.setGamma(1)
#mon.setSizePix(pyautogui.size())
    

# list keys for unbiased participants
list_unbiased = 'k, s, p, n, a, e, i, u'

# list keys for biased participants
list_biased = 'p, s, n, e, i, u'

# maximum length of words to be written
length_max = 8

# number of rounds (choose between 6 or 9)
tot_nb_rounds = 9

# choose 23 out of the 28 items 
#random.seed(group_num)  
#selec_items = random.sample(range(0, 28), 23)

    
# determine which items corresponds to each shape
shapes = [ [0, "nusa"], 
           [1, "nus"], 
           [2, "kesip"], 
           [3, "esip"],
           [4, "puak"], 
           [5, "nekuki"], 
           [6, "anap"], 
           [7, "aike"]]
    

# -------------------------- #
# ---- Stimuli creation ---- #

# create window and stimuli (now, in full screen)
win = visual.Window(allowGUI=True, color="lightgrey", colorSpace='rgb255',  fullscr=False, size=(1920, 1080), monitor=mon, units="deg")

# create images big and small
count=0
m = [0] * 8
smallm = [0] * 8
for el in range(8):
    namefile = str(el)
    m[count] = visual.ImageStim(win=win, image=path + 'Stimuli_new/' + namefile + ".png", units="pix", size=(400, 400))
    smallm[count] = visual.ImageStim(win=win, image=path + 'Stimuli_new/' + namefile + ".png", units="pix", size=(300, 300))
    count = count+1
 
# current task and block indicator
taskblock = visual.TextStim(win, text="O1", height=1, color="black", pos = [0, -27])

# TEXT
# main text (up)
titletext_roun = visual.TextStim(win, wrapWidth=1500, text="", color="black", height=50, units="pix", pos = [0, 300])
titletext_memo = visual.TextStim(win, wrapWidth=1500, text="Fantasietaal - Onthouden", color="black", height=50, units="pix", pos = [0, 300])
titletext_gues = visual.TextStim(win, wrapWidth=1500, text="Fantasietaal - Raden", color="black", height=50, units="pix", pos = [0, 300])
titletext_prod = visual.TextStim(win, wrapWidth=1500, text="Fantasy language - Zelf typen", color="black", height=50, units="pix", pos = [0, 300])
titletext_quest = visual.TextStim(win, wrapWidth=1500, text="Vragenlijst", color="black", height=50, units="pix", pos = [0, 300])

# explanation text (middle)
explaintext_roun = visual.TextStim(win, wrapWidth=1500, text="", color="black", height=40, units="pix", pos = [0, 0])
explaintext_memo = visual.TextStim(win, wrapWidth=1500, text="Dadelijk zie je een aantal afbeeldingen een voor een op het scherm verschijnen samen met het woord in fantasietaal dat die afbeelding beschrijft. Probeer zo goed mogelijk het juiste woord bij elke afbeelding te onthouden.", color="black", height=40, units="pix", pos = [0, 0])
explaintext_gues = visual.TextStim(win, wrapWidth=1500, text="Je partner heeft een afbeelding gezien en een woord getypt om het te beschrijven. Lees het woord op de computer van je partner en kies de juiste afbeelding uit de 8 mogelijke afbeeldingen (gebruik 1-2-3-4-5-6-7-8 op het toetsenbord om een keuze te maken). Je krijgt feedback over je keuze, probeer er van te leren. Maak tijdens het experiment zo min mogelijk fouten! Vergeet niet om de feedback aan je partner te laten zien. Je krijgt feedback over je keuze, probeer daarvan te leren.", color="black", height=40, units="pix", pos = [0, 0])
explaintext_prod = visual.TextStim(win, wrapWidth=1500, text="Nu krijg je een afbeelding te zien. Denk na over hoe je het zou noemen en druk op Enter als je klaar bent om te typen. Als je klaar bent met het schrijven van het woord, druk je nogmaals op enter en draai je de computer zodat je partner het woord kan lezen en kan raden welke afbeelding je beschrijft. Tijdens deze taak mag je de taal niet wijzigen naar Nederlands of andere bestaande talen. Gebruik ook niets dat heel erg op het Nederlands of andere talen lijkt. Ook mag je geen Nederlandse afkortingen, afkortingen of acroniemen gebruiken. Let op, je kunt niet alle letters gebruiken: alleen de letters die zichtbaar zijn op het toetsenbord kunnen worden gebruikt.", color="black", height=40, units="pix", pos = [0, 0])
explaintext_test = visual.TextStim(win, wrapWidth=1500, text="Nu is het tijd om te testen hoe goed je de fantasietaal onthoudt! U ziet dezelfde afbeeldingen. Denk goed na over hoe je ze een naam zou geven en druk op enter als je klaar bent om te typen (tijdens het typen kun je de scene niet meer zien). Maak je geen zorgen als je de naam van de afbeelding niet meer weet en beproef je geluk door een woord te typen.", color="black", height=40, units="pix", pos = [0, 0])
explaintext_lasttest = visual.TextStim(win, wrapWidth=1500, text="Nu hoef je niet meer met je partner te communiceren. U moet een reeks afbeeldingen een naam geven in de nieuwe taal die u gebruikte.", color="black", height=40, units="pix", pos = [0, 0])
explain_quest = visual.TextStim(win, wrapWidth=1500, text="De volgende uitspraken beschrijven een groot aantal veelvoorkomende situaties. Er zijn geen goede of foute antwoorden; het beste antwoord is het onmiddellijke, spontane antwoord. Lees elke zin aandachtig en vul het nummer in dat uw eerste reactie weergeeft. Vergeet niet dat deze gegevens volledig anoniem zijn. Gebruik 1-2-3-4-5 op het toetsenbord om een keuze te maken.", color="black", height=40, units="pix", pos = [0, 0])
quest = visual.TextStim(win, wrapWidth=1500, text="", color="black", height=80, units="pix", pos = [0, 1000])

# how to start
pressenter = visual.TextStim(win, wrapWidth=1500, text="[Druk op Enter om te beginnen.]", color="black", units="pix", height=30, pos = [0, -300])
pressenter_cont = visual.TextStim(win, wrapWidth=1500, text="[Druk op Enter om te gaan.]", color="black", units="pix", height=30, pos = [0, -400])
pressenter_type = visual.TextStim(win, wrapWidth=1500, text="[Druk op Enter om te typen.]", color="black", units="pix", height=30, pos = [0, -400])
pressenter_oktype = visual.TextStim(win, wrapWidth=1500, text="[Druk op Enter als je klaar bent met typen.]", color="black", units="pix", height=30, pos = [0, -400])

# create happy and sad smiley (only for training)
happy = visual.ImageStim(win=win, image = path + "CheckMark.png", units="pix", size=(200, 200))
sad = visual.ImageStim(win=win, image = path + "Wrong.png", units="pix", size=(200, 200))  
happyhigh = visual.ImageStim(win=win, image = path + "CheckMark.png", units="pix", size=(200, 200), pos=[0,400])
sadhigh = visual.ImageStim(win=win, image = path + "Wrong.png", units="pix", size=(200, 200), pos=[0,400])  

# white rectangle middle
rect = visual.Rect(win=win, width = 450, height = 450, lineWidth = 1, lineColor="black", fillColor="white",  units="pix", pos = [0, 0])
smallrect = visual.Rect(win=win, width = 430, height = 430, lineWidth = 1, lineColor="black", fillColor="white",  units="pix", pos = [0, 0])

# word
word_pos1 = visual.TextStim(win, wrapWidth = 1500, height = 80, text="tupoi", color="black", units="pix", pos = [0, +400])
word_pos2 = visual.TextStim(win, wrapWidth = 1500, height = 65, text="tupoi", color="black", units="pix", pos = [0, +480])
word_good = visual.TextStim(win, wrapWidth = 1500, height = 80, text="tupoi", color="black", units="pix", pos = [+400, +400])
word_yours = visual.TextStim(win, wrapWidth = 1500, height = 80, text="tupoi", color="black", units="pix", pos = [-400, +400])
word_yours_big = visual.TextStim(win, wrapWidth = 1500, height = 140, text="tupoi", color="black", units="pix", pos = [0, 0])

# feedback
your_answer = visual.TextStim(win, wrapWidth = 1500, height = 35, text="JOUW ANTWOORD", color="black", units="pix", pos = [-400, -250])
good_answer = visual.TextStim(win, wrapWidth = 1500, height = 35, text="JUISTE ANTWOORD", color="black", units="pix", pos = [400, -250])
your_answer_prod = visual.TextStim(win, wrapWidth = 1500, height = 20, text="JOUW ANTWOORD", color="black", units="pix", pos = [-400, 300])
good_answer_prod = visual.TextStim(win, wrapWidth = 1500, height = 20, text="JUISTE ANTWOORD", color="black", units="pix", pos = [400, 300])

# description
description = visual.TextStim(win, wrapWidth = 1500, height = 35, text="beschrijving", color="black", units="pix", pos = [-400, 0])
settext = visual.TextStim(win, wrapWidth = 500, height = 50, text="beschrijving", color="black", units="pix", pos = [100, 0], alignText='left')

# end
thanks = visual.TextStim(win, wrapWidth = 1500, height = 60, text="Bedankt voor uw deelname aan ons experiment!", color="black", units="pix", pos = [100, 0], alignText='left')

# now, we try to find the position of the squares in the screen
# as a reminder, our screen is 1920 pixels
# we want to fit 8 squares with a certain width (here 435 pixels)
# so the position of the center of the square the most on the left should be -700 and the one the most on the right +700
# then, splitting in between we get:
list_pos_x = [-700, -234, 234, 700, -700, -234, 234, 700]
list_pos_y = [ 215, 215, 215, 215,-240, -240, -240, -240] # for y I just selected something that looks good

# number for the 8 squares
numberss = [0] * 8
colored = [0] * 8
for el in range(8):
    numberss[el] = visual.TextStim(win=win, text=str(el+1), height = 28,  pos=[(list_pos_x[el]),(list_pos_y[el]+218)], color="black", units="pix")
    colored[el] = visual.Rect(win=win, width = 34, height = 34, lineWidth = 1, lineColor="black", fillColor="white", colorSpace='rgb255', units="pix", pos=[(list_pos_x[el]),(list_pos_y[el]+218)])

# number and scale for the 5 questionnaires
list_pos_x_quest = [-600, -300, 0, 300, 600]
list_text_quest = ["Nooit/bijna nooit", "Zelden", "Af en toe", "Vaak", "Altijd/bijna altijd"]
numbers_quest = [0] * 5
text_quest = [0] * 5
text_quest_small = [0] * 5
for el in range(5):
    numbers_quest[el] = visual.TextStim(win=win, text=str(el+1), height = 60,  pos=[(list_pos_x_quest[el]),-280], color="black", units="pix")
    text_quest[el] = visual.TextStim(win=win, text=list_text_quest[el], height = 30,  pos=[(list_pos_x_quest[el]),-400], color="black", units="pix")
    text_quest_small[el] = visual.TextStim(win=win, text=list_text_quest[el], wrapWidth=200, height = 30,  pos=[(list_pos_x_quest[el]),-400], color="black", units="pix")
   
# --------------------------- #
# ---- Various functions ---- #

# this function takes an angle and give a vector of movement in output 
def directions(angle):
    index_x = math.cos(angle * math.pi / 180) 
    index_y = math.sin(angle * math.pi / 180) 
    return index_x, index_y
 
# this function return unique items in a list
def unique(list1):
    x = np.array(list1)
    return(x)    
 
def find_partner(part, pair):
    for el in pair:
        if part in el : 
            if el[0] == part : partner = el[1]
            if el[1] == part : partner = el[0]
    return(partner) 
 
def find_indices(list_to_check, item_to_find):
    array = np.array(list_to_check)
    indices = np.where(array == item_to_find)[0]
    return list(indices)

def decompose_in_2_lists(my_list):
    # decompose in 3 lists for items, angles, and words
    list_items = [item[0] for item in my_list]
    list_words = [item[1] for item in my_list]
    return(list_items, list_words)



# --------------------------------- #
# ---- Task Switching function ---- #


grid = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/grid.png", units="pix", size=(500, 500))

list_instructions = ["instructions1.png", "instructions2.png", "instructions3.png", "instructions4.png", "instructions5.png"]
all_instructions = [0]*5
for el in range(5):    
    all_instructions[el] = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/"+list_instructions[el], units="pix")  

def intructions_taskswitching():
    
    for el in range(5):
        all_instructions[el].draw()
        win.flip()
        while True:
            k = event.getKeys(keyList="return,escape") # pause until there's a keypress
            if k: # if there was an actual key pressed:
                if k[0] == 'return' :
                    break
                if k[0] == 'escape':
                    win.close()
                    dataFile.close()
                    core.quit()

readyletters = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/readyletters.png", units="pix") 
readynumbers = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/readynumbers.png", units="pix") 
readylettersnumbers = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/readylettersnumbers.png", units="pix") 

error_task1 = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/task1.png", units="pix", pos=[430, 120]) 
error_task2 = visual.ImageStim(win=win, image = path + "Stimuli_TaskSwitching/task2.png", units="pix", pos=[430, -120]) 

# numbers and letters
all_letters_vow = ["A", "E", "I", "U"]
all_letters_con = ["G", "T", "R", "C"]
all_numbers_odd = [1,3,5,7]
all_numbers_eve = [2,4,6,8]

numbers = visual.TextStim(win=win, text="", height = 80, color="yellow", units="pix")
texts = visual.TextStim(win=win, text="", height = 80, color="yellow", units="pix")


def task1():

    # create list task1
    random.seed(2504)
    list_num_t1 = all_numbers_odd*5 + all_numbers_eve*5
    random.shuffle(list_num_t1)
    list_let_t1 = all_letters_vow*5 + all_letters_con*5
    random.shuffle(list_let_t1)

    # print instructions
    readyletters.draw()
    win.flip()
    while True:
        k = event.getKeys(keyList="return,escape") # pause until there's a keypress
        if k: # if there was an actual key pressed:
            if k[0] == 'return' :
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                dataFile_ts.close()
                core.quit()
                
    k = []
    for el in range(40):
        
        # find position of element based on index
        if (el % 2) == 0: 
            posx = 120
            side="right"
        else : 
            posx = -120
            side="left"
            
        # find whether it is a task switch or not
        if el == 0:  switch=1
        else : switch = 0
        
        # draw grid
        grid.draw()
        
        # set number, position, and draw number
        numbers.setText(list_num_t1[el])
        numbers.setPos([posx+28, 120])
        numbers.draw()
        
        # set letter, position, and draw letter
        texts.setText(list_let_t1[el])
        texts.setPos([posx-28, 120])
        texts.draw()
        
        # print all
        win.flip()
        
        # record time
        timer = core.Clock()
        
        # check for keypress
        while True:
            k = event.getKeys(keyList="return,q,p,escape") # pause until there's a keypress
            if k: # if there was an actual key pressed:
                
                # record the time
                rt = timer.getTime()

                # if part press q for consonnant or p for vowel, then success
                if (k[0] == 'q' and list_let_t1[el] in all_letters_con) or (k[0] == 'p' and list_let_t1[el] in all_letters_vow):
                    success = 1            
                    break
                # if part press p for consonnant or q for vowel, then fail
                elif (k[0] == 'q' and list_let_t1[el] in all_letters_vow) or (k[0] == 'p' and list_let_t1[el] in all_letters_con):
                    success = 0
                    break
                elif k[0] == 'escape':
                    win.close()
                    dataFile.close()
                    dataFile_ts.close()
                    core.quit()
                    
        # Write information on datafile          
        dataFile_ts.write('%s,%s,%s,%s,%i,%i,%i,%f\n'  %("letters", side, "letter", list_let_t1[el], list_num_t1[el], switch, success, rt))
        
        # if it is a fail, print the error message
        if success == 0:
            grid.draw()
            texts.draw()
            numbers.draw()
            error_task1.draw()
            win.flip()
            core.wait(3)


def task2():

    # create list task1
    random.seed(2505)
    list_num_t2 = all_numbers_odd*5 + all_numbers_eve*5
    random.shuffle(list_num_t2)
    list_let_t2 = all_letters_vow*5 + all_letters_con*5
    random.shuffle(list_let_t2)

    # print instructions    
    readynumbers.draw()
    win.flip()
    while True:
        k = event.getKeys(keyList="return,escape") # pause until there's a keypress
        if k: # if there was an actual key pressed:
            if k[0] == 'return' :
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()
                
    k = []
    for el in range(40):
        # find position of element based on index
        if (el % 2) == 0: 
            posx = 120
            side="right"
        else : 
            posx = -120
            side="left"
        
        # find whether it is a task switch or not
        if el == 0:  switch=1
        else : switch = 0
        
        # draw grid
        grid.draw()
        
        # set number, position, and draw number
        numbers.setText(list_num_t2[el])
        numbers.setPos([posx+28, -120])
        numbers.draw()
        
        # set letter, position, and draw letter
        texts.setText(list_let_t2[el])
        texts.setPos([posx-28, -120])
        texts.draw()
        
        # print all
        win.flip()
        
        # record time
        timer = core.Clock()
        
        # wait for keypress
        while True:
            k = event.getKeys(keyList="return,q,p,escape") # pause until there's a keypress
            if k: # if there was an actual key pressed:
                rt = timer.getTime()

                # if participant press q for odd or p for even, then success
                if (k[0] == 'q' and list_num_t2[el] in all_numbers_odd) or (k[0] == 'p' and list_num_t2[el] in all_numbers_eve):
                    success = 1            
                    break
                # if participant press q for even or p for odd, then fail
                elif (k[0] == 'q' and list_num_t2[el] in all_numbers_eve) or (k[0] == 'p' and list_num_t2[el] in all_numbers_odd):
                    success = 0
                    break
                if k[0] == 'escape':
                    win.close()
                    dataFile.close()
                    dataFile_ts.close()
                    core.quit()
                    
        # save data on datafile    
        dataFile_ts.write('%s,%s,%s,%s,%i,%i,%i,%f\n'  %("numbers", side, "number", list_let_t2[el], list_num_t2[el], switch, success, rt))
        
        # if error, print error message
        if success == 0:
            grid.draw()
            texts.draw()
            numbers.draw()
            error_task2.draw()
            win.flip()
            core.wait(3)


def task3():

    # list with position based on index
    upleft=[0,4,8,12,16,20,24,28,32,36]
    upright=[1,5,9,13,17,21,25,29,33,37]
    downright=[2,6,10,14,18,22,26,30,34,38]
    downleft=[3,7,11,15,19,23,27,31,35,39]

    # create list task1
    random.seed(2506)
    list_num_t3 = all_numbers_odd*5 + all_numbers_eve*5
    random.shuffle(list_num_t3)
    list_let_t3 = all_letters_vow*5 + all_letters_con*5
    random.shuffle(list_let_t3)

    # print instructions    
    readylettersnumbers.draw()
    win.flip()
    while True:
        k = event.getKeys(keyList="return,escape") # pause until there's a keypress
        if k: # if there was an actual key pressed:
            if k[0] == 'return' :
                break
            if k[0] == 'escape':
                win.close()
                dataFile_ts.close()
                dataFile.close()
                core.quit()
                
    k = []
    # find position of element based on index
    for el in range(40):
        if el in upleft: 
            posx = -120
            posy = 120
            side="left"
            task_now="letter"
        elif el in upright: 
            posx = 120
            posy = 120
            side="right"
            task_now="letter"
        if el in downright: 
            posx = 120
            posy = -120
            side="right"
            task_now="number"
        elif el in downleft : 
            posx = -120
            posy = -120
            side="left"
            task_now="number"
    
        # find whether it is a task switch or not
        if (el % 2) == 0: switch=1
        else : switch = 0
        
        # draw grid
        grid.draw()
        
        # set number, position, and draw number
        numbers.setText(list_num_t3[el])
        numbers.setPos([posx+28, posy])
        numbers.draw()
        
        # set letter, position, and draw letter
        texts.setText(list_let_t3[el])
        texts.setPos([posx-28, posy])
        texts.draw()
        
        # print all
        win.flip()
        
        # record time
        timer = core.Clock()
        
        k = []
        # wait for keypress
        while True:
            k = event.getKeys(keyList="return,q,p,escape") # pause until there's a keypress
            if k: # if there was an actual key pressed:
                rt = timer.getTime()

                if (k[0] == 'q' and list_num_t3[el] in all_numbers_odd and task_now == "number") or (k[0] == 'p' and list_num_t3[el] in all_numbers_eve and task_now == "number") or (k[0] == 'q' and list_let_t3[el] in all_letters_con and task_now == "letter") or (k[0] == 'p' and list_let_t3[el] in all_letters_vow and task_now == "letter") :
                    success = 1            
                    break
                elif (k[0] == 'q' and list_num_t3[el] in all_numbers_eve and task_now == "number") or (k[0] == 'p' and list_num_t3[el] in all_numbers_odd and task_now == "number") or (k[0] == 'q' and list_let_t3[el] in all_letters_vow and task_now == "letter") or (k[0] == 'p' and list_let_t3[el] in all_letters_con and task_now == "letter"):
                    success = 0
                    break
                elif k[0] == 'escape':
                    win.close()
                    dataFile_ts.close()
                    dataFile.close()
                    core.quit()
        
        # save data on datafile
        dataFile_ts.write('%s,%s,%s,%s,%i,%i,%i,%f\n'  %("lettersnumbers", side, task_now, list_let_t3[el], list_num_t3[el], switch, success, rt))
        
        # if failure for letter, print letter error message
        if success == 0 and task_now == "letter":
            grid.draw()
            texts.draw()
            numbers.draw()
            error_task1.draw()
            win.flip()
            core.wait(3)
            
        # if failure for number, print number error message
        elif success == 0 and task_now == "number":
            grid.draw()
            texts.draw()
            numbers.draw()
            error_task2.draw()
            win.flip()
            core.wait(3)
                    
 
    
# ---------------------------------------------- #
# ---- Functions for generating random sets ---- #


def generate_learning_set(shapes, N_repeat, part_id):
    

    
    # repeat them N times
    shapes2 = shapes*N_repeat
    
    # set seed with group number
    random.seed(group_num*int(part_id))
        
    random.shuffle(shapes2)
    block1 = shapes2.copy()

    random.shuffle(shapes2)
    block2 = shapes2.copy()

    random.shuffle(shapes2)
    block3 = shapes2.copy()

    random.shuffle(shapes2)
    block4 = shapes2.copy()
    
    random.shuffle(shapes2)
    block5 = shapes2.copy()
    
    random.shuffle(shapes2)
    testing_set = shapes2.copy()


    return(block1, block2, block3, block4, block5, testing_set)


def generate_CG_set(group_num, round_num):
    
    # select only furst 4 shapes
    shapes = list(range(8))
    
    # random seed with the group num
    random.seed(group_num*int(round_num))
        
    me = shapes.copy()
    random.shuffle(me)

    mypartner = me.copy()
    
    # shuffle the lists in a way that both are very different
    for i in range(0, len(mypartner)-1):
        pick = random.randint(i+1, len(mypartner)-1)
        mypartner[i], mypartner[pick] = mypartner[pick], mypartner[i]
      
    return(me, mypartner)



# ---------------------------- #
# ---- Print Instructions ---- #  
 

def alert_biased():
    titletext_roun.setText("LEESMIJ!")
    titletext_roun.draw()
    explaintext_roun.setText("Uw toetsenbord is niet zoals de toetsenborden van de andere deelnemers. Sommige brieven kunt u niet schrijven. Ze zouden het nog niet moeten weten, dus vertel het ze niet!")
    explaintext_roun.draw()
    pressenter_cont.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress
    
    
def instructions_round(my_round, part_id):
    if my_round == 0 or my_round == 1:
        if part_id == "1": sit_office = "A"
        elif part_id == "2": sit_office = "C"
        elif part_id == "3": sit_office = "B"
        elif part_id == "4": sit_office = "D"
    elif my_round == 2:
        if part_id == "1": sit_office = "A"
        elif part_id == "2": sit_office = "B"
        elif part_id == "3": sit_office = "C"
        elif part_id == "4": sit_office = "D"
    elif my_round == 3:
        if part_id == "1": sit_office = "B"
        elif part_id == "2": sit_office = "A"
        elif part_id == "3": sit_office = "C"
        elif part_id == "4": sit_office = "D"
    elif my_round == 4:
        if part_id == "1": sit_office = "C"
        elif part_id == "2": sit_office = "A"
        elif part_id == "3": sit_office = "B"
        elif part_id == "4": sit_office = "D"
    elif my_round == 5:
        if part_id == "1": sit_office = "D"
        elif part_id == "2": sit_office = "A"
        elif part_id == "3": sit_office = "B"
        elif part_id == "4": sit_office = "C"
    elif my_round == 6:
        if part_id == "1": sit_office = "D"
        elif part_id == "2": sit_office = "A"
        elif part_id == "3": sit_office = "C"
        elif part_id == "4": sit_office = "B"
    elif my_round == 7:
        if part_id == "1": sit_office = "D"
        elif part_id == "2": sit_office = "B"
        elif part_id == "3": sit_office = "C"
        elif part_id == "4": sit_office = "A"
    elif my_round == 8:
        if part_id == "1": sit_office = "D"
        elif part_id == "2": sit_office = "C"
        elif part_id == "3": sit_office = "B"
        elif part_id == "4": sit_office = "A"
    elif my_round == 9:
        if part_id == "1": sit_office = "D"
        elif part_id == "2": sit_office = "C"
        elif part_id == "3": sit_office = "A"
        elif part_id == "4": sit_office = "B" 
        
    if my_round == 0:
        titletext_roun.setText("Onthouden")
        explaintext_roun.setText("Zorg ervoor dat u plaatsneemt in kantoor " + sit_office + ".")
    if my_round == 1:    
        titletext_roun.setText("Round " + str(my_round) + " - Communiceren")
        explaintext_roun.setText("Blijf alsjeblieft zitten waar je zit.")
    if my_round >=2:   
        titletext_roun.setText("Round " + str(my_round) + " - Communiceren")
        explaintext_roun.setText("Ga zitten op kantoor " + sit_office + ". Vergeet niet de computer mee te nemen.")
        
    titletext_roun.draw()
    explaintext_roun.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_passive_exposure():
    
    titletext_memo.draw()
    explaintext_memo.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_guess_from_8():
    
    titletext_gues.draw()
    explaintext_gues.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_production():
        
    titletext_prod.draw()
    explaintext_prod.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_production_test():
        
    titletext_prod.draw()
    explaintext_test.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_production_lasttest():
        
    titletext_prod.draw()
    explaintext_lasttest.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress

def instructions_questionnaire():
        
    titletext_quest.draw()
    explain_quest.draw()
    pressenter.draw()
    win.flip()
    event.waitKeys(keyList="return") # pause until there's a keypress


# -------------------------------------- #
# ---- Print questionnaire function ---- #

def prosociality_scale_items(text):
    
    # clear event
    event.clearEvents()
    
    explain_quest.setText(text)
    explain_quest.draw()
    
    for el in range(len(numbers_quest)):
        numbers_quest[el].draw()
        text_quest[el].draw()
    win.flip()
    
    while True:
        k = event.getKeys(keyList="1,2,3,4,5,escape") # pause until there's a keypress
    
        if k: # if there was an actual key pressed:
            if k[0].isnumeric() == True :
                save_res = k[0]
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()
                
    return(save_res)

def prosociality_scale():
    
    list_questions = ["Ik help graag mijn vrienden/collega's bij hun activiteiten.",
                      "Ik deel spullen en/of geld dat ik heb met mijn vrienden.",
                      "Ik probeer anderen te helpen.",
                      "Ik ben beschikbaar voor vrijwilligersactiviteiten om mensen in nood te helpen.",
                      "Ik ben empathisch voor degenen die in nood zijn.",
                      "Ik help onmiddellijk degenen die in nood zijn.",
                      "Ik doe wat ik kan om anderen te helpen voorkomen dat ze in de problemen komen.",
                      "Ik voel intens wat anderen voelen",
                      "Ik ben bereid mijn kennis en vaardigheden beschikbaar te stellen aan anderen.",
                      "Ik probeer degenen die verdrietig zijn te troosten.",
                      "Ik leen gemakkelijk geld of andere dingen uit.",
                      "Ik plaats mezelf gemakkelijk in de schoenen van degenen die zich ongemakkelijk voelen.",
                      "Ik probeer dichtbij te zijn en te zorgen voor degenen die in nood zijn",
                      "Ik deel gemakkelijk elke goede kans die ik krijg met vrienden.",
                      "Ik breng tijd door met die vrienden die zich eenzaam voelen",
                      "Ik voel het ongemak van mijn vrienden onmiddellijk, zelfs als het niet rechtstreeks aan mij wordt meegedeeld."]
    
    for element in range(len(list_questions)) :
        resp = prosociality_scale_items(list_questions[element])
        dataFile_ps.write('%i,%i\n' %(int(element)+1, int(resp)))

    


def ask_age():
    
    # clear event
    event.clearEvents()
    
    explain_quest.setText("Hoe oud bent u?")
    explain_quest.draw() 
    textt = "____"
    
    first = False
    while True:
        k = event.getKeys(keyList="1,2,3,4,5,6,7,8,9,0,escape,return,backspace") # pause until there's a keypress
    
        if k: # if there was an actual key pressed:
            if first == False : textt = ""
            first = True
            if k[0].isnumeric() == True:
                my_res = k[0]
                textt = textt + k[0]
                
            if k[0] == "backspace" :
                textt = textt[:-1]

            if  k[0] == "return":
                dataFile_ps.write('%i,%i\n' %(9889, int(textt)))
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()
        numbers_quest[2].setText(textt)
        numbers_quest[2].draw()       
        explain_quest.draw()
        
        pressenter_oktype.draw()
        win.flip()


def ask_gender():
    
    # clear event
    event.clearEvents()
    
    explain_quest.setText("Wat is je geslacht?")
    explain_quest.draw() 
    
    numbers_quest[0].draw()
    text_quest[0].setText("female")
    text_quest[0].draw()
    
    numbers_quest[1].draw()
    text_quest[1].setText("male")
    text_quest[1].draw()
    
    numbers_quest[2].draw()
    text_quest[2].setText("other")
    text_quest[2].draw()
    win.flip()
    
    while True:
        k = event.getKeys(keyList="1,2,3,escape") # pause until there's a keypress
    
        if k: # if there was an actual key pressed:
            if k[0].isnumeric() == True :
                dataFile_ps.write('%i,%i\n' %(9889, int(k[0])))
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()

def ask_money():
    
    explain_quest.setText("Stel je voor dat ik je een extra bedrag van 100 euro geef vanwege de uitstekende prestaties van jouw groep tijdens dit experiment. Nu heb je de keuze om het volledige bedrag voor jezelf te houden, of het te delen met de andere deelnemers. Aangezien de andere deelnemers niet op de hoogte zijn van deze extra beloning, is de keuze geheel aan jou. Hoeveel besluit je te delen met de andere deelnemers?")
    explain_quest.draw() 
    
    numbers_quest[0].draw()
    text_quest_small[0].setText("0 euro (Ik houd alle 100 euro)")
    text_quest_small[0].draw()
    
    numbers_quest[1].draw()
    text_quest_small[1].setText("Tussen 0 en 75 euro (Ik deel, maar houd meer voor mezelf)")
    text_quest_small[1].draw()
    
    numbers_quest[2].draw()
    text_quest_small[2].setText("75 euro (25 euro voor iedereen)")
    text_quest_small[2].draw()
    
    numbers_quest[3].draw()
    text_quest_small[3].setText("Tussen 75 en 100 euro (Ik houd minder dan hen)")
    text_quest_small[3].draw()
 
    numbers_quest[4].draw()
    text_quest_small[4].setText("100 euro (Ik geef alles weg)")
    text_quest_small[4].draw()
    win.flip()
    
    while True:
        k = event.getKeys(keyList="1,2,3,4,5,escape") # pause until there's a keypress
    
        if k: # if there was an actual key pressed:
            if k[0].isnumeric() == True :
                dataFile_ps.write('%i,%i\n' %(888, int(k[0])))
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()

   
# ------------------------------------ #
# ---- Print experiment functions ---- #


## Explanation of the parameters:
    # item_num is the number of the item to draw
    # my_angle is the angle of the item to draw
    # my_word is the word used for the item drawn
def passive_exposure(item_num, my_word):
    
    # initialize timer
    timer = core.Clock()

    # affect position to moving image
    m[item_num].pos = [0, 0] # directly update both x *and* y
    
    # show during 10 seconds
    while timer.getTime() < 7:

        # draw all information
        rect.draw()
        m[item_num].draw()
        taskblock.draw()
        word_pos1.setText(my_word)
        word_pos1.draw()
        win.flip() 




## Explanation of the parameters:
    # list_items is list with the numbers of the items to draw
    # list_items is list with the angles of the items to draw
    # pos_item_num is the POSITION of the target item (it's not the number of the item but its position in the list !)
    # list_pos_x shows the x position of all the squares to be drawn (changing when moving)
    # list_pos_y shows the y position of all the squares to be drawn (changing when moving)
def guess_from_8(good_item, list_pos_x, list_pos_y, word_written):

    list_items = list(range(8))
    
    ### TRIAL ###
   
    # draw all items (rectangles and image)
    random.seed(group_num)
    random.shuffle(list_items)
    pos_item_num = list_items.index(good_item)

    for nb_square in range(0,len(list_pos_x)):
        
        # draw rectangle
        smallrect.setPos([list_pos_x[nb_square], list_pos_y[nb_square]])
        smallrect.draw()
        
        # draw image
        smallm[list_items[nb_square]].setPos([list_pos_x[nb_square], list_pos_y[nb_square]])
        smallm[list_items[nb_square]].draw()

        # draw number
        colored[nb_square].draw()
        numberss[nb_square].draw()       
        
    # draw task block number
    taskblock.draw()
    
    # draw word on the top
    word_pos2.setText(word_written)
    word_pos2.draw()

    # make the drawn things visible
    win.flip() 


    while True: # draw moving stimulus
        
        # wait for event
        k=event.getKeys(keyList = '1, 2, 3, 4, 5, 6, 7, 8, escape')
        # if ever we want to do by click, here is a code example
        # if mouse.isPressedIn(img[0]) or mouse.isPressedIn(img[1]) or mouse.isPressedIn(img[2]) or mouse.isPressedIn(img[3]) or mouse.isPressedIn(img[4]) or mouse.isPressedIn(img[5]) or mouse.isPressedIn(img[6]) or mouse.isPressedIn(img[7]) or mouse.isPressedIn(img[8]) or mouse.isPressedIn(img[9]) :
        #     response = mouse.getPos() # get mouse position
        #     timeanswer = clock2.getTime() # get time (time between the moment when the baskets hide and the time when the subject click on the basket)
        #     break
        if k: # if there was an actual key pressed:
            if k[0].isnumeric() == True :
                your_item = list_items[int(k[0])-1]
                key_pressed = k[0]
                if (int(k[0])-1) == pos_item_num : GoodAnswer = True
                else : GoodAnswer = False
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()

    # clear event
    event.clearEvents()
        
    
    ### FEEDBACK ###
    
    x_yours = -400
    y_yours = 0
    x_good = 400
    y_good = 0
    
    while True: # draw moving stimulus
        k=event.getKeys(keyList = 'return, escape')
        if k: # if there was an actual key pressed:
            if k[0] == 'return':
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()

        # draw the feedback
        if GoodAnswer == True : happy.draw()
        else : sad.draw()
        
        # draw the two fixed rectangles
        rect.setPos([-400, 0])
        rect.draw()
        rect.setPos([400, 0])
        rect.draw()
        
        # affect position to moving image and draw
        m[good_item].pos = [x_good, y_good] # directly update both x *and* y
        m[good_item].draw()
        m[your_item].pos = [x_yours, y_yours] # directly update both x *and* y
        m[your_item].draw()

        # draw task and block indicator
        taskblock.draw()
        
        # draw word
        #word_pos1.draw()
        your_answer.draw()
        good_answer.draw() 
        
        # Draw task block
        taskblock.draw()
            
        # draw press enter
        pressenter_cont.draw()
        
        # make the drawn things visible
        win.flip() 

    return(GoodAnswer, key_pressed, your_item, good_item, pos_item_num)


## Explanation of the parameters:
    # item_num is the num of the item to draw
    # my_angle is the angle of the item to draw
    # list_biased is the inventory of letters for the biased participant
    # list_unbiased is the inventory of letters for the unbiased participant
    # good_word is the word that should be used to describe this item (only relevant for the learning phase)
    # feedback is whether a feedback is needed (learning) or whether no feedback is needed (testing, generalization + ComGame)
    # type_test shows the type of test (learning, testing, ComGame..) only in ComGame the word will be printed in big

def production(item_num, list_biased, list_unbiased, good_word, feedback, type_test):
    
    ### STIMULI SHOW ###
    
    while True: # draw moving stimulus
        k=event.getKeys(keyList = 'return, escape')
        if k: # if there was an actual key pressed:
            if k[0] == 'return':
                break
            if k[0] == 'escape':
                win.close()
                dataFile.close()
                core.quit()

        # affect position to moving image
        m[item_num].pos = [0, 0] # directly update both x *and* y
        
        # draw all information
        rect.setPos([0,0])
        rect.draw()
        m[item_num].draw()
        taskblock.draw()
        pressenter_type.draw()
        win.flip() 

    
    ### WRITE OUTPUT ###

    # clear event
    event.clearEvents()
        
    # add other keys to list of possible keys
    list_unbiased_extended = list_unbiased + ', escape, return, backspace'
    list_biased_extended = list_biased + ', escape, return, backspace'
    
    newtext=""
    while True:
        
        # wait for the key event allowed in the repertory of sounds (different for biased and unbiased)
        if group_type == "HT" and int(part_id) == 1:
            k= event.getKeys(keyList = list_biased_extended)
        else:
            k= event.getKeys(keyList = list_unbiased_extended)
            
        if k: # if there was an actual key pressed:
            if k[0] == "backspace" :
                newtext = newtext[:-1]
            elif k[0] == 'escape' :
                win.close()
                dataFile.close()
                core.quit()
            
            # here I face a little problem. The program consider that all letters in return, q, escape are included in the good letters
            # thus I have to recheck 
            elif k[0] != "backspace" and k[0] != "return" and len(newtext) < length_max: # if there was an actual key pressed:
                if ((part_id != "1") or (group_type=="HM")) and str(k[0]) in list_unbiased.split(", "):
                    newtext = newtext + str(k[0])
                if (part_id == "1" and group_type=="HT") and str(k[0]) in list_biased.split(", "):
                    newtext = newtext + str(k[0])

        
        # draw information
        description.draw()
        pressenter_oktype.draw()
        settext.setText(newtext)
        settext.draw()
        taskblock.draw()
        win.flip()
        
        # if press enter, save final word and go out of the loop
        if k:
            if k[0] == "return" and len(newtext) <= length_max:
                word_chosen = newtext
                
                # if this is an unbiased participant, determine if this is a success or not
                if part_id != "1":
                    if word_chosen == good_word : success = True
                    else : success = False
                    
                # if this is a biased participant, the rules for determining success are a bit different
                else:
                    if type_test != 'CG' :
                        
                        success=False
                        
                        from string import ascii_letters as letters
                        from string import digits as digits
                        diglet = letters + digits + " " + "-"
                        
                        # for the shape
                        if word_chosen == good_word.replace('p', ''): success = True
                        for el1 in diglet:
                            good_word_new = good_word.replace('p', el1)
                            if good_word_new == word_chosen: success = True
                            for el2 in diglet:
                                compose = el1 + el2
                                good_word_new = good_word.replace('p', compose)
                                if good_word_new == word_chosen: success = True
                        
                    else : success = False

                break
            
    ### SHOW IN BIG ###
    
    if feedback == False and type_test != "testing" :
        word_yours_big.setText(word_chosen)
        word_yours_big.draw()
        pressenter.draw()
        taskblock.draw()
        win.flip()
        event.waitKeys(keyList="return") # pause until there's a keypress

    
    ### FEEDBACK ###

    # clear event
    event.clearEvents()
    
    if feedback == True:
        # starting position of the image
        
        while True: # draw moving stimulus
            k=event.getKeys(keyList = 'return, escape')
            if k: # if there was an actual key pressed:
                if k[0] == 'return':
                    break
                if k[0] == 'escape':
                    win.close()
                    dataFile.close()
                    core.quit()

            # affect position to moving image
            m[item_num].pos = [0, 0] # directly update both x *and* y
            
            # draw all information
            rect.draw()
            m[item_num].draw()
            taskblock.draw()
            pressenter_cont.draw()
            
            # Draw good word
            word_good.setText(good_word)
            word_good.draw()
            good_answer_prod.draw()
            
            # Draw your word
            word_yours.setText(word_chosen)
            word_yours.draw()
            your_answer_prod.draw()
            
            # Draw smiley
            if success == True: happyhigh.draw()
            else: sadhigh.draw()
            
            # Draw task block
            taskblock.draw()
            
            # Actual print of all items
            win.flip() 

    return(word_chosen, success)




# ---------------------------- #
# ---- FIRST PRESENTATION ---- #

if part_id == "1" and group_type=="HT":
    alert_biased()
else:
    instructions_round(0, part_id)
    
print("Learning - presentation")
    
# generate random set
block1, block2, block3, block4, block5, testing_set = generate_learning_set(shapes, 1, part_id)
# we are not going to use block 2 to block 5

# show instructions for passive exposure
instructions_passive_exposure()

# store the name of the type of test 
name_typetest = "block1_passive_exp"
taskblock.setText('L1') #only indicate first block
 
# decompose in 3 lists for items, angles, and words
list_items, list_words = decompose_in_2_lists(block1)

for el in range(len(list_items)):
    
    # print passive exposure of each item
    passive_exposure(list_items[el], list_words[el])
    
    # Save results on file
    dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                    %(group_num, group_type, name_typetest, int(part_id), 999, 0, list_items[el], 999, 999, 999, 999, 999, list_words[el], 0))
    

# store the name of the type of test 
name_typetest = "block2_passive_exp"
taskblock.setText('L2') #only indicate first block
 
# decompose in 3 lists for items, angles, and words
list_items, list_words = decompose_in_2_lists(block2)

for el in range(len(list_items)):
    
    # print passive exposure of each item
    passive_exposure(list_items[el], list_words[el])
    
    # Save results on file
    dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                    %(group_num, group_type, name_typetest, int(part_id), 999, 0, list_items[el], 999, 999, 999, 999, 999, list_words[el], 0))    
        
# ----------------- #
# ---- TESTING ---- #

# print instructions for production
instructions_production_test()
print("Testing")

# store the name of the type of test
taskblock.setText('LT')

# decompose in 3 lists for items, angles, and words
list_items, list_words = decompose_in_2_lists(testing_set)

# PRODUCTION
for el in range(len(list_items)):

    # Do production
    word_chosen, success = production(list_items[el], list_biased, list_unbiased, list_words[el], False, "testing")
    
    # Save results on file
    dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                    %(group_num, group_type, "testing_set", int(part_id), 999, 0, list_items[el], 999, 999, 999, 999, int(success), word_chosen, 0))




# -------------------------------------------- #
# ---- COMMUNICATION GAMES (ROUND 1 to 6) ---- #

# 3 possibilities for pairs
pair1 = [[1,2], [3,4]] # this means that part 1 and part 2 interact and part 3 and part 4 interact
pair2 = [[1,3], [2,4]]
pair3 = [[2,3], [4,1]]
# the order of the pairs is pair1, pair2, pair3, then again pair1, pair2, pair3


for my_round in range(1,(tot_nb_rounds+1)) :
    
    # Print round 
    print("Round " + str(my_round))
    
    # Show instructions
    instructions_round(my_round, part_id)
    
    # generate the set of element (depend based on the round number)
    list_items_me, list_items_partner = generate_CG_set(group_num, my_round)

    # and also affect pairs of participants
    if my_round == 1 or my_round == 4 or my_round == 7 : pair = pair1  
    elif my_round == 2 or my_round == 5 or my_round == 8 : pair = pair2
    elif my_round == 3 or my_round == 6 or my_round == 9 : pair = pair3
    
    # then go through each items: at each item, one of the participant is guesser, the other is producer
    if int(part_id) in [item[0] for item in pair]:        
        
        for el in range(len(list_items_me)):
            
            ### PRODUCTION ###
            
            # print taskblock
            taskblock.setText('R'+str(my_round)+'_'+str(el+1)+"P1")
            
            # store item number and angle 
            item_me = list_items_me[el]
            item_partner = list_items_partner[el]

             # print if instructions if it is the first time
            if my_round == 1 and ( el == 0 or el == 1):
                instructions_production()
                
            # choose production word (this word will be later guessed by another participant)
            word_chosen = production(item_me, list_biased, list_unbiased, "", False, "CG")
            
            # Save results on file
            dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                           %(group_num, group_type, "ComGame_Producer", int(part_id), find_partner(int(part_id), pair),  my_round, item_me, 999, 999, 999, 999, 999, word_chosen[0], el))
       
            ### GUESSING ###

            # print taskblock
            taskblock.setText('R'+str(my_round)+'_'+str(el+1)+"G2")

            # print if instructions if it is the first time
            if my_round == 1 and ( el == 0 or el == 1):
                instructions_guess_from_8()
                
            # Do guessing
            GoodAnswer, key_pressed, your_item, good_item, index_good = guess_from_8(item_partner, list_pos_x, list_pos_y, "")
            
            # Save results on file
            dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                           %(group_num, group_type, "ComGame_Guesser", int(part_id), find_partner(int(part_id), pair), my_round, item_partner, int(key_pressed), index_good, your_item, good_item, GoodAnswer, "none",el))

    if int(part_id) in [item[1] for item in pair]:        
        
        
        for el in range(len(list_items_me)):
            
            # store item number and angle 
            item_me = list_items_me[el]
            item_partner = list_items_partner[el]

            ### GUESSING ###
           
            # print taskblock
            taskblock.setText('R'+str(my_round)+'_'+str(el+1)+"G1")

            # print if instructions if it is the first time
            if my_round == 1 and ( el == 0 or el == 1):
                instructions_guess_from_8()
                
            # Do guessing
            GoodAnswer, key_pressed, your_item, good_item, index_good = guess_from_8(item_me, list_pos_x, list_pos_y, "")
            
            # Save results on file
            dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                           %(group_num, group_type, "ComGame_Guesser", int(part_id), find_partner(int(part_id), pair), my_round, item_me, int(key_pressed), index_good, your_item, good_item, GoodAnswer, "none",el))
            
            ### PRODUCTION ###
            
            # print taskblock
            taskblock.setText('R'+str(my_round)+'_'+str(el+1)+"2")
            
            # store item number and angle 
            item = list_items_me[el]

             # print if instructions if it is the first time
            if my_round == 1 and ( el == 0 or el == 1):
                instructions_production()
                
            # choose production word (this word will be later guessed by another participant)
            word_chosen = production(item_partner, list_biased, list_unbiased, "", False, "CG")
            
            # Save results on file
            dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                           %(group_num, group_type, "ComGame_Producer", int(part_id), find_partner(int(part_id), pair),  my_round, item_partner, 999, 999, 999, 999, 999, word_chosen[0], el))
       

        

# ------------------------------ #
# ---- FINAL TESTING ON ALL ---- #

# print instructions for production
instructions_production_lasttest()
print("Final Testing")
    
# decompose in 3 lists for items, angles, and words
list_items, list_words = decompose_in_2_lists(block5)

# PRODUCTION
for el in range(len(list_items)):
    
    # set task block
    taskblock.setText('RF')
    # Do production
    word_chosen, success = production(list_items[el], list_biased, list_unbiased, list_words[el], False, "testing")
    
    # Save results on file
    dataFile.write('%i,%s,%s,%i,%i,%i,%i,%i,%i,%i,%i,%i,%s,%i\n' 
                    %(group_num, group_type, "final_testing", int(part_id), 999, 0, list_items[el], 999, 999, 999, 999, 999, word_chosen, 0))

        

print("Prosociality scale")
instructions_questionnaire()
prosociality_scale()
ask_money()
ask_gender()
ask_age()
dataFile_ps.close()
print("Datafile prosociality saved")

print("TaskSwitching task")
intructions_taskswitching()
task1() 
task2() 
task3() 
# save data
dataFile_ts.close()
print("Datafile taskswitching saved")  

# Draw thank you
thanks.draw()
event.clearEvents()  
win.flip()
core.wait(10) # pause until there's a keypress

# close and quit
win.close()

# save data
dataFile.close()
print("Datafile saved")
