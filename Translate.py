from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
import srt
import os
import time


ta_text="இக்கட்டுரை தமிழ் மொழி பற்றியது. ஏனைய பயன்பாடுகளுக்குத் தமிழ் (மாற்றுப் பயன்பாடுகள்) பக்கத்தைப் பாருங்கள்."
path="D:/projects/Internship_frontend/models/translation_mbart"
model = MBartForConditionalGeneration.from_pretrained(path)
tokenizer = MBart50TokenizerFast.from_pretrained(path)

# translate Hindi to French
tokenizer.src_lang = "ta_IN"
encoded_hi = tokenizer(ta_text, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_hi,
    forced_bos_token_id=tokenizer.lang_code_to_id["en_XX"]
)
t=tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(t)