import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
from lbm_model_ui import lbm_model_ui
import os

class geonet_test_ui(lbm_model_ui):
    def __init__(self, tab):
        super().__init__()
        geo_loc_label = Label(tab,text="Please select GeoNet installation location:")
        geo_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        geo_loc_txt = Entry(tab)
        geo_loc_txt.grid(row=1,column=0,columnspan=4,sticky='ew')
        geo_loc_btn = Button(tab,text="Browse...",command=lambda:browse_folder(geo_loc_txt))
        geo_loc_btn.grid(row=1,column=4)
        geo_loc_mark = checkmark(tab,False)
        geo_loc_mark.grid(row=1,column=5)

        self.geo_pretrain_combo = ttk.Combobox(tab,state="readonly",\
            values=["Standard (model)","Scale Normalization (model_sn)"],width=25)
        self.geo_pretrain_combo.current(0)
        self.geo_pretrain_combo.grid(row=3,column=2,columnspan=2,sticky='ew')
        geo_pretrain_label = Label(tab,text="Please select the folder that contains pretrained weights:")
        geo_pretrain_label.grid(row=2,column=0,columnspan=2,sticky='w')
        self.geo_pretrain_txt = Entry(tab)
        self.geo_pretrain_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        geo_pretrain_btn = Button(tab,text="Browse...", command=lambda:self.load_pretrain_folder())
        geo_pretrain_btn.grid(row=3,column=4)
        geo_pretrain_mark = checkmark(tab,False)
        geo_pretrain_mark.grid(row=3,column=5)

        geo_dataset_label = Label(tab,text="Please select dataset folder↓  Split method→")
        geo_dataset_label.grid(row=4,column=0,columnspan=2)
        self.split_method = StringVar(tab,"eigen")
        geo_split_eigen = Radiobutton(tab,text="eigen",variable=self.split_method,value="eigen")
        geo_split_eigen.grid(row=4,column=2)
        geo_split_stereo = Radiobutton(tab,text="stereo",variable=self.split_method,value="stereo")
        geo_split_stereo.grid(row=4,column=3)
        geo_dataset_txt = Entry(tab)
        geo_dataset_txt.grid(row=5,column=0,columnspan=3,sticky='ew')
        geo_imgamt_label = Label(tab,text=self.get_img_str())
        geo_imgamt_label.grid(row=5,column=4)
        geo_dataset_btn = Button(tab,text="Browse...",
            command=lambda:self.browse_folder_and_count_img(geo_dataset_txt,geo_imgamt_label))
        geo_dataset_btn.grid(row=5,column=3)

        geo_chk_env_btn = Button(tab,text="Check Environment",command=lambda:self.check_envs())
        geo_chk_env_btn.grid(row=6,column=0,sticky='w')
        self.geo_env_mark = checkmark(tab,False)
        self.geo_env_mark.grid(row=6,column=1,sticky='w')
        geo_start_btn = Button(tab,text="Start")
        geo_start_btn.grid(row=6,column=5,sticky='w')

    def load_pretrain_folder(self):
        fldr_loc = browse_folder(self.geo_pretrain_txt)
        # obtain users' model choice
        choice = self.geo_pretrain_combo.get()
        if choice == "Standard (model)":
            if not os.path.exists(os.path.join(fldr_loc,"model.meta")):
                tkinter.messagebox.showinfo('Error','Model pretrain file does not exist!')
                return
            self.single_pretrain = os.path.join(fldr_loc,"model")
        elif choice == "Scale Normalization (model_sn)":
            if not os.path.exists(os.path.join(fldr_loc,"model_sn.meta")):
                tkinter.messagebox.showinfo('Error','Model pretrain file does not exist!')
                return
            self.single_pretrain = os.path.join(fldr_loc,"model_sn")
        else:
            tkinter.messagebox.showinfo('Error','Model pretrain file does not exist!')

    def check_envs(self):
        # for GeoNet to work, you are required to have:
        # CUDA 9.0, see https://en.wikipedia.org/wiki/CUDA for supported GPUs (nvcc --version)
        # Python 2.7 (python --version)
        # Tensorflow-gpu 1.5.0 (pip show tensorflow-gpu)
        res_dict = {}
        model_env_ready = True
        cudav = get_cuda_version()
        tfv = get_mllib_version("tensorflow-gpu")
        pyv = get_python_version()
        if cudav != "9.0":
            res_dict["CUDA 9.0"] = False
        else:
            res_dict["CUDA 9.0"] = True
        model_env_ready = model_env_ready and res_dict["CUDA 9.0"]
        if tfv != "1.5.0":
            res_dict["tensorflow-gpu 1.5.0"] = False
        else:
            res_dict["tensorflow-gpu 1.5.0"] = True
        model_env_ready = model_env_ready and res_dict["tensorflow-gpu 1.5.0"]
        if pyv == -1:
            res_dict["Python 2.x"] = False
        else:
            if pyv[0] != "2":
                res_dict["Python 2.x"] = False
            else:
                res_dict["Python 2.x"] =  True
        model_env_ready = model_env_ready and res_dict["Python 2.x"]
        self.show_env_result(res_dict)
        set_checkmark(self.geo_env_mark,model_env_ready)

