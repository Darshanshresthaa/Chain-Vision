from utils.audip_processor import process_data
from core.transcipt import transcribe_all_chunk
from core.Summary import summarize_data


data ="https://www.youtube.com/watch?v=K45s2PgywvI"

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