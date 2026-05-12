from utils.audip_processor import process_data
from core.Summary import summarize_data
from core.transcipt import transcribe_all_chunk
from core.extractor import build_chain,analyze_transcript
from core.rag import build_rag_chain,user_query

from dotenv import load_dotenv

load_dotenv()

def run_chainvision(source:str)->dict:
    print("Chain-vision")

    print("AI Video- Assistance")

    # LOADING DATA SOURCE AND CHUNKING
    chunks = process_data(source=source)

    # GENERATE TRANSCRIPT OF CHUNK AUDIO AND return str
    transcript = transcribe_all_chunk(chunks=chunks)

    # GENERATING TITLE
    title = summarize_data(transcript=transcript)['title']

    # GENERATE SUMMARY
    summary_points = summarize_data(transcript=transcript)['summary']

    # Summary ,Question ...analyze of videos/meeting
    decision = analyze_transcript(transcript=transcript,analysis_type='summary')

    # Question answer
    rag_chain = build_rag_chain(transcipt=transcript)


    component = {"title":title,
                 "transcript":transcript,
                 "summary":summary_points,
                 "actions and decision":decision,
                 "rag_chain":rag_chain}
    
    return component


if __name__ == "__main__":

    source = input("Enter Youtube URL or Local File Path: ")

    result = run_chainvision(source)

    print("\n" + "="*60)
    print("TITLE")
    print("="*60)
    print(result["title"])

    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(result["summary"])

    print("\n" + "="*60)
    print("MEETING ANALYSIS")
    print("="*60)
    print(result["actions and decision"])

    print("\n" + "="*60)
    print("TRANSCRIPT")
    print("="*60)
    print(result["transcript"])


    # RAG Question Answering Loop

    rag_chain = result["rag_chain"]

    while True:

        question = input("\nAsk Question (type 'exit' to quit): ")

        if question.lower() == "exit":
            print("Thanks for Taking My help. Good Bye and Have a beautiful Day")
            break

        user_query(rag_chain, question)


