import whisper
import os
import wave #used to read wav files

import numpy as np

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")

_model = None # meaning that the model is not loaded yet


def _load_wav_samples(chunk_path: str) -> np.ndarray:
    with wave.open(chunk_path, "rb") as wav_file:
        sample_width = wav_file.getsampwidth()
        channels = wav_file.getnchannels()
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())

    if sample_width != 2:
        raise ValueError(f"Expected 16-bit WAV audio, got {sample_width * 8}-bit audio")

    samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        samples = samples.reshape(-1, channels).mean(axis=1)
    if sample_rate != 16000:
        target_length = round(len(samples) * 16000 / sample_rate)
        source_positions = np.arange(len(samples))
        target_positions = np.linspace(0, len(samples) - 1, target_length)
        samples = np.interp(target_positions, source_positions, samples).astype(np.float32)
    return samples


def load_model():

    global _model  

    if _model is None: 
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL) 
        print("Whisper model loaded.")
    return _model 

def transcribe_chunk(chunk_path: str, translate: bool = False) -> str:
    if not os.path.exists(chunk_path):
        raise FileNotFoundError(f"Audio chunk file not found: {chunk_path}")
    
    model = load_model()
    task="translate" if translate else "transcribe"
    result = model.transcribe(_load_wav_samples(chunk_path), task=task)
    return result["text"]

def transcribe_all(chunks: list, translate: bool = False)-> str:
    full_transcript=""
    for i, chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}")
        text = transcribe_chunk(chunk, translate=translate)
        full_transcript += text + " "
    print("Transcription complete.")
    return full_transcript
