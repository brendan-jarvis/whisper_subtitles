import os
import filecmp
import tempfile
import argparse
from whisper_subtitles.main import generate_subtitles


def test_openai_subtitles():
    """
    Tests the open AI transcription.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate subtitles using the OpenAI Whisper
        mock_args = argparse.Namespace(
            model="base",
            language="en",
            input_directory="sample/",
            subtitle_format=".srt",
            output_directory=tmpdir,
            condition_on_previous_text=False,
            max_line_length=42,
            use_cpp=False,  # Won't use whisper.cpp
            fp16=False,  # Avoid FP32 warning
        )
        generate_subtitles(mock_args)
        # Compare the output SRT file to the expected SRT file
        assert filecmp.cmp(
            "sample/test0.srt",
            os.path.join(tmpdir, "test0.srt"),
            shallow=False,
        )


def test_whisper_cpp():
    """
    Tests the whisper.cpp transcription.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Generate subtitles using Whisper.cpp
        mock_args = argparse.Namespace(
            model="base.en",
            language="en",
            input_directory="sample/",
            subtitle_format=".srt",
            output_directory=tmpdir,
            condition_on_previous_text=False,
            max_line_length=42,
            use_cpp=True,  # Will use whisper.cpp
            fp16=True,
        )
        generate_subtitles(mock_args)
        # Compare the output SRT file to the expected SRT file
        assert filecmp.cmp(
            "sample/test0_whisper_cpp_base.en.srt",
            os.path.join(tmpdir, "test0.srt"),
            shallow=False,
        )
