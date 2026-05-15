import json
from pathlib import Path
INPUT_FILE = "output-1.json"
OUTPUT_FILE = "sanitized_output.json"
def sanitize_whitespace(value):
    """
    Removes leading/trailing whitespace
    from strings recursively.
    """
    if isinstance(value, str):
        return value.strip()
    elif isinstance(value, list):
        return [sanitize_whitespace(item) for item in value]
    elif isinstance(value, dict):
        return {
            key: sanitize_whitespace(val)
            for key, val in value.items()
        }
    return value
# Load original JSON
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)
# Sanitize entire JSON recursively
cleaned_data = sanitize_whitespace(data)
# Save sanitized JSON
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(cleaned_data, f, indent=4, ensure_ascii=False)
print(f"Sanitized JSON saved to: {OUTPUT_FILE}")