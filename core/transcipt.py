from faster_whisper import WhisperModel
import os
import torch



WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# preventing model from downloading replica again and again each time

IS_MODEL_PRESENT = None

def load_model():
    
    global IS_MODEL_PRESENT  #using global variable

    if  IS_MODEL_PRESENT is None:
        print("Loading Model Fast Whisper....")

        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        print(DEVICE)
        # If user dont have Gpu auto select Cpu
        IS_MODEL_PRESENT = WhisperModel(WHISPER_MODEL,
                                        device=DEVICE,
                                        compute_type="int8")

        print("Whisper model loaded Sucessfully")
    
    else:
        print("Model already present in the system ...")
    
    return IS_MODEL_PRESENT


def transcipt_chunk(chunk_path:str,translate:bool=False)->str:
    model = load_model()

# Checking does user want language translation or Not
    if translate:
        task = "translate"
    
    else:
        task = "transcribe"

    
    segments,info = model.transcribe(chunk_path,task=task)


    text_parts = []

    for segment in segments:
        text_parts.append(segment.text)

    return " ".join(text_parts)


def transcribe_all_chunk(chunks:list,translate:bool=False)->str:

    full_transcript = []

    for chunk_id ,chunk in enumerate(chunks,start=1):
        print(f" Transipt Chunk Id :  {chunk_id}")
        text = transcipt_chunk(chunk,translate=translate)

        full_transcript.append(text)

        print(f"Chunk ID {chunk_id} Transciption Continue ....")
    
    print("Transciption Completed")

    print("=="*30)
    print()
    print(full_transcript)
    print()
    print("=="*30)

    return " ".join(full_transcript)  #concatination into string
