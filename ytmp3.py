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
    return unique_link


def downloadSong(url):
    yt = YouTube(url)
    

    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    
    destination = './yt-download/'

    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)    

    # result of success
    print("Download Completed!!\n" + out_file.split('/')[-1]+'\n')


#main implementation
if len(sys.argv) == 2:
    url = sys.argv[1]
else:
    url = str(input("Enter the Song or Playlist Url:\n"))


if "playlist" in url:
    print("Downloading Playlist")
    song_list = getVideoUrls(url)
    for song in song_list:
        downloadSong(song)

else:
    print("Downloading Mp3")
    downloadSong(url)

print("\nDownload Location: \n"+os.getcwd()+'/yt-download/')
