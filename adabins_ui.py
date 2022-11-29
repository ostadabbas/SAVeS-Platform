import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
from lbm_model_ui import lbm_model_ui

class adabins_ui(lbm_model_ui):
    def __init__(self,tab):
        super().__init__()
        ada_loc_label = Label(tab,text="Please select AdaBins installation location:")
        ada_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        ada_loc_txt = Entry(tab)
        ada_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        ada_loc_btn = Button(tab,text="Browse...")
        ada_loc_btn.grid(row=1,column=3)
        ada_loc_mark = checkmark(tab,False)
        ada_loc_mark.grid(row=1,column=4)

        ada_pretrain_combo = ttk.Combobox(tab,state="readonly",\
            values=["KITTI","NYUv2"])
        ada_pretrain_combo.current(0)
        ada_pretrain_combo.grid(row=3,column=2,columnspan=1,sticky='ew')
        ada_pretrain_label = Label(tab,text="Please select the pretrained weights file:")
        ada_pretrain_label.grid(row=2,column=0,columnspan=2,sticky='w')
        ada_pretrain_txt = Entry(tab)
        ada_pretrain_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        ada_pretrain_btn = Button(tab,text="Browse...")
        ada_pretrain_btn.grid(row=3,column=3)
        ada_pretrain_mark = checkmark(tab,False)
        ada_pretrain_mark.grid(row=3,column=4)

        ada_dataset_label = Label(tab,text="Please select dataset folder:")
        ada_dataset_label.grid(row=4,column=0,columnspan=2,sticky='w')
        ada_dataset_txt = Entry(tab)
        ada_dataset_txt.grid(row=5,column=0,columnspan=3,sticky='ew')
        ada_imgamt_label = Label(tab,text=self.get_img_str())
        ada_imgamt_label.grid(row=5,column=4)
        ada_dataset_btn = Button(tab,text="Browse...",
            command=lambda:self.browse_folder_and_count_img(ada_dataset_txt,ada_imgamt_label))
        ada_dataset_btn.grid(row=5,column=3)

        self.ada_chk_env_btn = Button(tab,text="Check Environment",command=lambda:self.check_envs())
        self.ada_chk_env_btn.grid(row=6,column=0,sticky='w')
        self.ada_env_mark = checkmark(tab,False)
        self.ada_env_mark.grid(row=6,column=1,sticky='w')
        ada_start_btn = Button(tab,text="Start")
        ada_start_btn.grid(row=6,column=4,sticky='e')

    def check_envs(self):
        # for AdaBins to work, you are required to have:
        # CUDA 10.x/11.x, see https://en.wikipedia.org/wiki/CUDA for supported GPUs (nvcc --version)
        # Python >= 3.5 (python --version)
        # PyTorch 1.8 (pip show torch)
        res_dict = {}
        model_env_ready = True
        cudav = get_cuda_version()
        tfv = get_mllib_version("torch")
        pyv = get_python_version()
        if cudav == -1:
            res_dict["CUDA 10/11"] = False
            model_env_ready = False
        else:
            if cudav[:2] != "10" or cudav[:2] != "11":
                res_dict["CUDA 10/11"] = False
                model_env_ready = False
            else:
                res_dict["CUDA {}".format(cudav)] = True
        if tfv == -1:
            res_dict["PyTorch 1.8.x"] = False
            model_env_ready = False
        else:
            if tfv[:3] != "1.8":
                res_dict["PyTorch 1.8.x"] = False
                model_env_ready = False
            else:
                res_dict["Pytorch {}".format(tfv)] = True
        if pyv == -1:
            res_dict["Python >= 3.5"] = False
            model_env_ready = False
        else:
            if pyv[0] != "3" or int(pyv[2])<5:
                res_dict["Python >= 3.5"] = False
                model_env_ready = False
            else:
                res_dict["Python {}".format(pyv)] =  True
        self.show_env_result(res_dict)
        set_checkmark(self.ada_env_mark,model_env_ready)

