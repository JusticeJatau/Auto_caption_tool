import sys
import subprocess
import os
import whisper
from exporters.srt_exporter import save_srt
from exporters.vtt_exporter import save_vtt

MAX_WORDS = 5 #Max word to display
PUNTUATION_MARKS = {'.','?',',',';',':'}  # Puntuations to watch out for for good breaking
PAUSE_THRESHOLD = 0.5   # Seconds to break if gaps is larger than this 
audio_path = ""

def push_to_chunks(current, chunks):
    chunks.append({
        'text': current['text'],
        'start': current['start'],
        'end': current['end']
    })

def convert_to_audio(video_path):
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-acodec", "pcm_s16le",
        audio_path
    ]

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return audio_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <audio_or_video_file")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print(f"File {input_file} not found!")
        sys.exit(1)

    ext = os.path.splitext(input_file)[1].lower()
    if ext in [".mp4", ".mkv", ".mov", ".avi"]:
        print("Converting video to audio...")
        audio_file = convert_to_audio(input_file)
        cleanup_audio = True
    elif ext in [".mp3", ".wav", ".m4a", ".flac"]:
        audio_file = input_file
        cleanup_audio = False
    else:
        print("Unstopported file type.")
        sys.exit(1)

    print("Initializing model...")

    model = whisper.load_model("base")

    print(f"Processing: {audio_file}....")

    result = model.transcribe(
        audio_file,
        word_timestamps=True
    )

    chunks = []
    previous_end_time = None
    current = {
        'text': '',
        'start': None,
        'end': None,
    }

    segments = result['segments']

    for segment in segments:
        for words in segment['words']:
            should_break = False
            text = words['word']
            start = words['start']
            end = words['end']

            if current['text']:
                current['text'] += ' ' + text.strip()
            else:
                current['text'] = text

            if current['start'] is None:
                current['start'] = start
            
            current['end'] = end

            # Check for pause
            pause_detected = False
            if previous_end_time is not None:
                gap = current['start'] - previous_end_time
                if(gap > PAUSE_THRESHOLD):
                    print(f"Gap: {gap} word: {text} start: {start} end: {end} previous end: {previous_end_time}")
                    pause_detected = True

            # Check for max-word and punctuation
            end_with_punctuation = text and text[-1] in PUNTUATION_MARKS

            if pause_detected or end_with_punctuation or len(current['text'].split()) >= MAX_WORDS:
                push_to_chunks(current, chunks)

                current = {'text':'','start': None,'end': None}
            
            previous_end_time = end

    if len(current['text'].split()) > 0:
        push_to_chunks(current, chunks)


    print(f"Created {len(chunks)} Chunks\n")

    save_vtt(chunks)
    save_srt(chunks)
    