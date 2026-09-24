import os # For interacting with the operating system
from pathlib import Path

import imageio_ffmpeg  # For handling audio/video processing with FFmpeg  
                       # The imageio_ffmpeg library provides a convenient way to access the FFmpeg executable,
                       #  which is used for audio and video processing tasks. It allows you to perform operations such as format conversion, audio extraction, and more.  
import yt_dlp  # YouTube video download library

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe() 
os.environ["PATH"] = os.pathsep.join( 
    [str(Path(ffmpeg_exe).parent), os.environ.get("PATH", "")]
)

from pydub import AudioSegment  # Audio processing library

AudioSegment.converter = ffmpeg_exe

DOWNLOAD_DIR = "downloads"  # Directory to save downloaded audio files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_youtube_audio(url :str) ->str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s") # Output template for downloaded audio
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
        "quiet": True, 
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = Path(ydl.prepare_filename(info)).with_suffix(".wav")

    if not filename.exists():
        raise FileNotFoundError(f"Audio conversion completed, but output was not found: {filename}")

    return str(filename)





# Convert any audio/video file to WAV format 
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path


# Split a WAV file into chunks
#helps in processing large audio files by breaking them into 
# smaller segments for easier handling and analysis.
def chunk_audio(wav_path : str , chunk_minutes : int = 10) -> list:
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000 

    chunks = []

    for i, start in enumerate(range(0,len(audio),chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = f"{wav_path}_chunk_{i}.wav"
        chunk.export(chunk_path , format = "wav")

        chunks.append(chunk_path)
    
    return chunks

# Process input source (YouTube URL or local file) and return audio chunks

def process_input(source: str) -> list: 
    if source.startswith(("http://", "https://")): # Check if the source is a YouTube URL
        print("Detected YouTube URL. Downloading audio")
        wav_path = download_youtube_audio(source)
    else:
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source) 

    print("Chunking audio...")
    chunks = chunk_audio(wav_path) 
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks