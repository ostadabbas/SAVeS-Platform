from tkinter import *
from tkinter import filedialog as fd
import subprocess
import re
import numpy as np
import os
from datetime import datetime
import sys
from PIL import Image,ImageTk
import tkinter as tk

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
        widget = Label(parent,text="✕",fg='red')
        return widget
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
    
def test_torch_cuda():
    result = True
    try:
        import torch
        result = torch.cuda.is_available()
    except Exception as e:
        tk.messagebox.showerror(e)
        result = False
    return result

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
    
def scale_matching(gt,pred):
    scalor = np.median(gt[gt>0]) / np.median(pred[gt>0])
    new_res = pred.astype('float32') * scalor
    new_res[new_res>2**16-1]=2**16-1
    return new_res

def show_env_result(res_dict):
    cmd_window = Toplevel()
    cmd_window.wm_title("Check Result")
    widgets = []
    for cont,val in res_dict.items():
        widgets.append(Label(cmd_window,text=cont))
        widgets[-1].pack(side=LEFT)
        widgets.append(checkmark(cmd_window,val))
        widgets[-1].pack(side=LEFT)

def add_placeholder_to(entry, placeholder):
    entry.insert(0, placeholder)
    entry.bind('<FocusIn>', lambda event: entry.delete('0', 'end'))
    entry.bind('<FocusOut>', lambda event: entry.insert(0, placeholder) if not entry.get() else None)

def check_make_folder(folder_to_check):
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    if not os.path.exists(folder_to_check):
        os.makedirs(folder_to_check)
    else:
        # os.rename(dest_fldr_val,os.path.join(dest_fldr,"val_bkup_"+time.))
        os.rename(folder_to_check, f"{folder_to_check}_{timestamp}")
        os.makedirs(folder_to_check)

def get_curr_python():
    BIN2 = os.path.join(sys.exec_prefix, "bin", "python")
    if os.path.exists(BIN2):
        return BIN2
    else:
        return None

def on_close():
        # Do nothing here to prevent the user from closing the window
    pass

def make_top_wdnw(show_txt):
    img = Image.open("./images/warn.png")
    img = ImageTk.PhotoImage(img)
    top = tk.Toplevel()
    top.wm_title("Halt")
    top.protocol("WM_DELETE_WINDOW", on_close)
    wait_label = Label(top,image=img)
    wait_label.image = img
    wait_label.grid(row=0,column=0)
    wait_label2 = Label(top,text=show_txt)
    wait_label2.grid(row=1,column=0)
    top.update()
    return top