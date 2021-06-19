# -*- coding: utf-8 -*-
import git
import os, stat
import shutil
import subprocess
import time

start_time = time.time()

dir = r'C:/Users/GRLSat/Desktop/PETI/Programozás/smarthome'
git_dir = 'git://github.com/petya0927/smarthome'

print(f'Update script from {git_dir} into current directory...')

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

for i in os.listdir('.'):
    if i.endswith('git'):
        tmp = os.path.join(dir, i)
        while True:
            subprocess.call(['attrib', '-H', tmp])
            break
        shutil.rmtree(tmp, onerror=on_rm_error)
    else:
        os.remove(i)

git.Git('.').clone('git://github.com/petya0927/smarthome')

print(f'Updated in {time.time() - start_time} seconds')
print('Reopening session...')

subprocess.Popen(['python', 'weather.py'])
exit()