import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
import os
import glob
import shutil
from datetime import datetime

class style_test_ui:
    def __init__(self,tab) -> None:
        self.combo_list = []
        pretrained_fldr_label = Label(tab,text="Please Select Pretrained Weights Folder (style):")
        pretrained_fldr_label.grid(row=0,column=0)
        self.pre_fldr_txt = Entry(tab)
        self.pre_fldr_txt.grid(row=1,column=0,sticky="ew",columnspan=2)
        self.pre_fldr_btn = Button(tab,text="Browse...",command=lambda:self.browse_weights(self.pre_fldr_txt))
        self.pre_fldr_btn.grid(row=1,column=2)
        self.model_sel_combo = ttk.Combobox(tab,state="readonly",values=self.combo_list)
        self.model_sel_combo.grid(row=2,column=0,sticky="ew",columnspan=2)
        self.vsait_loc = None
        img_source_label = Label(tab,text="Please select source PNG images folder (content):")
        img_source_label.grid(row=3,column=0)
        self.img_source_txt = Entry(tab)
        self.img_source_txt.grid(row=4,column=0,sticky="ew",columnspan=2)
        self.img_source_btn = Button(tab,text="Browse...",command=lambda:browse_folder(self.img_source_txt))
        self.img_source_btn.grid(row=4,column=2)
        self.copy_img_btn = Button(tab,text="Load Images",command=lambda:self.copy_to_val(self.img_source_txt.get()))
        self.copy_img_btn.grid(row=5,column=0,sticky="e")
        self.dynamic_count_label = Label(tab,text=">>>>>>>>> 0 image(s) >>>>>>>>>")
        self.dynamic_count_label.grid(row=5,column=1)
        self.transfer_btn = Button(tab,text="Transfer",state=DISABLED)
        self.transfer_btn.grid(row=5,column=2)
        self.progress = ttk.Progressbar(tab, orient="horizontal")
        self.progress.grid(row=5,column=0,sticky="w")


    def browse_weights(self,txt_widget):
        the_path = browse_folder(txt_widget)
        the_list = list(os.listdir(the_path))
        self.combo_list = []
        for entry in the_list:
            if len(entry) <= 5:
                continue
            else:
                if entry[-4:] == "ckpt":
                    self.combo_list.append(entry)
        self.model_sel_combo['value'] = self.combo_list
        if len(self.combo_list) != 0:
            self.model_sel_combo.set(self.combo_list[0])

    def update_vsait_loc(self,loc):
        self.vsait_loc = loc

    def copy_to_val(self,source_fldr):
        if self.vsait_loc is None:
            tkinter.messagebox.showinfo('Error','Style Trasnfer Location Not Selected!')
            return
        else:
            dest_fldr = os.path.join(self.vsait_loc,"data","source")
            dest_fldr_val = os.path.join(dest_fldr,"val")
            self.progress["maximum"] = 100
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            if not os.path.exists(dest_fldr_val):
                os.makedirs(dest_fldr_val)
            else:
                # os.rename(dest_fldr_val,os.path.join(dest_fldr,"val_bkup_"+time.))
                os.rename(dest_fldr_val, f"{dest_fldr_val}_{timestamp}")
                os.makedirs(dest_fldr_val)
            # all ready to copy
            idx = 0
            png_files = glob.glob(f"{source_fldr}/*.png")
            count = len(png_files)
            for pngfile in glob.iglob(os.path.join(source_fldr, "*.png")):
                shutil.copy(pngfile, dest_fldr_val)
                perc = int(idx*100 / count)
                # print(count)
                self.progress["value"] = perc
                self.progress.update()
                self.dynamic_count_label.config(text=">>>>>>>>> {} image(s) >>>>>>>>>".format(idx))
                idx += 1
            self.transfer_btn.config(state=NORMAL)