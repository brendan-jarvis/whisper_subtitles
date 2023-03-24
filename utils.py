"""
Utilities for the transcript processing transcripts to SRT.
"""

from typing import Iterator, TextIO


def format_timestamp(seconds: float, always_include_hours: bool = False):
    """
    Format a timestamp in seconds as a string in the format HH:MM:SS.mmm.
    """
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    hours_marker = f"{hours}:" if always_include_hours or hours > 0 else ""
    return f"{hours_marker}{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def write_srt(transcript: Iterator[dict], file: TextIO):
    """
    Write a transcript to a file in SRT format.
    """
    for i, segment in enumerate(transcript, start=1):
        print(
            (
                f"{i}\n"
                f"{format_timestamp(segment['start'], always_include_hours=True)} --> "
                f"{format_timestamp(segment['end'], always_include_hours=True)}\n"
                f"{segment['text'].strip().replace('-->', '->')}\n"
            ),
            file=file,
            flush=True,
        )
