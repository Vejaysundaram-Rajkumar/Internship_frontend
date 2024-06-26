import jiwer

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
file1_path = 'D:/projects/Internship_frontend/extracted ad.txt'
file2_path = 'D:/projects/Internship_frontend/Sample1transcript (1).txt'

evaluation ,wer= evaluate_transcripts(file1_path, file2_path)
print(f"Accuracy: {evaluation:.2f}%")
print(f"Word Error Rate: {wer:.2f}")
