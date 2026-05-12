from utils.audip_processor import process_data
from core.transcipt import transcribe_all_chunk
from core.Summary import summarize_data
from core.extractor import analyze_transcript


data ="https://www.youtube.com/watch?v=1IxG7ywSNXk&t=116s"

chunks = process_data(source=data)

trancribe_all = transcribe_all_chunk(chunks=chunks,translate=True)

print("="*50)
print()

print(chunks)

print()
print("="*50) 



print("="*50)
print()

print(trancribe_all)

print()
print("="*50) 


print("="*50)
print()

print(summarize_data(trancribe_all))

print()
print("="*50) 


print("="*50)
print()

print(analyze_transcript(trancribe_all))

print()
print("="*50) 