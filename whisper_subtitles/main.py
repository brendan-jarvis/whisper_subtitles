"""
This is a Python script that utilizes the OpenAI Whisper and ggerganov 
whisper.cpp libraries to generate .srt files with subtitles for compatible files. 
The script generates .srt files for each file found in the directory using
Whisper or Whisper.cpp - based on CUDA detection or where '--use_cpp True' forces 
CPU transcription. 
Please note that the generated subtitles may not be completely accurate, 
and manual correction may be necessary.
"""


import os
import argparse
from torch import cuda
from .whisper_cpp import transcribe_with_cpp
from .openai import transcribe_with_whisper
try:
    from ._version import __version__ as version
except ImportError:
    from importlib.metadata import version as get_version
    version = get_version("whisper_subtitles")


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
        "-m",
        "--model",
        type=str,
        default="base",
        help="Language model to use. Options: tiny, base, small, medium, large",
    )
    parser.add_argument(
        "-i",
        "--input_directory",
        type=str,
        default=".",
        help="Directory containing files to subtitle",
    )
    parser.add_argument(
        "-o",
        "--output_directory",
        type=str,
        default=".",
        help="Directory to save subtitle files",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default="en",
        help="Language to use (see Whisper documentation for options)",
    )
    parser.add_argument(
        "-c",
        "--condition_on_previous_text",
        type=bool,
        default=False,
        help="Condition on previous text (see Whisper documentation)",
    )
    parser.add_argument(
        "-f",
        "--subtitle_format",
        type=str,
        default=".srt",
        help=(
            "Subtitle format. Options: .ass, .srt, .sub, .vtt, and other formats"
            " supported by pysubs2:"
            " https://pysubs2.readthedocs.io/en/latest/formats.html"
        ),
    )
    parser.add_argument(
        "-cl",
        "--char_limit",
        type=int,
        default=42,
        help="Maximum characters per line in the subtitles. Default is 42.",
    )
    parser.add_argument(
        "-ml",
        "--max_lines",
        type=int,
        default=2,
        help="Maximum lines per subtitle event. Default is 2.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"whisper_subtitles {version}",
        help="Print version information",
    )
    parser.add_argument(
        "-fp16",
        "--fp16",
        type=bool,
        default=True,
        help="Use fp16 for inference",
    )
    parser.add_argument(
        "-cpp",
        "--use_cpp",
        type=bool,
        default=False,
        help="Use Whisper.CPP for transcription",
    )
    parser.add_argument(
        "-g",
        "--use_gpu",
        type=bool,
        default=False,
        help="Force use of Whisper (GPU) for transcription",
    )
    args = parser.parse_args()
    generate_subtitles(args)


def generate_subtitles(args):
    """
    This function is the main function of the script. It loads the language model,
    searches for files to subtitle, and generates subtitles for each file.
    """
    file_array = []
    supported_extensions = [
        ".mp4",
        ".mkv",
        ".m4a",
        ".mp3",
        ".mpeg",
        ".mpga",
        ".wav",
        ".webm",
    ]

    print("Whisper Subtitles script loaded\n")

    print("Searching for files to subtitle...\n")

    try:
        if os.path.isfile(args.input_directory) and args.input_directory.endswith(
            tuple(supported_extensions)
        ):
            print("Input file is supported, added.\n")
            file_array.append(args.input_directory)
        elif os.path.isdir(args.input_directory):
            print("Adding supported files in input directory.\n")
            for file in os.listdir(args.input_directory):
                if file.endswith(tuple(supported_extensions)):
                    file_array.append(file)
        else:
            raise FileNotFoundError("Input is not a valid file or directory!")
        if len(file_array) == 0:
            raise FileNotFoundError("No supported file(s) found in the input!")
    except FileNotFoundError as file_error:
        print(f"FileNotFoundError: {file_error}")
        return

    print(
        f"Found {len(file_array)} file{'s' if len(file_array) > 1 else ''} to"
        " subtitle.\n"
    )

    if args.use_cpp:
        print("--use_cpp=True. Using Whisper.CPP (CPU).\n")
        transcribe_with_cpp(file_array, args)
    elif cuda.is_available() or args.use_gpu:
        print("CUDA is available. Using OpenAI Whisper (GPU).\n")
        transcribe_with_whisper(file_array, args)
    elif args.fp16 is False:
        print("--args.fp16 is False. Using OpenAI Whisper (CPU).\n")
        transcribe_with_whisper(file_array, args)
    else:
        print("CUDA is not available. Using Whisper.CPP (CPU)\n")
        transcribe_with_cpp(file_array, args)


if __name__ == "__main__":
    cli()
