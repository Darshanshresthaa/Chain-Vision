from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import torch

CHROMA_STORE_DIR = "Vector_db"  #local path to store vectordb

COLLECTION_NAME = "meeting_transcript"  #table name insode db

EMBEDDING_MODEL = "all-MiniLM-L6-V2"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def get_embedding():

    emb_model= HuggingFaceEmbeddings(model_name = EMBEDDING_MODEL,
                                model_kwargs = {"device":DEVICE})
    
    return emb_model
    

# Ceeating DB and adding Content
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
    
    embedding_model= get_embedding()
    # from doc cause we store chunk in Document Type
    vector_store = Chroma.from_documents(documents=docs,
                                         embedding=embedding_model,
                                         collection_name=COLLECTION_NAME,
                                         persist_directory=CHROMA_STORE_DIR
                                         )
    
    return vector_store

# Loading the existing VectorDb
def load_vector_store()-> Chroma:
    embadding_model= get_embedding() 

    vector_store = Chroma(
                          collection_name=COLLECTION_NAME,
                          embedding_function=embadding_model,
                          persist_directory=CHROMA_STORE_DIR
                          )
    
    return vector_store


# Retrive similar data
def get_retrival(vector_store :Chroma,k_value:5):
    retriver = vector_store.as_retriever(search_type ="similarity",
                              search_kwargs={"k":k_value})
    
    return retriver







