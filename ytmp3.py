#!/usr/bin/env python3

from pytube import YouTube
import os
import sys
import re
import requests


def getVideoUrls(url):
    print("Getting Individual Video links...")
    req = requests.get(url)
    content = req.text   
    arr = (re.findall('\/watch\?v\=.{11}', content))    
    all_links = ["https://www.youtube.com"+a for a in arr]
    unique_link = list(dict.fromkeys(all_links))
    print("length:"+str(len(unique_link)))
    return unique_link


def downloadSong(url):
    yt = YouTube(url)   


    # extract only audio
    
    title = yt.title.replace('|','').replace('.','')
    destination = './yt-mp3/'
    if(title not in local_songs):
        video = yt.streams.filter(only_audio=True).first()
        # download the file
        out_file = video.download(output_path=destination)
        
        # save the file
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file) 
        

        # result of success
        print("Download Completed!!\n" + base.split('/')[-1]+"\n\n")
    else:
        print("Skipped: " + title)

#main implementation

local_songs=[]
if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    url = str(input("Enter the Song or Playlist Url:\n"))

# list the downloaded songs
this_dir = os.listdir('.')
if("yt-mp3" in this_dir):
    all_songs = os.listdir('./yt-mp3')
    local_songs = [song.split('.')[0] for song in all_songs]


if "playlist" in url:
    print("Downloading Playlist....")
    song_list = getVideoUrls(url)
    for song in song_list:
        downloadSong(song)

else:
    print("Downloading Mp3....")
    downloadSong(url)

print("\nDownload Location: \n"+os.getcwd()+'/yt-mp3/')
