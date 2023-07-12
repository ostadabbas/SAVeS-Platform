import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from util import *
from depth.lbm_model_ui import lbm_model_ui
from PIL import Image,ImageTk
import os
import subprocess

class adabins_ui(lbm_model_ui):
    def __init__(self,tab):
        super().__init__()
        img = Image.open("./images/warn.png")
        self.img = ImageTk.PhotoImage(img)
        ada_loc_label = Label(tab,text="Please select AdaBins installation location:")
        ada_loc_label.grid(row=0,column=0,columnspan=2,sticky='w')
        self.ada_loc_txt = Entry(tab)
        self.ada_loc_txt.grid(row=1,column=0,columnspan=3,sticky='ew')
        ada_loc_btn = Button(tab,text="Browse...",command=lambda:browse_folder(self.ada_loc_txt))
        ada_loc_btn.grid(row=1,column=3)
        # ada_loc_mark = checkmark(tab,False)
        # ada_loc_mark.grid(row=1,column=4)

        self.ada_pretrain_combo = ttk.Combobox(tab,state="readonly",\
            values=["KITTI","NYUv2"])
        self.ada_pretrain_combo.current(0)
        self.ada_pretrain_combo.grid(row=3,column=2,columnspan=1,sticky='ew')
        ada_pretrain_label = Label(tab,text="Please select the pretrained weights file:")
        ada_pretrain_label.grid(row=2,column=0,columnspan=2,sticky='w')
        # ada_pretrain_txt = Entry(tab)
        # ada_pretrain_txt.grid(row=3,column=0,columnspan=2,sticky='ew')
        # ada_pretrain_btn = Button(tab,text="Browse...",command=lambda:self.load_pretrain(ada_pretrain_txt,"pth"))
        # ada_pretrain_btn.grid(row=3,column=3)
        # ada_pretrain_mark = checkmark(tab,False)
        # ada_pretrain_mark.grid(row=3,column=4)

        ada_dataset_label = Label(tab,text="Please select dataset folder:")
        ada_dataset_label.grid(row=4,column=0,columnspan=2,sticky='w')
        self.ada_dataset_txt = Entry(tab)
        self.ada_dataset_txt.grid(row=5,column=0,columnspan=3,sticky='ew')
        ada_imgamt_label = Label(tab,text=self.get_img_str())
        ada_imgamt_label.grid(row=5,column=4)
        ada_dataset_btn = Button(tab,text="Browse...",
            command=lambda:self.browse_folder_and_count_img(self.ada_dataset_txt,ada_imgamt_label))
        ada_dataset_btn.grid(row=5,column=3)

        self.ada_chk_env_btn = Button(tab,text="Check Environment",command=lambda:self.check_envs())
        self.ada_chk_env_btn.grid(row=6,column=0,sticky='w')
        self.ada_env_mark = checkmark(tab,False)
        self.ada_env_mark.grid(row=6,column=1,sticky='w')
        ada_start_btn = Button(tab,text="Start",command=lambda:self.start_eval())
        ada_start_btn.grid(row=6,column=4,sticky='e')

    def check_envs(self):
        # for AdaBins to work, you are required to have:
        # CUDA 10.x/11.x, see https://en.wikipedia.org/wiki/CUDA for supported GPUs (nvcc --version)
        # Python >= 3.5 (python --version)
        # PyTorch > 1.8 (pip show torch)
        res_dict = {}
        model_env_ready = True
        cudav = get_cuda_version()
        tfv = get_mllib_version("torch")
        pyv = get_python_version()
        if cudav == -1:
            res_dict["CUDA 10/11"] = False
            model_env_ready = False
        else:
            if cudav[:2] != "10" and cudav[:2] != "11" and cudav[:2] != "12":
                res_dict["CUDA 10-12"] = False
                model_env_ready = False
            else:
                res_dict["CUDA {}".format(cudav)] = True
        if tfv == -1:
            res_dict["PyTorch > 1.8.x"] = False
            model_env_ready = False
        else:
            main_v,small_v,_ = tfv.split(".")
            if int(small_v) <= 8 or int(main_v) != 1:
                res_dict["PyTorch > 1.8.x"] = False
                model_env_ready = False
            else:
                if test_torch_cuda():
                    res_dict["Pytorch {}".format(tfv)] = True
                else:
                    res_dict["PyTorch > 1.8.x"] = False
                    model_env_ready = False
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

    def start_eval(self):
        ada_loc = self.ada_loc_txt.get()
        env_py = get_curr_python()
        if env_py is None:
            tkinter.messagebox.showerror("Something went wrong: start_eval()->conda python bin not found")
            return
        if not os.path.exists(os.path.join(ada_loc,"test_demo.py")):
            tkinter.messagebox.showerror\
                ("Something went wrong: \nstart_eval()->test_demo.py not found in {}".format(ada_loc))
            return
        img_pth = self.ada_dataset_txt.get()
        all_pt = {"KITTI":"kitti","NYUv2":"nyu"}
        curr_pt = all_pt[self.ada_pretrain_combo.get()]
        test_command = \
            "cd {} ; {} test_demo.py --datapath {} --pt_used {}"\
            .format(ada_loc,env_py,img_pth,curr_pt)
        try:
            top = make_top_wdnw("Prediction is in progress, this window will close itself when done.")
            top.update()
            res = subprocess.check_output(test_command,shell=True)
            top.destroy()
            print(res.decode("utf-8"))
            tkinter.messagebox.showinfo(title="pred.npy Location",message=os.path.join(ada_loc,"pred.npy"))
        except Exception as e:
            print(e)

