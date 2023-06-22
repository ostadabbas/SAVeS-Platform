from tkinter import *
from tkinter import ttk
from util import *
import tkinter.messagebox
from PIL import Image,ImageTk,ImageOps
import glob
import os
import shutil
from datetime import datetime


class style_train_ui:
    def __init__(self,tab) -> None:
        content_label = Label(tab,text="Please select source dataset (content) location")
        content_label.grid(row=0,column=0)
        self.content_txt = Entry(tab)
        self.content_txt.grid(row=1,column=0,sticky="ew",columnspan=2)
        self.vsait_loc = None

        style_label = Label(tab,text="Please select target dataset (style) location")
        style_label.grid(row=2,column=0)
        self.style_txt = Entry(tab)
        self.style_txt.grid(row=3,column=0,sticky="ew",columnspan=2)

        self.train_name_txt = Entry(tab)
        add_placeholder_to(self.train_name_txt,"Enter name for this weight")
        self.train_name_txt.grid(row=4,column=0,sticky="ew",columnspan=2)
        self.load_btn = Button(tab,text="Load Images",command=lambda:self.copy_to_dest())
        self.load_btn.grid(row=5,column=0,sticky="w")
        self.progress = ttk.Progressbar(tab, orient="horizontal")
        self.progress.grid(row=5,column=0,sticky="e",columnspan=2)
        self.start_btn = Button(tab,text="Start Training",state=DISABLED,command=lambda:self.start_train())
        self.start_btn.grid(row=5,column=2)

        self.preview_sep = ttk.Labelframe(tab, text='Preview')
        self.preview_sep.grid(row=6,column=0,sticky="ew")
        wait_img = Image.open("./images/wait.png").resize((64,64))
        self.img = ImageTk.PhotoImage(wait_img)
        self.content_img_label = Label(self.preview_sep,image=self.img)
        self.content_img_label.grid(row=7,column=0)
        arrow_label = Label(self.preview_sep,text=">>>>>>>>")
        arrow_label.grid(row=7,column=1)
        self.style_img_label = Label(self.preview_sep,image=self.img)
        self.style_img_label.grid(row=7,column=2)
        self.content_count = Label(self.preview_sep,text="0 image(s)")
        self.content_count.grid(row=8,column=0)
        self.style_count = Label(self.preview_sep,text="0 image(s)")
        self.style_count.grid(row=8,column=2)

        content_btn = Button(tab,text="Browse...",command=lambda:self.browse_img_folder(self.content_txt,self.content_img_label))
        content_btn.grid(row=1,column=2)
        style_btn = Button(tab,text="Browse...",command=lambda:self.browse_img_folder(self.style_txt,self.style_img_label))
        style_btn.grid(row=3,column=2)

    def browse_img_folder(self,txt_widget,img_widget):
        desired_size = 64
        img_pth = browse_folder(txt_widget)
        png_files = glob.glob(f"{img_pth}/*.png")
        show_img = Image.open(os.path.join(img_pth,png_files[0]))
        old_size = show_img.size
        print(old_size)
        ratio = float(desired_size)/min(old_size)
        new_size = tuple([int(x*ratio) for x in old_size])
        print(new_size)
        show_img = show_img.resize(new_size, Image.ANTIALIAS)
        delta_w = desired_size - new_size[0]
        delta_h = desired_size - new_size[1]
        padding = (delta_w//2, delta_h//2, delta_w-(delta_w//2), delta_h-(delta_h//2))
        show_img = ImageOps.expand(show_img, padding)
        show_img = show_img.crop((0, 0, desired_size, desired_size))
        # show_img.save("./test.png")
        label_img = ImageTk.PhotoImage(show_img)
        img_widget.image = label_img
        img_widget.config(image=label_img)

    def update_vsait_loc(self,loc):
        self.vsait_loc = loc

    def copy_to_dest(self):
        if self.vsait_loc is None:
            tkinter.messagebox.showinfo('Error','Style Trasnfer Location Not Selected!')
            return
        dest_target_style_loc = os.path.join(self.vsait_loc,"data","target","train")
        dest_source_content_loc = os.path.join(self.vsait_loc,"data","source","train")
        check_make_folder(dest_source_content_loc)
        check_make_folder(dest_target_style_loc)
        # first do content
        idx = 0
        source_fldr = self.content_txt.get()
        png_files = glob.glob(f"{source_fldr}/*.png")
        sty_png_files = glob.glob(f"{self.style_txt.get()}/*.png")
        count = len(png_files) + len(sty_png_files)
        for pngfile in glob.iglob(os.path.join(source_fldr, "*.png")):
            shutil.copy(pngfile, dest_source_content_loc)
            perc = int(idx*100 / count)
            self.progress["value"] = perc
            self.progress.update()
            self.content_count.config(text="{} image(s)".format(idx))
            idx += 1
        for sty_png_file in glob.iglob(os.path.join(self.style_txt.get(), "*.png")):
            shutil.copy(sty_png_file, dest_target_style_loc)
            perc = int(idx*100 / count)
            self.progress["value"] = perc
            self.progress.update()
            self.style_count.config(text="{} image(s)".format(idx))
            idx += 1
        self.start_btn.config(state=NORMAL)

    def start_train(self):
        pyenv = get_curr_python()
        train_name = self.train_name_txt.get()
        if len(train_name) == 0 or train_name in "Enter name for this weight":
            train_name = datetime.now().strftime("%Y%m%d-%H%M%S")
        if pyenv is None:
            tkinter.messagebox.showerror("Something went wrong: start_eval()->conda python bin not found")
            return
        test_command = "cd {} ; {} train.py --name {}"\
            .format(self.vsait_loc, pyenv, train_name)
        try:
            # Training might takes days, depending the dataset size.\n
            top = make_top_wdnw("Training might takes days, depending the dataset size. \nThis window will close itself when done.")
            res = subprocess.check_output(test_command,shell=True)
            top.destroy()
            tkinter.messagebox.showinfo(title="ckpt Location",message=os.path.join(self.vsait_loc,"checkpoints",train_name,"version_0","checkpoints"))
        except Exception as e:
            print(e)