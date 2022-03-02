import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import QUESTION
from PIL import ImageTk, Image
from Files import get_file
import os
from pathlib import Path
import torch
from torchvision import transforms,models
from Mod2017 import *
from transformers import BertTokenizer, BertModel
# this is a function to get the user input from the text input box
ROOT = os.getcwd()
ROOT = Path(ROOT)
if os.path.basename(ROOT) == 'src':
    ROOT = ROOT.parent
ASSETS  = str(ROOT)+'/assets/'
MODELS = str(ROOT)+'/models/'
SAMPLE_IMAGES = ASSETS+'test_images/'
SAMPLE_QUESTIONS = ASSETS+'questions/'
BACKGROUND_IMAGE  = ASSETS+'background.jpeg'
MAX_SENTENCE_LEN = 25
EMBED_DIM = 768
_transform = transforms.Compose([transforms.Resize(256),
                                      transforms.CenterCrop(224),
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

class GUI : 
    def __init__(self) -> None:
        #Setting up the main window 
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased',
                                                    do_lower_case=True)
        self.bert_model = BertModel.from_pretrained('bert-base-uncased')
            # resnet = models.resnet101(pretrained=True)
            # self._resnet_conv = nn.Sequential(*list(resnet.children())[:-2])
        self.embeddings = self.bert_model.get_input_embeddings()
        self.resnet = models.resnet101(pretrained=True)
        self.res101_conv = nn.Sequential(*list(self.resnet.children())[:-2])
        main_image = None
        self.window = tk.Tk()
        self.window.configure(background="White")
        self.window=self.window
        self.window.title('VQA model demonstration')
        self.window_height = 500
        self.window_width = 900

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.window_height/2))

        self.window.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_cordinate, self.y_cordinate))
        self.window.resizable(False,False)
        self.window.iconbitmap(str(ROOT)+'/assets/vqa_icon.ico')

        #background image
        self.image = Image.open(BACKGROUND_IMAGE)
        self.image= self.image.resize((900,500), Image.ANTIALIAS)
        self.image  = ImageTk.PhotoImage(self.image)
        self.l = tk.Label(self.window)
        self.l.place(x=0, y=0, relwidth=1, relheight=1) # make label l to fit the parent window always
        self.l.image = self.image
        self.l.config(image=self.l.image)


        #Setting up the widgets
        self.image_widgets = list()
        #label 1 
        self.label = ttk.Label(self.window)
        self.label['text'] = "Hello there"
        # label.pack()

        #image panel
        self.img_panel = ttk.Label(self.window)
        # img_panel.pack()

        #sample images dropdown menu
        self.images = os.listdir(SAMPLE_IMAGES)
        self.parsed_images = list()
        for im in self.images:
            name = im.split(".")[0]
            self.parsed_images.append(name.capitalize() )
        self.clicked = StringVar()
        # clicked.set( "Test images" )
        self.drop =ttk.OptionMenu(self.window ,self.clicked ,"Test Images",*self.parsed_images,command = lambda _: self.image_menu_change())
        # drop['defulat'] ="Test images"
        # drop['defualt']
        # drop['values']=parsed_images
        # drop['command'] = lambda: image_menu_change(window,drop,img_panel,image_widgets)

        #load image button
        self.load_img_btn = ttk.Button(self.window)
        self.load_img_btn['text'] = 'Load Image'
        self.load_img_btn['command'] = self.load_image_click
        # load_img_btn.pack()

        #question entry box
        self.question_box = ttk.Entry(self.window)
        self.question_box['width']=100
        self.question_box.insert(0,"Ask me anything!")
        self.image_widgets.append((self.question_box,1,1))
        # question_box.pack()

        #answer label 
        self.answer_lbl = ttk.Label(self.window)
        self.answer_lbl['text'] = ""
        self.image_widgets.append((self.answer_lbl,3,1))

        # answer_lbl.pack() # need to move it down so the button is above the label

        #answer button 
        self.answer_btn = ttk.Button(self.window)
        self.answer_btn['text'] = "Answer me"
        self.answer_btn['command'] = lambda  : self.answer_click()
        self.image_widgets.append((self.answer_btn,2,1))
        # answer_btn.pack()

        #model selection combo box 
        self.models_list = self.get_all_models()
        self.load_models()
        self.model_cb = ttk.Combobox(self.window)
        self.model_cb['state'] = 'readonly'
        self.model_cb.set("Pick a model") 
        self.model_cb['values'] = [model[0] for model in self.models_list]
        # model_cb.pack()



        self.load_img_btn.grid(row=2, column=0, pady=5)
        self.model_cb.grid(row = 0 , column = 0, pady=5,padx=5)
        self.drop.grid(row=1,column=0, pady=5,padx=5)
        self.window.mainloop()
    def change_image_panel(self,file):
        if file:
            image = Image.open(file).convert('RGB')
            self.cur_image_tensor =torch.unsqueeze(_transform(image),0)
            image= image.resize((224,224), Image.ANTIALIAS)
            image  = ImageTk.PhotoImage(image)
            self.img_panel['image'] = image
            self.img_panel.grid(row=0 , column=1)
            for widget in self.image_widgets:
                widget[0].grid(row = widget[1], column =widget[2])
            self.window.mainloop()
            return True
        return False
    def load_image_click(self):
        file = get_file("Please select an image",filetype=[("png images","*.png")])
        if self.change_image_panel(file):
            self.clicked.set("Test images")
            self.question_box.delete(0,END)
            self.question_box.insert(0,"Ask me anything!")
            self.window.mainloop()
    def image_menu_change(self):
        selection = self.clicked.get()
        filename = str(selection).lower()
        imgname = filename+".png"
        image_path = SAMPLE_IMAGES+imgname
        question_path = SAMPLE_QUESTIONS+filename+".txt"
        f = open(question_path, "r")
        question = f.readlines()[0]
        f.close()
        self.question_box.delete(0,END)
        self.question_box.insert(0,question)
        self.change_image_panel(image_path)
        self.window.mainloop()
    def answer_click(self):
        input = self.question_box.get()
        model = self.model_cb.get()
        model = self.loaded_models_dict[str(model)]
        # print(self.loaded_models_dict)
        model.eval()
        # print(self.cur_image_tensor)
        image_tensor = self.res101_conv(self.cur_image_tensor)
        if(image_tensor.size(0)!=49):
            image_tensor = image_tensor.squeeze(0)
            image_tensor = image_tensor.view(image_tensor.size(0),image_tensor.size(1)*image_tensor.size(2))
            image_tensor = image_tensor.permute(1,0)
            image_tensor = torch.unsqueeze(image_tensor,0)
        question_tesnor = torch.unsqueeze(self.sentence_embedding(input),0)
        # print(image_tensor.shape,question_tesnor.shape)
        output = model(question_tesnor,image_tensor).squeeze()
        max_val = max(output.tolist())
        max_index = output.tolist().index(max_val)
        answer_string =""
        if max_index==0:
            answer_string = "No"
        else:
            answer_string= "Yes"
        self.answer_lbl['text']= "The answer for "+'" '+input+' "'+" is: "+answer_string
    def get_all_models(self,models_root_dir = "/models/"):
        models_list = list()
        for file in os.listdir(str(ROOT)+models_root_dir):
            if file.endswith(".nyp"): #change .txt to .nyp when you have the models...
                models_list.append((file.split(".")[0],str(ROOT)+models_root_dir+file))
        return models_list
    def load_models(self):
        self.loaded_models_dict = dict()
        for model in self.models_list:
            model_path =str(model[1])
            my_model = eval(model[0])()
            my_model.load_state_dict(torch.load(str(model_path)),strict = True)
            self.loaded_models_dict[model[0]] = my_model
    def sentence_embedding(self,sentence: str):
        input_ids = torch.tensor(self.tokenizer.encode(sentence))
        embeddings2 = self.embeddings(input_ids)
        pad_len = MAX_SENTENCE_LEN - len(embeddings2)
        padding = torch.zeros(pad_len, EMBED_DIM)
        embeddings2 = torch.cat((embeddings2, padding), dim=0)
        return embeddings2


GUI()