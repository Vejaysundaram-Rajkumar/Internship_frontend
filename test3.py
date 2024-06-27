from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torchaudio
import torch

# Load Wav2Vec 2.0 model and processor
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-large-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h")

# Function to transcribe audio
def transcribe_audio(audio_path):
    # Load audio file
    waveform, sample_rate = torchaudio.load(audio_path)
    
    # Perform inference
    input_values = processor(waveform, sampling_rate=sample_rate, return_tensors="pt").input_values
    logits = model(input_values).logits
    
    # Decode logits to transcription
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(predicted_ids)[0]
    
    return transcription

# Path to your audio file
audio_path = "D:/projects/Internship_frontend/Sample1.mp3"

# Transcribe audio and print the result
transcription = transcribe_audio(audio_path)
print("Transcription:", transcription)
