import tkinter as tk
import random
import csv
from datetime import datetime, timedelta
import numpy as np

duration = 5 #time for each emotion in seconds
amount =  4 #amount of emotions that is shown
test = 1

emotions = [0] * amount

if test == 0:
    for i in range(amount):
        print(f'Emotion {i + 1}')
        emotions[i] = input()
else:
    print('test')
    

#Showing the words
def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='white')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, emotion in enumerate(emotions):
    # binding word required because of the loop
    label.after(1000*duration * i, lambda w= emotion: label.configure(text=w))

filename = 'Simon_17-05-2022_em_test'

filename = f'.\\timestamps\\{filename}'
fo = open(filename, "w")
fo.close()

times = [0] * len(emotions)
increment = timedelta(seconds = duration)
j = 0
for i in range(0, len(emotions)):
    time = datetime.now() + increment * i
    times[j] = time.strftime("%H:%M:%S.%f")
    times[j] = times[j][:12]
    j = j + 1

bitjes = [0] * len(emotions)
all_data = [emotions, bitjes, times]
all_data = np.array(all_data).T.tolist()

with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)
    

root.mainloop()
