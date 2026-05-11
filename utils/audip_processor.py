import yt_dlp
from pydub import AudioSegment
import os

DOWNLAOD_DIR = "downloads"

os.makedirs(DOWNLAOD_DIR,exist_ok=True)  #if not exist make in same folder



def downlaod_youtube_audio(url:str)->str:
    output_path = os.path.join(DOWNLAOD_DIR,"%(title)s.%(ext)s")  # add audio mp file in this directory called Download dir

    ydl_opts = {
    "format": "bestaudio",
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "quiet": True,  #Hide downlaod logs in terminal
    "noplaylist": True,  #prevent from downlaoding whole playlist if vide is in playlist

    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        information = ydl.extract_info(url=url,download=True)  #take url and extract meta data fromt that file duration conent title
        file_name = ydl.prepare_filename(information).replace(".webm",".wav").replace(".mp4",".wav").replace(".m4a",".wav")  #yt-dlp get .mp4 format s
    return file_name


downlaod_youtube_audio(url="https://www.youtube.com/watch?v=rJ1Qao09CFI")

    

