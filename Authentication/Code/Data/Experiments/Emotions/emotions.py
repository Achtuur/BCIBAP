import tkinter as tk
import random
import csv
from datetime import datetime, timedelta
import numpy as np
import argparse
import os

my_parser = argparse.ArgumentParser(description="Code to run emotion experiment")
my_parser.add_argument('-disp',
                        required=False,
                        default=5,
                        metavar='-display time',
                        type=int,
                        help='The duration each word is shown'    
                    )
my_parser.add_argument('-len',
                        required=False,
                        default=10,
                        metavar='-length',
                        type=int,
                        help='The amount of words to show'    
                    )
my_parser.add_argument('-name',
                        required=True,
                        metavar='subject name',
                        type=str,
                        help='M or F followed by a number'  
                    )
my_parser.add_argument('-take',
                        required=True,
                        metavar='take',
                        type=str,
                        help='the nth time this experiment takes place' 
                    )
args = my_parser.parse_args()

duration = args.disp #time for each emotion in seconds
amount =  args.len #amount of emotions that is shown

emotions = ['amused','disgusted','sad','neutral']

data = []
bitjes = []
for j in range(0, amount):
    task = random.randint(0, len(emotions) - 1)
    data.append(emotions[task])
    bitjes.append(task)

#Showing the words
def refresh_label(label, word):
    label.configure(text=word)

root = tk.Tk()
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg='white')

label = tk.Label(text='', font=("Helvetica", 120))
label.pack(anchor=tk.CENTER, expand=tk.TRUE)

for i, emotion in enumerate(data):
    # binding word required because of the loop
    label.after(1000*duration * i, lambda w= emotion: label.configure(text=w))

date = str(datetime.now())[0:10]
filename = f'.\\timestamps\\{args.name}_{date}_emotions_take{args.take}'
if os.path.exists(f'{filename}.csv'):
    print('filename already exists')
    exit()


times = []
increment = timedelta(seconds = duration)
for j, i in enumerate(range(0, len(bitjes))):
    time = datetime.now() + increment * i
    times.append(time.strftime("%H:%M:%S.%f")[:12])


all_data = [data, bitjes, times]
all_data = np.array(all_data).T.tolist()

with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)
    

root.mainloop()
