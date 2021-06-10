import git
import os, stat
import shutil
import subprocess

dir = r'C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome'

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

for i in os.listdir(dir):
    if i.endswith('git'):
        tmp = os.path.join(dir, i)
        while True:
            subprocess.call(['attrib', '-H', tmp])
            break
        shutil.rmtree(tmp, onerror=on_rm_error)
    os.remove(i)

git.Git('C:/Users/GRLSat/Desktop/PETI/Programozás').clone('git://github.com/petya0927/smarthome')