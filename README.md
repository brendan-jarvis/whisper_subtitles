# WhisperSubtitles
Scans a directory for all supported audio/video files and generates .srt files.

## Requirements
Whisper requires Python3.7+ and a recent version of PyTorch (I used PyTorch 1.13.1):
- [Python](https://www.python.org/downloads/?ref=news-tutorials-ai-research) and 
- [PyTorch](https://pytorch.org/get-started/locally/?ref=news-tutorials-ai-research), also
- [CUDA](https://developer.nvidia.com/cuda-downloads)

## Uses
1. Transcribing audio/video content locally.
2. Fallback option for adding subtitles to movies/TV shows that don't already have them.
3. Adding lyrics to a song for DIY Spotify Karaoke.

## Tips
Assuming English audio the 'medium.en' produces good enough results in a relatively quick amount of time.
