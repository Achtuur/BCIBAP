import csv
import random
import numpy as np
import tkinter as tk
from datetime import datetime
from datetime import timedelta

length = 20 #amount of words shown, maximum 50
duration = 5 #Duration each word is shown in seconds
tagged = ['schoenveter','papier'] #passwords that were tagged for subject

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
print(words)

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

#Make filename
filename = str(datetime.now())
filename = filename.replace("/", "-")
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")

filename = f'.\\timestamps\\data_{str(filename)}'
fo = open(filename, "w")
fo.close()

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