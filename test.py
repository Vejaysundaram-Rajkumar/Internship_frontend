from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq
import torch
import librosa


def transcribe_audio(audio_path, model_name="openai/whisper-small"):
    # Load processor and model
    processor = AutoProcessor.from_pretrained("steja/whisper-small-tamil")
    model = AutoModelForSpeechSeq2Seq.from_pretrained("steja/whisper-small-tamil")

    # Load and preprocess the audio
    audio, rate = librosa.load(audio_path, sr=16000)  # Ensure audio is 16kHz
    inputs = processor(audio, return_tensors="pt", sampling_rate=rate)

    # Generate transcription
    with torch.no_grad():
        outputs = model.generate(input_ids=inputs["input_features"])

    # Decode the transcription
    transcription = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    return transcription

# Example usage
audio_file = "path_to_your_audio_file.wav"
transcript = transcribe_audio(audio_file)
print(f"Transcript: {transcript}")
