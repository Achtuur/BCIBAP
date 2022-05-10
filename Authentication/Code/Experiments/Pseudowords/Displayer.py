import time
import threading
import tkinter as tk
import csv
from datetime import datetime
from datetime import timedelta
import numpy as np
from Listgenerator import listgenerator


display_time = 5 #Display time for each word in seconds
length = 50 #lenght of wordlist, maximum 50
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

print(times)


filename = str(datetime.now())
filename = filename.replace("/", "-") 
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")

filename = f'.\\timestamps\\data_{str(filename)}'
fo = open(filename, "w")
fo.close()

all_data = [words, bitjes, times]

all_data = np.array(all_data).T.tolist()
    


with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)

root.mainloop()