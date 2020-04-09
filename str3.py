import os
import time
import glob
import datetime

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
song3 = collect.find({"streamingYN":False})[2]

print(song1["title"] + " - " + song1["singer"] + " : " + song1["url"])
print(song2["title"] + " - " + song2["singer"] + " : " + song2["url"])
print(song3["title"] + " - " + song3["singer"] + " : " + song3["url"])

def download(url):
    yt = pytube.YouTube(url)
    yt.streams.filter(only_audio=True).first().download(song_dir)

download_start = time.time()
download(song3["url"])
download(song2["url"])
download(song1["url"])
download_duration = int(time.time() - download_start)

print("Download_duration : " + str(download_duration))

song_duration = int(song1["duration"]) + int(song2["duration"]) + int(song3["duration"])
print("Song     duration : " + str(song_duration))

_files = glob.glob(song_dir+'/*')
_files.sort(key=os.path.getmtime, reverse=True)

def streaming() :
    os.system('\"' + _files[0] + '\"')
    time.sleep(int(song1["duration"]))
    collect.update_one(song1, { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )
    
    os.system('\"' + _files[1] + '\"')
    time.sleep(int(song2["duration"]))
    collect.update_one(song2, { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )

    os.system('\"' + _files[2] + '\"')
    time.sleep(int(song3["duration"]))
    collect.update_one(song3, { "$set": {"streamingYN":True, "up_date":datetime.datetime.now().strftime('%Y-%m-%d')}} )

    os.remove(_files[0])
    os.remove(_files[1])
    os.remove(_files[2])


if time.localtime().tm_wday==5 :
    print('today is holyday')
elif time.localtime().tm_wday==6 :
    print('today is holyday')
else :
    time.sleep(1200 - download_duration - song_duration - 5)
    streaming()


program_duration = int(time.time() - program_start)

print("Program Duration : " + str(program_duration))