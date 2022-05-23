from playsound import playsound
from pydub import AudioSegment
import random
import os
import os.path
import time
from datetime import datetime
import numpy as np
import csv
from pathlib import Path

# This is to easily run the script from the command line
# [] = optional
# Usage: python Music.py -name file_name -known known_song [-time] time [-song_dur] song_duration
import argparse

# Create parser
my_parser = argparse.ArgumentParser(description="Code to run music experiment")
my_parser.add_argument('-song_dur',
                        required=False,
                        default=5,
                        metavar='duration song sample',
                        type=int,
                        help='The duration each sample is played'    
                    )
my_parser.add_argument('-pause',
                        required=False,
                        default=5,
                        metavar='pause',
                        type=int,
                        help='The pause between each sample'    
                    )
my_parser.add_argument('-name',
                        required=True,
                        metavar='file name',
                        type=str,
                        help='The file name'
)
my_parser.add_argument('-known',
                        required=True,
                        metavar='known song',
                        type=str,
                        help='The number of the known song'
)
my_parser.add_argument('-take',
                        required=True,
                        metavar='take',
                        type=str,
                        help='the nth time this experiment takes place' 
                    )
args = my_parser.parse_args()

def get_song_amount():
    song_dir = Path('./songs')
    files = os.listdir(song_dir)

    # Get list of all files which contain .mp3 and subtract 
    num_songs = len([x for x in files if ".mp3" in x])
    return num_songs


#change parameters of experiment
songs_amount = get_song_amount() #amount of songs in the songs folder
songtime = args.song_dur #duration of song in seconds, max number is duration of song minus a minute
pause = args.pause #time between song fragments, at least 3
known_songs = args.known #number of the song that is known by the user
known_songs = list(known_songs)
songs = [0 for i in range(songs_amount)]

for i in range(1, songs_amount + 1):
    start = random.randint(0,60)
    starttime = 60*1000 + start*1000
    endtime = 60*1000 + (start + songtime)*1000
    filename = Path(f"./songs/Song{str(i)}.mp3")
    sound = AudioSegment.from_mp3(filename)
    songs[i-1] = sound[starttime:endtime]
    newname = Path(f'./songs/song_samples/song{str(i)}.mp3')
    songs[i-1].export(newname, format="mp3")

data = [0 for i in range(songs_amount)]

file = Path('./experiment_song_order')

date = str(datetime.now())[0:10]
filename = f'.\\results\\{args.name}_{date}_music_take{args.take}'
if os.path.exists(f'{filename}.csv'):
    print('filename already exists')
    exit()

times = [0 for i in range(songs_amount)]
bitjes = [0 for i in range(songs_amount)]
j = 0
exp_song_order = [i for i in range(1, songs_amount+1)]
random.shuffle(exp_song_order)
for index, num in enumerate(exp_song_order):
    songname = Path(f'./songs/song_samples/song{str(num)}.mp3')
    if str(num) in known_songs:
        bitjes[index] = 1
    else:
        bitjes[index] = 0
    data[index] = songname.stem
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    times[index] = datetime.now()
    times[index] = times[index].strftime("%H:%M:%S.%f")[:12]
    playsound(songname)
    time.sleep(pause - 3)

all_data = [data, bitjes, times]
all_data = np.array(all_data).T.tolist()


file = Path(f'{filename}.csv')
with open(file, 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(all_data)