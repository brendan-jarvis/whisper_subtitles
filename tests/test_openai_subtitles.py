import os
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
            input_directory="samples/",
            subtitle_format=".srt",
            output_directory=tmpdir,
            condition_on_previous_text=False,
            max_lines=2,
            char_limit=42,
            use_cpp=False,  # Won't use whisper.cpp
            fp16=False,  # Avoid FP32 warning
            use_gpu=False,  # Won't use GPU
        )
        generate_subtitles(mock_args)
        # It generates the subtitle files
        assert os.path.exists(os.path.join(tmpdir, "test0.srt"))
        assert os.path.exists(os.path.join(tmpdir, "test1.srt"))

        # test0.srt contains the words 'artificial intelligence'
        with open(os.path.join(tmpdir, "test0.srt"), "r", encoding="utf-8") as sub_file:
            assert "artificial intelligence" in sub_file.read()

        # test1.srt contains the word Americans
        with open(os.path.join(tmpdir, "test1.srt"), "r", encoding="utf-8") as sub_file:
            assert "Americans" in sub_file.read()
