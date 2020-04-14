import os
import time
import glob
import datetime
import subprocess

import pymongo
from pymongo import MongoClient
import pytube


##########
streamingcnt = 2
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
    mp4 = yt.streams.filter(only_audio=True).first()
    mp4.download(song_dir)
    os.system('ffmpeg -i \"' + os.path.join(song_dir, mp4.default_filename) + '\" \"' + os.path.join(song_dir, str(i+1)+'.mp3') + '\"')
download_duration = int(time.time() - download_start)

print("Download_duration : " + str(download_duration))
print("Song     duration : " + str(song_duration))


_files = glob.glob(song_dir+'/*.mp3')
_files.sort(key=os.path.getmtime, reverse=False)

remove_files = glob.glob(song_dir+'/*')

def streaming() :
    for i, s in enumerate(_files) :
        streamdata = db.streamings.find({})[0]
        db.streamings.update_one(streamdata, { "$set": {"str":True, "song": song[i]}} )
        os.system('\"' + _files[i] + '\"')
        time.sleep(int(song[i]["duration"]))
        collect.update_one(song[i], { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )
    
    streamdata = db.streamings.find({})[0]
    db.streamings.update_one(streamdata, { "$set": {"str":False, "song": {}}})
    for file in remove_files :
        os.remove(file)

if time.localtime().tm_wday==5 :
    print('today is holyday')
elif time.localtime().tm_wday==6 :
    print('today is holyday')
else :
    time.sleep(900 - download_duration - song_duration - 3)
    streaming()

program_duration = int(time.time() - program_start)

print("Program Duration : " + str(program_duration))