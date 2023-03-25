import os
import filecmp
import tempfile
from whisper_subtitles.main import generate_subtitles


def test_generate_subtitles():
    """
    This function tests the generate_subtitles function.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate subtitles using the function
        generate_subtitles(
            model="base",
            language="en",
            input_directory="sample/",
            subtitle_format=".srt",
            output_directory=tmpdir,
            condition_on_previous_text=False,
            max_line_length=42,
        )
        # Compare the output SRT file to the expected SRT file
        assert filecmp.cmp(
            "sample/test0.srt", os.path.join(tmpdir, "test0.srt"), shallow=False
        )
