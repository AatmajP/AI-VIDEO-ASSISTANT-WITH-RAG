from dotenv import load_dotenv
load_dotenv()    # MUST be before any core/ imports

from utils.audio_processor import process_input 
from core.transcriber import transcribe_all
from core.summarize import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions


source = "https://www.youtube.com/watch?v=_Q-e_nczWqM&t=223s"
language = "english"   # "english" → Whisper 



chunks = process_input(source) # means that the audio from the source (YouTube video) is processed and divided into smaller segments or chunks for easier transcription. This is typically done to handle long audio files more efficiently and to improve the accuracy of the transcription process.


transcript = transcribe_all(chunks, translate=language != "english")
print("\n" + "=" * 60) 
print("📝 TRANSCRIPT")  
print("=" * 60)   
print(transcript[:500] + "..." if len(transcript) > 500 else transcript)


title = generate_title(transcript) 
summary = summarize(transcript) 

print("\n" + "=" * 60) 
print(f"📌 TITLE: {title}") 
print("=" * 60)
print("\n📋 SUMMARY")
print("-" * 60)
print(summary)



action_items = extract_action_items(transcript)
decisions = extract_key_decisions(transcript)
questions = extract_questions(transcript)


#tells the user what the action items
print("\n" + "=" * 60)
print("✅ ACTION ITEMS") 
print("=" * 60)
print(action_items)

#tells the user what the key decisions are
print("\n" + "=" * 60)
print("🔑 KEY DECISIONS")
print("=" * 60)
print(decisions)

#tells the user what the open questions are
print("\n" + "=" * 60)
print("❓ OPEN QUESTIONS")
print("=" * 60)
print(questions) 