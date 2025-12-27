import pyautogui as pg
import keyboard as mykeyboard
from pynput import mouse, keyboard
from tkinter import *
from tkinter import messagebox,ttk
import threading
import os
from collections import deque

thread=None
filename=None

st=deque()

def mylistener():
    print(filename.read())
    for line in filename:
        print(line)
        command=line.strip().split(",")
        if command[0] == "PLeftClick":
            pg.leftClick(int(command[1]),int(command[2]))
        elif command[0] == "RLeftClick":
            pg.rightClick(int(command[1]),int(command[2]))
        elif command[0] == "KeyPress":
            command[1]=command[1].removeprefix("KeyboardEvent")
            command[1]=command[1].removeprefix("(")
            command[1]=command[1].removesuffix(")")
            command[1]=command[1].split(" ")
            print(command[1])
            if(command[1][1]=="down"):
                st.append(command[1])
            else:
                st.pop(command[1])
            
    # pg.click(bl, bt)
    pg.typewrite(["backspace"] * 5)
    pass

def stopGame():
    thread.join()
    filename.close()
    messagebox.showinfo("Info", "Recording stopped")
    exit()
  
def startGame(ref):
    global thread,filename
    path=""
    if(os.path.exists("./tasks/"+(ref.children['!combobox'].get()))):
        path="./tasks/"+(ref.children['!combobox'].get())
    else:
        path="./tasks/def.txt"
    filename = open(path,"r")
    thread = threading.Thread(target=mylistener,daemon=True)
    thread.start()
    ref.children['!button'].config(text='Stop', command=lambda: stopGame(),background='red')

def menu():
    
    mn = Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 100, mn.winfo_screenwidth() -300, mn.winfo_screenheight() -200))

    # Create a combobox
    combobox = ttk.Combobox(mn)
    folder_path = "./tasks/"
    file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(file_list)

    options = file_list

    # Set the options to the combobox
    combobox['values'] = options

    # Set the initial value of the combobox (optional)
    combobox.set("Select an option")

    # Bind the selection event to the handler function
    # combobox.bind("<<ComboboxSelected>>", on_select)

    # Pack the combobox into the window
    combobox.pack(pady=10)
    button = Button(mn, text='Start', command=lambda: startGame(mn))
    button.pack(side=TOP, pady=5)
    mn.mainloop()

if __name__ == '__main__':
    menu()
    filename.close()

