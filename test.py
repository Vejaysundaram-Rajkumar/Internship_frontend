from faster_whisper import WhisperModel
import os
from pydub import AudioSegment
import torch

def format_time(seconds):
    print("Formatting.....")
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt_file(transcripts, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        segment_number = 1
        for transcript in transcripts:
            f.write(f"{segment_number}\n")
            start_time = format_time(transcript["start"])
            end_time = format_time(transcript["end"])
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{transcript['text']}\n\n")
            segment_number += 1
    return output_file

def transcribe_segment(model, segment, start_time):
    print("Transcribing....")
    segments, _ = model.transcribe(segment)
    transcripts = []
    print("Done transcribing....")
    for seg in segments:
        transcripts.append({
            "start": start_time + seg.start,
            "end": start_time + seg.end,
            "text": seg.text
        })
    return transcripts

def main_func(audio_file):
    # Set environment variable to suppress OpenMP warning
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    # Initialize WhisperModel for transcription
    model_size = "medium"  # Try using 'small' or 'base'
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    # Ensure full CPU utilization
    torch.set_num_threads(os.cpu_count())

    # Preprocess audio to 16kHz
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000)
    print("audio pre-processing done")
    # Split audio into 30-second segments
    segment_length = 30 * 1000  # 30 seconds in milliseconds
    audio_segments = [audio[i:i + segment_length] for i in range(0, len(audio), segment_length)]
    print("audio segmenting done",len(audio_segments))
    all_transcripts = []
    for idx, segment in enumerate(audio_segments):
        # Export each segment to a temporary file
        temp_audio_file = f"temp_audio_{idx}.mp3"
        segment.export(temp_audio_file, format="mp3")
        
        # Transcribe the segment
        start_time = idx * 30
        transcripts = transcribe_segment(model, temp_audio_file, start_time)
        all_transcripts.extend(transcripts)
        
        # Clean up temporary audio file
        os.remove(temp_audio_file)
        print("A Frame of transcript complete.")

    # Generate SRT file
    output_file = audio_file.split('.')[0] + "_transcript3.srt"
    output_file = generate_srt_file(all_transcripts, output_file)
    return output_file

main_func("D:/projects/Internship_frontend/uploads/tamilsample_audio.mp3")
