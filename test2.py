from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import srt
import time



# Load model and tokenizer
path = "D:/projects/Internship_frontend/models/translation"
model = MBartForConditionalGeneration.from_pretrained(path)
tokenizer = MBart50TokenizerFast.from_pretrained(path)

# Function to translate text
def translate_text(text, src_lang="en_XX", tgt_lang="ta_IN"):
    tokenizer.src_lang = src_lang
    encoded_text = tokenizer(text, return_tensors="pt")
    generated_tokens = model.generate(
        **encoded_text,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang]
    )
    translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
    return translated_text[0]

st=time.time()
# Read the English .srt file
input_srt_file = "D:/projects/Internship_frontend/Sample_3_audio_transcript.srt"
output_srt_file = "D:/projects/Internship_frontend/Sample_3_audio_transcript_tamil.srt"

with open(input_srt_file, "r", encoding="utf-8") as file:
    english_subtitles = list(srt.parse(file.read()))

# Translate each subtitle
translated_subtitles = []
for subtitle in english_subtitles:
    translated_text = translate_text(subtitle.content)
    translated_subtitles.append(srt.Subtitle(index=subtitle.index,
                                             start=subtitle.start,
                                             end=subtitle.end,
                                             content=translated_text))

# Write the translated subtitles to a new .srt file
with open(output_srt_file, "w", encoding="utf-8") as file:
    file.write(srt.compose(translated_subtitles))
end=time.time()
t=end-st
print("Translation complete. Tamil subtitles saved in ",t)
