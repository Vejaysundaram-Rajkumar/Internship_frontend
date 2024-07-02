import pandas as pd
from pydub import AudioSegment
import os

def preprocess_audio(audio_path):
    audio = AudioSegment.from_file(audio_path)
    audio = audio.set_frame_rate(16000).set_channels(1)
    processed_path = audio_path.replace(".mp3", "_16k.wav")
    audio.export(processed_path, format="wav")
    return processed_path

def preprocess_data(data_path):
    df = pd.read_csv(data_path, sep='\t')
    df['path'] = df['path'].apply(preprocess_audio)
    return df

train_df = preprocess_data('data/train.tsv')
train_df.to_csv('data/train_preprocessed.tsv', sep='\t', index=False)
