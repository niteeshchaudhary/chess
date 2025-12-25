from tkinter import *    

class Selector(Frame):
    def __init__(self,master,msg=""):
        Frame.__init__(self,master=None)
        dfmsg="We were unable to detect grid,\nplease select the grid manually,\nNote: draw rectangle very close to grid \n"
        if msg=="":
            msg=dfmsg
        w=master.winfo_screenwidth()
        h=master.winfo_screenheight()
        self.root=master
        self.x = self.y = 0
        self.canvas = Canvas(self, bg='grey', cursor="cross", height=h, width=w, highlightthickness=0)
        self.canvas.grid(row=h,column=w)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        Label(self,text=msg,
                    bg="green", bd = 100, fg = "white",
                    width="20",
                    font=("Arial", 20)).place(x = 4*w//6,y = h//4)

        self.rect = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None 

    def on_button_press(self, event):
        # save mouse drag start position
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)

        # create rectangle if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        # expand rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)    

    def on_button_release(self, event):
        self.end_x = self.canvas.canvasx(event.x)
        self.end_y = self.canvas.canvasy(event.y)
        self.root.destroy()

def getSelection(msg=""):
    root=Tk()
    root.overrideredirect(True)
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry('%dx%d+%d+%d' % (width+10, height, -10, 0))
    root.configure(bg='grey')
    root.wait_visibility(root)
    root.attributes('-alpha', 0.2)
    app = Selector(root,msg)
    app.pack()  # Set transparency to 30% (0.3)
    root.mainloop()
    if(app.start_x>app.end_x):
        app.start_x,app.end_x=app.end_x,app.start_x
    if(app.start_y>app.end_y):
        app.start_y,app.end_y=app.end_y,app.start_y
    return [app.start_x,app.start_y,app.end_x,app.end_y]



# from tkinter import *
# import tkinter
 
# root = Tk()
# def helloCallBack():
#    root.overrideredirect(False)
   
# # Create object


# width = root.winfo_screenwidth()
# height = root.winfo_screenheight() 
# root.attributes('-alpha',0.5)

# button = Button(root, text = 'Geeks',command = helloCallBack)
# # pady is used for giving some padding in y direction
# button.pack(side = TOP, pady = 5)
# # Adjust size
# root.overrideredirect(True)
# root.geometry('%dx%d+%d+%d' % (width+10, height, -10, 0))


# Execute tkinter