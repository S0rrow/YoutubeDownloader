import pytest
import os
import sys
from io import StringIO
from class_test import Download_Module
import shutil

def remove_folder(key):
    result_folder = os.path.join(os.getcwd(), "results")

    shutil.rmtree(f"{result_folder}/{key}")

def test_video_title():
    downloader = Download_Module("https://www.youtube.com/watch?v=AXuhZ8h8_cU")
    assert downloader.video_title == "Cyberpunk (サイバーパンク) Sakuga MAD"

def test_video_key():
    downloader = Download_Module("https://www.youtube.com/watch?v=AXuhZ8h8_cU")
    assert downloader.video_key == "AXuhZ8h8_cU"

def test_download():
    downloader = Download_Module("https://www.youtube.com/watch?v=rEES3mGMJSE")
    downloader.download_video()
    downloader.download_audio()
    downloader.download_thumbnail()
    assert os.path.exists(os.path.join(downloader.result_folder, downloader.video_key, downloader.video_key + ".mp4"))
    assert os.path.exists(os.path.join(downloader.result_folder, downloader.video_key, downloader.video_key + ".mp3"))
    assert os.path.exists(os.path.join(downloader.result_folder, downloader.video_key, downloader.video_key + ".jpg"))
    remove_folder(downloader.video_key)
