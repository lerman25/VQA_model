from sre_constants import ASSERT
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
ASSETS  = str(ROOT)+'/assets/'
SAMPLE_IMAGES = ASSETS+'test_images/'
SAMPLE_QUESTIONS = ASSETS+'questions/'
BACKGROUND_IMAGE  = ASSETS+'background.jpeg'
main_image = None
def change_image_panel(root,file,img_panel,widgets):
    if file:
        image = Image.open(file)
        image= image.resize((224,224), Image.ANTIALIAS)
        image  = ImageTk.PhotoImage(image)
        img_panel['image'] = image
        img_panel.grid(row=0 , column=1)
        for widget in widgets:
            widget[0].grid(row = widget[1], column =widget[2])
        root.mainloop()
        return True
    return False

def load_image_click(root,img_panel,widgets,clicked):
    file = get_file("Please select an image",filetype=[("png images","*.png")])
    if change_image_panel(root,file,img_panel,widgets):
        clicked.set("Test images")
def image_menu_change(root,drop_menu,img_panel,widgets):
    selection = drop_menu.get()
    filename = str(selection).lower()
    imgname = filename+".png"
    image_path = SAMPLE_IMAGES+imgname
    question_path = SAMPLE_QUESTIONS+filename+".txt"
    f = open(question_path, "r")
    question = f.readlines()[0]
    f.close()
    entry_box = ttk.Entry(root)
    entry_box['width']=100
    entry_box.delete(0,END)
    entry_box.insert(0,question)
    new_tup = (entry_box,widgets[0][1],widgets[0][2])
    widgets[0]=new_tup
    change_image_panel(root,image_path,img_panel,widgets)
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

#background image
image = Image.open(BACKGROUND_IMAGE)
image= image.resize((900,500), Image.ANTIALIAS)
image  = ImageTk.PhotoImage(image)
l = tk.Label(root)
l.place(x=0, y=0, relwidth=1, relheight=1) # make label l to fit the parent window always
l.image = image
l.config(image=l.image)


#Setting up the widgets
image_widgets = list()
#label 1 
label = ttk.Label(root)
label['text'] = "Hello there"
# label.pack()

#image panel
img_panel = ttk.Label(root)
# img_panel.pack()

#sample images dropdown menu
images = os.listdir(SAMPLE_IMAGES)
parsed_images = list()
for im in images:
    name = im.split(".")[0]
    parsed_images.append(name.capitalize() )
clicked = StringVar()
# clicked.set( "Test images" )
lambda x=None: ...
drop =ttk.OptionMenu(root ,clicked ,"Test Images",*parsed_images,command=lambda _: image_menu_change(root,clicked,img_panel,image_widgets))
# drop['defulat'] ="Test images"
# drop['defualt']
# drop['values']=parsed_images
# drop['command'] = lambda: image_menu_change(root,drop,img_panel,image_widgets)

#load image button
load_img_btn = ttk.Button(root)
load_img_btn['text'] = 'Load Image'
load_img_btn['command'] = lambda: load_image_click(root,img_panel,image_widgets,clicked)
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



load_img_btn.grid(row=2, column=0, pady=5)
model_cb.grid(row = 0 , column = 0, pady=5,padx=5)
drop.grid(row=1,column=0, pady=5,padx=5)
window.mainloop()
