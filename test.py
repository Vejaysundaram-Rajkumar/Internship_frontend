# Load model directly
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


path="D:/projects/Internship_frontend/models/translation_2"
tokenizer = AutoTokenizer.from_pretrained(path)
model = AutoModelForSeq2SeqLM.from_pretrained(path)
translator=pipeline('translation', model=model, tokenizer=tokenizer,src_lang="eng_Latn", tgt_lang='tam_Taml',max_length=700)
print(translator("Excuse me. Hi. I'm trying to relax. Would you mind? Oh, sorry Mr. Adam. Hey, kid. Kid. Kid. Just come over here and sit down, would you? Okay. What's your name, Mr. My name is Adam. You look like my grandpa. He's not as old. That's very rude. I'm Adam. Who are you? Joseph. Where's your mother? She's with her boyfriend. I'm supposed to wait over here. I'm eight and three quarters, Mr. How old are you? Mr. You're boring. Hey, listen, kid. I'd like some peace and quiet. Please? You're grumpy, Mr.. Is that why that woman left you on the bench? Was she your girlfriend? No. No, she wasn't. Listen. I have a girlfriend, Mr. and I'm only in this second grade. Where's your girlfriend? My wife, Elizabeth, is gone. Well, where has she gone to? She's gone. Gone. Ted. Oh. That's sad. Well, my girlfriend, Katie, she's still really young. Was she your good girlfriend? Katie's the best I've had. Yes. Elizabeth was one of a kind. Why? Have you ever had any other girlfriends? Yesterday, I brought Katie a flower, and she gave me a kiss on the cheek. Have you ever brought a girl flower? A kid. You've got a lot to learn about relationships. Have you ever looked into someone's eyes and had a whole conversation in an instant? Laughed with someone. Kept laughing until you even forgot why you were laughing. Have you ever cried when... I cried last night when I said goodbye to Katie. But that was because I had a scrape. My name's Elizabeth. Mr. Yes. Are you going to get a new girlfriend for all those things? No. I'm happy just by myself. I think you're grumpy. I have lots of girlfriends, Mr. Over six. Lizzy was my one and only. Well, you talk about your girlfriend a lot. My why? I love getting girlfriends, Mr. You should try it. No. I guess not enough time left for me for those kind of shenanigans. Plus, I thought I was a boring, grumpy old guy. Nah. You're nice. Well, once you stop breathing. See that pretty girl over there? I'm about to get a new girlfriend in ten seconds. There's always time. Gotta go, Mr. Bye. Bye. I'm going to get a new girlfriend. Nice day, isn't it? Yeah. That's beautiful."))