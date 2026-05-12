
from langchain_core.prompts import ChatPromptTemplate,PromptTemplate
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage
from langchain_core.output_parsers import StrOutputParser

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableSequence,RunnableParallel,RunnablePassthrough,RunnableLambda

import os
from dotenv import load_dotenv

load_dotenv()

# Loading model Mistral

from core.model import get_llm


llm = get_llm()






def chunk_text(transcript: str) -> list:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )

    return splitter.split_text(transcript)


# Summaize and convert to boolean 
def summarize_data(transcript: str) -> str:

    parser = StrOutputParser()

    llm = get_llm()


# GENERATE SUMMARY OF EVERY CHUNK

    summarize_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a helpful AI assistant.

            Summarize the transcript chunk clearly using:
            - simple language
            - short sentences
            - easy explanations

            Keep important technical points.
            """
        ),
        (
            "human",
            "{chunk_transcript_text}"
        )
    ])


    chunk_list = chunk_text(transcript)

     
# GENERATE A TITLE OF TOPIC
    title_prompt = ChatPromptTemplate.from_messages([
    ("system",
        """
        You are an expert title generator.

        Generate one clear, professional, and concise title
        based on the provided transcript summary.

        Instructions:
        - Keep the title short and meaningful
        - Capture the main topic accurately
        - Make it easy to understand
        - Avoid clickbait or overly dramatic wording
        - Return only the title

        """),

    ("human","{summary}")
    ])




    chunk_summary = []
     # CHAIN -1  Chunk every transcipt ->list
    summarize_chain = summarize_prompt | llm | parser

    for chunk in chunk_list:

        summary_chunk = summarize_chain.invoke({
            "chunk_transcript_text": chunk
        })

        chunk_summary.append(summary_chunk)

    combined_summary = " ".join(chunk_summary)


    # CHAIN -2 -> Generate TOPIC TITLE
    chain_title = title_prompt | llm | parser

    # title = chain_title.invoke({"summary":combined_summary})

    final_combine_summarize = PromptTemplate.from_template("""
    You are a helpful AI assistant.

    Combine all partial summaries into one final structured summary.

    Instructions:
    - Use simple and easy-to-understand language
    - Cover all important points
    - Write the summary in bullet points
    - Keep the summary concise but informative
    - Highlight important keywords using **bold**
    - Focus on key concepts, examples, and explanations
    - Avoid repeating the same information

    Partial Summaries:
    {summary}

    Final Summary:
    """)

    final_chain = final_combine_summarize | llm | parser

    # final_summary = final_chain.invoke({
    #     "summaries": combined_summary
    # })

    # return final_summary
    
    # Final Chain


    final_parallel_chain = RunnableParallel({
    "title": chain_title,
    "summary": final_chain
    })

    final_output = final_parallel_chain.invoke({"summary":combined_summary})

    return final_output



