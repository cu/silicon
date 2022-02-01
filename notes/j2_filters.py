from datetime import datetime

def human_timestamp(timestamp):
    return datetime.fromisoformat(timestamp).strftime('%B %d %Y, %H:%M:%S')
