class Tokens:
    def __init__(self, x, y, color,name):
        self.x = x
        self.y = y
        self.color = color
        self.name=name
        self.icon = ""
        self.enable = True

    def setEnable(self, val):
        self.enable = val

    def isEnable(self):
        return self.enable

    def setPosition(self):
        pass

    def getPosition(self):
        pass
