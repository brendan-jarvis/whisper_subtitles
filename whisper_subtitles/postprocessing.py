"""
Utility functions for the subtitle generator.
"""
import pysubs2


def split_long_lines(text, max_line_length=42):
    """
    Split long lines into multiple lines. This is useful for subtitles, where
    long lines can cause problems with display.
    Default 42 characters
    """
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line + word) + 1 > max_line_length:
            lines.append(current_line)
            current_line = word
        else:
            if current_line == "":
                current_line = word
            else:
                current_line += " " + word

    if current_line != "":
        lines.append(current_line)

    return "\n".join(lines)


def fix_overlapping_display_times(subs):
    """Find overlapping lines, reduce end time of first sub by 00:00:00,001 to fix the error."""
    for i in range(len(subs) - 1):
        if subs[i].end > subs[i + 1].start:
            subs[i].end = subs[i + 1].start - 1
