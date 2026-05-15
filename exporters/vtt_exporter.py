def format_vtt_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milisec = int((seconds - int(seconds)) * 1000)

    return f"{hours:02}:{minutes:02}:{secs:02}.{milisec:03}"

def export_vtt(captions):
    vtt = ["WEBVTT\n"]

    for caption in captions:
        start = format_vtt_time(caption['start'])
        end = format_vtt_time(caption['end'])
        text = caption['text']

        vtt.append(f"{start} --> {end}\n{text}")

    return "\n\n".join(vtt)

def save_vtt(captions, path="output.vtt"):
    content = export_vtt(captions)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return path