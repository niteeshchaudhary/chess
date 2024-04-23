import os
import selector
import pyautogui as pg
import numpy as np
import os
import cv2
from tkinter import *
from tkinter import messagebox
import time
from  tokens_2 import Rook, Knight, Bishop, Queen, King, Pawn

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
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(main_image, pt, (pt[0] + w-3, pt[1] + h), (0,0,255), 2)
    #     break
    return loc,w,h


class Game:
    def __init__(self):
        self.cur_locations=[[None for i in range(8)] for j in range(8)]
        self.board_data=[[None for i in range(8)] for j in range(8)]
        self.bl=0
        self.bt=0
        self.blkw=0
        self.blkh=0
        self.token_folder_path = "tokens_images"
        self.screenshot = None

    def play(self):
            self.screenshot = pg.screenshot()
            self.screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
            board=""
            folder_path = "boardimages"
            
            num_files = len(os.listdir(folder_path))

            for regi in range(1, num_files+1):
                try:
                    board,w,h = locate_image(self.screenshot,f'./{folder_path}/{regi}.png')
                    if board:
                        board = Obj2(board,w,h)
                        break
                except:
                    pass

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
                print(board)
                cntgc=0
                errv = 4
                errw = 1
                bh = board.height
                bw = board.width
                self.bl = board.left
                self.bt = board.top
                self.blkh = (bh - errv) // 8
                self.blkw = (bw - errw) // 8
                cv2.rectangle(
                    self.screenshot,
                    (self.bl, self.bt),
                    (self.bl + bw, self.bt + bh),
                    (255, 255, 0),
                    3)
                
                i = 0
                # num_token_files = len(os.listdir(token_folder_path))
                self.board_data=[[None for i in range(8)] for j in range(8)]
                lst=[]
                nslst=[]
                cnt=0
                while i < 8:
                    for ind in range(8):
                        if i == 0:
                            pg.click(self.bl, self.bt)

                        # print(ind)
                        sub_image = self.screenshot[self.bt + self.blkh * i: self.bt + self.blkh * i + self.blkh,self.bl + self.blkw * ind: self.bl + self.blkw * ind + self.blkw]
                        self.cur_locations[i][ind]=((self.bl + self.blkw * ind+ self.bl + self.blkw * ind + self.blkw)//2,(self.bt + self.blkh * i+self.bt + self.blkh * i + self.blkh)//2)
                        cv2.circle(
                            self.screenshot,
                            self.cur_locations[i][ind],
                            2,
                            (255, 0, 0),3)
                        
                        
                        cv2.rectangle(
                            self.screenshot,
                            (self.bl + self.blkw * ind, self.bt + self.blkh * i),
                            (self.bl + self.blkw * ind + self.blkw, self.bt + self.blkh * i + self.blkh),
                            (255, 0, 255),3)
                        
                        
                        for regi in os.listdir(self.token_folder_path):
                            token=""
                            try:
                                token,w,h=locate_image(sub_image, f'./{self.token_folder_path}/{regi}')
                                if token:
                                    cnt+=1
                                    myobj=regi.split("_")
                                    #print(eval(f"{myobj[0]}('{myobj[1]}')"))
                                    self.board_data[i][ind]=eval(f"{myobj[0]}('{myobj[1]}')")
                                    # print(cnt,f'./{self.token_folder_path}/{regi}')
                                    for pt in zip(*token[::-1]):
                                        # cv2.rectangle(sub_image, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
                                        cv2.putText(sub_image, regi, pt,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), 1)
                                        break
                                    token=regi
                                    break
                                # 3)
                                # token=regi
                            except Exception as e:
                                print("error",cnt,f'./{self.token_folder_path}/{regi}')
                                print(e)
                                token="*"
                                pass

                        
                    # lst.append(nslst)
                    i += 1

                # cv2.imshow("scrn",self.screenshot)
                #     # #smelt
                # cv2.waitKey(0)
                return self.board_data,self.cur_locations
                

                
                # for i in range(8):
                #     print(self.board_data[i])
            else:
                return None,None

    def read_board(self):
        self.screenshot = pg.screenshot()
        self.screenshot = cv2.cvtColor(np.array(self.screenshot), cv2.COLOR_RGB2BGR)
        i = 0
        # num_token_files = len(os.listdir(token_folder_path))
        self.board_data=[[None for i in range(8)] for j in range(8)]
        lst=[]
        nslst=[]
        cnt=0
        while i < 8:
            for ind in range(8):

                sub_image = self.screenshot[self.bt + self.blkh * i: self.bt + self.blkh * i + self.blkh,self.bl + self.blkw * ind: self.bl + self.blkw * ind + self.blkw]
                
                
                for regi in os.listdir(self.token_folder_path):
                    token=""
                    try:
                        token,w,h=locate_image(sub_image, f'./{self.token_folder_path}/{regi}')
                        if token:
                            cnt+=1
                            myobj=regi.split("_")
                            #print(eval(f"{myobj[0]}('{myobj[1]}')"))
                            self.board_data[i][ind]=eval(f"{myobj[0]}('{myobj[1]}')")
                            # print(cnt,f'./{self.token_folder_path}/{regi}')
                            for pt in zip(*token[::-1]):
                                cv2.rectangle(sub_image, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)
                                cv2.putText(sub_image, regi, pt,cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,0,0), 1)
                                break
                            token=regi
                            break
                        # 3)
                        # token=regi
                    except Exception as e:
                        print("error",cnt,f'./{self.token_folder_path}/{regi}')
                        print(e)
                        token="*"
                        pass
                
            # lst.append(nslst)
            i += 1

        # cv2.imshow("scrn",self.screenshot)
        #             # #smelt
        # cv2.waitKey(0)
        return self.board_data

class Obj:
    def __init__(self,b_inf):
        self.top=b_inf[1]
        self.left=b_inf[0]
        self.width=b_inf[2]-b_inf[0]
        self.height=b_inf[3]-b_inf[1]

class Obj2:
    def __init__(self,board,w,h):
        lst=list(zip(*board[::-1]))
        self.top=lst[0][1]
        self.left=lst[0][0]
        self.width=w
        self.height=h
    
    

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

