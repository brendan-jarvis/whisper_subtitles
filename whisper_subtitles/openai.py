import os
import time
import whisper
from pysubs2 import load_from_whisper, exceptions
from whisper_subtitles.postprocessing import (
    split_long_lines,
    fix_overlapping_display_times,
)


def transcribe_with_whisper(file_array, args):
    """
    Transcribes audio files using OpenAI's Whisper.
    """
    try:
        print(f"Loading the {args.model} language model...")
        model = whisper.load_model(args.model)
        if not model:
            raise RuntimeError("Failed to load model")
    except RuntimeError as model_error:
        print(f"RuntimeError loading the model: {model_error}")
        return

    total_time = 0
    for file in file_array:
        file_name = os.path.splitext(file)[0]
        subtitle_path = (
            os.path.join(args.output_directory, file_name) + args.subtitle_format
        )
        if os.path.exists(subtitle_path):
            print(f"{subtitle_path} already exists. Skipping...")
            continue

        print(f"Generating subtitles for {file}...")

        audio = whisper.load_audio(os.path.join(args.input_directory, file))

        # decode the audio and save subtitles
        try:
            start_time = time.time()
            result: dict = model.transcribe(
                audio,
                verbose=True,
                language=args.language,
                condition_on_previous_text=args.condition_on_previous_text,
                word_timestamps=True,
                fp16=args.fp16,
            )

            try:
                # Load subtitle file from OpenAI Whisper transcript
                subs = load_from_whisper(result)
                # Split long lines into multiple lines
                for sub in subs:
                    sub.text = split_long_lines(sub.text, args.max_line_length)
                # Remove miscellaneous events
                subs.remove_miscellaneous_events()
                # Fix overlapping display times
                fix_overlapping_display_times(subs)
                subs.save(subtitle_path)

            except exceptions.Pysubs2Error as pysubs2_error:
                print(f"Error while running pysubs2: {pysubs2_error}")
                continue

            end_time = time.time()
            subtitle_time = end_time - start_time
            total_time += subtitle_time
            print(
                f"Subtitles for {file} saved as {subtitle_path} in {subtitle_time:.2f}s"
            )
        except FileNotFoundError as audio_error:
            print(f"FileNotFoundError: {audio_error}")
            continue
        except RuntimeError as transcode_error:
            print(f"RuntimeError: {transcode_error}")
            continue

    print(f"Generated subtitles for {len(file_array)} files in {total_time:.2f}s")
