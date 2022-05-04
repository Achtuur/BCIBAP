import time
import threading
import tkinter as tk
import csv

with open('wordlist4.csv', newline='') as f:
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

root.mainloop()