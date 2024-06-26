import moviepy.editor 
import os
import whisper
import shutil

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



def text_generation(name):
    #Loading the model
    model = whisper.load_model("base.en")

    #loading the audio
    audio = whisper.load_audio(name)

    # Transcribe the audio in english
    result_english = model.transcribe(audio, language='en')
    filename=name.split('.')[0]+"transcript.srt"
    with open(filename, 'w', encoding='utf-8') as srt_file:
        for segment in result_english['segments']:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            
            # Convert time to SRT format (hours, minutes, seconds, milliseconds)
            def srt_time(seconds):
                ms = int((seconds % 1) * 1000)
                s = int(seconds)
                m, s = divmod(s, 60)
                h, m = divmod(m, 60)
                return f"{h:02}:{m:02}:{s:02},{ms:03}"
            
            srt_file.write(f"{segment['id'] + 1}\n")
            srt_file.write(f"{srt_time(start)} --> {srt_time(end)}\n")
            srt_file.write(f"{text}\n\n")
    # print the recognized text
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


