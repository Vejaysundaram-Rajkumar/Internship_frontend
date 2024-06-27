import noisereduce as nr
from pydub import AudioSegment
import numpy as np
import jiwer
def preprocess_audio(audio_file):
    audio = AudioSegment.from_file(audio_file)
    
    # Convert to numpy array
    audio_data = np.array(audio.get_array_of_samples())
    
    # Get sampling rate
    sr = audio.frame_rate
    
    # Reduce noise using noise reduction algorithm (example)
    noise_reduced = nr.reduce_noise(audio_data, sr)
    
    # Convert back to AudioSegment
    reduced_audio = AudioSegment(
        data=noise_reduced.tobytes(),
        sample_width=audio.sample_width,
        frame_rate=sr,
        channels=audio.channels
    )
    
    # Convert to mono if needed
    if audio.channels > 1:
        reduced_audio = reduced_audio.set_channels(1)
    
    
    # Export the preprocessed audio
    preprocessed_file = "D:/projects/Internship_frontend/preprocessed_audio.mp3"
    audio.export(preprocessed_file, format="mp3")
    print(f"Preprocessed audio saved at: {preprocessed_file}")

# # Example usage: Preprocessing a sample audio file
#audio_file = "D:/projects/Internship_frontend/tamilsample.mp3"
#preprocess_audio(audio_file)

def evaluate_transcripts(file1_path, file2_path):
    """
    Evaluate the accuracy of two transcripts stored in text files.

    Args:
        file1_path (str): Path to the first text file (reference transcript).
        file2_path (str): Path to the second text file (generated transcript).

    Returns:
        float: Accuracy percentage based on Word Error Rate (WER).
    """
    # Read contents of the files
    with open(file1_path, 'r', encoding='utf-8') as file1:
        reference = file1.read().strip()

    with open(file2_path, 'r', encoding='utf-8') as file2:
        hypothesis = file2.read().strip()

    # Calculate WER using jiwer
    wer = jiwer.wer(reference, hypothesis)
    
    # Calculate accuracy from WER
    accuracy = (1 - wer) * 100

    return accuracy,wer

# Example usage
file1_path = 'D:/projects/Internship_frontend/extracted ad (1).txt'
file2_path = 'D:/projects/Internship_frontend/output_transcript3.txt'

evaluation ,wer= evaluate_transcripts(file1_path, file2_path)
print(f"Accuracy: {evaluation:.2f}%")
print(f"Word Error Rate: {wer:.2f}")
