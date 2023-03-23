from setuptools import setup

setup(
    name="WhisperSubtitles",
    version="0.5",
    author="Brendan Jarvis",
    description="Generate subtitles for audio/video files in a directory using OpenAI's Whisper",
    packages=["WhisperSubtitles"],
    install_requires=['openai-whisper'],
)
