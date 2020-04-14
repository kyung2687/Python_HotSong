import os
import time
import glob
import datetime
import subprocess

import pymongo
from pymongo import MongoClient
import pytube


##########
streamingcnt = 1
##########
program_start = time.time()
conn = MongoClient('127.0.0.1')

db = conn.admin
collect = db.songs
song_dir = "C:/Users/admin/Desktop/HotSong/python/mp3"

songs = collect.find({"streamingYN":False})
song_duration = 0 #int(song1["duration"]) + int(song2["duration"])
song = []

for index in range(0, streamingcnt):
    song.append(songs[index])

download_start = time.time()
for i, s in enumerate(song):
    print(s["title"] + " - " + s["singer"] + " : " + s["duration"])
    song_duration = song_duration + int(s["duration"]) 
    yt = pytube.YouTube(s["url"])
    mp4 = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    mp4.download(song_dir)
download_duration = int(time.time() - download_start)

print("Download_duration : " + str(download_duration))
print("Song     duration : " + str(song_duration))

_files = glob.glob(song_dir+'/*.mp4')
_files.sort(key=os.path.getmtime, reverse=False)

remove_files = glob.glob(song_dir+'/*')

def streaming() :
    for i, s in enumerate(_files) :
        os.system('\"' + _files[i] + '\"')
        time.sleep(int(song[i]["duration"]))
   
    for file in remove_files :
        os.remove(file)

if time.localtime().tm_wday==5 :
    print('today is holyday')
elif time.localtime().tm_wday==6 :
    print('today is holyday')
else :
    streaming()

program_duration = int(time.time() - program_start)

print("Program Duration : " + str(program_duration))