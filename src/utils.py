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


def create_subtitle_from_words(words, max_line_length=37, max_duration_per_word=0.375):
    """Takes a dict of words that have a start and end time
    creates an SSAFile composed of SSAEvents that start with the first word start time
    and end with the last word end time
    Default 37 characters and 0.375 seconds per word."""

    # Create an empty SSAFile to store the subtitles
    subs = pysubs2.SSAFile()

    # Initialize variables to store the current line and its duration
    lines = []
    current_line = ""
    current_duration = 0

    # Iterate over each word in the input dictionary
    for word in words:
        # Check if adding the current word would exceed
        # the maximum line length or duration per number of words in it.
        if (
            len(current_line + word) + 1 > max_line_length
            or (current_duration + len(current_line.split()) * max_duration_per_word)
            > 2
        ):
            # If so, add the current line to list of lines and reset it.
            lines.append(current_line)
            current_line = word

            # Reset duration of current line to that new first word.
            current_duration = len(word) * max_duration_per_word

        else:
            # If not add `current_word` to existing line.

            if current_line == "":
                # If this is first iteration then set `current_line` as `word`
                current_line = word

                # Set `current_duration` as `word_duration`
                current_duration = len(word) * max_duration_per_word

            else:
                # Otherwise append `word` to `current_line`
                current_line += " " + word

                # Add `word_duration` to `current_duration`
                current_duration += len(word) * max_duration_per_word

        if len(lines) >= 2:
            break

    if current_line != "":
        lines.append(current_line)

    text = "\\N".join(lines)

    event = pysubs2.SSAEvent()

    event.start = list(words.values())[0]["start"]

    event.end = list(words.values())[-1]["end"]

    event.text = text

    subs.append(event)

    return subs
