from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableLambda

import os
from dotenv import load_dotenv

def get_llm():
    return ChatMistralAI(model_name="mistral-small-latest")