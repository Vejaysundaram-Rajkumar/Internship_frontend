import whisper



def text_generation(name):
    #Loading the model
    model = whisper.load_model("base")

    #loading the audio
    audio = whisper.load_audio(name)

    # Transcribe the audio in english
    result_english = model.transcribe(audio, language='en')
    filename=name.split('.')[0]+"transcribed.srt"
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
    print("Transcription saved sucessfully!")