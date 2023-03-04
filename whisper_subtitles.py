import argparse
import os
import time
import whisper
from whisper.utils import get_writer


def main(args):
    model = args.model
    file_array = []
    supported_extensions = [".mp4", ".m4a",
                            ".mp3", ".mpeg", ".mpga", ".wav", ".webm"]

    print("Whisper Subtitles script loaded")

    try:
        print(f"Loading the {model} language model...")
        model = whisper.load_model(model)
        if not model:
            raise Exception("Failed to load model")
    except Exception as e:
        print(f"Error: {e}")
        return

    print("Searching for files to subtitle...")

    try:
        for file in os.listdir(args.directory):
            if file.endswith(tuple(supported_extensions)):
                file_array.append(file)
        if len(file_array) == 0:
            raise Exception("No files found")
    except Exception as e:
        print(f"Error: {e}")
        return

    # print number of files added to array
    print(f"Found {len(file_array)} files to subtitle.")

    total_time = 0
    for file in file_array:
        file_name = os.path.splitext(file)[0]
        srt_path = os.path.join(args.output_directory, file_name + '.srt')
        if os.path.exists(srt_path):
            print(f"{srt_path} already exists. Skipping...")
            continue

        print(f"Generating subtitles for {file}...")

        # load audio
        audio = whisper.load_audio(os.path.join(args.directory, file))

        # decode the audio and save as .srt
        try:
            start_time = time.time()
            result = model.transcribe(
                audio, verbose=True, language=args.language,
                condition_on_previous_text=args.condition_on_previous_text)
            with open(os.path.join(args.output_directory, file_name + '.srt'),
                      "w", encoding="utf-8") as srt_file:
                get_writer("srt", args.output_directory)(
                    result["segments"], srt_file)
            end_time = time.time()
            subtitle_time = end_time - start_time
            total_time += subtitle_time
            print(
                f"Subtitles for {file} saved as {file_name}.srt in {subtitle_time:.2f}s")
        except Exception as e:
            print(f"Error: {e}")
            continue

    print(
        f"Generated subtitles for {len(file_array)} files in {total_time:.2f}s")


def cli():
    WS_DESCRIPTION = "This is a Python script that utilizes the OpenAI Whisper library to generate .srt files with subtitles for compatible files. Before running the script, ensure that the required dependencies, namely OpenAI's Whisper, are installed. The script generates .srt files for each file found in the directory using Whisper. Please note that the generated subtitles may not be completely accurate, and manual correction may be necessary."
    parser = argparse.ArgumentParser(description=WS_DESCRIPTION)
    parser.add_argument('--model', type=str, default='large',
                        help='Language model to use. Options: tiny, base, small, medium, large')
    parser.add_argument('--directory', type=str, default='.',
                        help='Directory containing files to subtitle')
    parser.add_argument('--output_directory', type=str,
                        default='.', help='Directory to save subtitle files')
    parser.add_argument('--language', type=str, default='en',
                        help='Language to use (see Whisper documentation for options)')
    parser.add_argument('--condition_on_previous_text', type=bool, default=False,
                        help='Condition on previous text (see Whisper documentation)')
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    cli()
