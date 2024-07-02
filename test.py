from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
path="D:/projects/Internship_frontend/models/translation"
model = MBartForConditionalGeneration.from_pretrained(path)
tokenizer = MBart50TokenizerFast.from_pretrained(path)

article_ta = "Over the past two years, youth unemployment has been on the rise. It currently represents just under 40% of all unemployment in Australia. Young graduates leaving university and finding it more and more difficult to enter any form of creative industry.Now the common stipulation is that you can't get a job without experience, but you can't get a job to get the experience.Now meanwhile, 42% of small businesses failed in 2003-2007 and the figures haven't improved much.Amongst many reasons this is happening is a consistent lack of quality in their branding,marketing, websites and designs.The kind of training that these graduates have just spent 3-6 years training for.Now what if there was an enterprise that bridged these two sets of frightening statistics?I want to build that bridge."
# translate Arabic to English
tokenizer.src_lang = "en_XX"
encoded_ar = tokenizer(article_ta, return_tensors="pt")
generated_tokens = model.generate(
    **encoded_ar,
    forced_bos_token_id=tokenizer.lang_code_to_id["ta_IN"]
)
trans_text=tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)
print(trans_text)