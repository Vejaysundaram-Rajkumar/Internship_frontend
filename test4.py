from faster_whisper import WhisperModel

# Initialize and load the model
model_size = "medium"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

# Save the model to a local directory
model.save_pretrained("D:/projects/Internship_frontend/local_model")

print("Model saved locally.")
