import tkinter as tk
import random
from datetime import datetime, timedelta
import csv
import os.path
import numpy as np
from pathlib import Path

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

    
filename = 'Simon_17-05-2022_mt_take4'

filename = Path(f'.\\tasklists\\{filename}')



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
