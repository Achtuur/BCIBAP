from playsound import playsound
from pydub import AudioSegment
import random
import os
import os.path
import time
from datetime import datetime
import numpy as np
import csv

#change parameters of experiment
songs_amount = 8 #amount of songs in the songs folder
songtime = 5 #duration of song in seconds, max number is duration of song minus a minute
pause = 5 #time between song fragments, at least 3
known_song = 8 #number of the song that is known by the user

amount = list(range(1,songs_amount + 1))
songs = [0] * songs_amount
j = 0

for i in amount:
    start = random.randint(0,60)
    starttime = 60*1000 + start*1000
    endtime = 60*1000 + (start + songtime)*1000
    #print(starttime)
    #print(endtime)
    filename = ".\songs\Song"
    #print(filename)s
    filename = [filename, str(i), '.mp3']
    filename = ''.join(filename)
    #print(filename)
    filename = os.path.abspath(os.path.join(os.getcwd(), filename))
    #print(filename)
    sound = AudioSegment.from_mp3(filename)
    songs[j] = sound[starttime:endtime]
    newname = ['song', str(i), '.mp3']
    newname = ''.join(newname)
    songs[j].export(newname, format="mp3")
    j = j + 1

data = [0] * songs_amount

filename = datetime.now()
filename = filename.strftime("%d/%m/%Y %H:%M:%S")
filename = filename.replace("/", "-")
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")

times = [0] * songs_amount
bitjes = [0] * songs_amount
j = 0
random.shuffle(amount)
for i in amount:
    songname = ['song', str(i), '.mp3']
    songname = ''.join(songname)
    if songname == f'song{known_song}.mp3':
        bitjes[j] = 1
    else:
        bitjes[j] = 0
    data[j] = songname
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    times[j] = datetime.now()
    times[j] = times[j].strftime("%H:%M:%S.%f")[:12]
    playsound(songname)
    time.sleep(pause - 3)
    j = j + 1 

all_data = [data, times, bitjes]
all_data = np.array(all_data).T.tolist()

filename = str(datetime.now())
filename = filename.replace("/", "-")
filename = filename.replace(" ", "_")
filename = filename.replace(":", "-")
filename = f'.\song_lists\songlist_{filename}'
data_tekst = ''.join(data)

with open(f'{filename}.csv', 'w') as f:
      
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)