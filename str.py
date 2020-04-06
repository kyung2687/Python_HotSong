import os
import time
import glob

import pymongo
from pymongo import MongoClient
import pytube

conn = MongoClient('127.0.0.1')

db = conn.admin
collect = db.songs
song_dir = "C:/Users/admin/Desktop/HotSong/python/mp3"

duration1 = int(collect.find({"streamingYN":False})[0]["duration"])
duration2 = int(collect.find({"streamingYN":False})[1]["duration"])
duration = duration1 + duration2
print(600 - duration)

def streaming() :
    result = collect.find_one({"streamingYN":False})
    if(str(type(result)) == "<class 'NoneType'>"):
        print('null sinsong')
    else: 
        print(result["url"] + " : " + result["duration"])
        download(result["url"])
        _file = glob.glob(song_dir+'/*')[0]
        print(_file)
        os.system('\"' + _file + '\"')
        time.sleep(int(result["duration"]))
        os.remove(_file)
        collect.update_one(result, { "$set": {"streamingYN":True}} )

def download(url) :
    yt = pytube.YouTube(url)
    print(yt.streams.filter(only_audio=True).all())
    yt.streams.filter(only_audio=True).first().download(song_dir)

if time.localtime().tm_wday==5 :
    print('today is holyday')
elif time.localtime().tm_wday==6 :
    print('today is holyday')
else :
    time.sleep(600-(duration+10))
    streaming()
    streaming()


#files = glob.glob(song_dir+'/*')
#files.sort(key=os.path.getmtime, reverse=False)
#
#print(files[0])
#for file in files:
#    print(file)
#    os.system('\"' + file + '\"')
#    time.sleep(10)
#    os.remove(file)