import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import os

# Specify the save directory
save_directory = "D:\\WhisperModels"

# Create the directory if it does not exist
os.makedirs(save_directory, exist_ok=True)

# Load model and processor for Tamil language
processor = WhisperProcessor.from_pretrained("openai/whisper-large-v2")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-large-v2")

# Apply dynamic quantization to the model
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)

# Save the quantized model to disk for faster future loading
quantized_model_path = os.path.join(save_directory, "quantized_whisper_large_v2.pth")
torch.save(quantized_model.state_dict(), quantized_model_path)

# Save the processor for future use
processor.save_pretrained(save_directory)

print(f"Quantized model saved at: {quantized_model_path}")
print(f"Processor saved at: {save_directory}")
