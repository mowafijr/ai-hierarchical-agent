from pathlib import Path

def read_file(path: str) -> str:
    try:
        p = Path(path).expanduser().resolve()
        if not p.is_file():
            return f"File not found: {path}"
        content = p.read_text(encoding='utf-8')
        if len(content) > 2000:
            content = content[:2000] + "\n... (truncated)"
        return content
    except Exception as e:
        return f"Error reading file: {e}"