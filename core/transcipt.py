from faster_whisper import WhisperModel
import os

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "medium")

# preventing model from downloading replica again and again each time

IS_MODEL_PRESENT = None

def load_model():
    
    global IS_MODEL_PRESENT  #using global variable

    if  IS_MODEL_PRESENT is None:
        print("Loading Model Fast Whisper....")
        IS_MODEL_PRESENT = WhisperModel(WhisperModel,device="cuda",compute_type="int8")

        print("Whisper model loaded Sucessfully")
    
    else:
        print("Model already present in the system ...")
    
    return IS_MODEL_PRESENT


