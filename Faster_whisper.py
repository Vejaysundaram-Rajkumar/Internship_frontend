from faster_whisper import WhisperModel
import os
from pydub import AudioSegment
import torch

def main_func(audio_file):
    def format_time(seconds):
        """Convert seconds to SRT timestamp format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        milliseconds = int((seconds % 1) * 1000)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    def generate_srt_file(segments, output_file):
        with open(output_file, 'w', encoding='utf-8') as f:
            segment_number = 1
            for segment in segments:
                f.write(f"{segment_number}\n")
                start_time = format_time(segment.start)
                end_time = format_time(segment.end)
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{segment.text}\n\n")
                segment_number += 1
        return output_file

    # Set environment variable to suppress OpenMP warning
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    # Initialize WhisperModel for transcription
    model_size = "medium"
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    torch.set_num_threads(os.cpu_count())

    # Preprocess audio to 16kHz
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000)
    # Transcribe audio
    segments, info = model.transcribe(audio_file)

    filename = audio_file.split('.')[0] + "_transcript.srt"
    filename = generate_srt_file(segments, filename)
    return filename
