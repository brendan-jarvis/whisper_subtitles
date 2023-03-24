"""
Utility functions for the subtitle generator.
"""


def split_long_lines(text, max_line_length=37):
    """
    Split long lines into multiple lines. This is useful for subtitles, where
    long lines can cause problems with display.
    Default 37 characters based on BBC Subtitle Guidelines:
    https://www.bbc.co.uk/accessibility/forproducts/guides/subtitles/
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
