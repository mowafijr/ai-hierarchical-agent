from datetime import datetime

def get_time() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")