import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter import filedialog as fd
from util import *
import os
import numpy as np
from PIL import Image
import imageio
import cv2
import math
import threading
import time

class depth_ana_ui:
    def __init__(self, tab) -> None:
        super().__init__()
        # check kitti file valid
        if not os.path.exists("./kitti_eval_tools/evaluate_depth"):
            tkinter.messagebox.showinfo('Error','KITTI Evaluation toolchain not detected! Program will not work!')
        self.dest_fldr = None
        npy_loc_label = Label(tab,text="Please select depth prediction file (*.npy):")
        npy_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        self.npy_loc_txt = Entry(tab)
        self.npy_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        npy_loc_btn = Button(tab,text="Browse...",command=lambda:self.validate_ct(True))
        npy_loc_btn.grid(row=1,column=3)

        gt_loc_label = Label(tab,text="Please select folder of ground truth:")
        gt_loc_label.grid(row=2,column=0,columnspan=2,sticky='w')
        self.gt_loc_txt = Entry(tab)
        self.gt_loc_txt.grid(row=3,column=0,columnspan=3,sticky='ew')
        gt_loc_btn = Button(tab,text="Browse...",command=lambda:self.validate_ct(False))
        gt_loc_btn.grid(row=3,column=3)

        self.ct_eql_mark = checkmark(tab,False)
        self.ct_eql_mark.grid(row=4,column=0)
        self.ct_desc_label = Label(tab,text="0 images from prediction file, 0 in ground truth folder")
        self.ct_desc_label.grid(row=4,column=1)

        self.extract_btn = Button(tab,text="Extract",command=lambda:self.extract_img())
        self.extract_btn.grid(row=5,column=0)
    
    def extract_img(self,extract_loc=None):
        if self.npy_loc_txt.get() == "":
            print("empty container")
            top = tk.Toplevel()
            top.wm_title("Output Name")
            top.protocol("WM_DELETE_WINDOW", self.on_close)
            top.update()
            time.sleep(5)
            # do something time consuming but exact time can't be determined
            top.destroy()
            
        if extract_loc is None:
            fldr_name = self.npy_loc_txt.get().split("/")[-1] + "_extract"
            fldr_path = os.path.join(".","extracted",fldr_name)
            if not os.path.exists(fldr_path):
                os.makedirs(fldr_path)
            self.dest_fldr = fldr_path
        else:
            self.dest_fldr = extract_loc

        self.img_coll = np.load(self.npy_loc_txt.get())
        self.num_img = self.img_coll.shape[0]
        # start assign workload
        thread_ct = 8
        each_thread_ct = math.ceil((self.num_img-10)/thread_ct)
        threads_handle = []
        name_arr = list(os.listdir(self.gt_loc_txt.get()))
        name_arr.sort()
        # with open("img_seq.txt",'r') as f:
        #     name_arr = f.readlines()
        # tkinter.messagebox.showinfo('Attention','This window will close itself when extraction is finished!')
        for th_ct in range(thread_ct):
            start = 5 + th_ct * each_thread_ct
            end = 5+(th_ct+1)*each_thread_ct
            # for the last thread
            if th_ct == thread_ct-1:
                if end != self.num_img - 5:
                    end = self.num_img - 5
            print(start,end)
            
            threads_handle.append(threading.Thread(target=self.__open_and_cvt,args=(self.gt_loc_txt.get(),start,end,name_arr,)))
            threads_handle[-1].start()

        for th_ct in range(thread_ct):
            threads_handle[th_ct].join()
    
    def on_close(self):
        # Do nothing here to prevent the user from closing the window
        pass
    # must be called by extract_img
    def __open_and_cvt(self,gt_folder,start,end,name_arr):
        reshape = (1216,352)
        for i in range(start, end):
            if i % 100 == 0:
                print(i)
            gt = np.array(Image.open(gt_folder+"/"+name_arr[i]))
            interm_img = cv2.resize(self.img_coll[i],reshape,interpolation=cv2.INTER_LINEAR)
            new_img = scale_matching(gt,interm_img)
            imageio.imwrite(self.dest_fldr+"/"+name_arr[i], new_img.astype(np.uint16))

    def validate_ct(self,is_npy):
        if is_npy:
            browse_file(self.npy_loc_txt,"Numpy File","npy")
        else:
            browse_folder(self.gt_loc_txt)
        try:
            pred_arr = np.load(self.npy_loc_txt.get())
            pred_len = pred_arr.shape[0]
        except:
            pred_len = 0
        try:
            gt_dir = self.gt_loc_txt.get()
            gt_len = len(list(os.listdir(gt_dir)))
        except:
            gt_len = 0
        if pred_len != 0 and gt_len != 0:
            if pred_len == gt_len:
                set_checkmark(self.ct_eql_mark, True)
        
        ct_str = "{} images from prediction file, {} in ground truth folder".format(pred_len,gt_len)
        self.ct_desc_label.config(text=ct_str)
        
