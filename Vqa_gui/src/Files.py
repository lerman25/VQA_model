import tkinter as tk
from tkinter import filedialog
import time
from datetime import datetime

def get_file(title = "Please select a file:", filetype = None):
    root = tk.Tk()
    root.withdraw()
    if filetype:
        xl_file_path = filedialog.askopenfilename(title=title,filetypes=filetype)
    else:
        xl_file_path = filedialog.askopenfilename(title=title)
    return xl_file_path
def get_folder(title= "Please select a Directory:"):
    root = tk.Tk()
    root.withdraw()
    folder_path = filedialog.askdirectory(title= title)
    return folder_path   
def write_list_to_file(list,file):
    with open(file, 'w') as f:
        for item in list:
            f.write("%s\n" % item)
def now_file_format():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    return dt_string