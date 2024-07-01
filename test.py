import os
import torch
import logging
from pydub import AudioSegment
from faster_whisper import WhisperModel
from concurrent.futures import ProcessPoolExecutor, as_completed

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def format_time(seconds):
    """Convert seconds to SRT timestamp format."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def generate_srt_segment(segment, segment_number):
    """Generate SRT segment text."""
    start_time = format_time(segment['start'])
    end_time = format_time(segment['end'])
    return f"{segment_number}\n{start_time} --> {end_time}\n{segment['text']}\n\n"

def transcribe_segment(params):
    """Transcribe a segment of audio."""
    audio_chunk_path, chunk_start_time = params
    try:
        model_size = "medium"
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_chunk_path)
        # Adjust the start and end times based on the chunk's start time
        adjusted_segments = [
            {'start': seg.start + chunk_start_time, 'end': seg.end + chunk_start_time, 'text': seg.text}
            for seg in segments
        ]
        return adjusted_segments
    except Exception as e:
        logger.error(f"Error transcribing segment: {e}")
        return []

def preprocess_audio(audio_file):
    """Preprocess audio to 16kHz."""
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_frame_rate(16000)
    return audio

def save_audio_chunk(audio_chunk, chunk_index, base_filename):
    chunk_filename = f"{base_filename}_chunk_{chunk_index}.mp3"
    audio_chunk.export(chunk_filename, format="mp3")
    return chunk_filename

def merge_transcripts(transcribed_segments):
    """Merge transcripts into one."""
    merged_segments = []
    for segments in transcribed_segments:
        merged_segments.extend(segments)
    return merged_segments

def generate_srt_file(segments, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for segment_number, segment in enumerate(segments, start=1):
            srt_segment = generate_srt_segment(segment, segment_number)
            f.write(srt_segment)
    return output_file

def text_generation(audio_file):
    # Set environment variable to suppress OpenMP warning
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

    # Preprocess audio
    audio = preprocess_audio(audio_file)

    # Split audio into 30-second segments and save them as files
    segment_length_ms = 30000  # 30 seconds in milliseconds
    base_filename = os.path.splitext(audio_file)[0]
    audio_chunk_files = []
    chunk_start_times = []
    for i in range(0, len(audio), segment_length_ms):
        chunk = audio[i:i + segment_length_ms]
        chunk_start_time = i / 1000  # Convert milliseconds to seconds
        chunk_filename = save_audio_chunk(chunk, i // segment_length_ms, base_filename)
        audio_chunk_files.append(chunk_filename)
        chunk_start_times.append(chunk_start_time)

    # Initialize multiprocessing for transcription
    num_cores = os.cpu_count()
    params = list(zip(audio_chunk_files, chunk_start_times))
    transcribed_segments = []
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(transcribe_segment, param) for param in params]
        for future in as_completed(futures):
            transcribed_segments.append(future.result())

    # Merge transcripts into one
    merged_segments = merge_transcripts(transcribed_segments)

    # Generate SRT file
    srt_filename = generate_srt_file(merged_segments, base_filename + "_transcript.srt")
    
    return srt_filename

if __name__ == "__main__":
    audio_file_path = "D:/projects/Internship_frontend/tamilsample_audio.mp3"  
    result = text_generation(audio_file_path)
    print(f"Generated SRT file: {result}")
