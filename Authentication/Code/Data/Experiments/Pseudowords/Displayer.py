import time
import threading
import tkinter as tk
import csv
from datetime import datetime
from datetime import timedelta
import numpy as np
from Listgenerator import listgenerator
from pathlib import Path
import os
from functools import partial

# This is to easily run the script from the command line
# [] = optional
# Usage: python Frequencytagging.py -pw password -freq frequency [-time] time
import argparse

# Create parser


def Displayer(length = 40, display_time = 1, filename = 'error', orderd = True, pseudo = False):
    root = tk.Tk()
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
    root.configure(bg='')

    frame = tk.Frame(root)
    frame.pack()

    slider_label = tk.Label(frame, text = 'randomize:')
    slider_label.pack(side = tk.LEFT)
    slider = tk.Scale(
    frame,
    from_=0,
    to=1,
    orient='horizontal',  # horizontal
    )   
    slider.pack(side = tk.LEFT)

    L1 = tk.Label(frame, text="Amount of words:")
    L1.pack( side = tk.LEFT)
    E1 = tk.Entry(frame, bd =5)
    E1.pack(side = tk.LEFT)

    L2 = tk.Label(frame, text="Amount of miliseconds:")
    L2.pack( side = tk.LEFT)
    E2 = tk.Entry(frame, bd =5)
    E2.pack(side = tk.LEFT)

    L3 = tk.Label(frame, text="Filename:")
    L3.pack( side = tk.LEFT)
    E3 = tk.Entry(frame, bd =5)
    E3.pack(side = tk.LEFT)



    def displaytkinter(length, display_time, filename, orderd):
        orderd = slider.get()
        print(orderd)
        if orderd == 1:
            orderd = False
        else:
            orderd = True
        length = int(E1.get()) 
        display_time = int(E2.get())
        filename = E3.get()
        print(filename)
        print(length)

        
        words, bitjes = listgenerator(length, orderd)
        def refresh_label(label, word):
            label.configure(text=word)



        label = tk.Label(text='', font=("Helvetica", 120))
        label.pack(anchor=tk.CENTER, expand=tk.TRUE)

        for i, word in enumerate(words):
            # binding word required because of the loop
            label.after(display_time * i, lambda w=word: label.configure(text=w, padx= 800))

        times = []

        increment = timedelta(milliseconds = display_time)
        j = 0
        for index in range(length):
            time = datetime.now() + increment * index
            times.append(time.strftime("%H:%M:%S.%f")[:12])



        date = str(datetime.now())[0:10]
        filename = f'.\\results\\{filename}'
        if os.path.exists(f'\\results{filename}.csv'):
            print('filename already exists')
            exit()


        all_data = [words, bitjes, times]

        all_data = np.array(all_data).T.tolist()
            


        with open(f'{filename}.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerows(all_data)


    
    showwords = tk.Button(frame,
                text="Start",
                command=partial(displaytkinter, length, display_time, filename, orderd))
    showwords.pack(side=tk.LEFT)



    root.mainloop()
       
    
    return 

if __name__ == '__main__':
    Displayer()


        