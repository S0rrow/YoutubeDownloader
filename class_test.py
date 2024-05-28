import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
from pytube.cli import on_progress
import argparse

class Download_Module:
    
    pwd = os.getcwd()
    result_folder = os.path.join(pwd, "results")

    def __init__(self, url) -> None:
        
        self.video_url = url
        self.youtube = YouTube(self.video_url, on_progress_callback=on_progress)
        self.video_title = self.youtube.title
        self.video_key = self.video_url.split("v=")[1]

    
    def check_if_file_exists(self, type):

        if os.path.exists(os.path.join(self.result_folder, self.video_title, self.video_title + "." + type)):
            print("> Video already exists, skipping download...")
            return True

    def download_video(self):
        
        if self.check_if_file_exists("mp4"):
            return
        
        mp4_file = self.youtube.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
        mp4_file.download(os.path.join(self.result_folder, self.video_title), filename=self.video_title+".mp4")
        print(f"Downloaded video to result\{self.video_title} as {self.video_title}.mp4")

    def download_audio(self):
        if self.check_if_file_exists("mp3"):
            return
            
        mp3_file = self.youtube.streams.filter(adaptive=True, only_audio=True).first()

        mp3_file.download(os.path.join(self.result_folder, self.video_title), filename=f"{self.video_title}.mp3")
        print(f"Downloaded audio to result\{self.video_title} as {self.video_title}.mp3")

    def combine_video(self):
        
        my_clip = mpe.VideoFileClip(os.path.join(self.result_folder, self.video_title, self.video_title + ".mp4"))
        audio_background = mpe.AudioFileClip(os.path.join(self.result_folder, self.video_title, self.video_title + ".mp3"))

        final_clip = my_clip.set_audio(None)
        final_clip = my_clip.set_audio(audio_background)

        final_clip.write_videofile(os.path.join(self.result_folder, self.video_title, self.video_title + "_combined.mp4"))

        os.remove(os.path.join(self.result_folder, self.video_title, self.video_title + ".mp4"))
        os.remove(os.path.join(self.result_folder, self.video_title, self.video_title + ".mp3"))

        os.rename(os.path.join(self.result_folder, self.video_title, self.video_title + "_combined.mp4"), os.path.join(self.result_folder, self.video_title, self.video_title + ".mp4"))
        print("> Combined video and audio as \"" + self.video_title + ".mp4\"")

    def download_thumbnail(self):

        if self.check_if_file_exists("jpg"):
            return
            
        # get the url of thumbnail as highest quality
        url = "https://img.youtube.com/vi/" + self.video_key + "/maxresdefault.jpg"
        image = urllib.request.urlopen(url)
        print("> Downloading image...\n")
        with open(os.path.join(self.result_folder, self.video_title, self.video_title + ".jpg"), "wb") as f:
            f.write(image.read())
        print(f"Downloaded audio to result\{self.video_title} as '{self.video_title}.jpg'")