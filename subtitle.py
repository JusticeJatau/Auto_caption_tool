import sys
import whisper

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

# segments = result['segments'][0]['words']
# segments = result['segments']
# words = segments['words']

# for w in segments:
#     print(f"word: {w['words']}, start: {w['start']}, end: {w['end']}\n")

# # print(segments[0])

# segments = result['segments']

# # for segment in segments:
# #     for word in segment['words']:
# #         print(word)

# # Phase 1 - Basic SRT 
# for segment in segments:
#     print(segment['text'])


# Formatting the time
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milisec = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milisec:03}"

print(format_time(10000))


# Writing in a file
# But before that i need to store my segment in an array/list of dictionaries/object
# e.g subtitles = [
#         {
#           "start":1,
#           "end":3,
#           "text":"Hello World"
#         }
# ]

# Or we just do the formatting directly to give the output

segments = result['segments']
# subtitles = []

# for i,segment in enumerate(segments, start = 1):
#     print(f"{i}\n{format_time(segment['start'])} --> {format_time(segment['end'])}\n{segment['text']}")

# Now having the correct output
# We can now write it in a file

print("Writing SRT file....")

with open(f"{audio_file}.srt", "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments, start = 1):
        f.write(f"{i}\n")
        f.write(f"{format_time(segment['start'])} --> {format_time(segment['end'])}\n")
        f.write(f"{segment['text']}\n\n")

