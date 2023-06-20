import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
import time
from util import *
import os
from styled.test_ui import style_test_ui
from styled.train_ui import style_train_ui

class style_frame(Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.pack()
        self.master.title("SAVeS+: Reduces Domain Gap")
       
        self.tabsystem = ttk.Notebook(self)
        self.tab_train = Frame(self.tabsystem)
        self.tab_test = Frame(self.tabsystem)

        self.vsait_test = style_test_ui(self.tab_test)
        self.vsait_train = style_train_ui(self.tab_train)

        self.load_sep = ttk.Labelframe(self, text='VSAIT Configure')
        self.load_sep.pack(expand=1,fill="both")

        self.load_vsait_label = Label(self.load_sep,text="Please Select VSAIT Installation Location:")
        self.load_vsait_label.grid(row=0,column=0)
        self.load_vsait_entry = Entry(self.load_sep)
        self.load_vsait_entry.grid(row=1,column=0,sticky="ew",columnspan=2)
        self.load_vsait_btn = Button(self.load_sep,text="Browse...",command=lambda:browse_folder(self.load_vsait_entry))
        self.load_vsait_btn.grid(row=1,column=2)
        self.chk_env_btn = Button(self.load_sep,text="Check Environments",command=lambda:self.check_envs())
        self.chk_env_btn.grid(row=2,column=0,sticky="w")
        self.env_chkmark = checkmark(self.load_sep,False)
        self.env_chkmark.grid(row=2,column=2)

        self.tabsystem.pack(expand=1, fill=tk.Y)
        self.__hide_all_tabs(False)
    def __hide_all_tabs(self,do_hide):
        if do_hide:
            self.tabsystem.hide(self.tab_train)
            self.tabsystem.hide(self.tab_test)
        else:
            self.tabsystem.add(self.tab_train, text='Train New Style Weight')
            self.tabsystem.add(self.tab_test, text='Generate Using Existing Weights')

    def check_envs(self):
        # for VSAIT to work, you are required to have:
        # CUDA 11.x, see https://en.wikipedia.org/wiki/CUDA for supported GPUs (nvcc --version)
        # Python >= 3.8 (python --version)
        # PyTorch 1.11 (pip show torch)
        res_dict = {}
        model_env_ready = True
        cudav = get_cuda_version()
        tfv = get_mllib_version("torch")
        pyv = get_python_version()
        lightningv = get_mllib_version("pytorch-lightning")
        if cudav == -1:
            res_dict["CUDA 11"] = False
            model_env_ready = False
        else:
            if cudav[:2] != "11":
                res_dict["CUDA 11"] = False
                model_env_ready = False
            else:
                res_dict["CUDA {}".format(cudav)] = True
        if tfv == -1:
            res_dict["PyTorch >= 1.11.x"] = False
            model_env_ready = False
        else:
            if float(tfv[:4]) <= 1.11:
                res_dict["PyTorch >= 1.11.x"] = False
                model_env_ready = False
            else:
                res_dict["Pytorch {}".format(tfv)] = True
        if pyv == -1:
            res_dict["Python >= 3.8"] = False
            model_env_ready = False
        else:
            if pyv[0] != "3" or int(pyv[2])<8:
                res_dict["Python >= 3.8"] = False
                model_env_ready = False
            else:
                res_dict["Python {}".format(pyv)] =  True
        if lightningv == -1:
            res_dict["PyTorch-Lightning"] = False
            model_env_ready = False
        else:
            res_dict["pytorch-lightning {}".format(lightningv)] =  True
        
        file_ready = os.path.exists(os.path.join(self.load_vsait_entry.get(),"train.py"))
        model_env_ready = file_ready and model_env_ready
        show_env_result(res_dict)
        set_checkmark(self.env_chkmark,model_env_ready)
        self.__hide_all_tabs(not model_env_ready)
        self.vsait_test.update_vsait_loc(self.load_vsait_entry.get())
        self.vsait_train.update_vsait_loc(self.load_vsait_entry.get())

if __name__ == '__main__':
    style_frame().mainloop()