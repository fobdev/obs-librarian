import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import sys
import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    # Re-run the script with admin privileges
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()


DEFAULT_PATH = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
TASK_NAME = "Start OBS Replay Buffer"

class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        root.title("OBS Task Scheduler")
        root.geometry("600x150")
        
        # Label
        self.label = tk.Label(root, text="OBS Directory:")
        self.label.pack(anchor="w", padx=10, pady=(10, 0))
        
        # File selector frame
        frame = tk.Frame(root)
        frame.pack(fill="x", padx=10)
        
        self.path_var = tk.StringVar(value=DEFAULT_PATH)
        self.entry = tk.Entry(frame, textvariable=self.path_var)
        self.entry.pack(side="left", fill="x", expand=True)
        
        self.browse_button = tk.Button(frame, text="Browse...", command=self.browse_file)
        self.browse_button.pack(side="left", padx=5)
        
        # Create Task button
        self.create_button = tk.Button(root, text="Create Task Schedule", command=self.create_task)
        self.create_button.pack(pady=15)

    def browse_file(self):
        filepath = filedialog.askopenfilename(
            title="Select OBS Executable",
            filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
        )
        if filepath:
            self.path_var.set(filepath)

    def create_task(self):
        exe_path = self.path_var.get()
        if not os.path.isfile(exe_path):
            messagebox.showerror("Error", "The specified OBS executable does not exist.")
            return
        
        # Arguments for the task
        arguments = '--disable-shutdown-check --startreplaybuffer --minimize-to-tray'

        # Build the schtasks command
        cmd = [
            "schtasks",
            "/Create",
            "/SC", "ONLOGON",
            "/RL", "HIGHEST",               # Run with highest privileges
            "/TN", TASK_NAME,
            "/TR", f'"{exe_path}" {arguments}'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.show_confirmation_dialog()
            else:
                messagebox.showerror("Error", f"Failed to create task.\n{result.stderr}")
        except Exception as e:
            messagebox.showerror("Error", f"Exception occurred:\n{e}")

    def show_confirmation_dialog(self):
        response = messagebox.askquestion(
            "Task Created",
            "The task has been created.\nYou need to restart the computer for the task to take effect.\n\nRestart now?",
            icon='info',
            type='yesno'
        )
        if response == 'yes':
            # restart now
            self.restart_computer()
        else: 
            # close app
            self.root.quit()
    
    def restart_computer(self):
        try:
            if sys.platform == "win32":
                subprocess.run("shutdown /r /t 0", shell=True)
            else:
                messagebox.showinfo("Info", "Restart is only supported on Windows.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart computer:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()
