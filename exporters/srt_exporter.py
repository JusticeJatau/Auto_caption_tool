def format_srt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milisec = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02},{milisec:03}"

def export_srt(captions):
    srt = []

    for index, caption in enumerate(captions, start=1):
        start = format_srt_time(caption['start'])
        end = format_srt_time(caption['end'])
        text = caption['text']

        srt.append(f"{index}\n{start} --> {end}\n{text}")
    return "\n\n".join(srt)

def save_srt(captions, path="output.srt"):
    content = export_srt(captions)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path