"""
Utility functions for the subtitle generator.
"""


def split_long_lines(result, max_line_length=42, max_lines=2):
    """
    Split long lines into multiple lines. This is useful for subtitles, where
    long lines can cause problems with display.
    Default 42 characters
    """
    # create a new dictionary to store the modified result
    word_timed_segments = {"text": result["text"], "segments": []}
    new_segment = {"id": 0, "start": 0, "end": 0, "text": ""}

    # loop through each segment in the original result
    for segment in result["segments"]:
        words = segment["words"]

        # calculate the total length of the segment in characters
        total_length = len(segment["text"])

        # segment text is greater than the maximum line length
        if total_length > max_line_length:
            lines = []
            current_line = ""

            for word in words:
                if len(current_line + word["word"]) + 1 > max_line_length:
                    lines.append(current_line)
                    current_line = word["word"]
                elif current_line == "":
                    new_segment["start"] = word["start"]
                    current_line = word["word"]
                else:
                    new_segment["end"] = word["end"]
                    current_line += word["word"]

            if current_line != "":
                lines.append(current_line)

            new_segment["text"] = "\n".join(lines)

            # add the line to the new list of segments
            word_timed_segments["segments"].append(new_segment)
        else:
            # if the segment is shorter than the maximum line length,
            # simply add it to the new list of segments
            new_segment = {
                "id": new_segment["id"],
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"],
            }
            word_timed_segments["segments"].append(new_segment)
        # reset new_segment with incremented id
        new_segment = {
            "id": new_segment["id"] + 1,
            "start": 0,
            "end": 0,
            "text": "",
        }

    # return the modified result
    return word_timed_segments


def fix_overlapping_display_times(subs):
    """Find overlapping lines, reduce end time of first sub by 00:00:00,001 to fix the error."""
    for i in range(len(subs) - 1):
        if subs[i].end > subs[i + 1].start:
            subs[i].end = subs[i + 1].start - 1
