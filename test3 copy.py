from faster_whisper import WhisperModel
import os

def generate_srt_file(segments, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        segment_number = 1
        for segment in segments:
            f.write(f"{segment_number}\n")
            start_time = segment.start
            end_time = segment.end
            f.write(f"{start_time:.3f} --> {end_time:.3f}\n")
            f.write(f"{segment.text}\n\n")
            segment_number += 1

# Set environment variable to suppress OpenMP warning
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Initialize WhisperModel for transcription
model_size = "medium"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Transcribe audio
segments, info = model.transcribe("D:/projects/Internship_frontend/Sample1.mp3")

# Generate and save SRT file
output_srt_file = "output_transcript2.srt"
generate_srt_file(segments, output_srt_file)
print(f"SRT file '{output_srt_file}' generated successfully.")
