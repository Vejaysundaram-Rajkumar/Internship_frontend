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
    model = whisper.load_model("base")

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
    base_name = os.path.basename(gen)  # Get the base filename from the source path
    file_name, file_ext = os.path.splitext(base_name)  # Split filename and extension
    
    # Check if the destination folder already has a file with the same name
    dest_path = os.path.join(spc, base_name)
    if not os.path.exists(dest_path):
        shutil.copy(gen, dest_path)
        #print(f"Copied {gen} to {dest_path}")
    else:
        # Subsequent copies, add _copy suffix
        i = 1
        while True:
            new_name = f"{file_name}_copy{i}{file_ext}"
            new_path = os.path.join(spc, new_name)
            if not os.path.exists(new_path):
                shutil.copy(gen, new_path)
                #print(f"Copied {gen} to {new_path}")
                break
            i += 1
