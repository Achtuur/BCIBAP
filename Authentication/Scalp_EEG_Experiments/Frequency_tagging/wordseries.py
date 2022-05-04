import csv
import random
import numpy as np
import tkinter as tk

tagged = ['penetratie','sam heeft een kleine piemel']
print(tagged)

with open('woorden.csv', newline='') as f:
    reader = csv.reader(f)
    echt = list(reader)

flat_list = []
for sublist in echt:
    for item in sublist:
        flat_list.append(item)
words = flat_list

for x in tagged:
  words.append(x)

random.shuffle(words)
print(words)

def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, word in enumerate(words):
    # binding word required because of the loop
    label.after(1000 * i, lambda w=word: label.configure(text=w))

root.mainloop()