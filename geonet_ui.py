import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *

class geonet_test_ui():
    def __init__(self, tab):
        geo_loc_label = Label(tab,text="Please select GeoNet installation location:")
        geo_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        geo_loc_txt = Entry(tab)
        geo_loc_txt.grid(row=1,column=0,columnspan=4,sticky='ew')
        geo_loc_btn = Button(tab,text="Browse...")
        geo_loc_btn.grid(row=1,column=4)
        geo_loc_mark = checkmark(tab,False)
        geo_loc_mark.grid(row=1,column=5)

        geo_pretrain_combo = ttk.Combobox(tab,state="readonly",\
            values=["Standard (model)","Scale Normalization (model_sn)"],width=25)
        geo_pretrain_combo.current(0)
        geo_pretrain_combo.grid(row=3,column=2,columnspan=2,sticky='ew')
        geo_pretrain_label = Label(tab,text="Please select the folder that contains pretrained weights:")
        geo_pretrain_label.grid(row=2,column=0,columnspan=2,sticky='w')
        geo_pretrain_txt = Entry(tab)
        geo_pretrain_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        geo_pretrain_btn = Button(tab,text="Browse...")
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
        geo_dataset_btn = Button(tab,text="Browse...")
        geo_dataset_btn.grid(row=5,column=3)
        geo_imgamt_label = Label(tab,text="0 images(s)")
        geo_imgamt_label.grid(row=5,column=4)

        geo_chk_env_btn = Button(tab,text="Check Environment")
        geo_chk_env_btn.grid(row=6,column=0,sticky='w')
        geo_env_mark = checkmark(tab,False)
        geo_env_mark.grid(row=6,column=1,sticky='w')
        geo_start_btn = Button(tab,text="Start")
        geo_start_btn.grid(row=6,column=5,sticky='w')