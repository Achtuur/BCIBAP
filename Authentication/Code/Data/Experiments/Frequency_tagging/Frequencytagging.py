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
from base64 import b16encode




def tagging(responserecogntion, chosen_words = 'hoi doei dag', frequency = 15, time = 2, color = '110'):
    root = tk.Tk()
    root.title('password')
    if responserecogntion == 'False':
        responserecogntion = False
    else:
        responserecogntion = True

    label = tk.Label(font=("Helvetica", 150),bg='black')
    label.pack(anchor=tk.CENTER, expand=tk.TRUE)

    with open('woorden.csv', newline='') as f:
        reader = csv.reader(f)
        allwords = list(reader)

    flatlist = []
    for sublist in allwords:
        for item in sublist:
            flatlist.append(item)
    words = flatlist
    random.shuffle(words)
    print(responserecogntion)
    if responserecogntion:
        words = words[:40]
    else:
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
    #Determine size and location of window
    window_width = 600
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)

    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    label.pack(anchor=tk.CENTER, expand=tk.TRUE)

#Background beun
######################################################

    
    period = int(1000/frequency)
    if responserecogntion:
        frame_rate = 30
    else:
        frame_rate = 60 #amount of ms that a screen is shown
    flash_rate = 15
    word_rate = 0.5
    frame_period = int(1000/frame_rate)
    flash_period = int(1000/flash_rate)
    flash_period = frame_period * round(flash_period / frame_period)
    word_period = int(1000/word_rate)
    word_period = flash_period * round(word_period / flash_period)
    frames_per_flash = int(flash_period/frame_period)
    flash_per_word = int(word_period/flash_period)
    total_backgrounds = frames_per_flash * flash_per_word
    print(total_backgrounds)
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

    backgrounds = []
    print(flash_per_word)
    for index, word in enumerate(words):
        if (int(index % 2) == 1 and responserecogntion) or (int(index % 2) == 0 and responserecogntion == False):
            for a in range(flash_per_word):
                for b in rgb_list:
                    backgrounds.append(b)
        else:
            for a in range(flash_per_word):
                for b in rgb_list:
                    backgrounds.append(f'#FFFFFF')
    bitjes = []
    print(len(backgrounds))
    for i, background in enumerate(backgrounds):
                textcolor = 'black'
                root.after(len(backgrounds) * period * 1000,lambda:root.destroy())
                label.after(int(i * frame_period), lambda c=background, t=textcolor: label.configure(bg = c, fg = t))
                root.attributes('-topmost', 1)
    print(word_period)
    for j,word in enumerate(words):
        label.after(int(word_period * j), lambda w=word: label.configure(text=w))
        if (j % 2 == 1 and responserecogntion) or (word in chosen_words):
            bitjes.append(1)
        elif word == ' ':
            pass
        else: 
            bitjes.append(0)
    if responserecogntion == False:
        words.remove(' ')
    #mainloop is used to run the window
    start_time = str(datetime.now())
    root.mainloop()
    
    return bitjes, start_time, words

