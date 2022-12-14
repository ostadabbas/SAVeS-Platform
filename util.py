from tkinter import *
from tkinter import filedialog as fd
import subprocess
import re

def set_entry_txt(entry_widget,txt):
    entry_widget.delete(0,END)
    entry_widget.insert(0,txt)

def browse_folder(show_widget,start_dir=r"."):
    filepath=fd.askdirectory(initialdir=start_dir,title="Select Folder")
    if type(filepath) is tuple:
        if len(filepath) == 0:
            filepath = "."
        else:
            filepath = filepath[0]
    show_widget.delete(0,END)
    show_widget.insert(0,filepath)
    return filepath

def browse_file(show_widget,ext_desc,ext,start_dir='~/Downloads'):
    filetypes = ((ext_desc, "*.{}".format(ext)),)
    filename = fd.askopenfilename(title=ext_desc,initialdir=start_dir,filetypes=filetypes)
    show_widget.delete(0,END)
    show_widget.insert(0,filename)
    return filename

def checkmark(parent,val):
    if not val:
        return Label(parent,text="✕",fg='red')
    else:
        return Label(parent,text="✓",fg='green')

def set_checkmark(show_widget,set_val):
    if not set_val:
        show_widget.configure(text="✕",fg='red')
    else:
        show_widget.configure(text="✓",fg='green')

def get_cuda_version():
    command = "nvcc --version"
    test_str = "nvcc: NVIDIA (R) Cuda compiler driver\n Copyright (c) 2005-2017 NVIDIA Corporation\n Built on Fri_Sep__1_21:08:03_CDT_2017\n Cuda compilation tools, release 9.0, V9.0.176"
    try:
        h = subprocess.check_output(command,shell=True)
        pattern = r"release [0-9]+\.[0-9]"
        res = re.compile(pattern).findall(h.decode())
        # print(res[0].split(" ")[-1])
        return res[0].split(" ")[-1]
    except:
        return -1

def get_mllib_version(package):
    '''
    supports tensorflow-gpu and torch
    '''
    command = "pip show {}".format(package)
    test_str = "DEPRECATION: Python 2.7 will reach the end of its life on January 1st, 2020. Please upgrade your Python as Python 2.7 won't be maintained after that date. A future version of pip will drop support for Python 2.7. More details about Python 2 support in pip, can be found at https://pip.pypa.io/en/latest/development/release-process/#python-2-support\nName: tensorflow-gpu\nVersion: 1.5.0\nSummary: TensorFlow helps the tensors flow"
    try:
        h = subprocess.check_output(command,shell=True)
        pattern = r"Version: [0-9]+\.[0-9]+\.[0-9]+"
        res = re.compile(pattern).findall(h.decode())
        ret = res[0].split(" ")[-1]
        return ret
    except:
        return -1

def get_python_version():
    command = "python --version"
    try:
        h = subprocess.check_output(command,shell=True)
        pattern = r"Python [0-9]+\.[0-9]+\.[0-9]+"
        res = re.compile(pattern).findall(h.decode())
        ret = res[0].split(" ")[-1]
        return ret
    except Exception as e:
        print(e)
        return -1