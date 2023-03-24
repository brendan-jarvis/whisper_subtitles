"""
This is a Python script that utilizes the OpenAI Whisper library to generate
.srt files with subtitles for compatible files. Before running the script,
ensure that the required dependencies, namely OpenAI's Whisper, are installed.
The script generates .srt files for each file found in the directory using
Whisper. Please note that the generated subtitles may not be completely
accurate, and manual correction may be necessary.
"""

import argparse
import os
import time
import whisper
from pysubs2 import load_from_whisper
from utils import split_long_lines


def main(args):
    """
    This function is the main function of the script. It loads the language model,
    searches for files to subtitle, and generates subtitles for each file.
    """
    model = args.model
    file_array = []
    supported_extensions = [".mp4", ".m4a", ".mp3", ".mpeg", ".mpga", ".wav", ".webm"]

    print("Whisper Subtitles script loaded")

    try:
        print(f"Loading the {model} language model...")
        model = whisper.load_model(model)
        if not model:
            raise Exception("Failed to load model")
    except Exception as model_error:
        print(f"Error: {model_error}")
        return

    print("Searching for files to subtitle...")

    try:
        for file in os.listdir(args.directory):
            if file.endswith(tuple(supported_extensions)):
                file_array.append(file)
        if len(file_array) == 0:
            raise Exception("No files found")
    except Exception as file_error:
        print(f"Error: {file_error}")
        return

    print(f"Found {len(file_array)} files to subtitle.")

    total_time = 0
    for file in file_array:
        file_name = os.path.splitext(file)[0]
        subtitle_path = os.path.join(args.output_directory, file_name) + args.format
        if os.path.exists(subtitle_path):
            print(f"{subtitle_path} already exists. Skipping...")
            continue

        print(f"Generating subtitles for {file}...")

        audio = whisper.load_audio(os.path.join(args.directory, file))

        # decode the audio and save subtitles
        try:
            start_time = time.time()
            result: dict = model.transcribe(
                audio,
                verbose=True,
                language=args.language,
                condition_on_previous_text=args.condition_on_previous_text,
            )
            # Split long lines into multiple lines
            for segment in result["segments"]:
                segment["text"] = split_long_lines(segment["text"])

            # Load subtitle file from OpenAI Whisper transcript
            subs = load_from_whisper(result)
            subs.save(subtitle_path)

            end_time = time.time()
            subtitle_time = end_time - start_time
            total_time += subtitle_time
            print(
                f"Subtitles for {file} saved as {subtitle_path} in {subtitle_time:.2f}s"
            )
        except Exception as transcode_error:
            print(f"Error: {transcode_error}")
            continue

    print(f"Generated subtitles for {len(file_array)} files in {total_time:.2f}s")


def cli():
    """
    This function parses the command line arguments and calls the main function.
    """
    ws_description = (
        "This is a Python script that utilizes the OpenAI Whisper library to generate"
        " .srt files with subtitles for compatible files. Before running the script,"
        " ensure that the required dependencies, namely OpenAI's Whisper, are"
        " installed. The script generates .srt files for each file found in the"
        " directory using Whisper. Please note that the generated subtitles may not be"
        " completely accurate, and manual correction may be necessary."
    )
    parser = argparse.ArgumentParser(description=ws_description)
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        help="Language model to use. Options: tiny, base, small, medium, large",
    )
    parser.add_argument(
        "--directory",
        type=str,
        default=".",
        help="Directory containing files to subtitle",
    )
    parser.add_argument(
        "--output_directory",
        type=str,
        default=".",
        help="Directory to save subtitle files",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language to use (see Whisper documentation for options)",
    )
    parser.add_argument(
        "--condition_on_previous_text",
        type=bool,
        default=False,
        help="Condition on previous text (see Whisper documentation)",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="srt",
        help=(
            "Subtitle format. Options: .ass, .srt, .sub, .vtt, and other formats"
            " supported by pysubs2:"
            " https://pysubs2.readthedocs.io/en/latest/formats.html"
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version="whisper_subtitles 1.0.2",
        help="Print version information",
    )
    args = parser.parse_args()
    main(args)


if __name__ == "__main__":
    cli()
