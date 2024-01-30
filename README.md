# Youtube Downloader
- A CLI-based simple youtube downloader written in python

## Pre-requisites
- Python 3.6+
- pip packages
  - pytube
  - moviepy

## Installation
- Clone the repository
- Install the dependencies

  ```
   install.bat
  ```

## Usage
- Launch `main.py` with the following arguments
- If no argument is given, the program will ask for the url
> `python main.py [-v | video only] [-a | audio only] [-c | combine video with audio] [-t | thumbnail only] <url>`

## Example
- Download video only
> `python main.py -v {youtube_url}`

- Download audio only
> `python main.py -a {youtube_url}`

- Download video and audio and combine them
> `python main.py -c {youtube_url}`

- Download thumbnail only
> `python main.py -t {youtube_url}`

- Download all
> `python main.py {youtube_url}`

- Download all, with url later given
> `python main.py`<br>
> `> Enter url of youtube video :  {youtube_url}`