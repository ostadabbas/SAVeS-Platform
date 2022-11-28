import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *

class dpt_ui():
    def __init__(self,tab):
        dpt_loc_label = Label(tab,text="Please select DPT installation location:                                                                                   ")
        dpt_loc_label.grid(row=0,column=0,columnspan=3,sticky='w')
        dpt_loc_txt = Entry(tab)
        dpt_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        dpt_loc_btn = Button(tab,text="Browse...")
        dpt_loc_btn.grid(row=1,column=3)
        dpt_loc_mark = checkmark(tab,False)
        dpt_loc_mark.grid(row=1,column=4)

        dpt_scale_combo = ttk.Combobox(tab,state="readonly",\
            values=["dpt_hybrid","dpt_large"])
        dpt_scale_combo.current(0)
        dpt_scale_combo.grid(row=2,column=0,columnspan=1,sticky='ew')
        dpt_finetune_combo = ttk.Combobox(tab,state="readonly",\
            values=["dpt_hybrid_kitti","dpt_hybrid_nyu"])
        dpt_finetune_combo.grid(row=2,column=1,columnspan=3,sticky='ew')
        dpt_finetune_combo.configure(state=DISABLED)

        dpt_pretrain_label = Label(tab,text="Please select the pretrained weights file:")
        dpt_pretrain_label.grid(row=3,column=0,columnspan=3,sticky='w')
        dpt_pretrain_txt = Entry(tab)
        dpt_pretrain_txt.grid(row=4,column=0,columnspan=3,sticky='ew')
        dpt_pretrain_btn = Button(tab,text="Browse...")
        dpt_pretrain_btn.grid(row=4,column=3)
        dpt_pretrain_mark = checkmark(tab,False)
        dpt_pretrain_mark.grid(row=4,column=4)

        dpt_dataset_label = Label(tab,text="Please select dataset folder:")
        dpt_dataset_label.grid(row=5,column=0,columnspan=2,sticky='w')
        dpt_dataset_txt = Entry(tab)
        dpt_dataset_txt.grid(row=6,column=0,columnspan=3,sticky='ew')
        dpt_dataset_btn = Button(tab,text="Browse...")
        dpt_dataset_btn.grid(row=6,column=3)
        dpt_imgamt_label = Label(tab,text="0 images(s)")
        dpt_imgamt_label.grid(row=6,column=4)

        dpt_chk_env_btn = Button(tab,text="Check Environment")
        dpt_chk_env_btn.grid(row=7,column=0,sticky='w')
        dpt_env_mark = checkmark(tab,False)
        dpt_env_mark.grid(row=7,column=1,sticky='w')
        dpt_start_btn = Button(tab,text="Start")
        dpt_start_btn.grid(row=7,column=4,sticky='e')