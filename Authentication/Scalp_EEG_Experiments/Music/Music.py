from playsound import playsound
from pydub import AudioSegment
# AudioSegment.converter = "C:\ffmpeg\bin\ffmpeg.exe"
# AudioSegment.ffmpeg = "C:\ffmpeg\bin\ffmpeg.exe"
# AudioSegment.ffprobe ="C:\ffmpeg\bin\ffprobe.exe"
import random
import os
import os.path
import time

#change parameters of experiment
songs = 5 #amount of songs in the songs folder
songtime = 2 #duration of song in seconds, max number is duration of song minus a minute
pause = 5 #time between song fragments

amount = list(range(1,songs + 1))
songs = [0] * songs
j = 0

for i in amount:
    start = random.randint(0,60)
    starttime = 60*1000 + start*1000
    endtime = 60*1000 + (start + songtime)*1000
    #print(starttime)
    #print(endtime)
    filename = ".\songs\Song"
    #print(filename)
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

random.shuffle(amount)
for i in amount:
    filename = ['song', str(i), '.mp3']
    filename = ''.join(filename)
    print(filename)
    print('3')
    time.sleep(1)
    print('2')
    time.sleep(1)
    print('1')
    playsound(filename)
    time.sleep(pause)


# p = vlc.MediaPlayer(songs[j])
#     p.play()
#     time.sleep(5)