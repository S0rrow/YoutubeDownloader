import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
from pytube.cli import on_progress
import argparse

class Downloader:
    def __init__(self, url) -> None:
        self.vide_url = url
        self.pwd = os.getcwd()
        self.result_folder = os.path.join(self.pwd, "results")
        self.video_data = None
    
    def check_if_file_exists(self, video_title, type):

        if os.path.exists(os.path.join(self.result_folder, video_title, video_title + "." + type)):
            print("> Video already exists, skipping download...")
            return True

    def video_data(self):

        youtube = YouTube(self.ideo_url, on_progress_callback=on_progress)
        video_title = youtube.title
        video_key = self.video_url.split("v=")[1]

        self.video_data = [video_title, video_key, youtube]

    def download_video(self, video_title, youtube):
        
        if self.check_if_file_exists(video_title, "mp4"):
            return
        
        mp4_file = youtube.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
        mp4_file.download(os.path.join(self.result_folder, video_title), filename=video_title+".mp4")
        print(f"Downloaded video to result\{video_title} as {video_title}.mp4")

    def download_audio(self.video_title, youtube):
        if self.check_if_file_exists(video_title, "mp3"):
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