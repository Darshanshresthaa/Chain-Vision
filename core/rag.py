from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

from langchain_core.prompts import ChatPromptTemplate

from core.vectorstore import build_vector_store,get_retrival,load_vector_store

from dotenv import load_dotenv
import os


load_dotenv()

def get_llm():

    model =  ChatMistralAI(
        model_name="mistral-small-latest",
        mistral_api_key=os.getenv("MISTRAL_API_KEY"),
        temperature=0.1
    )
    return model


def format_docs(doc_list:list)->str:

    document = []
    for doc in  doc_list:
        document.append(doc.page_content)
    
    return " ".join(document)


def build_rag_chain(transcipt:str):

    parser = StrOutputParser()
    
    vector_store = build_vector_store(transcipt=transcipt)  #load data to VS
    retriver = get_retrival(vector_store=vector_store,k_value=5)

    text_gen_llm= get_llm()

    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful AI assistant.

        Answer the user's question ONLY using the provided context.

        Rules:
        - Do NOT use outside knowledge
        - If answer is not found, say:
          "Answer not found in provided document."
        - Keep answer clear and concise
        """
    ),

    (
        "human",
        """
        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    ])


    rag_chain = ({"context":retriver | RunnableLambda(format_docs),  #search similar data data related  to user input and display k no of similar data
                  "question":RunnablePassthrough()} | prompt |text_gen_llm | parser)
    
    return rag_chain



# loading existing rag

def load_rag_chain():
    vector_store = load_vector_store()
    retriver = get_retrival(vector_store=vector_store,k_value=5)

    text_gen_llm = get_llm()

    parser = StrOutputParser()

    prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful AI assistant.

        Answer the user's question ONLY using the provided context.

        Rules:
        - Do NOT use outside knowledge
        - If answer is not found, say:
          "Answer not found in provided document."
        - Keep answer clear and concise
        """
    ),

    (
        "human",
        """
        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
    ])

    rag_chain = ({"context":retriver | RunnableLambda(format_docs),  #search similar data data related  to user input and display k no of similar data
                  "question":RunnablePassthrough()} |prompt |text_gen_llm |parser )
    
    return rag_chain


def user_query(rag_chain,question:str)->str:

    print("="*40)
    print("USer Question :",question)

    answer = rag_chain.invoke(question)

    print("AI :",answer)

    return answer



    