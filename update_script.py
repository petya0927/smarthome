# -*- coding: utf-8 -*-
import git
import os, stat
import shutil
import subprocess
import time

start_time = time.time()

git_dir = 'git://github.com/petya0927/smarthome'

print('Update script from {}'.format(git_dir))

def on_rm_error(func, path, exc_info):
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)

for i in os.listdir('.'):
    if i.endswith('git'):
        tmp = os.path.join(dir, i)
        #while True:
            #subprocess.call(['attrib', '-H', tmp])
            #break
        shutil.rmtree(tmp, onerror=on_rm_error)
    else:
        os.remove(i)

git.Git('..').clone('git://github.com/petya0927/smarthome')

print('Updated in {} seconds'.format(time.time() - start_time))
print('Reopening session...')

subprocess.Popen(['python3', 'weather.py'])
exit()