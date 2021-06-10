import git
import os, stat
import time
import shutil
'''
#os.rmdir('smarthome')
#os.chmod('C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome', stat.S_IWRITE)
shutil.rmtree('C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome/', ignore_errors=True)
time.sleep(5)
git.Git('C:/Users/GRLSat/Desktop/PETI/Programozás/').clone('https://github.com/petya0927/smarthome')

import subprocess
subprocess.Popen(['python', 'weather.py'])'''

repo = git.Repo("C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome")
repo.remotes.pull()
input()