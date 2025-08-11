import os
import sys
import time
import shutil
import configparser
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import ctypes

def show_message_box(title, text):
    # MessageBoxW from user32.dll; MB_OK = 0
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Load config.ini from same folder as script/exe
config_path = os.path.join(get_current_dir(), "config.ini")
config = configparser.ConfigParser()
config.read(config_path)

OBS_CLIPS_DIR = config.get("Settings", "OBS_CLIPS_DIR", fallback="").strip()

if not OBS_CLIPS_DIR:
    show_message_box("Configuration Missing", "Configuration not found or OBS_CLIPS_DIR is empty.\nPlease run the installer first.")
    sys.exit(1)

if not os.path.isdir(OBS_CLIPS_DIR):
    show_message_box("Invalid Path", f"The configured OBS clips directory does not exist:\n{OBS_CLIPS_DIR}")
    sys.exit(1)

# Placeholder for your fullscreen detection, adjust as needed
def get_fullscreen_window_process_name():
    # TODO: implement your fullscreen/windowed detection logic here
    return None

class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path

        # Wait to ensure file is fully written
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
