import noisereduce as nr
import numpy as np
import jiwer
from pydub import AudioSegment

# # Example usage: Preprocessing a sample audio file
audio_file = "D:/projects/Internship_frontend/uploads/tamilsample_audio.mp3"
audio = AudioSegment.from_file(audio_file)
audio = audio.set_frame_rate(16000)
audio.export("temp_audio.mp3", format="mp3")



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


