"""
Utilities for the transcript processing transcripts to SRT.
"""
import pysubs2


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


def create_subtitles(data):
    """
    This function creates subtitles from the data returned by the model.
    """
    subs = pysubs2.SSAFile()
    for segment in data["segments"]:
        subs.append(
            pysubs2.SSAEvent(
                start=segment["start"] * 1000,
                end=segment["end"] * 1000,
                text=segment["text"],
            )
        )
    return subs
