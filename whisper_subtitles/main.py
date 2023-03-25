"""
This is a Python script that utilizes the OpenAI Whisper library to generate
.srt files with subtitles for compatible files. Before running the script,
ensure that the required dependencies, namely OpenAI's Whisper, are installed.
The script generates .srt files for each file found in the directory using
Whisper. Please note that the generated subtitles may not be completely
accurate, and manual correction may be necessary.
"""


import os
import time
import whisper
from pysubs2 import load_from_whisper, exceptions
from whisper_subtitles.postprocessing import (
    split_long_lines,
    fix_overlapping_display_times,
)


def generate_subtitles(
    model,
    input_directory,
    output_directory,
    language,
    condition_on_previous_text,
    subtitle_format,
    max_line_length,
    fp16,
):
    """
    This function is the main function of the script. It loads the language model,
    searches for files to subtitle, and generates subtitles for each file.
    """
    file_array = []
    supported_extensions = [".mp4", ".m4a", ".mp3", ".mpeg", ".mpga", ".wav", ".webm"]

    print("Whisper Subtitles script loaded")

    print("Searching for files to subtitle...")
    try:
        for file in os.listdir(input_directory):
            if file.endswith(tuple(supported_extensions)):
                file_array.append(file)
        if len(file_array) == 0:
            raise FileNotFoundError("No supported files found in the input directory")
    except FileNotFoundError as file_error:
        print(f"FileNotFoundError: {file_error}")
        return

    print(f"Found {len(file_array)} files to subtitle.")

    try:
        print(f"Loading the {model} language model...")
        model = whisper.load_model(model)
        if not model:
            raise RuntimeError("Failed to load model")
    except RuntimeError as model_error:
        print(f"RuntimeError loading the model: {model_error}")
        return

    total_time = 0
    for file in file_array:
        file_name = os.path.splitext(file)[0]
        subtitle_path = os.path.join(output_directory, file_name) + subtitle_format
        if os.path.exists(subtitle_path):
            print(f"{subtitle_path} already exists. Skipping...")
            continue

        print(f"Generating subtitles for {file}...")

        audio = whisper.load_audio(os.path.join(input_directory, file))

        # decode the audio and save subtitles
        try:
            start_time = time.time()
            result: dict = model.transcribe(
                audio,
                verbose=True,
                language=language,
                condition_on_previous_text=condition_on_previous_text,
                word_timestamps=True,
                fp16=fp16,
            )

            try:
                # Load subtitle file from OpenAI Whisper transcript
                subs = load_from_whisper(result)
                # Split long lines into multiple lines
                for sub in subs:
                    sub.text = split_long_lines(sub.text, max_line_length)
                # Remove miscellaneous events
                subs.remove_miscellaneous_events()
                # Fix overlapping display times
                fix_overlapping_display_times(subs)
                subs.save(subtitle_path)

            except exceptions.Pysubs2Error as pysubs2_error:
                print(f"Error while running pysubs2: {pysubs2_error}")
                continue

            end_time = time.time()
            subtitle_time = end_time - start_time
            total_time += subtitle_time
            print(
                f"Subtitles for {file} saved as {subtitle_path} in {subtitle_time:.2f}s"
            )
        except FileNotFoundError as audio_error:
            print(f"FileNotFoundError: {audio_error}")
            continue
        except RuntimeError as transcode_error:
            print(f"RuntimeError: {transcode_error}")
            continue

    print(f"Generated subtitles for {len(file_array)} files in {total_time:.2f}s")
