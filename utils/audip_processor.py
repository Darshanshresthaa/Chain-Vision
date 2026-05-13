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

    # Converting downlaod audio into mp3
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        information = ydl.extract_info(url=url,download=True)  #take url and extract meta data fromt that file duration conent,title and it downlaod file
        # Converitng other file downlad into mp3 but its extension doesnt change so changing manually
        file_name = (ydl.prepare_filename(information)
                     .replace(".webm", ".mp3")
                     .replace(".m4a", ".mp3")
                     .replace(".mp4", ".mp3"))
    return file_name


def convert_to_wav_format(input_path)->str:

    output_path = os.path.splitext(input_path)[0] +"_converted.wav"  #splittext split based on . (file_name , .ext)
    audio = AudioSegment.from_file(input_path)  #detect fole format mp3,mp4 using pydub
    audio = audio.set_channels(1).set_frame_rate(16000)   #converting audio to mono audio and setting 16Khz(requirement for wisper)
    audio.export(output_path,format="wav")
    return output_path



# Converting audio into Chunks

# Making chunk of 10 Minute

def chunk_audio(wav_path:str,chunk_duration:int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)  
    chunk_milisecond = chunk_duration*60*1000

    chunks = []
    for part,data in enumerate(range(0,len(audio),chunk_milisecond),start=1):

        chunk = audio[data:data+chunk_milisecond]
        chunk_path = f"{wav_path}_chunk_{part}.wav"
        chunk.export(chunk_path,format="wav")

        chunks.append(chunk_path)
    
    return chunks




def process_data(source:str)->list:

    if source.startswith("http://") or source.startswith("https://"):
        print("Detected Youtube Link Downloading Content ....")
        mp3_path = downlaod_youtube_audio(source)
        wav_path = convert_to_wav_format(mp3_path)

    else:
        print("Detected File Locally Convetring to audio.....")
        wav_path = convert_to_wav_format(source)

    
    print("Chunking audio into 10 minute interval. Might take time....")
    print()
    print("=="*30)
    print()

    print(f"Length of Video: {len(AudioSegment.from_wav(wav_path))} ms")
    print(f"Length of Video: {len(AudioSegment.from_wav(wav_path)) / (1000 * 60):.2f} minutes")

    chunks_list = chunk_audio(wav_path=wav_path)

    print(f"Audio ready. Audio is Chunked into {len(chunks_list)} Parts")

    return chunks_list


# Testing and debugging

# result ="https://www.youtube.com/watch?v=etcYBI7L1D8"

# final_chunk_list = process_data(source=result)
# # # Debugging

# # print("==="*50)
# # print()
# # print(result)
# # print()
# # print("==="*50)
# # print()

# # mono_audio = convert_to_wav_format(result)

# # path_list = chunk_audio(mono_audio)

# # print(path_list) #list of path




