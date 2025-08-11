import os
import sys
import time
import shutil
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes
from ctypes import wintypes

# Get folder where this script or exe lives
def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Load config.ini from the same folder as the exe/script
config_path = os.path.join(get_current_dir(), "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

OBS_CLIPS_DIR = config.get("Settings", "OBS_CLIPS_DIR", fallback=None)
if not OBS_CLIPS_DIR or not os.path.isdir(OBS_CLIPS_DIR):
    print(f"Error: OBS_CLIPS_DIR is not set or does not exist: {OBS_CLIPS_DIR}")
    sys.exit(1)

user32 = ctypes.WinDLL('user32', use_last_error=True)

# Your fullscreen/windowed fullscreen detection (replace with your real logic)
def get_fullscreen_window_process_name():
    # TODO: Implement actual detection and return process name string
    return None

class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path

        # Wait a bit to ensure OBS finished writing the clip file
        time.sleep(1)

        game_process = get_fullscreen_window_process_name()
        target_folder = os.path.join(OBS_CLIPS_DIR, game_process if game_process else "Desktop")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        try:
            shutil.move(filepath, target_folder)
            print(f"Moved {filepath} to {target_folder}")
        except Exception as e:
            print(f"Error moving file: {e}")

if __name__ == "__main__":
    event_handler = ClipHandler()
    observer = Observer()
    observer.schedule(event_handler, OBS_CLIPS_DIR, recursive=False)
    observer.start()
    print(f"Watching {OBS_CLIPS_DIR} for new clips...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
