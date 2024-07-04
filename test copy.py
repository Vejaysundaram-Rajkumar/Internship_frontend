from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

path="D:/projects/Internship_frontend/models/translation_mbart"
model = MBartForConditionalGeneration.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
tokenizer = MBart50TokenizerFast.from_pretrained("facebook/mbart-large-50-many-to-many-mmt")
translator=pipeline('translation', model=model, tokenizer=tokenizer,src_lang="tam_Taml", tgt_lang='eng_Latn',max_length=700)
print(translator("இக்கட்டுரை தமிழ் மொழி பற்றியது. ஏனைய பயன்பாடுகளுக்குத் தமிழ் (மாற்றுப் பயன்பாடுகள்) பக்கத்தைப் பாருங்கள்."))