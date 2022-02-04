import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
from webbrowser import get 
from Files import get_file
import os
from pathlib import Path
# this is a function to get the user input from the text input box
ROOT = os.getcwd()
ROOT = Path(ROOT)
if os.path.basename(ROOT) == 'src':
    ROOT = ROOT.parent
main_image = None
def load_image_click(root,img_panel,widgets):
    file = get_file("Please select an image",filetype=[("png images","*.png")])
    if file:
        image = tk.PhotoImage(file=file)
        img_panel['image'] = image
        img_panel.grid(row=0 , column=1)
        for widget in widgets:
            widget[0].grid(row = widget[1], column =widget[2])
        root.mainloop()
def answer_click(root,lbl,question):
    input = question.get()
    lbl['text']= "The answer for "+'" '+input+' "'+" is: "+" nothing to answer yet"
def get_all_models(models_root_dir = "/models/"):
    models_list = list()
    for file in os.listdir(str(ROOT)+models_root_dir):
        if file.endswith(".txt"): #change .txt to .nyp when you have the models...
            models_list.append((file.split(".")[0],models_root_dir+file))
    return models_list

#Setting up the main window 
window = tk.Tk()
window.configure(background="White")
root=window
window.title('VQA model demonstration')
window_height = 500
window_width = 900

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
window.resizable(False,False)
window.iconbitmap(str(ROOT)+'/assets/vqa_icon.ico')


#Setting up the widgets
image_widgets = list()
#label 1 
label = ttk.Label(root)
label['text'] = "Hello there"
# label.pack()

#image panel
img_panel = ttk.Label(root)
# img_panel.pack()

#load image button
load_img_btn = ttk.Button(root)
load_img_btn['text'] = 'Load Image'
load_img_btn['command'] = lambda: load_image_click(root,img_panel,image_widgets)
# load_img_btn.pack()

#question entry box
question_box = ttk.Entry(root)
question_box['width']=100
question_box.insert(0,"Ask me anything!")
image_widgets.append((question_box,1,1))
# question_box.pack()

#answer label 
answer_lbl = ttk.Label(root)
answer_lbl['text'] = ""
image_widgets.append((answer_lbl,3,1))

# answer_lbl.pack() # need to move it down so the button is above the label

#answer button 
answer_btn = ttk.Button(root)
answer_btn['text'] = "Answer me"
answer_btn['command'] = lambda: answer_click(root,answer_lbl,question_box)
image_widgets.append((answer_btn,2,1))
# answer_btn.pack()

#model selection combo box 
models_list = get_all_models()
model_cb = ttk.Combobox(root)
model_cb['state'] = 'readonly'
model_cb.set("Pick a model") 
model_cb['values'] = [model[0] for model in models_list]
# model_cb.pack()

model_cb.grid(row = 0 , column = 0, pady=5,padx=5)
load_img_btn.grid(row=1, column=0, pady=5)

window.mainloop()
