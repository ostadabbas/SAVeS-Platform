from tkinter import *
from tkinter import filedialog as fd

def set_entry_txt(entry_widget,txt):
    entry_widget.delete(0,END)
    entry_widget.insert(0,txt)

def browse_folder(show_widget,start_dir=r"."):
    filepath=fd.askdirectory(initialdir=start_dir,title="Select Folder")
    if type(filepath) is tuple:
        if len(filepath) == 0:
            filepath = "."
        else:
            filepath = filepath[0]
    show_widget.delete(0,END)
    show_widget.insert(0,filepath)
    return filepath

def browse_file(show_widget,ext_desc,ext,start_dir='~/Downloads'):
    filetypes = ((ext_desc, "*.{}".format(ext)),)
    filename = fd.askopenfilename(title=ext_desc,initialdir=start_dir,filetypes=filetypes)
    show_widget.delete(0,END)
    show_widget.insert(0,filename)
    return filename
