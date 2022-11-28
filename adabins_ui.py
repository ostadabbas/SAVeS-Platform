import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *

class adabins_ui():
    def __init__(self,tab):
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
        ada_dataset_btn = Button(tab,text="Browse...")
        ada_dataset_btn.grid(row=5,column=3)
        ada_imgamt_label = Label(tab,text="0 images(s)")
        ada_imgamt_label.grid(row=5,column=4)

        ada_chk_env_btn = Button(tab,text="Check Environment")
        ada_chk_env_btn.grid(row=6,column=0,sticky='w')
        ada_env_mark = checkmark(tab,False)
        ada_env_mark.grid(row=6,column=1,sticky='w')
        ada_start_btn = Button(tab,text="Start")
        ada_start_btn.grid(row=6,column=4,sticky='e')