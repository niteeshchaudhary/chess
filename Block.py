from tkinter import Button

class Block(Button):

    def __init__(self,LeftFrame,text,font,width,height,bg,command):
        super().__init__(LeftFrame,text = text,font = font,width = width,height=height,activebackground=bg,bg = bg,command=command)
        self.prevcolor = bg
        self.parent=None

    def setColor(self,color):
        self.configure(bg=color)

    def setIcon(self,text):
        self.configure(text=text)

    def getColor(self):
        return self['bg']

    def getIcon(self):
        return self['text']

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent

    def resetColor(self):
        self.configure(bg=self.prevcolor)

    def resetParent(self):
        self.parent=None

