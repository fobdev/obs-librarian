import os
import shutil
import time
import psutil
import win32gui
import win32process
import win32api
import win32con
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


OBS_CLIPS_DIR = str(Path.home() / "Videos" / "OBS Clips") 
# Change "OBS Clips" to your OBS output folder
# if it's in another dir than "Videos", also change it
# e.g.: str(Path.home() / "OBS") or str(Path.home() / "Videos" / "OBS")
#
# WARNING: if you don't set the correct directory it will return a error
# the software needs to watch the directory to do it's action.

last_fullscreen_app = "Desktop"  # Default if nothing is detected

def detect_fullscreen_or_windowed_fullscreen():
    """Detect fullscreen or borderless fullscreen app and return its window title (or exe name as fallback)."""
    try:
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return None

        # Get window dimensions
        rect = win32gui.GetWindowRect(hwnd)
        win_width = rect[2] - rect[0]
        win_height = rect[3] - rect[1]

        # Screen resolution
        screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        fullscreen_margin = 5
        if (abs(win_width - screen_width) <= fullscreen_margin and
            abs(win_height - screen_height) <= fullscreen_margin):
            
            # Try to get window title
            title = win32gui.GetWindowText(hwnd).strip()
            if title:
                return title
            
            # Fallback to exe name
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            return process.name()

        return None
    except:
        return None

def track_foreground_app():
    """Background thread that updates last_fullscreen_app continuously."""
    global last_fullscreen_app
    while True:
        app = detect_fullscreen_or_windowed_fullscreen()
        if app:
            last_fullscreen_app = app
        time.sleep(0.2)  # Check 5 times per second

class ClipHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        time.sleep(0.3)  # Let OBS finish writing file

        game_name = last_fullscreen_app or "Desktop"
        dest_dir = os.path.join(OBS_CLIPS_DIR, game_name)
        os.makedirs(dest_dir, exist_ok=True)
        dest_path = os.path.join(dest_dir, os.path.basename(file_path))
        shutil.move(file_path, dest_path)

        print(f"Moved {file_path} -> {dest_path}")

if __name__ == "__main__":
    # Start background tracker
    tracker_thread = threading.Thread(target=track_foreground_app, daemon=True)
    tracker_thread.start()

    # Watch OBS Clips folder
    event_handler = ClipHandler()
    observer = Observer()
    observer.schedule(event_handler, OBS_CLIPS_DIR, recursive=False)
    observer.start()
    print("Watching for new clips...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
