import os
import selector
import pyautogui as pg
import numpy as np
import os
import cv2
from tkinter import *
from tkinter import messagebox
import time

import cv2
import numpy as np

def locate_image(main_image_path, template_image_path):
    # Read the main image and the template image
    main_image = main_image_path
    template_image = cv2.imread(template_image_path)

    # Convert images to grayscale
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # Get the dimensions of the template image
    w, h = template_gray.shape[::-1]

    # Perform template matching
    res = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8  # Adjust threshold as needed
    loc = np.where(res >= threshold)

    if loc[0].size == 0:
        return None, None, None
    # Draw rectangles around the matched regions
    for pt in zip(*loc[::-1]):
        cv2.rectangle(main_image, pt, (pt[0] + w-3, pt[1] + h), (0,255,0), 2)
    return loc,w,h




class Game:

    def play(self):
            screenshot = pg.screenshot()
            screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            board=""
            folder_path = "boardimages"
            token_folder_path = "tokens_images"
            num_files = len(os.listdir(folder_path))

            for regi in range(1, num_files+1):
                try:
                    board,_,_ = locate_image(screenshot,f'./{folder_path}/{regi}.png')
                    if board:
                        break
                except:
                    pass
            cv2.imshow("scrn",screenshot)
                    # #smelt
            cv2.waitKey(0)
            return
            exe = ''
            roi = ""
            if not board:
                print("please choose the correct region")
                b_inf = list(map(int, selector.getSelection()))
                print(b_inf)
                if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                    menu()
                sc = pg.screenshot()
                roi = sc.crop(b_inf)
                roi.save(f"./{folder_path}/{num_files + 1}.png")
                board = Obj(b_inf)

            prev = ""
            if board:
                cntgc=0
                errv = 4
                errw = 1
                bh = board.height
                bw = board.width
                bl = board.left
                bt = board.top
                blkh = (bh - errv) // 8
                blkw = (bw - errw) // 8
                cv2.rectangle(
                    screenshot,
                    (bl, bt),
                    (bl + bw, bt + bh),
                    (255, 255, 0),
                    3)
                i = 0
                # num_token_files = len(os.listdir(token_folder_path))
                lst=[]
                nslst=[]
                cnt=0
                while i < 8:
                    
                    for ind in range(8):
                        if i == 0:
                            pg.click(bl, bt)

                        # print(ind)
                        sub_image = screenshot[bt + blkh * i: bt + blkh * i + blkh,bl + blkw * ind: bl + blkw * ind + blkw]
                        
                        
                        cv2.rectangle(
                            screenshot,
                            (bl + blkw * ind, bt + blkh * i),
                            (bl + blkw * ind + blkw, bt + blkh * i + blkh),
                            (255, 0, 255),3)
                        
                        
                        for regi in os.listdir(token_folder_path):
                            token=""
                            try:
                                token,w,h=locate_image(sub_image, f'./{token_folder_path}/{regi}')
                                if token:
                                    cnt+=1
                                    print(cnt,f'./{token_folder_path}/{regi}')
                                    for pt in zip(*token[::-1]):
                                        cv2.rectangle(sub_image, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
                                        cv2.putText(sub_image, regi, pt,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), 1)
                                    token=regi
                                    break
                                # 3)
                                # token=regi
                            except Exception as e:
                                print("error",cnt,f'./{token_folder_path}/{regi}')
                                print(e)
                                token="*"
                                pass

                    # lst.append(nslst)
                    i += 1

                # for row in range(8):
                #     for col in range(8):
                #         for regi in os.listdir(token_folder_path):
                #             token=""
                #             try:
                #                 locate_image(main_image_path, template_image_path)
                #                 token = pg.locateOnScreen(f'./{token_folder_path}/{regi}')
                #                 cv2.rectangle(
                #                 screenshot,
                #                 (token.left, token.top),
                #                 (token.left + token.width, token.top + token.height),
                #                 (255, 255, 0),
                #                 3)
                #                 token=regi
                #             except Exception as e:
                #                 # print(e)
                #                 token="*"
                #                 pass
            
                    # print(regi)
                    # try:
                    #     token_image = cv2.imread(f'./{token_folder_path}/{regi}')
                    #     token = cv2.matchTemplate(sub_image, token_image, cv2.TM_CCOEFF_NORMED) #pg.locateOnScreen(f'./{token_folder_path}/{regi}')
                    #     if token:
                    #         token=regi
                    #         break
                    # except Exception as e:
                    #     # print(e)
                    #     token="*"
                    #     pass

                    # nslst.append(token)
                cv2.imshow("scrn",screenshot)
                    # #smelt
                cv2.waitKey(0)
                print(nslst)

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

