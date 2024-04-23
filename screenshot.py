import os
import selector
import pyautogui as pg
import numpy as np
import os
import cv2
from tkinter import *
from tkinter import messagebox
import time

class Game:

    def play(self):
            screenshot = pg.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            folder_path = "./tokens_image"
            for i in range(20):
                print("please choose the correct region")
                b_inf = list(map(int, selector.getSelection()))
                print(b_inf)
                sc = pg.screenshot()
                roi = sc.crop(b_inf)
                roi.save(f"./{folder_path}/{i + 1}.png")
                # if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                #     menu()


class Obj:
    def __init__(self,b_inf):
        self.top=b_inf[1]
        self.left=b_inf[0]
        self.width=b_inf[2]-b_inf[0]
        self.height=b_inf[3]-b_inf[1]
    
class Blockc:
    def findColor(self,img,y,x):
        b,g,r = img[y,x]
        return [int(b),int(g),int(r)]
    def isGreen(self,img,y_,x_):
        if [78,141,83]==self.findColor(self,img,y_,x_):
            return True
        return False
    def isYellow(self,img,y_,x_):
        if [59,159,181]==self.findColor(self,img,y_,x_):
            return True
        return False
    def isgrey(self,img,y_,x_):
        if [60,58,58]==self.findColor(self,img,y_,x_):
            return True
        return False
    

def startGame(ref):
    ref.destroy()
    gm = Game()
    gm.play()

def error():
    mn = Tk()
    messagebox.showerror("Error", "We faced issue in detecting grid region selected by you! Please try to select exact grid next time.")
    exit()

def menu():
    mn = Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 50, mn.winfo_screenwidth() // 2, mn.winfo_screenheight() // 2))
    button = Button(mn, text='Play', command=lambda: startGame(mn))
    button.pack(side=TOP, pady=5)
    mn.mainloop()

if __name__ == '__main__':
    menu()

