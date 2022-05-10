import tkinter as tk
import random

amount = 4 #number of emotions that is remembered
time = 5 #time for each emotion in seconds

emotions = list(range(0,amount))

#Showing the words
def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='white')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i in emotions:
    # binding word required because of the loop
    label.after(1000*time * i, lambda w= f'Emotion {i + 1}': label.configure(text=w))

root.mainloop()
