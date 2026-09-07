import os
from pathlib import Path

import imageio_ffmpeg
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
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
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


data=download_youtube_audio("https://youtu.be/PkcW3POORnU?si=nc6e40IuRJvnFgr0")


# Convert any audio/video file to WAV format 
def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to WAV format using pydub."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000) #16khz
    audio.export(output_path, format="wav")
    return output_path

print(convert_to_wav(data))