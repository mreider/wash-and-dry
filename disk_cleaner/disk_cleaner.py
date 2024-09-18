import os
import time
from datetime import datetime, timedelta

TRACE_FILE_PATH = "/var/log/otel-traces.json"
WATERFALL_DIR_PATH = "/var/log/waterfall"
CLEANUP_INTERVAL = 60  # seconds
FILE_EXPIRATION_TIME = timedelta(minutes=1)

def cleanup_files():
    now = datetime.now()
    if os.path.exists(TRACE_FILE_PATH):
        file_mod_time = datetime.fromtimestamp(os.path.getmtime(TRACE_FILE_PATH))
        if now - file_mod_time > FILE_EXPIRATION_TIME:
            os.remove(TRACE_FILE_PATH)
    
    if os.path.exists(WATERFALL_DIR_PATH):
        for filename in os.listdir(WATERFALL_DIR_PATH):
            file_path = os.path.join(WATERFALL_DIR_PATH, filename)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mod_time > FILE_EXPIRATION_TIME:
                os.remove(file_path)

def main():
    while True:
        cleanup_files()
        time.sleep(CLEANUP_INTERVAL)

if __name__ == "__main__":
    main()
