# Load model directly
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

path=""
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForSeq2SeqLM.from_pretrained(path)

def language_translator(text):
    tokenized = tokenizer([text], return_tensors='pt')
    out = model.generate(**tokenized, max_length=128)
    return tokenizer.decode(out[0],skip_special_tokens=True)

text_to_translate = "hardwork never fail"
output = language_translator(text_to_translate)
print(output)
