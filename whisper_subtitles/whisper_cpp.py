import os
import subprocess
import tempfile


def transcribe_with_cpp(file_array, args):
    """
    Takes an array of files, converts them to .wav 16khz (if necessary), and runs whisper.cpp.
    """
    # Check if whisper.cpp exists
    if not os.path.exists("whisper.cpp"):
        subprocess.run(
            ["git", "clone", "https://github.com/ggerganov/whisper.cpp.git"], check=True
        )

    # Build whisper.cpp using cmake if not already built
    if not os.path.exists("whisper.cpp/build/bin/whisper-cli"):
        subprocess.run(["cmake", "-B", "build"], check=True, cwd="whisper.cpp")
        subprocess.run(
            ["cmake", "--build", "build", "--config", "Release"],
            check=True,
            cwd="whisper.cpp",
        )

    # Check if the model exists, download if needed
    if not os.path.exists(f"whisper.cpp/models/ggml-{args.model}.bin"):
        print(f"Model {args.model} does not exist. Downloading...")
        subprocess.run(
            ["bash", "whisper.cpp/models/download-ggml-model.sh", f"{args.model}"],
            check=True,
        )

    # Create a temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        for file in file_array:
            # Check encoding of file is 16-bit using ffprobe
            encoding = subprocess.run(
                [
                    "ffprobe",
                    "-v",
                    "error",
                    "-show_entries",
                    "stream=bits_per_sample",
                    "-of",
                    "default=noprint_wrappers=1:nokey=1",
                    f"{args.input_directory}{file}",
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            encoding = encoding.stdout.decode("utf-8").strip()

            if encoding == "16" and file.endswith(".wav"):
                # If file is already 16-bit WAV format, copy it to the temp directory
                print(f"\nCopying {file} to {temp_dir}\n")
                subprocess.run(
                    [
                        "cp",
                        f"{args.input_directory}{file}",
                        f"{temp_dir}/{os.path.splitext(os.path.basename(file))[0]}.wav",
                    ],
                    check=True,
                )
            else:
                # Otherwise convert file to 16-bit WAV format and save it in the temp directory
                output_file_name = os.path.splitext(os.path.basename(file))[0]
                print(
                    f"In {os.getcwd()} converting {args.input_directory}{file} to"
                    " 16-bit WAV format...\n"
                )
                print(f"\nConverting {file} to 16-bit WAV format...\n")
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        f"{args.input_directory}{file}",
                        "-ar",
                        "16000",
                        "-ac",
                        "1",
                        "-c:a",
                        "pcm_s16le",
                        f"{temp_dir}/{output_file_name}.wav",
                    ],
                    check=True,
                )

                print(
                    f"\nConverted {output_file_name} to 16-bit WAV format and saved it"
                    f" in {temp_dir}\n"
                )

            print(f"\nRunning Whisper.cpp on /{output_file_name}.wav\n")

            # Run whisper.cpp on the 16-bit .wav file
            subprocess.run(
                [
                    "whisper.cpp/build/bin/whisper-cli",
                    "-f",
                    f"{temp_dir}/{output_file_name}.wav",
                    "-m",
                    f"whisper.cpp/models/ggml-{args.model}.bin",
                    "--max-len",
                    f"{args.char_limit}",
                    f"--output-{args.subtitle_format.replace('.', '')}",
                    "-of",
                    f"{args.output_directory}/{output_file_name}",
                ],
                check=True,
            )

            print(
                "Saved to "
                f" \n{args.output_directory}/{output_file_name}{args.subtitle_format}\n"
            )
