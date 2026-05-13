from utils.audip_processor import process_data
from core.Summary import summarize_data
from core.transcipt import transcribe_all_chunk
from core.extractor import analyze_transcript
from core.rag import build_rag_chain,load_rag_chain,user_query

from dotenv import load_dotenv

import os
import shutil

load_dotenv()



def run_chainvision(source: str) -> dict:

    print("Chain-Vision")
    print("AI Video Assistant")

    chunks = process_data(source=source)

    print("\nAudio Processing Completed")

    transcript = transcribe_all_chunk(chunks=chunks)

    print("\nTranscription Completed")

    summary_result = summarize_data(
        transcript=transcript
    )

    title = summary_result["title"]
    summary_points = summary_result["summary"]

    print("\nSummary Generated")


    decision = analyze_transcript(
        transcript=transcript,
        analysis_type='summary'
    )

    print("\nTranscript Analysis Completed")


    print("\nBuilding Vector Store...")

    rag_chain = build_rag_chain(
        transcipt=transcript
    )

    print("Vector Store Created Successfully")

    print("\nCleaning Temporary Files...")

    try:

        # Delete chunk files
        if chunks:

            for file in chunks:

                if os.path.exists(file):

                    os.remove(file)

        # Delete downloads folder
        if os.path.exists("downloads"):

            shutil.rmtree("downloads")

        print("Temporary Files Deleted Successfully")

    except Exception as e:

        print(f"Cleanup Error: {e}")

    component = {

        "title": title,

        "transcript": transcript,

        "summary": summary_points,

        "actions and decision": decision,

        "rag_chain": rag_chain
    }

    return component



if __name__ == "__main__":

    print("1. Process New Video")
    print("2. Load Existing Vector Database")

    choice = input("\nEnter Choice: ")



    if choice == "1":

        source = input(
            "\nEnter Youtube URL or Local File Path: "
        )

        result = run_chainvision(source)

        print("\n" + "=" * 60)
        print("TITLE")
        print("=" * 60)

        print(result["title"])


        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        print(result["summary"])


        print("\n" + "=" * 60)
        print("MEETING ANALYSIS")
        print("=" * 60)

        print(result["actions and decision"])


        rag_chain = result["rag_chain"]




    elif choice == "2":

        print("\nLoading Existing Vector Database...")

        rag_chain = load_rag_chain()

        print("Vector Database Loaded Successfully")


    else:

        print("Invalid Choice")

        exit()


    while True:

        question = input(
            "\nAsk Question (type 'exit' to quit): "
        )

        if question.lower() == "exit":

            print(
                "\nThanks for Taking My Help.\n"
                "Good Bye and Have a Beautiful Day."
            )

            break


        user_query(
            rag_chain=rag_chain,
            question=question
        )