# Specially for meeting analysis like:
# - action items
# - deadlines
# - decisions
# - questions

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda,RunnablePassthrough

import os
from dotenv import load_dotenv

load_dotenv()



# Loading LLM from LLM model

from core.model import get_llm_simple

llm = get_llm_simple()


# BUILD REUSABLE CHAIN


def build_chain(system_prompt: str):

    llm = get_llm_simple()

    parser = StrOutputParser()

    chain = (
        RunnablePassthrough() | RunnableLambda(lambda x: {"text": x})| ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{text}")
        ]) | llm | parser)

    return chain



# ALL PROMPTS Required


PROMPTS = {


    "summary": """
    You are an expert transcript analyst..

    Analyze the meeting transcript and generate a structured meeting summary.

    Include:
    - Main discussion points
    - Important decisions
    - Action items
    - Assigned tasks
    - Deadlines
    - Risks or blockers
    - Important questions asked

    Rules:
    - Use simple and professional language
    - Use bullet points
    - Highlight important information using **bold**
    - Keep the summary concise but informative
    - If something is not mentioned, skip it
    """,


   

    "action_items": """
    You are an expert transcript analyst..

    Extract all action items from the meeting transcript.

    For each action item extract:
    - task
    - assigned person
    - deadline
    - priority if mentioned

    Rules:
    - If assigned person is not mentioned, write "Not Mentioned"
    - If deadline is not mentioned, write "Not Mentioned"
    - If priority is not mentioned, write "Not Mentioned"
    - Use simple and professional language
    """,




    "decisions": """
    You are an expert transcript analyst..

    Extract all important decisions made during the meeting.

    Rules:
    - Focus only on final decisions or confirmed agreements
    - Ignore casual discussions or suggestions
    - Return output in bullet points
    - Use concise and professional language
    - If no decisions are mentioned, write:
      "No Key Decisions Mentioned"
    """,



    "questions": """
    You are an expert transcript analyst..

    Extract all important questions asked during the meeting.

    Rules:
    - Extract direct and indirect questions
    - Remove duplicate questions
    - Use bullet points
    - Keep questions clear and readable
    - If no questions are found, write:
      "No Questions Mentioned"
    """,



    "deadlines": """
   You are an expert transcript analyst..

    Extract all deadlines mentioned in the meeting.

    Rules:
    - Mention related tasks with deadlines
    - Use bullet points
    - If no deadlines are mentioned, write:
      "No Deadlines Mentioned"
    """,


    "risks": """
    You are an expert transcript analyst..

    Extract all risks, blockers, delays, or issues mentioned.

    Rules:
    - Focus on problems affecting progress
    - Use concise language
    - Return bullet points
    - If no risks are found, write:
      "No Risks Mentioned"
    """
}


#  ANALYZER


def analyze_transcript(transcript: str, analysis_type: str = "summary") -> str:

    # if analysis_type not in PROMPTS:
    #     raise ValueError(f"Invalid analysis type: {analysis_type}")

    system_prompt = PROMPTS[analysis_type]

    chain = build_chain(system_prompt)

    result = chain.invoke(transcript)

    return result



# TESTING METHOD Functionality

# if __name__ == "__main__":

#     transcript = """
#     Darshan will complete frontend by Friday.

#     Ram needs to test the backend API before Monday.

#     The team decided to deploy using Docker.

#     Should we migrate to FastAPI next month?

#     There might be delay because the server is unstable.
#     """

#     print("\n===== ACTION ITEMS =====\n")
#     print(analyze_transcript(transcript, "action_items"))

#     print("\n===== DECISIONS =====\n")
#     print(analyze_transcript(transcript, "decisions"))

#     print("\n===== QUESTIONS =====\n")
#     print(analyze_transcript(transcript, "questions"))

#     print("\n===== DEADLINES =====\n")
#     print(analyze_transcript(transcript, "deadlines"))

#     print("\n===== RISKS =====\n")
#     print(analyze_transcript(transcript, "risks"))