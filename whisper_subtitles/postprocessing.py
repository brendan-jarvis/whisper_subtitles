"""
Utility functions for the subtitle generator.
"""
import pysubs2


def split_long_lines(result, max_line_length=42, max_lines=2):
    """
    Split long lines into multiple lines. Returns a SSAFile
    """
    # Create a new SSAFile object
    subs = pysubs2.SSAFile()

    # Add the subtitles to the file as SSAEvents
    for segment in result["segments"]:
        # Split the line into words
        words = segment["words"]

        # Create a new line
        line = ""

        # Create a new subtitle
        subtitle = pysubs2.SSAEvent()

        # Add words to the line until it is too long
        for word in words:
            if len(line) + len(word) + 1 > max_line_length:
                subtitle.text = line
                subs.append(subtitle)
                line = ""
                subtitle = pysubs2.SSAEvent()
                subtitle.start = int(word["start"] * 1000)
            line += word["word"]
            subtitle.end = int(word["end"] * 1000)

        # Add the last subtitle
        subtitle.text = line
        subs.append(subtitle)

    # Return the file
    return subs


def fix_overlapping_display_times(subs):
    """Find overlapping lines, reduce end time of first sub by 00:00:00,001 to fix the error."""
    for i in range(len(subs) - 1):
        if subs[i].end > subs[i + 1].start:
            subs[i].end = subs[i + 1].start - 1
