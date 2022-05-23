import csv
import random
import numpy as np
import tkinter as tk
from datetime import datetime
from datetime import timedelta
import os
from pathlib import Path

# This is to easily run the script from the command line
# [] = optional
# Usage: python wordseries.py -pw1 password1 -pw2 password2 -file filename [-wl] amount_of_words [-dur] word_duration
import argparse

# Create parser
my_parser = argparse.ArgumentParser(description="Code to run frequency tagging experiment")
my_parser.add_argument('-pw1',
                        required=True,
                        metavar='-password 1',
                        type=str,
                        help='The 1st password to tag'    
                    )

my_parser.add_argument('-pw2',
                        required=True,
                        metavar='-password 2',
                        type=str,
                        help='The 2nd password to tag'    
                    )

my_parser.add_argument('-name', 
                        required=True,
                        metavar='subject',
                        type=str,
                        help='The name of the subject'
)

my_parser.add_argument('-wl',
                        required=False,
                        metavar='-amount of words',
                        type=int,
                        help='The amount of words to show',
                        default=20
                    )
my_parser.add_argument('-dur',
                        required=False,
                        metavar='-word duration',
                        type=int,
                        help='The duration of each word',
                        default=5
                    )
my_parser.add_argument('-take',
                        required=True,
                        metavar='take',
                        type=str,
                        help='the nth time this experiment takes place' 
                    )

args = my_parser.parse_args()

length = args.wl 
duration = args.dur
tagged = [args.pw1, args.pw2] #passwords that were tagged for subject

with open('woorden.csv', newline='') as f:
    reader = csv.reader(f)
    echt = list(reader)

flat_list = []
for sublist in echt:
    for item in sublist:
        flat_list.append(item)
words = flat_list

random.shuffle(words)
words =  words[:length]

for x in tagged:
  words.append(x) 
  


random.shuffle(words)
# print(words)

bitjes = [0] * len(words)
j = 0 
for i in words:
    if i in tagged:
        bitjes[j] = 1
    else:
        bitjes[j] = 0
    j = j + 1




def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, word in enumerate(words):
    # binding word required because of the loop
    label.after(1000*duration * i, lambda w=word: label.configure(text=w))

#Make list to show what words were tagged 
bitjes = [0] * len(words)
j = 0 
for i in words:
    if i in tagged:
        bitjes[j] = 1
    else:
        bitjes[j] = 0
    j = j + 1

date = str(datetime.now())[0:10]
filename = f'.\\results\\{args.name}_{date}_ft_take{args.take}'
if os.path.exists(f'{filename}.csv'):
    print('filename already exists')
    exit()


#Create timestamps for words
times = [0] * len(words)
increment = timedelta(seconds = duration)
j = 0
for i in range(0, len(words)):
    time = datetime.now() + increment * i
    times[j] = time.strftime("%H:%M:%S.%f")
    times[j] = times[j][:12]
    j = j + 1

all_data = [words, bitjes, times]
all_data = np.array(all_data).T.tolist()

with open(f'{filename}.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)

root.mainloop()