import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
from pytube.cli import on_progress
import argparse
#path data
pwd = os.getcwd()
result_folder = os.path.join(pwd, "results")

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
    
    # if no args given, all is true
    if not args.video and not args.audio and not args.combine and not args.thumbnail:
        all = True
    
    # check if result folder exists
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    video_url = args.url
    video_title, video_key, youtube = video_data(video_url)
    
    # check if video_key directory exists
    if not os.path.exists(os.path.join(result_folder, video_title)):
        os.mkdir(os.path.join(result_folder, video_title))

    # check if video is requested
    if args.video or args.combine or all:
        download_video(video_title=video_title, youtube=youtube)
    
    # check if audio is requested
    if args.audio or args.combine or all:
        download_audio(video_title=video_title, youtube=youtube)
    
    # check if combine is requested
    if args.combine or all:
        combine_video(video_title=video_title)
    
    # check if thumbnail is requested
    if args.thumbnail or all:
        download_thumbnail(video_key=video_key, video_title=video_title)
    
    print(f"> Done downloading from {video_url}")

def check_if_file_exists(video_title, type):

    if os.path.exists(os.path.join(result_folder, video_title, video_title + "." + type)):
        print("> Video already exists, skipping download...")
        return True

def video_data(video_url):

    youtube = YouTube(video_url, on_progress_callback=on_progress)
    video_title = youtube.title
    video_key = video_url.split("v=")[1]

    return video_title, video_key, youtube

def download_video(video_title, youtube):
    
    if check_if_file_exists(video_title, "mp4"):
        return
    
    mp4_file = youtube.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
    mp4_file.download(os.path.join(result_folder, video_title), filename=video_title+".mp4")
    print(f"Downloaded video to result\{video_title} as {video_title}.mp4")

def download_audio(video_title, youtube):
    if check_if_file_exists(video_title, "mp3"):
        return
        
    mp3_file = youtube.streams.filter(adaptive=True, only_audio=True).first()

    mp3_file.download(os.path.join(result_folder, video_title), filename=f"{video_title}.mp3")
    print(f"Downloaded audio to result\{video_title} as {video_title}.mp3")

def combine_video(video_title):
    
    my_clip = mpe.VideoFileClip(os.path.join(result_folder, video_title, video_title + ".mp4"))
    audio_background = mpe.AudioFileClip(os.path.join(result_folder, video_title, video_title + ".mp3"))

    final_clip = my_clip.set_audio(None)
    final_clip = my_clip.set_audio(audio_background)

    final_clip.write_videofile(os.path.join(result_folder, video_title, video_title + "_combined.mp4"))

    os.remove(os.path.join(result_folder, video_title, video_title + ".mp4"))
    os.remove(os.path.join(result_folder, video_title, video_title + ".mp3"))

    os.rename(os.path.join(result_folder, video_title, video_title + "_combined.mp4"), os.path.join(result_folder, video_title, video_title + ".mp4"))
    print("> Combined video and audio as \"" + video_title + ".mp4\"")

def download_thumbnail(video_title, video_key):

    if check_if_file_exists(video_title, "jpg"):
        return
        
    # get the url of thumbnail as highest quality
    url = "https://img.youtube.com/vi/" + video_key + "/maxresdefault.jpg"
    image = urllib.request.urlopen(url)
    print("> Downloading image...\n")
    with open(os.path.join(result_folder, video_title, video_title + ".jpg"), "wb") as f:
        f.write(image.read())
    print(f"Downloaded audio to result\{video_title} as '{video_title}.jpg'")

if __name__ == "__main__":
    main(sys.argv)