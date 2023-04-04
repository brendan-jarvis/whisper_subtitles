"""
Utility functions for the subtitle generator.
"""
import pysubs2
import json


def split_long_lines(result, max_line_length=42, max_lines=2):
    """
    Split long lines into multiple lines. Returns a SSAFile
    """
    # Create a new SSAFile object
    subs = pysubs2.SSAFile()

    # Save result to a file
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    # Add the subtitles to the file as SSAEvents
    for segment in result["segments"]:
        subtitle = pysubs2.SSAEvent()

        if len(segment["text"]) < max_line_length:
            first_word = segment["words"][0]
            last_word = segment["words"][-1]
            subtitle.start = int(first_word["start"] * 1000)
            subtitle.end = int(last_word["end"] * 1000)
            subtitle.text = segment["text"]
            subs.append(subtitle)
            continue

        lines = []
        current_line = ""

        for word in segment["words"]:
            if len(current_line) + len(word) + 1 > max_line_length:
                # If the number of lines is less than the maximum number of lines
                # Then add the current line to the lines array and reset it
                if len(lines) < max_lines - 1:
                    lines.append(current_line)
                    current_line = ""
                else:
                    lines.append(current_line)
                    subtitle.text = "\n".join(lines)
                    last_word = segment["words"][len(lines) - 1]
                    subtitle.start = int(segment["words"][0]["start"] * 1000)
                    subtitle.end = int(last_word["end"] * 1000)
                    subs.append(subtitle)
                    current_line = ""
                    subtitle = pysubs2.SSAEvent()
                    subtitle.start = int(word["start"] * 1000)
            else:
                current_line += word["word"]
                subtitle.end = int(word["end"] * 1000)

        # Add the last line
        print(current_line)
        print(subtitle.start, subtitle.end, subtitle.text)
        lines.append(current_line)
        subtitle.text = "\n".join(lines)
        subs.append(subtitle)

    # Return the file
    return subs


def fix_overlapping_display_times(subs):
    """Find overlapping lines, reduce end time of first sub by 00:00:00,001 to fix the error."""
    for i in range(len(subs) - 1):
        if subs[i].end > subs[i + 1].start:
            subs[i].end = subs[i + 1].start - 1
