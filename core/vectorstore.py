from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import torch

CHROMA_STORE_DIR = "Vector_db"

COLLECTION_NAME = "meeting_transcript"

EMBEDDING_MODEL = "all-MiniLM-L6-V2"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_embedding():

    emb_model= HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL,
                                model_kwargs = {"device":DEVICE})
    
    return emb_model
    

def build_vector_store(transcipt:str)->Chroma:
    print("Building Vector Store")

    # Splitting The Trasncipt into Chunk

    splitter = RecursiveCharacterTextSplitter(chunk_size = 1000,
                                              chunk_overlap = 200)
    
    chunk_list = splitter.split_text(transcipt)  #list or chunk

    docs = []
    for chunk_id,chunk in enumerate (chunk_list,start=1):
        data = Document(page_content=chunk,metadata = {"Chunk_index":chunk_id})
        docs.append(data)




