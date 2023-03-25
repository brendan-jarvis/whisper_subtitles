"""
Checks if whisper.cpp exists in the current directory. If it doesn't, it clones the 
repository and builds it using make. Then, it creates a temp directory and 
converts all files in filesArr to 16-bit WAV format using ffmpeg, saving 
the converted files in the temp directory. Finally, it runs whisper.cpp on 
all .wav files in the temp directory.
"""

import os
import subprocess


def whisper_cpp(file_array):
    """
    Takes an array of files, converts them to .wav 16khz and runs whisper.cpp.
    """
    if not os.path.exists("whisper.cpp"):
        subprocess.run(
            ["git", "clone", "https://github.com/ggerganov/whisper.cpp.git"], check=True
        )
        os.chdir("whisper.cpp")
        subprocess.run(["make"], check=True)

    os.makedirs("temp", exist_ok=True)
    for file in file_array:
        # Convert file to 16-bit WAV format and save it in the temp directory
        subprocess.run(
            [
                "ffmpeg",
                "-i",
                file,
                "-ar",
                "16000",
                "-ac",
                "1",
                "-c:a",
                "pcm_s16le",
                f"temp/{os.path.basename(file)}.wav",
            ],
            check=True,
        )

    subprocess.run(["./main", "-f", "temp/*.wav"], check=True)

    # Delete the temp directory
    subprocess.run(["rm", "-rf", "temp"], check=True)
