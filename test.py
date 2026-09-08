from utils.audio_processor import process_input
from core.transcriber import transcribe_all

source="https://youtu.be/ZVDAt3pzU5M?si=AiVKR7Wa-HRaP_ft"
chunks=process_input(source)
print(transcribe_all(chunks)