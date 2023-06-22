import os
import glob
import shutil
from datetime import datetime
import shlex
import subprocess
import sys

timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
ENVBIN = sys.exec_prefix
BIN2 = os.path.join(sys.exec_prefix, "bin", "python")
is_there = os.path.exists(BIN2)
print(BIN2,is_there)
# for windows
# test_command = "cd /D D:/LocalProjects/synthetic2/vsait && D:/Programs/Anaconda/envs/vsait/bin/python.exe test.py --name=\"20230621-191546\" --checkpoint=\"D:/LocalProjects/synthetic2/vsait/checkpoints/all\epoch=26-step=59564.ckpt\""
# test_command = r"cd D:\\ && cd LocalProjects/synthetic2/vsait && 'D:\\Programs\\Anaconda\\envs\\vsait\\bin\\python.exe'"
test_command = "cd /mnt/d/LocalProjects/synthetic2/AdaBins/ ; /home/petebai/anaconda3/envs/adabins/bin/python test_demo.py --datapath /mnt/d/LocalProjects/synthetic2/Presil_full/images/content/ --pt_used kitti"

# test_command = shlex.split(test_command)
print(test_command)
res = subprocess.check_output(test_command,shell=True)
print(res)
print(res.decode("utf-8"))