import urllib.request
import os
import sys
import moviepy.editor as mpe
from pytube import YouTube
from pytube.cli import on_progress
import argparse
from utils import Logger

class DownloadModule:

    pwd = os.getcwd()
    result_folder = os.path.join(pwd, "results")
    
    def __init__(self, url) -> None:
        try:
            self.video_url = url
            self.logger = Logger()
            self.youtube = YouTube(url=self.video_url, on_progress_callback=on_progress)
            self.video_title = self.youtube.title
            self.video_key = self.video_url.split("v=")[1]
        except Exception as e:
            self.logger.log(f"Exception occurred while initiating module: {e}", flag=1)
    
    def check_if_file_exists(self, type):

        if os.path.exists(os.path.join(self.result_folder, self.video_key, self.video_key + "." + type)):
            self.logger.log("Requested file already exists, skipping download...", flag=4)
            return True

    def download_video(self):

        if self.check_if_file_exists("mp4"):
            return
        try:
            self.logger.log("Attempting download through pytube...", flag=4)
            mp4_file = self.youtube.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first()
            mp4_file.download(os.path.join(self.result_folder, self.video_key), filename=self.video_key+".mp4")
            self.logger.log(f"Downloaded video to result\{self.video_key} as {self.video_key}.mp4...", flag=4)
        except Exception as e:
            self.logger.log(f"Failed to download video with key [{self.video_key}] with exception: {e}", flag=1)

    def download_audio(self):
        if self.check_if_file_exists("mp3"):
            return
        try:
            mp3_file = self.youtube.streams.filter(adaptive=True, only_audio=True).first()
            mp3_file.download(os.path.join(self.result_folder, self.video_key), filename=f"{self.video_key}.mp3")
            self.logger.log(f"Downloaded audio to result\{self.video_key} as {self.video_key}.mp3", flag=4)
        except Exception as e:
            self.logger.log(f"Failed to download audio with key [{self.video_key}] with exception: {e}", flag=1)

    def combine_video(self):
        try:
            my_clip = mpe.VideoFileClip(os.path.join(self.result_folder, self.video_key, self.video_key + ".mp4"))
            audio_background = mpe.AudioFileClip(os.path.join(self.result_folder, self.video_key, self.video_key + ".mp3"))

            final_clip = my_clip.set_audio(None)
            final_clip = my_clip.set_audio(audio_background)

            final_clip.write_videofile(os.path.join(self.result_folder, self.video_key, self.video_key + "_combined.mp4"))

            os.remove(os.path.join(self.result_folder, self.video_key, self.video_key + ".mp4"))
            os.remove(os.path.join(self.result_folder, self.video_key, self.video_key + ".mp3"))

            os.rename(os.path.join(self.result_folder, self.video_key, self.video_key + "_combined.mp4"), os.path.join(self.result_folder, self.video_key, self.video_key + ".mp4"))
            self.logger.log(f"Combined video and audio as \"{self.video_key}.mp4\"")
        except Exception as e:
            self.logger.log(f"Exception occurred while combining audio with video clips: {e}", flag=1)


    def download_thumbnail(self):
        if self.check_if_file_exists("jpg"):
            return
        try:
            # get the url of thumbnail as highest quality
            url = "https://img.youtube.com/vi/" + self.video_key + "/maxresdefault.jpg"
            image = urllib.request.urlopen(url)
            self.logger.log("Downloading image...", flag=4)
            with open(os.path.join(self.result_folder, self.video_key, self.video_key + ".jpg"), "wb") as f:
                f.write(image.read())
            self.logger.log(f"Downloaded audio to result\{self.video_key} as '{self.video_key}.jpg'", flag=4)
        except Exception as e:
            self.logger.log(f"Exception occurred while downloading thumbname from given key [{self.video_key}]: {e}", flag=1)