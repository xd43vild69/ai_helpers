import tkinter
import tkinter.messagebox
import customtkinter
from Normalizer import Normalizer 
import os
import sys
import datetime
import uuid
import glob
from tkinter import filedialog
from pathlib import Path
from distutils.dir_util import copy_tree
import pathlib

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):

    LORA = ""

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Dataset helper")
        self.geometry(f"{600}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        
        gpady = 10
        gpadx = 20

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Preparation", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=0, pady=gpady)
        
        self.siderbar_loraValue = customtkinter.CTkEntry(self.sidebar_frame, placeholder_text="LoraName")
        self.siderbar_loraValue.grid(row=1, column=0, padx=gpadx, pady=gpady)

        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Normalizer 768", command=self.normalizer)
        self.sidebar_button_1.grid(row=2, column=0, padx=gpadx, pady=gpady)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Augmentation", command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=3, column=0, padx=gpadx, pady=gpady)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Captation", command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=4, column=0, padx=gpadx, pady=gpady)

        # self is the right window place

        self.labelTitle = customtkinter.CTkLabel(self, text="Calculations from source", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.labelTitle.place(x=280, y=10) 

        self.buttonl1 = customtkinter.CTkButton(self, text="Select Path", command=self.selectInputFiles)
        self.buttonl1.place(x=200, y=60)      
        self.sourceEntry = customtkinter.CTkEntry(self, placeholder_text="SourceImgs")
        self.sourceEntry.place(x=360, y=60)

        self.quantityImgs = customtkinter.CTkLabel(self, text="QuantityFiles")
        self.quantityImgs.place(x=200, y=110)
        self.quantityFiles = customtkinter.CTkEntry(self, placeholder_text="QuantityFiles")
        self.quantityFiles.place(x=360, y=110)

        self.repeatition = customtkinter.CTkLabel(self, text="Repets")
        self.repeatition.place(x=200, y=160)
        self.quantityRepeatition = customtkinter.CTkEntry(self, placeholder_text="Repets")
        self.quantityRepeatition.place(x=360, y=160)

        self.epochs = customtkinter.CTkLabel(self, text="Epochs")
        self.epochs.place(x=200, y=210)
        self.quantityEpochs = customtkinter.CTkEntry(self, placeholder_text="Epochs")
        self.quantityEpochs.place(x=360, y=210)

        self.batchSize = customtkinter.CTkLabel(self, text="batchSize")
        self.batchSize.place(x=200, y=260)
        self.quantityBatchSize = customtkinter.CTkEntry(self, placeholder_text="BatchSize")
        self.quantityBatchSize.place(x=360, y=260)

        self.totalTrain = customtkinter.CTkLabel(self, text="totalTrain")
        self.totalTrain.place(x=200, y=310)
        self.quantityTotalTrain = customtkinter.CTkEntry(self, placeholder_text="totalTrain")
        self.quantityTotalTrain.place(x=360, y=310)

        self.buttonRecalculate = customtkinter.CTkButton(self, text="Calculation", command=self.recalculate)
        self.buttonRecalculate.place(x=200, y=360)

        self.buttonCreateStructure = customtkinter.CTkButton(self, text="Create Structure", command=self.createStructure)
        self.buttonCreateStructure.place(x=360, y=360)

        self.buttonClean = customtkinter.CTkButton(self, text="Clean", command=self.cleanFiles)
        self.buttonClean.place(x=200, y=410)        

    def sidebar_button_event(self):
        print("sidebar_button click")

    def normalizer(self):
        if (self.validationName()):
            normalizer = Normalizer(self.siderbar_loraValue.get())
        return
    
    def open_input_dialog_normalize_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type lora name:", title="Normalizer")
        print("Normalizer:", dialog.get_input())

    def selectInputFiles(self):
        if (self.validationName()):
            
            self.LORA = self.siderbar_loraValue.get()

            dir_path = filedialog.askdirectory(title="Select input directory")
            quantity_imgs = self.countFiles(dir_path) / 2

            if quantity_imgs <= 0:
                print("Empty folder")
                return

            self.labelTitle.configure(text = f'Source : {os.path.basename(dir_path)}')

            self.sourceEntry.insert(0,dir_path)    
            self.quantityFiles.insert(0, quantity_imgs)
            self.quantityEpochs.insert(0, 1)
            self.quantityBatchSize.insert(0, 2)
            self.quantityRepeatition.insert(0, 20)
            totalCalculation = quantity_imgs * 1 * 20 / 2
            self.quantityTotalTrain.insert(0, totalCalculation)
        return

    def countFiles(self, dir_path):
        count = 0
        for path in os.listdir(dir_path):
            if os.path.isfile(os.path.join(dir_path, path)):
                count += 1
        return count
    
    def recalculate(self):
        self.quantityTotalTrain.delete(0, tkinter.END)
        self.totalCalculation = float(self.quantityFiles.get()) * int(self.quantityEpochs.get()) * int(self.quantityRepeatition.get()) / int(self.quantityBatchSize.get())
        self.quantityTotalTrain.insert(0, self.totalCalculation)

    def cleanFiles(self):
        self.sourceEntry.delete(0, tkinter.END)
        self.quantityFiles.delete(0, tkinter.END)
        self.quantityEpochs.delete(0, tkinter.END)
        self.quantityBatchSize.delete(0, tkinter.END)
        self.quantityRepeatition.delete(0, tkinter.END)
        self.quantityTotalTrain.delete(0, tkinter.END)
        self.labelTitle.configure(text = f'Lora Helper :')
        return

    def createStructure(self):
        path_dir = Path(self.sourceEntry.get())
        baseName = os.path.basename(path_dir)

        if not os.path.exists(f'{path_dir.parent.absolute()}\lora_{baseName}'):
            os.makedirs(f'{path_dir.parent.absolute()}\lora_{self.LORA}')
            os.makedirs(f'{path_dir.parent.absolute()}\lora_{self.LORA}\image')
            os.makedirs(f'{path_dir.parent.absolute()}\lora_{self.LORA}\log')
            os.makedirs(f'{path_dir.parent.absolute()}\lora_{self.LORA}\model')
            os.makedirs(f'{path_dir.parent.absolute()}\lora_{self.LORA}\image\{self.quantityRepeatition.get()}_{self.LORA}')
            copy_tree(self.sourceEntry.get(), f'{path_dir.parent.absolute()}\lora_{self.LORA}\image\{self.quantityRepeatition.get()}_{self.LORA}')
            self.createLog(f'{path_dir.parent.absolute()}\lora_{self.LORA}')
            self.createConfigJson()
            self.setKeywordLora()
        else:
            print("Folder already exists")
        return

    def createLog(self, path):
                
        file_name = f'{path}\log-{datetime.date.today()}_{uuid.uuid4()}.txt'
        text1 = F'quantity files: {self.quantityFiles.get()}, quantity epochs: {self.quantityEpochs.get()}, quantity batch size: {self.quantityBatchSize.get()}, quantity repeats: {self.quantityRepeatition.get()}, total calculation: {self.quantityTotalTrain.get()}'

        with open(file_name, 'w') as file:
            file.write(text1)
        return

    def createConfigJson(self):    
        path_dir = Path(self.sourceEntry.get())

        with open('LoraD13.json', 'r') as file:
            # read a list of lines into data
            data = file.readlines()

        logging_dir = f'  \"logging_dir\":\"{path_dir.parent.absolute()}\\lora_{self.LORA}\\log", '
        output_dir =  f'  \"output_dir\":\"{pathlib.PureWindowsPath(path_dir.parent.absolute())}\\lora_{self.LORA}\\model", '
        train_data_dir =  f'  \"train_data_dir\":\"{pathlib.PurePath(path_dir.parent.absolute())}\\lora_{self.LORA}\\image", '
        output_lora = f'  \"output_name\":\"{self.LORA}", '
        sample_prompts = f'  \"sample_prompts\":\"{self.getInitialPrompt()}", '

        data[32] = r"" + logging_dir.replace("\\", "\\\\") + "\n"
        data[59] = r"" + output_dir.replace("\\", "\\\\") + "\n"
        data[60] = r"" + output_lora.replace("\\", "\\\\") + "\n"
        data[86] = r"" + train_data_dir.replace("\\", "\\\\") + "\n"        
        data[70] = sample_prompts + "\n"

        if not os.path.exists(f'{path_dir.parent.absolute()}\\lora_{self.LORA}\\lora_config_{self.LORA}.json'):
            with open(f'{path_dir.parent.absolute()}\\lora_{self.LORA}\\lora_config_{self.LORA}.json', 'w') as file:
                file.writelines( data )
        return
    
    def setKeywordLora(self):
        path_dir = Path(self.sourceEntry.get())

        path_init = f'{path_dir.parent.absolute()}\lora_{self.LORA}\image\{self.quantityRepeatition.get()}_{self.LORA}'

        files = glob.glob(path_init + "\\*.txt")
        data = ""
        for file in files:
            with open(file, 'r') as f:
                data = f.readlines()
            dataAlteration = self.LORA + ", " + data[0]
            with open(file, 'w', encoding='utf-8') as f:
                f.write(dataAlteration)

        return           

    def getInitialPrompt(self):
        path_dir = Path(self.sourceEntry.get())        

        path_init = f'{path_dir.parent.absolute()}\lora_{self.LORA}\image\{self.quantityRepeatition.get()}_{self.LORA}'

        files = glob.glob(path_init + "\\*.txt")

        data = ""
        with open(files[0], 'r') as file:
            data = file.readlines()[0][:-2]
        return data        
    
    def validationName(self):
        if (self.siderbar_loraValue.get() == ""):
            print("No lora name defined")
            return False
        else:
            return True


if __name__ == "__main__":
    app = App()
    app.mainloop()