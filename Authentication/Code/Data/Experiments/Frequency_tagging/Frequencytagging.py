from decimal import ROUND_CEILING
import tkinter as tk
from tkinter import ttk
from xmlrpc.client import boolean
import numpy as np
from datetime import datetime
import csv
import random
# This is to easily run the script from the command line
# [] = optional
# Usage: python Frequencytagging.py -pw password -freq frequency [-time] time

# import rhinoscriptsytnax as rs




def tagging(step, chosen_words = 'hoi doei dag', frequency = 15, time = 2, color = '101'):
    #Set up tkinter settings
    root = tk.Tk()
    root.title('password')
    label = tk.Label(font=("Helvetica", 150))
    label.pack(anchor=tk.CENTER, expand=tk.TRUE)
    window_width = 600
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    #bg.pack()

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    label.pack(anchor=tk.CENTER, expand=tk.TRUE)
    #Check if function is used for step 1 or step 2 of our frequencytagging plan
    if step == '1':
        responserecogntion = True
    else:
        responserecogntion = False


    #Create list of words, 40 random for response recognition and 3 random + 3 known for tagging
    with open('woorden.csv', newline='') as f:
        reader = csv.reader(f)
        allwords = list(reader)

    flatlist = []
    for sublist in allwords:
        for item in sublist:
            flatlist.append(item)
    words = flatlist
    random.shuffle(words)
    words = words[:40]
    if step == '2':
        chosen_words = list(chosen_words.split(" "))
        words = words[:3]
        for chosen_word in chosen_words:
            words.append(chosen_word)
        random.shuffle(words)
        empty = [' '] * len(words)
        result = [None]*(len(words) * 2)
        result[::2] = words
        result[1::2] = empty
        words = result
    elif step == '3':
        chosen_words = list(chosen_words.split(" "))
        for chosen_word in chosen_words:
            words.append(chosen_word)
        for chosen_word in chosen_words:
            words.append(chosen_word)
        random.shuffle(words)
        
    #Determine size and location of window


#Background beun
######################################################

    
    #create all important values in the code
    if responserecogntion:
        frame_rate = 30
    else:
        frame_rate = 60 #amount of ms that a screen is shown
    flash_rate = frequency
    word_rate = 1/time
    frame_period = int(1000/frame_rate)
    flash_period = int(1000/flash_rate)
    flash_period = frame_period * round(flash_period / frame_period)
    word_period = int(1000/word_rate)
    word_period = flash_period * round(word_period / flash_period)
    frames_per_flash = int(flash_period/frame_period)
    flash_per_word = int(word_period/flash_period)
    total_backgrounds = frames_per_flash * flash_per_word * len(words)
    

    #create rgb values based on a sine and the frame rate
    rgb_value = []
    step_size = np.pi / frames_per_flash
    for i in range(0,int(frames_per_flash)):
        blue = 254 * np.sin(step_size*i) + 1
        rgb_value.append(blue)
    color = list(color)  
    rgb_list = []
    for index, b in enumerate(rgb_value):
        
        rgb = []
        for i, c in enumerate(color):
            if c == '1':
                d = f'{hex(int(b))}q'.replace('0x','')
                if d[1] == 'q':
                    d = f'0{d[0]}'
                else:
                    d = d[:2]
                rgb.append(d)
            else:
                rgb.append('FF')
        rgb_list.append(f'#{rgb[0]}{rgb[1]}{rgb[2]}')

    #create list of all backgrounds that are needed
    backgrounds = []
    for index, word in enumerate(words):
        if (int(index % 2) == 1 and responserecogntion) or (int(index % 2) == 0 and responserecogntion == False):
            for a in range(flash_per_word):
                for b in rgb_list:
                    backgrounds.append(b)
        else:
            for a in range(flash_per_word):
                for b in rgb_list:
                    backgrounds.append(f'#FFFFFF')

    #add backgrounds to tkinter window
    bitjes = []
    for i, background in enumerate(backgrounds):
                label.after(int(i * frame_period), lambda c=background: label.configure(bg = c, pady = 350, padx = 800))
                root.attributes('-topmost', 1)
    print(word_period)

    #add words to tkinter window, also creates the labels
    for j,word in enumerate(words):
        label.after(int(word_period * j), lambda w=word: label.configure(text=w))
        if (j % 2 == 1 and responserecogntion) or (word in chosen_words):
            bitjes.append(1)
        elif word == ' ':
            pass
        else: 
            bitjes.append(0)

    words = [x for x in words if x != ' ']
        
    print(words)
    #close the window when experiment is over
    root.after(int(frame_period * total_backgrounds),lambda:root.destroy())

    
    start_time = str(datetime.now())
    
    #mainloop is used to run the window
    root.mainloop()
    
    return bitjes, start_time, words

