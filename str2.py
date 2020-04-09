import os
import time
import glob
import datetime
import subprocess

import pymongo
from pymongo import MongoClient
import pytube

program_start = time.time()
conn = MongoClient('127.0.0.1')

db = conn.admin
collect = db.songs
song_dir = "C:/Users/admin/Desktop/HotSong/python/mp3"

song1 = collect.find({"streamingYN":False})[0]
song2 = collect.find({"streamingYN":False})[1]

print(song1["title"] + " - " + song1["singer"] + " : " + song1["url"])
print(song2["title"] + " - " + song2["singer"] + " : " + song2["url"])

def download(url, title):
    yt = pytube.YouTube(url)
    mp4 = yt.streams.filter(only_audio=True).first()
    mp4.download(song_dir)
    print(os.path.join('.\mp3', mp4.default_filename))
    os.system('ffmpeg -i \"' + os.path.join('.\mp3', mp4.default_filename) + '\" \"' + os.path.join('.\mp3', title) + '\"')
    #print('ffmpeg -i '+song_dir+'/\"'+mp4.default_filename+'\" '+song_dir+'/'+title )
    

download_start = time.time()
download(song2["url"], "1.mp3")
download(song1["url"], "2.mp3")
download_duration = int(time.time() - download_start)

print("Download_duration : " + str(download_duration))

song_duration = int(song1["duration"]) + int(song2["duration"])
print("Song     duration : " + str(song_duration))

_files = glob.glob(song_dir+'/*.mp3')
_files.sort(key=os.path.getmtime, reverse=True)

remove_files = glob.glob(song_dir+'/*')

def streaming() :
    os.system('\"' + _files[0] + '\"')
    time.sleep(int(song1["duration"]))
    collect.update_one(song1, { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )
    
    os.system('\"' + _files[1] + '\"')
    time.sleep(int(song2["duration"]))
    collect.update_one(song2, { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )

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