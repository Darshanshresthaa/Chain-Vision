from langchain_mistralai import ChatMistralAI
import os

# Loading models Mistral

# Use in 
# - Summarize.py 

def get_llm():
    return ChatMistralAI(model_name="mistral-small-latest",
                         mistral_api_key=os.getenv("MISTRAL_API_KEY"),
                         temperature=0.5,
                         max_retries=5,
                         timeout=60)


# Use
# - extract.py
# - rag.py

def get_llm_simple():

    return ChatMistralAI(
        model_name="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.1,
        max_retries=5,
        timeout=60
    )


