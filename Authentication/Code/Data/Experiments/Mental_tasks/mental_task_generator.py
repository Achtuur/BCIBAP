import tkinter as tk
import random
from datetime import datetime, timedelta
import csv
import os.path
import numpy as np
from pathlib import Path
import argparse

my_parser = argparse.ArgumentParser(description="Code to run mental task experiment")
my_parser.add_argument('-disp',
                        required=False,
                        default=5,
                        metavar='-display time',
                        type=int,
                        help='The duration each word is shown'    
                    )
my_parser.add_argument('-len',
                        required=False,
                        default=10,
                        metavar='-length',
                        type=int,
                        help='The amount of words to show'    
                    )
my_parser.add_argument('-name',
                        required=True,
                        metavar='subject name',
                        type=str,
                        help='M or F followed by a number'  
                    )
my_parser.add_argument('-take',
                        required=True,
                        metavar='take',
                        type=str,
                        help='the nth time this experiment takes place' 
                    )
args = my_parser.parse_args()

amount = 10 #amount of tasks that will be shown on the screen
duration = 5 #duration of each task in seconds
tasks = ['Solve sums ', 'Rotate object ', 'Imagine finger movement ', 'Imagine song '] #tasks that are shown on screen


data = ['0'] * (amount + 1)
data[-1] = 'FINISHED'
bitjes = [0] * amount #sums = 0, rotate = 1, imagine movement = 2, imagine song = 3

k = list(range(0,amount))
for j in k:
    task = random.randint(0,len(tasks) - 1)
    data[j] = tasks[task]
    if data[j] == 'Solve sums ':
        bitjes[j] = 0
    elif data[j] == 'Rotate object ':
        bitjes[j] = 1
    elif data[j] == 'Imagine finger movement ':
        bitjes[j] = 2
    elif data[j] == 'Imagine song ':
        bitjes[j] = 3
    else:
        bitjes[j] = ''

    
date = str(datetime.now())[0:10]
filename = f'.\\tasklists\\{args.name}_{date}_mt_take{args.take}'
if os.path.exists(f'{filename}.csv'):
    print('filename already exists')
    exit()



#Showing the words
def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='white')

label = tk.Label(text='', font=("Helvetica", 60))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, word in enumerate(data):
    # binding word required because of the loop
    label.after(1000*duration * i, lambda w=word: label.configure(text=w))

#Create timestamps for words
times = [0] * len(data)
increment = timedelta(seconds = duration)
j = 0
for i in range(0, len(data)):
    time = datetime.now() + increment * i
    times[j] = time.strftime("%H:%M:%S.%f")
    times[j] = times[j][:12]
    j = j + 1

all_data = [data, bitjes, times]
all_data = np.array(all_data).T.tolist()

with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)

root.mainloop()
