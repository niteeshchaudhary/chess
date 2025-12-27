import time
import selector
import pyautogui as pg
import numpy as np
import os
import cv2
from tkinter import *
from tkinter import messagebox


class Game:
    def __init__(self):
        self.data = [*open("dict.txt").read().split("\n")]
        self.wd = self.data
        self.p = ['*', '*', '*', '*', '*']
        self.v = ['*', '*', '*', '*', '*']
        self.b = ""
        self.suggest = ['their', 'black', 'gowns', 'jumpy']
        print(len(self.data))

    def checker(self, wr):
        for x, i in enumerate(self.p):
            if (i != "*"):
                if (i != wr[x]):
                    return False

        for x, i in enumerate(self.v):
            if (i != "*"):
                if i not in wr:
                    return False
                elif i == wr[x]:
                    return False

        for i in wr:
            if i in self.b:
                if i in self.p or i in self.v:
                    if (self.p.count(i)+self.v.count(i)) != wr.count(i):
                        return False
                else:
                    return False
            
        return True

    def getWord(self,n=6):
        print("**",self.v,self.p.count("*"))
        if n < 4 and (10-self.p.count("*")-self.v.count("*")) < 5:
            self.wd = list(filter(lambda x: self.checker(x), self.wd))
            print(len(self.wd))
            return self.suggest[n]
        else:   
            self.wd = list(filter(lambda x: self.checker(x), self.wd))
            if len(self.wd) == 0:
                print("Word does not exists in our dictionary")
                exit()
            print(self.wd)
            return self.wd[0]


    def play(self):
        self.wd = self.data
        screenshot = pg.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        board=""
        folder_path="./boardpng"
        num_files = len(os.listdir(folder_path))
        for regi in range(1, num_files+1):
            board = pg.locateOnScreen(f'./boardpng/blk{regi}.png')
            if board:
                break
        self.b = ''
        self.p = ['*', '*', '*', '*', '*']
        roi=""
        if not board:
            print("please choose the correct region")
            b_inf = list(map(int, selector.getSelection()))
            print(b_inf)
            if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                menu()
            sc = pg.screenshot()
            roi = sc.crop(b_inf)
            roi.save(f"./boardpng/blk{num_files+1}.png")
            board = Obj(b_inf)

        stoper = 0
        prev=""
        if board:
            cntgc=0
            errv = 4
            errw = 1
            bh = board.height
            bw = board.width
            bl = board.left
            bt = board.top
            blkh = (bh - errv) // 6
            blkw = (bw - errw) // 5
            cv2.rectangle(
                screenshot,
                (bl, bt),
                (bl + bw, bt + bh),
                (255, 255, 0),
                3)
            i = 0
            while i < 6:
                
                for ind in range(5):
                    if i == 0:
                        pg.click(bl, bt)

                    print(ind)
                    cv2.rectangle(
                        screenshot,
                        (bl + blkw * ind, bt + blkh * i),
                        (bl + blkw * ind + blkw, bt + blkh * i + blkh),
                        (255, 0, 255), 3)

                wrd = self.getWord(i)
                self.v=["*","*","*","*","*"]
                if wrd == prev:
                    if roi!="": os.remove(f"./boardpng/blk{num_files+1}.png")
                    error()
                print(wrd, self.b, self.p)
                # print("->",gm.getWord())
                pg.typewrite(wrd + "\n")
                # cv2.imshow("scrn",screenshot)
                # cv2.waitKey(0)
                time.sleep(1.8) #1.7-1.8
                screenshot = pg.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                cntg = 0
                for wind in range(5):
                    b, g, r = screenshot[bt + blkh * i + 8, bl + blkw * wind + blkw // 2]
                    cv2.circle(screenshot, (bl + blkw * wind + blkw // 2, bt + blkh * i + 8), 5, (0, 0, 255), -1)
                    if [int(b), int(g), int(r)] == [59, 159, 181] or [int(b), int(g), int(r)]==[55, 194, 243]:
                        self.v[wind]=wrd[wind]
                    elif [int(b), int(g), int(r)] == [78, 141, 83] or [int(b), int(g), int(r)] == [81, 184, 121]: 
                        self.p[wind] = wrd[wind]
                        cntg += 1
                    elif [int(b), int(g), int(r)] == [60, 58, 58] or [int(b), int(g), int(r)]==[84, 64, 61]:
                        if(self.p[wind] == ''):
                            self.p[wind] = '*'
                        self.b += wrd[wind]
                    elif [int(b), int(g), int(r)] == [19, 18, 18] or [int(b), int(g), int(r)]==[43, 43, 43] or\
                            [int(b), int(g), int(r)]==[88, 87, 86] :
                        cv2.imshow("scrn", screenshot)
                        cv2.waitKey(0)
                        pg.typewrite(["backspace"] * 5)
                        i -= 1
                        print("-----------------------------")
                        screenshot = pg.screenshot()
                        stoper+=1
                        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                        if stoper>3:
                            exit(0)
                        break
                    else:
                        print("xxxxxx ",[int(b), int(g), int(r)]," xxxxxxxxxx")
                        cv2.imshow("scrn", screenshot)
                        cv2.waitKey(0)
                        error()
                        return 0
                    print("&*", self.p,self.v, self.b, i)

                if cntg >= 5:
                    return 1
                prev = wrd
                i += 1

class Obj:
    def __init__(self,b_inf):
        self.top=b_inf[1]
        self.left=b_inf[0]
        self.width=b_inf[2]-b_inf[0]
        self.height=b_inf[3]-b_inf[1]


def startGame(ref):
    ref.destroy()
    gm = Game()
    gm.play()

def error():
    mn = Tk()
    messagebox.showerror("Error", "We faced issue in detecting grid region selected by you! Please try to select exact grid next time.")
    exit()
    mn.mainloop()

def menu():
    mn = Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 50, mn.winfo_screenwidth() // 2, mn.winfo_screenheight() // 2))
    button = Button(mn, text='Solve', command=lambda: startGame(mn))
    button.pack(side=TOP, pady=5)
    mn.mainloop()

if __name__ == '__main__':
    menu()




