import tkinter as tk
import random
from datetime import datetime, timedelta
import csv
import os.path
import numpy as np

amount = 10 #amount of tasks that will be shown on the screen
duration = 5 #duration of each task in seconds
tasks = ['Solve sums ', 'Rotate object ', 'Imagine finger movement ', 'Imagine song '] #tasks that are shown on screen

data = ['0'] * amount

k = list(range(0,amount))
for j in k:
    task = random.randint(0,len(tasks) - 1)
    data[j] = tasks[task]
    
filename = str(datetime.now())
filename = filename.replace("/", "-")
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")

filename = f'.\\tasklists\\data_{str(filename)}'
fo = open(filename, "w")
fo.close()


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

all_data = [data, times]
all_data = np.array(all_data).T.tolist()

with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)

root.mainloop()
