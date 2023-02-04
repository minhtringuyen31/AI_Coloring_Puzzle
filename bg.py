from tkinter import *
from tkinter import filedialog
import numpy as np
from PIL import Image, ImageTk
from variable import board
from agent import XAT
from setting import* 
import time
import sys
import os


class Background(Frame):

    def __init__(self, window):
        Frame.__init__(self, window)
        window.title("Coloring Puzzle")
        window.geometry("1200x700")
        self.image = ImageTk.PhotoImage(Image.open(self.path(BG_IMAGE)))
        self.image_label = Label(window, image=self.image, bg= '#10c4e8')
        self.image_label.place(x=0,y=0)
        self.Draw_Button(window)
        self.window = window
        self._boardInput = None

    def Load_File(self): # load file from your test case in your computer
        self.time.configure(textvariable=0)
        self.filename = filedialog.askopenfilename(
            initialdir="/", title="Select A File", filetype=(('text files', 'txt'), ("all files", "*.*")))
        self.path_file.set(self.filename)
        self.label.configure(textvariable=self.path_file)
        openFile = open(self.filename, 'r')
        lines = openFile.readline().strip()
        lines = openFile.readlines()
        lines_int = [list(map(int, line.strip().split(' '))) for line in lines]
        self.boardInput = np.array(lines_int)
        self._board = board(self.window, self.boardInput)
        self.__xat = XAT(self._board)
        self.__xat.buildKB()

    
    def Draw_Button(self, window): # Draw button , text on tkinter creen
        self.labelFrame = Label(window, text='Choose file', font=('Pursia', 11),fg='#310470')
        self.labelFrame.place(x=710, y=240,height=30)
        
        self.path_file = StringVar(value='')
        self.label = Entry(window, textvariable=self.path_file,width=35, font=('Pursia', 11),fg='#310470')
        self.label.place(x=800, y=240,height=30)

        self.button = Button(window, text="Browse",command=self.Load_File, font=('Pursia', 11),fg='#310470')
        self.button.place(x=1110 , y=240,height=30)

        self.value_options = {'PySAT': '1', 'A Star': '2','Brute Force': '3', 'Backtracking': '4'}
        self.getAlgo = StringVar(window, '1')
        self.labelFrame = Label(window, text='Algorithms', font=('Pursia', 11),fg='#310470')
        self.labelFrame.place(x=710, y=300,height=30)
        i = 1
        for (text, value) in self.value_options.items():
            Radiobutton(window, text=text, variable=self.getAlgo,value=value,fg='#310470',font=('Pursia', 9)).place(x=(97 * i) + 700, y=300,height=30,width= 96)
            i += 1
        self.start_button = Button( window, text="Start", width=12, font=('Pursia', 11),command= self.Choose_Algorithms,fg='#310470')
        self.start_button.place(x=895, y=400,height=30)
  
        #Time 
        self.running_time = StringVar(window, 0)
        self.timeFrame = Label(window, text='Time', font=('Pursia', 11),fg='#310470')
        self.timeFrame.place(x=710, y=350,height=30,width= 70)
        self.time = Entry(window, textvariable=self.running_time,width=40, font=('Pursia', 11),fg='#310470')
        self.time.place(x=800, y=350,height=30)
    

        

    def Choose_Algorithms(self):
        if self.getAlgo.get() == '1':
            Time_Start = time.time()
            self.time.configure(textvariable='Running')
            self.result = self.__xat.usePySAT()
            print ("OutPut:")
            print(np.array(self._board.toLogicMatrix()))
            Time_End = time.time()
            self.running_time.set(Time_End - Time_Start)
            self.time.configure(textvariable=self.running_time)
            self.drawPuzzel()
        elif self.getAlgo.get() == '2':
            t0 = time.time()
            self.time.configure(textvariable='Running')
            self.result = self.__xat.useAStar()
            t1 = time.time()
            self.running_time.set(t1 - t0)
            self.time.configure(textvariable=self.running_time)
            print(np.array(self._board.toLogicMatrix()))
            self.drawPuzzel()
        elif self.getAlgo.get() == '3':
            Time_Start = time.time()
            self.time.configure(textvariable='Running')
            self.result = self.__xat.useBruceForce()
            print ("OutPut:")
            print(np.array(self._board.toLogicMatrix()))
            Time_End = time.time()
            self.running_time.set(Time_End - Time_Start)
            self.time.configure(textvariable=self.running_time)
            self.drawPuzzel()
        elif self.getAlgo.get() == '4':
            Time_Start = time.time()
            self.time.configure(textvariable='Running')
            self.result = self.__xat.useBackTracking()
            print ("OutPut:")
            print(np.array(self._board.toLogicMatrix()))
            Time_End = time.time()
            self.running_time.set(Time_End - Time_Start)
            self.time.configure(textvariable=self.running_time)
            self.drawPuzzel()

    def drawPuzzel(self):
        self._board.draw()


# Load picture background
    @staticmethod
    def path(file_name):
        file_name = 'assets\\' + file_name
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".") 

        return os.path.join(base_path, file_name) 