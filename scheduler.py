import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import win32com.client
import ctypes

DEFAULT_PATH = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
TASK_NAME = "Start OBS Replay Buffer"
TASK_DESCRIPTION = "Start OBS Replay Buffer on logon with arguments."

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class TaskSchedulerApp:
    def __init__(self, root):
        self.root = root
        root.title("OBS Task Scheduler")
        root.geometry("600x150")

        self.label = tk.Label(root, text="OBS Directory:")
        self.label.pack(anchor="w", padx=10, pady=(10, 0))

        frame = tk.Frame(root)
        frame.pack(fill="x", padx=10)

        self.path_var = tk.StringVar(value=DEFAULT_PATH)
        self.entry = tk.Entry(frame, textvariable=self.path_var)
        self.entry.pack(side="left", fill="x", expand=True)

        self.browse_button = tk.Button(frame, text="Browse...", command=self.browse_file)
        self.browse_button.pack(side="left", padx=5)

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

        try:
            self.create_task_with_pywin32(exe_path)
            self.show_confirmation_dialog()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create task:\n{e}")

    def create_task_with_pywin32(self, exe_path):
        folder = os.path.dirname(exe_path)
        arguments = '--disable-shutdown-check --startreplaybuffer --minimize-to-tray'

        scheduler = win32com.client.Dispatch('Schedule.Service')
        scheduler.Connect()

        root_folder = scheduler.GetFolder('\\')

        task_def = scheduler.NewTask(0)

        # Create trigger: Logon trigger
        TASK_TRIGGER_LOGON = 9
        trigger = task_def.Triggers.Create(TASK_TRIGGER_LOGON)

        # Task settings
        task_def.RegistrationInfo.Description = TASK_DESCRIPTION
        task_def.Settings.Enabled = True
        task_def.Settings.StartWhenAvailable = True
        task_def.Settings.Hidden = False

        # Create action to run the executable with arguments
        TASK_ACTION_EXEC = 0
        action = task_def.Actions.Create(TASK_ACTION_EXEC)
        action.Path = exe_path
        action.Arguments = arguments
        action.WorkingDirectory = folder  # Set "Start in" directory

        # Register the task
        TASK_CREATE_OR_UPDATE = 6
        TASK_LOGON_INTERACTIVE_TOKEN = 3

        root_folder.RegisterTaskDefinition(
            TASK_NAME,
            task_def,
            TASK_CREATE_OR_UPDATE,
            '',  # No user
            '',  # No password
            TASK_LOGON_INTERACTIVE_TOKEN
        )

    def show_confirmation_dialog(self):
        response = messagebox.askquestion(
            "Task Created",
            "The task has been created.\nYou need to restart the computer for the task to take effect.\n\nRestart now?",
            icon='info',
            type='yesno'
        )
        if response == 'yes':
            self.restart_computer()
        else:
            self.root.quit()

    def restart_computer(self):
        try:
            subprocess.run("shutdown /r /t 0", shell=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart computer:\n{e}")


if __name__ == "__main__":
    if not is_admin():
        # Relaunch the script with admin privileges
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit()

    root = tk.Tk()
    app = TaskSchedulerApp(root)
    root.mainloop()
