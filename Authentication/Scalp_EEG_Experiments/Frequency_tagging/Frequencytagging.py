import tkinter as tk
from tkinter import ttk
import numpy as np

#Information for tagging
password = 'Octopus' #Fill in your password here
time = 30 #Fill in the duration of the tagging in seconds
frequency = 6 #Fill in the frequency of the flashing background in Hz

root = tk.Tk()
root.title('Password')

label = tk.Label(text = password, font=("Helvetica", 200),bg='black')
label.pack(anchor=tk.CENTER, expand=tk.TRUE)


#Determine size and location of window

window_width = 600
window_height = 100
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)


period = int((1/frequency) * 1000)
print(period)

flashes = np.array(range(0,time*frequency))

backgrounds = [0] * len(flashes)
for i in flashes:
    if i % 2 == 0:
         backgrounds[i] = 'black'
    else:
        backgrounds[i] = 'white'

print(backgrounds)

for i, background in enumerate(flashes):
    print(i)
    background = backgrounds[i]
    textcolor = backgrounds[i - 1]
    label.after(period * i, lambda c=background, t=textcolor: label.configure(text=password,bg = c, fg = t))
    root.attributes('-topmost', 1)

#mainloop is used to run the window
root.mainloop()