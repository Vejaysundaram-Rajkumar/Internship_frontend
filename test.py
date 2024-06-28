import torch
from datasets import load_dataset
from huggingface_hub import hf_hub_download
from whisper import load_model, transcribe

distil_large_v2 = hf_hub_download(repo_id="distil-whisper/distil-large-v2", filename="original-model.bin")
model = load_model(distil_large_v2)

dataset = load_dataset("hf-internal-testing/librispeech_asr_dummy", "clean", split="validation")
sample = dataset[0]["audio"]["array"]
sample = torch.from_numpy(sample).float()

pred_out = transcribe(model, audio="D:/projects/Internship_frontend/uploads/tamilsample_audio.mp3")

print(pred_out["text"])
