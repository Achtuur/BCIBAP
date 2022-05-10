import tkinter as tk
import random
from datetime import datetime
import csv
import os.path


tasks = ['Solve_sums ', 'Rotate_object ', 'Imagine_finger_movement ', 'Imagine song ']

data = ['0'] * 11
data[0] = datetime.now()
data[0] = data[0].strftime("%d/%m/%Y %H:%M:%S")

k = list(range(1,11))
for j in k:
    task = random.randint(0,3)
    task = tasks[task]
    data[j] = task
    
print(data)
data[0] = data[0].replace("/", "-")
data[0] = data[0].replace(" ", "_")
data[0] = data[0].replace(":", "-")

filename = f'.\\tasklists\\tasklist_{str(data[0])}.txt'
#print(filename)
fo = open(filename, "w")
fo.close()
data_tekst = ''.join(data)
data_tekst = data_tekst.replace(' ', '\n')

with open(filename, 'w', newline ='') as f:
    f.write(data_tekst)

data[0] = 'Execute mental tasks'
j = 0
for i in data:
    data[j] = i.replace('_', ' ')
    j = j + 1


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
    label.after(10000 * i, lambda w=word: label.configure(text=w))

root.mainloop()
