"""
Utility functions for the subtitle generator.
"""
import pysubs2


def split_long_lines(result, max_line_length=42, max_lines=2):
    """
    Split long lines into multiple lines. Returns a SSAFile.
    """
    # Create a new SSAFile object
    subs = pysubs2.SSAFile()

    # Add the subtitles to the file as SSAEvents
    for segment in result["segments"]:
        subtitle = pysubs2.SSAEvent()
        if len(segment["words"]) > 0:
            first_word = segment["words"][0]
            last_word = segment["words"][-1]
            subtitle.start = int(first_word["start"] * 1000)
            subtitle.end = int(last_word["end"] * 1000)
        else:
            # If there are no words in the segment, skip it
            continue
        if len(segment["text"]) < max_line_length:
            subtitle.start = int(segment["start"] * 1000)
            subtitle.end = int(segment["end"] * 1000)
            subtitle.text = segment["text"]
            subs.append(subtitle)
            continue

        lines = []
        current_line = ""

        for word in segment["words"]:
            if len(current_line) + len(word["word"].strip() + " ") > max_line_length:
                if len(lines) < max_lines - 1:
                    # Add the line and reset
                    lines.append(current_line)
                    current_line = word["word"].strip() + " "
                    subtitle.end = int(word["end"] * 1000)
                else:
                    # Yield a SSAEvent
                    lines.append(current_line)
                    subtitle.text = "\n".join(lines)
                    subs.append(subtitle)

                    # Reset the variables
                    current_line = word["word"].strip() + " "
                    lines = []
                    subtitle = pysubs2.SSAEvent()
                    subtitle.start = int(word["start"] * 1000)
                    subtitle.end = int(word["end"] * 1000)
            else:
                current_line += word["word"].strip() + " "
                subtitle.end = int(word["end"] * 1000)

        # Add the last line in the segment
        lines.append(current_line)
        subtitle.text = "\n".join(lines)
        subs.append(subtitle)

    # Return the file
    return subs


def fix_overlapping_display_times(subs):
    """Find overlapping lines, reduce end time of first sub by 00:00:00,001 to fix the error."""
    for i in range(len(subs) - 1):
        if subs[i].end >= subs[i + 1].start:
            subs[i].end = subs[i + 1].start - 1
