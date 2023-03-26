"""
This is a Python script that utilizes the OpenAI Whisper library to generate
.srt files with subtitles for compatible files. Before running the script,
ensure that the required dependencies, namely OpenAI's Whisper, are installed.
The script generates .srt files for each file found in the directory using
Whisper. Please note that the generated subtitles may not be completely
accurate, and manual correction may be necessary.
"""


import os
from torch import cuda
from .whisper_cpp import transcribe_with_cpp
from .openai import transcribe_with_whisper


def generate_subtitles(args):
    """
    This function is the main function of the script. It loads the language model,
    searches for files to subtitle, and generates subtitles for each file.
    """
    file_array = []
    supported_extensions = [".mp4", ".m4a", ".mp3", ".mpeg", ".mpga", ".wav", ".webm"]

    print("Whisper Subtitles script loaded")

    print("Searching for files to subtitle...")
    try:
        for file in os.listdir(args.input_directory):
            if file.endswith(tuple(supported_extensions)):
                file_array.append(file)
        if len(file_array) == 0:
            raise FileNotFoundError("No supported files found in the input directory")
    except FileNotFoundError as file_error:
        print(f"FileNotFoundError: {file_error}")
        return

    print(f"Found {len(file_array)} files to subtitle.")

    if args.use_cpp:
        print("Using Whisper.CPP")
        transcribe_with_cpp(file_array, args)
    if cuda.is_available():
        print("Using GPU")
        transcribe_with_whisper(file_array, args)
    else:
        print("Using CPU")
        transcribe_with_cpp(file_array, args)
