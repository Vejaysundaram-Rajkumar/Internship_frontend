from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
path="D:/projects/Internship_frontend/models/translation"
model = MBartForConditionalGeneration.from_pretrained(path)
tokenizer = MBart50TokenizerFast.from_pretrained(path)

article_ta = "Vijay"
# translate Arabic to English
tokenizer.src_lang = "en_XX"
encoded_ar = tokenizer(article_ta, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_ar,
    forced_bos_token_id=tokenizer.lang_code_to_id["ta_IN"]
)
trans_text=tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(trans_text)