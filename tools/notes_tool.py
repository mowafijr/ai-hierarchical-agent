from pathlib import Path
import datetime

NOTES_DIR = Path("notes")
NOTES_DIR.mkdir(exist_ok=True)

def save_note(title: str, content: str) -> str:
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if not safe_title:
        safe_title = "note"
    filename = NOTES_DIR / f"{safe_title}.txt"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_content = f"[{timestamp}]\n{content}\n"
    filename.write_text(full_content, encoding='utf-8')
    return f"Note saved: {filename}"

def list_notes() -> str:
    files = sorted(NOTES_DIR.glob("*.txt"))
    if not files:
        return "No notes found."
    return "\n".join(f"- {f.stem}" for f in files)