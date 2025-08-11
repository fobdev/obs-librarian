# Use OBS for clips + Folder Librarian

## Folder Librarian - Sort the videos by folder:
I created a script that can sort your videos by fullscreen/borderless software, so your videos folder will look just like in Radeon ReLive or GeForce Experience.
**you just need to run the installer**

### Check the releases page or click here to [download](https://github.com/fobdev/obs-librarian/releases/download/first/obs_librarian.zip) 

# Using OBS as a Clips software: Guide
Tired of your AMD or NVIDIA clipping software to stop working or being bugged? OBS is the best software for recording your screen and you can configure it to create clips the same way as NVIDIA and AMD! **you can even use obs_librarian to sort it by folder!**

### How to set OBS to clip like GeForce Experience and Radeon ReLive

#### Alternatively, you can just [run this script](https://github.com/fobdev/obs-librarian/releases/download/first/schedule_obs.ps1) with PowerShell as Administrator, and it will create the task for you automatically.

#### 1 - Open your OBS Settings
![Image 1](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/1.png)
#### 2 - (important) Configure the output path and set the recording quality, recording format and video encoder to Hardware encoding if possible.
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/2.png)
#### 3 - Go to Hotkeys and scroll to Replay Buffer, and set a key combination save the replay.
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/3.png)
#### Search for Task Scheduler on Windows and Create Basic task
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/5.png)
#### Set a name and proceed
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/6.png)
#### Set to "When I log on" and proceed
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/7.png)
#### Set to Start a program and proceed
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/8.png)
#### Select your OBS folder with the software and set the arguments
Normally, the OBS directory is "C:\Program Files\obs-studio\bin\64bit\obs64.exe"
#### Arguments: **--disable-shutdown-check --startreplaybuffer --minimize-to-tray**
![Image 2](https://raw.githubusercontent.com/fobdev/obs-librarian/refs/heads/main/readme-images/9.png)
#### Click next, and then finish.
Now everything is set up and your OBS will start the replay buffer everytime you start your computer.







