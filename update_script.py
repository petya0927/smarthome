import git
repo = git.Repo('C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome')
repo.remotes.origin.pull()

import subprocess
subprocess.Popen(['python', 'weather.py'])