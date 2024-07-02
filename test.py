from faster_whisper import WhisperModel
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
# Path to the directory containing the model files
model_dir = "D:/projects/Internship_frontend/model"

# Load the WhisperModel from local files
model = WhisperModel(model_dir, device="cpu", compute_type="int8")

# Example: Transcribe an audio file
audio_path = "D:/projects/Internship_frontend/Sample 3.mp3"
segments, info = model.transcribe(audio_path)

# Process the transcription results
for segment in segments:
    print(f"Start: {segment.start}, End: {segment.end}, Text: {segment.text}")
