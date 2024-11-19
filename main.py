import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
from pytube.cli import on_progress
import argparse
from DownloadModule import DownloadModule
#path data

def main(argv):
    # argv is url of youtube video
    # -v = download video only
    # -a = download audio only
    # -c = combine video and audio
    # -t = download thumbnail only
    
    # use argparse to parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of youtube video", nargs="?") # nargs="?" means that it is optional
    parser.add_argument("-v", "--video", help="download video only", action="store_true")
    parser.add_argument("-a", "--audio", help="download audio only", action="store_true")
    parser.add_argument("-c", "--combine", help="combine video and audio", action="store_true")
    parser.add_argument("-t", "--thumbnail", help="download thumbnail only", action="store_true")
    args = parser.parse_args()
    all = False

    # if args.url does not exist, ask for url
    if not args.url:
        args.url = input("> Enter url of youtube video : ")
    # check if url is valid
    if not args.url.startswith("https://www.youtube.com/watch?v="):
        if args.url.startswith("https://youtube.com/shorts/"):
            args.url = args.url.replace("https://youtube.com/shorts/", "https://www.youtube.com/watch?v=")
        else:
            print("> Invalid url, please enter a valid youtube video url")
            return
    
    video_url = args.url
    downloader = DownloadModule(video_url)
    
    # if no args given, all is true
    if not args.video and not args.audio and not args.combine and not args.thumbnail:
        all = True
    
    # check if result folder exists
    if not os.path.exists(downloader.result_folder):
        os.mkdir(downloader.result_folder)

    
    # check if video_key directory exists
    if not os.path.exists(os.path.join(downloader.result_folder, downloader.video_key)):
        os.mkdir(os.path.join(downloader.result_folder, downloader.video_key))

    # check if video is requested
    if args.video or args.combine or all:
        downloader.download_video()
    
    # check if audio is requested
    if args.audio or args.combine or all:
        downloader.download_audio()
        #download_audio(video_key=video_key, youtube=youtube)
    
    # check if combine is requested
    if args.combine or all:
        downloader.combine_video()
        #combine_video(video_key=video_key)
    
    # check if thumbnail is requested
    if args.thumbnail or all:
        downloader.download_thumbnail()
        #download_thumbnail(video_key=video_key, video_key=video_key)
    
    print(f"> Done downloading from {video_url}")

if __name__ == "__main__":
    main(sys.argv)
