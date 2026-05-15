import sys
import whisper
from exporters.srt_exporter import save_srt
from exporters.vtt_exporter import save_vtt

if len(sys.argv) < 2:
    print("Usage: python subtitle.py audio.mp3")
    sys.exit()

audio_file = sys.argv[1]

print("Initializing model....")

model = whisper.load_model("base")

print(f"Processing: {audio_file}....")

result = model.transcribe(
    audio_file,
    word_timestamps=True
)

MAX_WORDS = 5 #Max word to display
PUNTUATION_MARKS = {'.','?',',',';',':'}  # Puntuations to watch out for for good breaking
PAUSE_THRESHOLD = 0.5   # Seconds to break if gaps is larger than this 

def push_to_chunks(current, chunks):
    chunks.append({
        'text': current['text'],
        'start': current['start'],
        'end': current['end']
    })

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

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milisec = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milisec:03}"


print(f"Created {len(chunks)} Chunks\n")

save_vtt(chunks)
save_srt(chunks)
    