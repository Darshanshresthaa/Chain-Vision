from langchain_mistralai import ChatMistralAI
import os

# from langchain_openai import ChatOpenAI
# Loading models Mistral

from dotenv import load_dotenv

load_dotenv()

# Use in 
# - Summarize.py 

def get_llm():
    return ChatMistralAI(model_name="mistral-small-latest",
                         mistral_api_key=os.getenv("MISTRAL_API_KEY"),
                         temperature=0.5,
                         max_retries=5,
                         timeout=30)


# Use
# - extract.py
# - rag.py

def get_llm_simple():

    return ChatMistralAI(
        model_name="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.1,
        max_retries=5,
        timeout=30
    )


# # Use in 
# # - Summarize.py 

# def get_llm():

#     return ChatOpenAI(
#         model="google/gemma-3-27b-it:free",
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#         base_url="https://openrouter.ai/api/v1",
#         temperature=0.5,
#         max_retries=5,
#         timeout=60
#     )


# # # Use
# # # - extract.py
# # # - rag.py

# def get_llm_simple():

#     return ChatOpenAI(
#         model="google/gemma-3-27b-it:free",
#         api_key=os.getenv("OPENROUTER_API_KEY"),
#         base_url="https://openrouter.ai/api/v1",
#         temperature=0.1,
#         max_retries=5,
#         timeout=60
#     )
