import os
import shutil
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import sys
import time

def get_current_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def check_already_installed():
    startup_folder = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    watcher_path = os.path.join(startup_folder, "obs_librarian.exe")
    if os.path.exists(watcher_path):
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the window
        temp_root.eval('tk::PlaceWindow . center')  # Center on screen
        messagebox.showinfo("Already Installed", "OBS Librarian watcher is already installed and will start with Windows.")
        temp_root.destroy()
        sys.exit(0)

def select_folder():
    folder = filedialog.askdirectory(title="Select your OBS Clips folder")
    if folder:
        folder_var.set(folder)

def install():
    obs_folder = folder_var.get()
    if not obs_folder:
        messagebox.showerror("Error", "Please select your OBS Clips folder.")
        return
    if not os.path.isdir(obs_folder):
        messagebox.showerror("Error", "The folder path entered does not exist. Please enter a valid folder.")
        return

    current_dir = get_current_dir()
    watcher_exe = os.path.join(current_dir, "obs_librarian.exe")

    # Config path will now be in the user profile folder
    user_profile_dir = os.getenv("USERPROFILE")
    config_path = os.path.join(user_profile_dir, "librarian-config.ini")

    if not os.path.exists(watcher_exe):
        messagebox.showerror("Error", "obs_librarian.exe not found in installer folder.")
        return

    try:
        # Write librarian-config.ini with the user's OBS clips folder path
        config = configparser.ConfigParser()
        config["Settings"] = {"OBS_CLIPS_DIR": obs_folder}
        with open(config_path, "w") as configfile:
            config.write(configfile)

        # Copy watcher exe to startup folder
        startup_folder = os.path.join(
            os.getenv("APPDATA"),
            r"Microsoft\Windows\Start Menu\Programs\Startup"
        )
        shutil.copy(watcher_exe, startup_folder)

        time.sleep(0.5)  # wait a moment for copies to complete

        # Verify librarian-config.ini exists in the user profile folder
        if not os.path.exists(config_path):
            messagebox.showerror("Error", "librarian-config.ini not found in user profile folder after copying!")
            return

        if run_now.get():
            subprocess.Popen([os.path.join(startup_folder, "obs_librarian.exe")], cwd=startup_folder)

        messagebox.showinfo("Success", "Installation complete! The watcher will start automatically with Windows.")
        root.destroy()

    except Exception as e:
        messagebox.showerror("Error", f"Installation failed: {e}")

# --- Check before creating main window ---
check_already_installed()

# --- Main installer window ---
root = tk.Tk()
root.title("OBS Librarian Installer")
root.geometry("450x200")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')

folder_var = tk.StringVar()

tk.Label(root, text="Select your OBS Clips folder:").pack(pady=10)

frame = tk.Frame(root)
frame.pack()

tk.Entry(frame, textvariable=folder_var, width=40).pack(side=tk.LEFT)
tk.Button(frame, text="Browse", command=select_folder).pack(side=tk.LEFT, padx=5)

run_now = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Run obs_librarian after install", variable=run_now).pack(anchor="w", padx=20, pady=10)

tk.Button(root, text="Install", command=install, width=20).pack(pady=20)

root.mainloop()
