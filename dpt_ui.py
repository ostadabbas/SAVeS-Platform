import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
from lbm_model_ui import lbm_model_ui

class dpt_ui(lbm_model_ui):
    def __init__(self,tab):
        super().__init__()
        dpt_loc_label = Label(tab,text="Please select DPT installation location:                                                                                   ")
        dpt_loc_label.grid(row=0,column=0,columnspan=3,sticky='w')
        dpt_loc_txt = Entry(tab)
        dpt_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        dpt_loc_btn = Button(tab,text="Browse...",command=lambda:browse_folder(dpt_loc_txt))
        dpt_loc_btn.grid(row=1,column=3)
        dpt_loc_mark = checkmark(tab,False)
        dpt_loc_mark.grid(row=1,column=4)

        self.scale_val = StringVar()
        self.hybrid_val = StringVar()

        self.dpt_finetune_combo = ttk.Combobox(tab,state="readonly",\
            values=["No fine-tuning","dpt_hybrid_kitti","dpt_hybrid_nyu"])
        self.dpt_finetune_combo.current(0)
        self.dpt_finetune_combo.grid(row=2,column=1,columnspan=3,sticky='ew')
        dpt_scale_combo = ttk.Combobox(tab,state="readonly",\
            values=["dpt_hybrid","dpt_large"],textvariable=self.scale_val)
        dpt_scale_combo.current(0)
        dpt_scale_combo.grid(row=2,column=0,columnspan=1,sticky='ew')
        dpt_scale_combo.bind('<<ComboboxSelected>>', self.check_if_hybrid)
        # dpt_finetune_combo.configure(state=DISABLED)

        dpt_pretrain_label = Label(tab,text="Please select the pretrained weights file:")
        dpt_pretrain_label.grid(row=3,column=0,columnspan=3,sticky='w')
        dpt_pretrain_txt = Entry(tab)
        dpt_pretrain_txt.grid(row=4,column=0,columnspan=3,sticky='ew')
        dpt_pretrain_btn = Button(tab,text="Browse...",command=lambda:self.load_pretrain(dpt_pretrain_txt,"pt"))
        dpt_pretrain_btn.grid(row=4,column=3)
        dpt_pretrain_mark = checkmark(tab,False)
        dpt_pretrain_mark.grid(row=4,column=4)

        dpt_dataset_label = Label(tab,text="Please select dataset folder:")
        dpt_dataset_label.grid(row=5,column=0,columnspan=2,sticky='w')
        dpt_dataset_txt = Entry(tab)
        dpt_dataset_txt.grid(row=6,column=0,columnspan=3,sticky='ew')
        dpt_imgamt_label = Label(tab,text=self.get_img_str())
        dpt_imgamt_label.grid(row=6,column=4)
        dpt_dataset_btn = Button(tab,text="Browse...",
            command=lambda:self.browse_folder_and_count_img(dpt_dataset_txt,dpt_imgamt_label))
        dpt_dataset_btn.grid(row=6,column=3)

        dpt_chk_env_btn = Button(tab,text="Check Environment", command=lambda:self.check_envs())
        dpt_chk_env_btn.grid(row=7,column=0,sticky='w')
        self.dpt_env_mark = checkmark(tab,False)
        self.dpt_env_mark.grid(row=7,column=1,sticky='w')
        dpt_start_btn = Button(tab,text="Start")
        dpt_start_btn.grid(row=7,column=4,sticky='e')

    def check_if_hybrid(self,event):
        select = self.scale_val.get()
        print(select)
        if select == "dpt_hybrid":
            self.dpt_finetune_combo.configure(state=NORMAL)
        else:
            self.dpt_finetune_combo.configure(state=DISABLED)

    def check_envs(self):
        # for DPT to work, you are required to have:
        # CUDA 10.x/11.x, see https://en.wikipedia.org/wiki/CUDA for supported GPUs (nvcc --version)
        # Python >= 3.5 (python --version)
        # PyTorch 1.8 (pip show torch)
        # opencv 4.5.1, timm 0.4.5
        res_dict = {}
        model_env_ready = True
        cudav = get_cuda_version()
        tfv = get_mllib_version("torch")
        opcv = get_mllib_version("opencv-python")
        timmv = get_mllib_version("timm")
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
        if timmv == -1:
            res_dict["timm 0.4.5"] = False
            model_env_ready = False
        else:
            if timmv != "0.4.5":
                res_dict["timm 0.4.5"] = False
                model_env_ready = False
            else:
                res_dict["timm 0.4.5"] = True
        if opcv == -1:
            res_dict["OpenCV 4.5"] = False
            model_env_ready = False
        else:
            if opcv[:3] != "4.5":
                res_dict["OpenCV 4.5"] = False
                model_env_ready = False
            else:
                res_dict["OpenCV {}".format(opcv)] = True
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
        set_checkmark(self.dpt_env_mark,model_env_ready)