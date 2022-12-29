import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
import argparse

# Global variables
pbar = None
downloaded = 0
filesize = 0
pwd = os.getcwd()
result_folder = os.path.join(pwd, "results")
video_key = ""
video_url = ""

# Path: main.py
def main(argv):
    # argv is url of youtube video
    # -v = download video only
    # -a = download audio only
    # -c = combine video and audio
    # -t = download thumbnail only
    if len(argv) < 2:
        print("> Usage: python main.py <youtube video url> [-v|-a|-c|-t]")
        return
    # use argparse to parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of youtube video")
    parser.add_argument("-v", "--video", help="download video only", action="store_true")
    parser.add_argument("-a", "--audio", help="download audio only", action="store_true")
    parser.add_argument("-c", "--combine", help="combine video and audio", action="store_true")
    parser.add_argument("-t", "--thumbnail", help="download thumbnail only", action="store_true")
    args = parser.parse_args()
    all = False
    # check if url is valid
    if not args.url.startswith("https://www.youtube.com/watch?v="):
        print("> Invalid url, please enter a valid youtube video url")
        return
    
    # if no args given, all is true
    if not args.video and not args.audio and not args.combine and not args.thumbnail:
        all = True
    
    # check if result folder exists
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    global video_url
    global video_key

    video_url = args.url
    video_key = video_url.split("v=")[1]
    
    # check if video_key directory exists
    if not os.path.exists(os.path.join(result_folder, video_key)):
        os.mkdir(os.path.join(result_folder, video_key))

    # check if video is requested
    if args.video or all:
        download_video()
    
    # check if audio is requested
    if args.audio or all:
        download_audio()
    
    # check if combine is requested
    if args.combine or all:
        combine_video_with_audio()
    
    # check if thumbnail is requested
    if args.thumbnail or all:
        download_thumbnail()
    
    print(f"> Done downloading from {video_url}")

def download_video():
    global video_key
    global video_url
    # check if file already exists
    if os.path.exists(os.path.join(result_folder, video_key, video_key + ".mp4")):
        print("> Video already exists, skipping download...")
        return
    youtube = YouTube(video_url, on_progress_callback=progress_function)
    mp4_file = youtube.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
    # get filesize of video
    global filesize
    filesize = mp4_file.filesize
    print("> Downloading video...")
    mp4_file.download(os.path.join(result_folder, video_key), filename=video_key+".mp4")
    print("\n> Downloaded video to result as \"" + video_key + ".mp4\"")

def download_audio():
    global video_key
    global video_url
    if os.path.exists(os.path.join(result_folder, video_key, video_key + ".mp3")):
        print("> Audio already exists, skipping download...")
        return
    youtube = YouTube(video_url, on_progress_callback=progress_function)
    mp3_file = youtube.streams.filter(adaptive=True, only_audio=True).first()
    # get filesize of audio
    global filesize
    filesize = mp3_file.filesize
    print("> Downloading audio...")
    mp3_file.download(os.path.join(result_folder, video_key), filename=video_key+".mp3")
    print("\n> Downloaded audio to result as \"" + video_key + ".mp3\"")

def combine_video_with_audio():
    global video_key
    global video_url
    # check if file already exists
    if os.path.exists(os.path.join(result_folder, video_key, video_key + "_combined.mp4")):
        print("> Combined video already exists, skipping combine...")
        return
    mp4_file = video_key + ".mp4"
    mp3_file = video_key + ".mp3"

    video = mpe.VideoFileClip(os.path.join(result_folder, video_key, mp4_file))
    audio = mpe.AudioFileClip(os.path.join(result_folder, video_key, mp3_file))

    # remove audio from video
    video = video.set_audio(None)
    
    # combine video and audio
    video.audio = audio
    video.write_videofile(os.path.join(result_folder, video_key, video_key + "_combined.mp4"))
    # remove original video and audio
    os.remove(os.path.join(result_folder, video_key, mp4_file))
    os.remove(os.path.join(result_folder, video_key, mp3_file))
    # rename combined video
    os.rename(os.path.join(result_folder, video_key, video_key + "_combined.mp4"), os.path.join(result_folder, video_key, video_key + ".mp4"))
    print("> Combined video and audio as \"" + video_key + ".mp4\"")

def download_thumbnail():
    global video_key
    global video_url
    # check if file already exists
    if os.path.exists(os.path.join(result_folder, video_key, video_key + ".jpg")):
        print("> Thumbnail already exists, skipping download...")
        return
    # get the url of thumbnail as highest quality
    url = "https://img.youtube.com/vi/" + video_key + "/maxresdefault.jpg"
    image = urllib.request.urlopen(url)
    print("> Downloading image...\n")
    with open(os.path.join(result_folder, video_key, video_key + ".jpg"), "wb") as f:
        f.write(image.read())
    print("> Downloaded image as \"" + video_key + ".jpg\"")

def progress_function(chunk, file_handle, bytes_remaining):
    global filesize
    current = ((filesize - bytes_remaining)/filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    sys.stdout.write(' ↳ |{bar}| {percent}%\r'.format(bar=status, percent=percent))
    sys.stdout.flush()

if __name__ == "__main__":
    main(sys.argv)