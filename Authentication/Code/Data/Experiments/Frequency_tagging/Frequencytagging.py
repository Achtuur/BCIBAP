import tkinter as tk
from tkinter import ttk
import numpy as np
from datetime import datetime

# This is to easily run the script from the command line
# [] = optional
# Usage: python Frequencytagging.py -pw password -freq frequency [-time] time
import argparse

# Create parser
my_parser = argparse.ArgumentParser(description="Code to frequency tag a password")
my_parser.add_argument('-pw',
                        required=True,
                        metavar='-password',
                        type=str,
                        help='The password to tag'    
                    )
my_parser.add_argument('-freq',
                        required=True,
                        metavar='-frequency',
                        type=int,
                        help='The frequency of the tagged password'    
                    )
my_parser.add_argument('-time',
                        required=False,
                        metavar='-time',
                        type=int,
                        help='The duration of the tagging',
                        default=15
)
args = my_parser.parse_args()

#Information for tagging
password = args.pw
time = args.time
frequency = args.freq

print(f'Password: {password}, Frequency: {frequency}, Time')

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

flashes = np.array(range(0,time*frequency))

backgrounds = [0] * len(flashes)
for i in flashes:
    if i % 2 == 0:
         backgrounds[i] = 'black'
    else:
        backgrounds[i] = 'white'


for i, background in enumerate(flashes):
    # print(i)
    background = backgrounds[i]
    textcolor = backgrounds[i - 1]
    label.after(period * i, lambda c=background, t=textcolor: label.configure(text=password,bg = c, fg = t))
    root.attributes('-topmost', 1)

#mainloop is used to run the window
root.mainloop()