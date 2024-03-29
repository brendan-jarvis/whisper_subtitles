from setuptools import setup, find_packages
from whisper_subtitles.version import __version__ as version

setup(
    name="whisper_subtitles",
    author="Brendan Jarvis",
    url="https://github.com/brendan-jarvis/whisper_subtitles",
    license="MIT",
    version={version},
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=["openai-whisper", "pysubs2"],
    entry_points={
        "console_scripts": [
            "whisper_subtitles=whisper_subtitles.main:cli",
        ],
    },
    extras_require={"dev": ["pytest", "black"]},
)
