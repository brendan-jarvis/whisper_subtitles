import os
import time
import whisper
import pysubs2
from whisper_subtitles.postprocessing import (
    split_long_lines,
    fix_overlapping_display_times,
)


def transcribe_with_whisper(file_array, args):
    """
    Transcribes audio files using OpenAI's Whisper.
    """
    try:
        print(f"Loading the {args.model} language model...\n")
        model = whisper.load_model(args.model)
        if not model:
            raise RuntimeError("Failed to load model!")
    except RuntimeError as model_error:
        print(f"RuntimeError loading the model: {model_error}!")
        return

    total_time = 0
    total_transcribed = 0
    for file in file_array:
        file_name = os.path.splitext(os.path.basename(file))[0]
        subtitle_path = (
            os.path.join(args.output_directory, file_name) + args.subtitle_format
        )
        print(f"Transcribing {file} to {subtitle_path}\n")
        if os.path.exists(subtitle_path):
            print(
                "Skipping transcription as there are already subtitles at"
                f" {subtitle_path}\n"
            )
            continue

        print(f"Generating subtitles for {file}...")

        # load the audio
        if os.path.isfile(args.input_directory):
            audio = whisper.load_audio(args.input_directory)
        else:
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
            subs: pysubs2.SSAFile = split_long_lines(
                result, args.char_limit, args.max_lines
            )

            try:
                # Remove miscellaneous events
                subs.remove_miscellaneous_events()
                # Fix overlapping display times
                fix_overlapping_display_times(subs)
                subs.save(subtitle_path)

            except pysubs2.Pysubs2Error as pysubs2_error:
                print(f"Error while running pysubs2: {pysubs2_error}")
                continue

            end_time = time.time()
            subtitle_time = end_time - start_time
            total_time += subtitle_time
            total_transcribed += 1
            print(
                f"Subtitles for {file} saved as {subtitle_path} in {subtitle_time:.2f}s"
            )
        except FileNotFoundError as audio_error:
            print(f"FileNotFoundError: {audio_error}")
            continue
        except RuntimeError as transcode_error:
            print(f"RuntimeError: {transcode_error}")
            continue

    print(f"Generated subtitles for {total_transcribed} files in {total_time:.2f}s")
