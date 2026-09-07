import yt_dlp  # YouTube video download library
from pydub import AudioSegment  # Audio processing library
import os

DOWNLOAD_DIR = "downloads"  # Directory to save downloaded audio files
os.makedirs(DOWNLOAD_DIR, exist_ok=True)  
