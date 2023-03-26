import os
import filecmp
import tempfile
from whisper_subtitles.main import generate_subtitles


def test_generate_subtitles():
    """
    This function tests the generate_subtitles function.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate subtitles using the OpenAI Whisper
        args = {
            "model": "base.en",
            "language": "en",
            "input_directory": "sample/",
            "subtitle_format": ".srt",
            "output_directory": tmpdir,
            "condition_on_previous_text": False,
            "max_line_length": 42,
            "use_cpp": False,  # Won't use whisper.cpp
            "fp16": False,  # Avoid FP32 warning
        }
        generate_subtitles(args)
        # Compare the output SRT file to the expected SRT file
        assert filecmp.cmp(
            "sample/test0.srt", os.path.join(tmpdir, "test0.srt"), shallow=False
        )
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate subtitles using Whisper.cpp
        args = {
            "model": "base.en",
            "language": "en",
            "input_directory": "sample/",
            "subtitle_format": ".srt",
            "output_directory": tmpdir,
            "condition_on_previous_text": False,
            "max_line_length": 42,
            "use_cpp": True,  # Will use whisper.cpp
            "fp16": True,
        }
        generate_subtitles(args)
        # Compare the output SRT file to the expected SRT file
        assert filecmp.cmp(
            "sample/test0_whisper_cpp_base.en.srt",
            os.path.join(tmpdir, "test0.srt"),
            shallow=False,
        )
