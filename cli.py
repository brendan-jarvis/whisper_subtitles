"""
This module contains the command line interface for the whisper_subtitles package.
"""

import argparse
from whisper_subtitles.main import generate_subtitles


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
        "-ml",
        "--max_line_length",
        type=int,
        default=42,
        help="Maximum characters per line in the subtitles. Default is 42.",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version="whisper_subtitles 1.0.2",
        help="Print version information",
    )
    parser.add_argument(
        "-fp16",
        "--fp16",
        type=bool,
        default=True,
        help="Use fp16 for inference",
    )
    args = parser.parse_args()
    generate_subtitles(
        args.model,
        args.input_directory,
        args.output_directory,
        args.language,
        args.condition_on_previous_text,
        args.subtitle_format,
        args.max_line_length,
        args.fp16,
    )


if __name__ == "__main__":
    cli()
