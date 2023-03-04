import argparse
import os
from utils import write_srt
import whisper


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
                # Add to array
                file_array.append(file)
        if len(file_array) == 0:
            raise Exception("No files found")
    except Exception as e:
        print(f"Error: {e}")
        return

    # print number of files added to array
    print(f"Found {len(file_array)} files to subtitle.")

    for file in file_array:
        print(f"Generating subtitles for {file}...")

        # load audio and pad/trim it to fit 30 seconds
        audio = whisper.load_audio(os.path.join(args.directory, file))

        # decode the audio and save as .srt
        try:
            result = whisper.transcribe(model, audio, verbose=True)
            if len(result["segments"]) == 0:
                raise Exception(f"No subtitles generated for {file}")
            file_name = os.path.splitext(file)[0]
            with open(os.path.join(args.output_directory, file_name + '.srt'), "w", encoding="utf-8") as srt_file:
                write_srt(result["segments"], file=srt_file)
            print(f"Subtitles for {file} saved as {file_name}.srt")
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Whisper Subtitles')
    parser.add_argument('--model', type=str, default='large',
                        help='Language model to use. Options: tiny, base, small, medium, large')
    parser.add_argument('--directory', type=str, default='.',
                        help='Directory containing files to subtitle')
    parser.add_argument('--output_directory', type=str,
                        default='.', help='Directory to save subtitle files')
    args = parser.parse_args()
    main(args)