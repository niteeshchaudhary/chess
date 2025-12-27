import os
import selector
import pyautogui as pg
import numpy as np
import cv2
from tkinter import *
from tkinter import messagebox
import time

# Try to use mss for better Linux/Wayland support
try:
    import mss
    USE_MSS = True
except ImportError:
    USE_MSS = False
    print("Warning: mss not installed. Using pyautogui for screenshots (may not work on Wayland).")
    print("Install with: pip install mss")


def take_screenshot():
    """Take a screenshot using the best available method."""
    if USE_MSS:
        with mss.mss() as sct:
            # Use monitors[0] to capture ALL monitors (virtual screen)
            # This ensures coordinates from tkinter selector match the screenshot
            monitor = sct.monitors[0]  # All monitors combined
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
    else:
        screenshot = pg.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


class Game:

    def play(self):
            screenshot = take_screenshot()
            folder_path = "./tokens_image"
            for i in range(20):
                print("please choose the correct region")
                b_inf = list(map(int, selector.getSelection()))
                print(b_inf)
                sc = take_screenshot()
                # Crop using numpy array slicing: [y1:y2, x1:x2]
                roi = sc[b_inf[1]:b_inf[3], b_inf[0]:b_inf[2]]
                cv2.imwrite(f"./{folder_path}/{i + 1}.png", roi)
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

