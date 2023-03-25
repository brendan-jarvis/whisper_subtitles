# Whisper Subtitles

This is a Python script that utilizes the OpenAI Whisper library to generate .srt files with subtitles for compatible audio and video files. The script generates .srt files for each file found in the specified directory using Whisper. Please note that the generated subtitles may not be completely accurate, and manual correction may be necessary.

## Uses

1. Transcribing audio/video content locally.
2. Fallback option for adding subtitles to movies/TV shows that don't already have them.
3. Adding lyrics to a song for DIY Spotify Karaoke.

## Installation

To use the Whisper Subtitles Python script, you'll need to create a virtual environment and install the required dependencies. Here's how you can do that:

Clone the repository and navigate into it

```sh
git clone https://github.com/brendan-jarvis/whisper_subtitles
cd whisper_subtitles/
```

Using either conda or venv create a Python environment. For example, to create a new virtual environment named "venv" using venv, you can run the following command:

```sh
python -m venv venv
```

Activate the virtual environment. On Unix or Linux systems, you can use the following command:

```sh
source venv/bin/activate
```

On Windows, use the following command:

```sh
source venv/Scripts/activate
```

Once your virtual environment is activated, you can install the required dependencies by running the following command:

```sh
pip install -r requirements.txt
```

This command will install all the Python dependencies, including OpenAI's Whisper library and its dependencies.

### Whisper.cpp dependencies

Whisper.cpp usage requires [ffmpeg](https://ffmpeg.org/download.html), to convert input to 16-bit WAV files:

```sh
sudo apt update
sudo apt install ffmpeg
```

Whisper requires Python3.7+ and a recent version of PyTorch (I used PyTorch 1.13.1):

- [Python](https://www.python.org/downloads/?ref=news-tutorials-ai-research) and
- [PyTorch](https://pytorch.org/get-started/locally/?ref=news-tutorials-ai-research), also
- [CUDA](https://developer.nvidia.com/cuda-downloads)

Finally, you can run the whisper_subtitles.py script by running the following command:

```sh
python whisper_subtitles.py
```

You can also pass in any of the optional arguments listed in the script's usage instructions to customize the behavior of the script.

That's it! You should now be able to use the Whisper Subtitles script to generate subtitles for compatible files.

### Tips

1. Assuming English audio the 'medium.en' produces good enough results in a relatively quick amount of time.
2. You can edit the generated subtitles using [Subtitle Edit](https://github.com/SubtitleEdit/subtitleedit)
3. You could try "automagically" synchronizing subtitles using [FFsubsync](https://github.com/smacke/ffsubsync) - **Note: this project is intended to re-align timing on otherwise 100% accurate subtitles and may not be helpful for correcting timings on AI-generated subtitles.**

## Usage

Before running the script, ensure that the required dependencies, namely OpenAI's Whisper, are installed.

To run the script, use the following command:

```sh
python whisper_subtitles.py [-h] [--model MODEL] [--directory DIRECTORY] [--output_directory OUTPUT_DIRECTORY]
[--language LANGUAGE] [--condition_on_previous_text CONDITION_ON_PREVIOUS_TEXT]
```

The script accepts the following optional arguments:

- **--model**: Language model to use. Options: tiny, base, small, medium, large
- **--directory**: Directory containing files to subtitle
- **--output_directory**: Directory to save subtitle files
- **--language**: Language to use (see Whisper documentation for options)
- **--condition_on_previous_text**: Condition on previous text (see Whisper documentation)

For example, to generate subtitles for all files in the current directory using the large language model and save the subtitles in the subtitles directory, run:

```
python whisper_subtitles.py --model medium.en --language en
```
