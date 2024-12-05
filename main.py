from utils import Logger
import os, re
from yt_dlp import YoutubeDL

# Initialize Logger
logger = Logger(options={"name": "YouTubeDownloader"})

def extract_video_key(url: str) -> str:
    """
    Extracts the video key from a valid YouTube URL.
    :param url: YouTube URL (shortened or full).
    :return: The video key if valid, else raises a ValueError.
    """
    # Define a regex pattern to match YouTube URLs
    youtube_pattern = re.compile(
        r'(?:https?://)?'                          # Optional protocol
        r'(?:www\.)?'                              # Optional 'www.'
        r'(?:youtube\.com/watch\?v=|youtu\.be/)'   # Domain and path
        r'([a-zA-Z0-9_-]{11})'                     # Video key (11 characters)
    )
    
    match = youtube_pattern.search(url)
    if not match:
        raise ValueError(f"Invalid YouTube URL: {url}")
    
    return match.group(1)


def download_youtube_content(url, choice):
    try:
        # Validate and extract video key
        video_key = extract_video_key(url)
        logger.log(f"Extracted video key: {video_key}", flag=3)
        base_dir = os.path.join("results", video_key)
        os.makedirs(base_dir, exist_ok=True)  # Create directory if it doesn't exist

        logger.log(f"Starting download for {url} with choice '{choice}'", flag=3)

        if choice in {"thumbnail", "all"}:
            logger.log(f"Downloading thumbnail for {video_key}...", flag=4)
            ydl_opts_thumbnail = {
                'skip_download': True,
                'writethumbnail': True,
                'outtmpl': os.path.join(base_dir, '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'EmbedThumbnail',
                }],
            }
            with YoutubeDL(ydl_opts_thumbnail) as ydl:
                ydl.download([url])

        if choice in {"audio", "all"}:
            logger.log(f"Downloading audio for {video_key}...", flag=4)
            ydl_opts_audio = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(base_dir, '%(title)s.%(ext)s'),
            }
            with YoutubeDL(ydl_opts_audio) as ydl:
                ydl.download([url])

        if choice in {"video", "all"}:
            logger.log(f"Downloading video (no sound) for {video_key}...", flag=4)
            ydl_opts_video_no_sound = {
                'format': 'bestvideo[ext=mp4]',
                'outtmpl': os.path.join(base_dir, '%(title)s (no sound).%(ext)s'),
            }
            with YoutubeDL(ydl_opts_video_no_sound) as ydl:
                ydl.download([url])

            logger.log(f"Downloading video (with sound) for {video_key}...", flag=4)
            ydl_opts_video_with_sound = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(base_dir, '%(title)s (sound).%(ext)s'),
            }
            with YoutubeDL(ydl_opts_video_with_sound) as ydl:
                ydl.download([url])

        logger.log(f"Downloads completed for {video_key}. Files saved in '{base_dir}'", flag=3)

    except Exception as e:
        logger.log(f"Error occurred: {str(e)}", flag=1)

# Example usage
if __name__ == "__main__":
    youtube_url = input("Enter the YouTube URL: ")
    print("Options: thumbnail, audio, video, all")
    user_choice = input("Choose what to download: ").lower()

    if user_choice not in {"thumbnail", "audio", "video", "all"}:
        logger.log(f"Invalid choice '{user_choice}' entered.", flag=2)
        print("Invalid choice! Options are: thumbnail, audio, video, all.")
    else:
        download_youtube_content(youtube_url, user_choice)
