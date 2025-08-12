import os
import sys
import time
import shutil
import configparser
import ctypes
from ctypes import wintypes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import win32gui
import win32process
import psutil

def show_message_box(title, text):
    ctypes.windll.user32.MessageBoxW(0, text, title, 0)

def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Load config.ini from the user profile folder
config_path = os.path.join(os.getenv("USERPROFILE"), "librarian-config.ini")
config = configparser.ConfigParser()
config.read(config_path)

OBS_CLIPS_DIR = config.get("Settings", "OBS_CLIPS_DIR", fallback="").strip()

if not OBS_CLIPS_DIR:
    show_message_box(
        "Configuration Missing",
        "Configuration not found or OBS_CLIPS_DIR is empty.\nPlease run the installer first."
    )
    sys.exit(1)

if not os.path.isdir(OBS_CLIPS_DIR):
    show_message_box(
        "Invalid Path",
        f"The configured OBS clips directory does not exist:\n{OBS_CLIPS_DIR}"
    )
    sys.exit(1)

def is_fullscreen(hwnd):
    if not hwnd:
        return False
    rect = win32gui.GetWindowRect(hwnd)
    # Get screen size
    screen_width = ctypes.windll.user32.GetSystemMetrics(0)
    screen_height = ctypes.windll.user32.GetSystemMetrics(1)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top
    tolerance = 10  # pixels tolerance for borders
    return width >= screen_width - tolerance and height >= screen_height - tolerance

def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd and is_fullscreen(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title:
            return title
    return None

def sanitize_folder_name(name: str) -> str:
    # Remove characters not allowed in Windows folder names
    invalid_chars = '<>:"/\\|?*'
    for ch in invalid_chars:
        name = name.replace(ch, '')
    return name.strip() or "Unknown"

class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        filepath = event.src_path

        # Wait to ensure file is fully written
        time.sleep(5)

        window_title = get_active_window_title()
        folder_name = sanitize_folder_name(window_title) if window_title else "Desktop"

        target_folder = os.path.join(OBS_CLIPS_DIR, folder_name)
        os.makedirs(target_folder, exist_ok=True)
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
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
