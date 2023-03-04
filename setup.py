from setuptools import setup, find_packages

setup(
    version="0.5",
    name="WhisperSubtitles",
    packages=find_packages(),
    py_modules=["whisper_subtitles"],
    author="Brendan Jarvis",
    install_requires=[
        'openai-whisper'
    ],
    description="Generate subtitles for videos using Whisper",
    entry_points={
        'console_scripts': ['whisper_subtitles=whisper_subtitles.main:main'],
    },
    include_package_data=True,
)
