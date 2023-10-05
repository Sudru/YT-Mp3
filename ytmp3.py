#!/usr/bin/env python3

import os
import sys
import re
import requests
import getpass
import yt_dlp


# Function to get video URLs from a playlist URL
def getVideoUrls(url):
    try:
        req = requests.get(url)
        req.raise_for_status()
        content = req.text
        arr = re.findall(r"\/watch\?v\=.{11}", content)
        all_links = ["https://www.youtube.com" + a for a in arr]
        unique_links = list(set(all_links))
        print("Number of videos in the playlist: " + str(len(unique_links)))
        return unique_links
    except Exception as e:
        print(f"Error fetching video URLs: {e}")
        return []


# Function to download and save a YouTube video as an MP3 file
def downloadVideo(url, output_directory):
    try:
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(output_directory, "%(title)s.%(ext)s"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    except Exception as e:
        print(f"Error downloading video: {e}")


# Function to handle downloading for a single video or a playlist
def handleDownload(url, output_directory):
    if "playlist" in url:
        print("Downloading videos from playlist...")
        video_urls = getVideoUrls(url)
        for video_url in video_urls:
            downloadVideo(video_url, output_directory)
    else:
        downloadVideo(url, output_directory)


# Main function
def main():
    output_directory = "yt-mp3"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    if len(sys.argv) == 2:
        url = sys.argv[1]
    else:
        url = input("Enter the YouTube video URL or playlist URL: ")

    handleDownload(url, output_directory)


if __name__ == "__main__":
    main()
