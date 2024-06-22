import whisper

#Loading the model
model = whisper.load_model("base")

#loading the audio
audio = whisper.load_audio("tamil.mp3")


# Transcribe the audio in Tamil
result_tamil = model.transcribe(audio, language='ta')

# Tamil audio to english
result_english = model.transcribe(audio, task='translate', language='en')

# Tamil audio to french
result_french = model.transcribe(audio, task='translate', language='fr')

# Function to save transcription in SRT format
def save_as_srt(transcription, filename):
    with open(filename, 'w', encoding='utf-8') as srt_file:
        for segment in transcription['segments']:
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

# Save the transcriptions to SRT files
save_as_srt(result_tamil, "transcription_tamil.srt")
save_as_srt(result_english, "transcription_english.srt")
save_as_srt(result_french, "transcription_french.srt")

print("Transcriptions saved to transcription_tamil.srt, transcription_english.srt, and transcription_french.srt")
