from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough,RunnableLambda

from langchain_core.prompts import ChatPromptTemplate

from core.vectorstore import build_vector_store,get_retrival,load_vector_store

from dotenv import load_dotenv
import os


load_dotenv()
# Loading Simple LLM 

from core.model import get_llm_simple


def format_docs(doc_list: list) -> str:

    document = []

    for doc in doc_list:
        document.append(doc.page_content)

    return "\n\n".join(document)

def rewrite_query(question: str) -> str:

    q = question.lower()

    replacements = {
        "physical ai": "physical world AI robotics",
        "robotics": "AI robotics general purpose robots",
        "summary": "overall discussion summary",
        "main points": "important discussion points",
        "answers": "answers to important questions from document"
    }

    for key, value in replacements.items():

        if key in q:
            return value

    return question



prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a helpful AI assistant.

        Use BOTH:
        1. Conversation history
        2. Retrieved context

        to answer the user's question.

        Rules:
        - Use previous conversation if needed
        - Do not use outside knowledge
        - Keep answers under 300 words
        - If related information exists, provide closest answer
        - Only say "Answer not found in provided document"
          when absolutely nothing relevant exists
        - Keep answers clear and concise
        """
    ),

    (
        "human",
        """
        Chat History:
        {history}

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )
])




def build_rag_chain(transcipt: str):

    parser = StrOutputParser()

    vector_store = build_vector_store(transcipt=transcipt)

    retriver = get_retrival(
        vector_store=vector_store,
        k_value=4
    )

    text_gen_llm = get_llm_simple()

    rag_chain = (
        {
            "context":
                RunnableLambda(
                    lambda x: rewrite_query(x["question"])
                )
                | retriver
                | RunnableLambda(format_docs),

            "question":
                lambda x: x["question"],

            "history":
                lambda x: x["history"]

        }
        | prompt
        | text_gen_llm
        | parser
    )

    return rag_chain




def load_rag_chain():

    parser = StrOutputParser()

    vector_store = load_vector_store()

    retriver = get_retrival(
        vector_store=vector_store,
        k_value=4
    )

    text_gen_llm = get_llm_simple()

    rag_chain = (
        {
            "context":
                RunnableLambda(
                    lambda x: rewrite_query(x["question"])
                )
                | retriver
                | RunnableLambda(format_docs),

            "question":
                lambda x: x["question"],

            "history":
                lambda x: x["history"]

        }
        | prompt
        | text_gen_llm
        | parser
    )

    return rag_chain




CHAT_HISTORY = []



def user_query(rag_chain, question: str) -> str:

    global CHAT_HISTORY

    # print("=" * 40)
    print("User Question :", question)

    # Build history string
    history_text = "\n".join(CHAT_HISTORY)

    # Invoke chain
    answer = rag_chain.invoke({
        "question": question,
        "history": history_text
    })

    # Save conversation
    CHAT_HISTORY.append(f"User: {question}")
    CHAT_HISTORY.append(f"AI: {answer}")

    print("\nAI:")
    print(answer)

    return answer