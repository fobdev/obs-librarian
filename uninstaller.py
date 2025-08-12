import os
import psutil
import tkinter as tk
from tkinter import messagebox

def kill_process_by_name(name="obs_librarian.exe"):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == name.lower():
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except Exception as e:
                print(f"Could not terminate {name}: {e}")

def uninstall():
    startup_folder = os.path.join(
        os.getenv("APPDATA"),
        r"Microsoft\Windows\Start Menu\Programs\Startup"
    )
    user_profile_dir = os.getenv("USERPROFILE")

    exe_path = os.path.join(startup_folder, "obs_librarian.exe")
    config_path = os.path.join(user_profile_dir, "librarian-config.ini")

    kill_process_by_name("obs_librarian.exe")

    removed_any = False

    # Remove exe from Startup
    if os.path.exists(exe_path):
        try:
            os.remove(exe_path)
            removed_any = True
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not delete obs_librarian.exe: {e}")

    # Remove librarian-config.ini from user profile
    if os.path.exists(config_path):
        try:
            os.remove(config_path)
            removed_any = True
        except Exception as e:
            messagebox.showwarning("Warning", f"Could not delete librarian-config.ini: {e}")

    if removed_any:
        messagebox.showinfo("Uninstaller", "Uninstallation complete! Watcher exe and librarian-config.ini removed.")
    else:
        messagebox.showinfo("Uninstaller", "No watcher files found.")

    root.destroy()

# GUI setup
root = tk.Tk()
root.title("OBS Librarian Uninstaller")
root.geometry("350x150")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')  # Center window on screen

tk.Label(root, text="This will remove obs_librarian files from startup folder.").pack(pady=20)
tk.Button(root, text="Uninstall", command=uninstall, width=20).pack(pady=10)

root.mainloop()
