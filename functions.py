import moviepy.editor 
import os
import shutil
from faster_whisper import WhisperModel
from pydub import AudioSegment
import torch

#extracting the audio from the video file
def converter(path,filename):
    cvt_vd = moviepy.editor.VideoFileClip(path)
    ext_ad= cvt_vd.audio
    
    output_directory = "D:\\projects\\Internship_frontend\\uploads"
    # Create the full output file path
    name = os.path.join(output_directory, filename.split('.')[0] + "_audio.mp3")
    ext_ad.write_audiofile(name)
    cvt_vd.close()
    ext_ad.close()
    return name



def text_generation(audio_file):
    
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
    # Path to the directory containing the model files
    model_dir = "D:/projects/Internship_frontend/models/transcription"

    # Load the WhisperModel from local files
    model = WhisperModel(model_dir, device="cpu", compute_type="int8")
    torch.set_num_threads(os.cpu_count())

    # Preprocess audio to 16kHz
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000)
    # Transcribe audio
    segments, info = model.transcribe(audio_file)

    filename = audio_file.split('.')[0] + "_transcript.srt"
    filename = generate_srt_file(segments, filename)
    return filename
    
def save_file(gen, spc):
    base_name = os.path.basename(gen)  
    file_name, file_ext = os.path.splitext(base_name)  
    # Check if the destination folder already has a file with the same name
    dest_path = os.path.join(spc, base_name)
    list_=manage_file(gen)
    if not os.path.exists(dest_path):
        shutil.copy(gen, dest_path)
    else:
        i = 1
        while True:
            new_name = f"{file_name}_copy{i}{file_ext}"
            new_path = os.path.join(spc, new_name)
            if not os.path.exists(new_path):
                shutil.copy(gen, new_path)
                break
            i += 1
    return list_
# Function to read data from the file
def read_from_file():
    file_path= "uploads/list.txt"
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        return []  # If the file doesn't exist, return an empty list

def manage_file(new_line):
    file_path = "uploads/list.txt"
    
    # Function to write data to the file
    def write_to_file(lines):
        with open(file_path, 'w') as file:
            for line in lines:
                file.write(line + '\n')
        print(f"The list has been written to {file_path}.")

    
    # Read existing lines from the file
    lines = read_from_file()
    
    # Add the new line to the buffer
    lines.append(new_line)
    
    # If the buffer exceeds 2 lines, remove the oldest line
    if len(lines) > 2:
        path=lines.pop(0)
        os.remove(path)
    # Write the updated buffer to the file
    write_to_file(lines)
    
    return lines


