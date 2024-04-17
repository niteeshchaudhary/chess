def play(self):
        screenshot = pg.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        board=""
        folder_path = "./boardun"
        num_files = len(os.listdir(folder_path))
        for regi in range(1, num_files+1):
            board = pg.locateOnScreen(f'./boardun/wt{regi}.png')
            if board:
                break
        exe = ''
        word = ['', '', '', '', '', '*', '*', '*', '*', '*']
        roi = ""
        if not board:
            print("please choose the correct region")
            b_inf = list(map(int, selector.getSelection()))
            print(b_inf)
            if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                menu()
            sc = pg.screenshot()
            roi = sc.crop(b_inf)
            roi.save(f"./boardun/wt{num_files + 1}.png")
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
                    elif ind == 5:
                        break
                    print(ind)
                    cv2.rectangle(
                        screenshot,
                        (bl + blkw * ind, bt + blkh * i),
                        (bl + blkw * ind + blkw, bt + blkh * i + blkh),
                        (255, 0, 255),3)

                wrd = self.getWord(''.join(word), exe,i)
                if wrd == prev:
                    if roi != "": os.remove(f"./boardun/wt{num_files + 1}.png")
                    error()
                print(wrd, exe, word)
                # print("->",gm.getWord())
                pg.typewrite(wrd + "\n")
                # cv2.imshow("scrn",screenshot)
                # #smelt
                # cv2.waitKey(0)
                time.sleep(2)
                screenshot = pg.screenshot()
                screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                cntg = 0
                for wind in range(5):
                    xcor=bt + blkh * i + 8+i*2
                    ycor=bl + blkw * wind + blkw // 2
                    b, g, r = screenshot[xcor, ycor]
                    k=2
                    while [int(b), int(g), int(r)] == [255, 255, 255] or [int(b), int(g), int(r)] == [233, 225, 222]:
                        xcor = bt + blkh * i + 8 + i * 2+k
                        ycor = bl + blkw * wind + blkw // 2
                        b, g, r = screenshot[xcor, ycor]
                        k+=2
                    # print(xcor,ycor)
                    cv2.circle(screenshot, (ycor,xcor), 5, (0, 0, 255), -1)

                    print("**",r,g,b)
                    if [int(b), int(g), int(r)] == [55, 194, 243]:
                        word[wind+5] = wrd[wind].upper()
                    elif [int(b), int(g), int(r)] == [81, 184, 121]:
                        for upi, upx in enumerate(word[5:]):
                            if upx.lower() == wrd[wind].lower():
                                word[5+upi] = "*"
                        word[wind] = wrd[wind].lower()
                        cntg += 1
                    elif [int(b), int(g), int(r)] == [196, 174, 164]:
                        if(word[wind] == ''):
                            word[wind] = '*'
                        exe += wrd[wind].lower()
                    elif [int(b), int(g), int(r)] == [255, 252, 251]:
                        pg.typewrite(["backspace"] * 5)
                        i -= 1
                        print("-----------------------------")
                        screenshot = pg.screenshot()
                        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                        break
                    else:
                        print("xxxxxx ",[int(b), int(g), int(r)]," xxxxxxxxxx")
                        cv2.imshow("scrn", screenshot)
                        cv2.waitKey(0)
                        return 0
                    print("&*", word, exe, i)

                # cv2.imshow("scrn", screenshot)
                # cv2.waitKey(0)

                if cntg >= 5:
                    return 1
                i += 1

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