import openai
openai.api_key = "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"
with open("extracted_ad.mp3", "rb") as audio_file:
    transcript = openai.Audio.transcribe(
        file = audio_file,
        model = "whisper-1",
        response_format="text",
        language="en"
    )
print(transcript)
