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

# This is to easily run the script from the command line
# [] = optional
# Usage: python Frequencytagging.py -pw password -freq frequency [-time] time
import argparse

# Create parser
my_parser = argparse.ArgumentParser(description="Code to run pseudowords experiment")
my_parser.add_argument('-disp',
                        required=False,
                        default=5,
                        metavar='-display time',
                        type=int,
                        help='The duration each word is shown'    
                    )
my_parser.add_argument('-len',
                        required=False,
                        default=50,
                        metavar='-length',
                        type=int,
                        help='The amount of words to show'    
                    )
my_parser.add_argument('-name',
                        required=True,
                        metavar='subject name',
                        type=str,
                        help='The file name'
)
my_parser.add_argument('-take',
                        required=True,
                        metavar='take',
                        type=str,
                        help='the nth time this experiment takes place' 
                    )
args = my_parser.parse_args()

display_time = args.disp 
length = args.len
words, bitjes = listgenerator(length)

def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, word in enumerate(words):
    # binding word required because of the loop
    label.after(display_time*1000 * i, lambda w=word: label.configure(text=w))

times = [0] * length

increment = timedelta(seconds = display_time)
j = 0
for i in range(0, len(words)):
    time = datetime.now() + increment * i
    times[j] = time.strftime("%H:%M:%S.%f")
    times[j] = times[j][:12]
    j = j + 1


date = str(datetime.now())[0:10]
filename = f'.\\results\\{args.name}_{date}_pseudo_take{args.take}'
if os.path.exists(f'{filename}.csv'):
    print('filename already exists')
    exit()


all_data = [words, bitjes, times]

all_data = np.array(all_data).T.tolist()
    


with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)

root.mainloop()