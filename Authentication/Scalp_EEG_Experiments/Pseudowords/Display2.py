import time
import threading
import tkinter as tk
import csv
from datetime import datetime
from datetime import timedelta


with open('wordlist1.csv', newline='') as f:
    reader = csv.reader(f)
    words = list(reader)

def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, word in enumerate(words):
    # binding word required because of the loop
    label.after(5000 * i, lambda w=word: label.configure(text=w))


times = [0] * 51

increment = timedelta(seconds = 5)
j = 0
for i in times:
    time = datetime.now() + increment * i
    times[j] = time.strftime("%H:%M:%S")
    j = j + 1

print(times)

filename = str(datetime.now())
filename = filename.replace("/", "-")
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")

filename = f'.\\timestamps\\timestamps_{str(filename)}.txt'
fo = open(filename, "w")
fo.close()

data_tekst = ''.join(times)
data_tekst = data_tekst.replace(' ', '\n')

with open(filename, 'w', newline ='') as f:
    f.write(data_tekst)

root.mainloop()