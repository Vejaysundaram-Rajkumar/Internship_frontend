import os
import logging
import multiprocessing
from pydub import AudioSegment
from faster_whisper import WhisperModel

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

def transcribe_segment_with_whisper(audio_chunk_path, chunk_start_time, result_queue):
    """Transcribe a segment of audio using Whisper model and put results in queue."""
    try:
        model = WhisperModel("medium", device="cpu", compute_type="int8")
        segments, _ = model.transcribe(audio_chunk_path)
        adjusted_segments = [
            {'start': seg.start + chunk_start_time, 'end': seg.end + chunk_start_time, 'text': seg.text}
            for seg in segments
        ]
        result_queue.put((chunk_start_time, adjusted_segments))  # Include start time for sorting
    except Exception as e:
        logger.error(f"Error transcribing segment with Whisper model: {e}")

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
    """Merge and sort transcripts into one."""
    merged_segments = []
    for start_time, segments in sorted(transcribed_segments):
        for seg in segments:
            seg['start'] += start_time
            seg['end'] += start_time
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

    # Split audio into chunks with overlap and save them as files
    segment_length_ms = 20000  # 10 seconds in milliseconds
    overlap_ms = 2000  # 2 seconds overlap
    base_filename = os.path.splitext(audio_file)[0]
    audio_chunk_files = []
    chunk_start_times = []
    for i in range(0, len(audio) - segment_length_ms, segment_length_ms - overlap_ms):
        chunk = audio[i:i + segment_length_ms]
        chunk_start_time = i / 1000  # Convert milliseconds to seconds
        chunk_filename = save_audio_chunk(chunk, i // (segment_length_ms - overlap_ms), base_filename)
        audio_chunk_files.append(chunk_filename)
        chunk_start_times.append(chunk_start_time)

    # Initialize multiprocessing for transcription
    result_queue = multiprocessing.Queue()
    processes = []
    for audio_chunk_path, chunk_start_time in zip(audio_chunk_files, chunk_start_times):
        process = multiprocessing.Process(target=transcribe_segment_with_whisper,
                                          args=(audio_chunk_path, chunk_start_time, result_queue))
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Retrieve transcriptions from the result queue
    transcribed_segments = []
    while not result_queue.empty():
        transcribed_segments.append(result_queue.get())

    # Merge and sort transcripts
    merged_segments = merge_transcripts(transcribed_segments)

    # Generate SRT file
    srt_filename = generate_srt_file(merged_segments, base_filename + "_transcript.srt")
    
    return srt_filename

if __name__ == "__main__":
    audio_file_path = "D:/projects/Internship_frontend/tamilsample_audio.mp3"  
    result = text_generation(audio_file_path)
    print(f"Generated SRT file: {result}")
