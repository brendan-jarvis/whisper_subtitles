"""Script that generates .srt files with subtitles for .mp4 files using OpenAI Whisper library.

Usage:
- Place the script in the directory containing the .mp4 files to generate subtitles for.
- Ensure the required dependencies are installed: OpenAI's Whisper library, Python's os module.
- Run the script using Python interpreter: `python WhisperSubtitles.py`

The script generates .srt files for each .mp4 file found in the directory using Whisper.

Note: Generated subtitles may not be 100% accurate, please correct errors manually.
"""
import os
from utils import write_srt
import whisper


def main():
    model = "large"
    file_array = []
    supported_extensions = [".mp4", ".m4a",
                            ".mp3", ".mpeg", ".mpga", ".wav", ".webm"]

    print("Whisper Subtitles script loaded")

    print(f"Loading the {model} language model...")

    model = whisper.load_model(model)

    if model:
        print("Model loaded successfully")
    else:
        return print("Failed to load model. Exiting...")

    print("Searching for files to subtitle...")

    for file in os.listdir():
        if file.endswith(tuple(supported_extensions)):
            # Add to array
            file_array.append(file)

    # print number of files added to array
    if len(file_array) >= 1:
        print(f"Found {len(file_array)} files to subtitle.")
    else:
        return print("No files found. Exiting...")

    for file in file_array:
        print(f"Generating subtitles for {file}...")

        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(file)
        audio = whisper.pad_or_trim(audio)

        # decode the audio and save as .srt
        result = whisper.transcribe(
            model, audio, verbose=True)

        if len(result["segments"]) == 0:
            print(f"Failed to generate subtitles for {file}. Skipping...")
            continue

        file_name = os.path.splitext(file)[0]

        with open(file_name+'.srt', "w", encoding="utf-8") as srt_file:
            write_srt(result["segments"], file=srt_file)

        # success message
        print(f"Subtitles for {file} saved as {file_name}.srt")


if __name__ == '__main__':
    main()
