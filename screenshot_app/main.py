import pyautogui
import keyboard as mykeyboard
from pynput import mouse
from tkinter import *
from tkinter import messagebox
import threading
from collections import deque

thread=None
filename=None
listener=None
keyboard_listener=None
te=threading.Event()

def on_click(x, y, button, pressed):
    global filename
    if button == mouse.Button.left:
        print('{} {}'.format('PLC' if pressed else 'RLC', (x, y))) # pressed left click and released left click
        filename.write('{},{},{}\n'.format('PLC' if pressed else 'RLC', x, y)) 
    else:
        print('{} {}'.format('PRC' if pressed else 'RRC', (x, y))) # pressed right click and released right click
        filename.write('{},{},{}\n'.format('PRC' if pressed else 'RRC', x, y))

def on_scroll(x, y, dx, dy):
    global filename
    print('{} {} {}'.format('SC', dx, dy)) # scroll
    filename.write('{},{},{}\n'.format('SC', dx, dy))
    

# lst=["ctrl+c","ctrl+v","ctrl+shift+c","ctrl+shift+v","ctrl+f","ctrl+s","ctrl+h"]
# def on_hotkey():
#     keys_pressed = mykeyboard._pressed_events
#     print(f"Keys {keys_pressed} pressed")g
#     filename.write('{},{},{}\n'.format("Hotkey", keys_pressed, 0))
def on_key_press(key):
    # if isinstance(key, mykeyboard.KeyCode):
    #     key_str = key.char
    # else:
    print(key.name,key.event_type)
    # print(f"Key: {key.name}")a
    # print(f"Scan Code: {key.scan_code}")
    # print(f"Time: {key.time}")
    # print(f"Device: {key.device}")
    # print(f"key Type: {key.event_type}")
    # print("-" * 30)
    
    
    # if ord(key_str[0])<31:tp 
    #     return

    # if(key.event_type=="up"):
    #     stack.append(key.name)
    # elif(key.event_type=="down"):
    #     mykey=stack.pop()
    #     if(len(stack)>0):
    #         nextkey=stack.pop()+"+"+mykey
    #         stack.append(nextkey)
    #         print(nextkey)
    #     else:
    filename.write('{},{},{}\n'.format("K",key.event_type, key.name))
        
def mylistener():
    global listener
    global keyboard_listener
    listener = mouse.Listener(on_click=on_click,on_scroll=on_scroll)
    listener.start()

    
    # keyboard_listener = keyboard.Listener(on_press=on_key_press)
    mykeyboard.hook(on_key_press)
    # for i in lst:
    #     print(i)
    #     mykeyboard.add_hotkey(i,on_hotkey)

    # keyboard_listener.start()
    listener.join()
    # keyboard_listener.join()

def stopGame():
    global listener
    global keyboard_listener
    global thread
    global filename
    listener.stop()
    thread.join()
    mykeyboard.unhook_all()
    filename.close()
    messagebox.showinfo("Info", "Recording stopped")
    exit()
  
def startGame(ref):
    global filename
    global thread
    filename = open("./tasks/"+(ref.children['!entry'].get() or "def")+".txt","w+")
    thread = threading.Thread(target=mylistener,daemon=True)
    thread.start()
    ref.children['!button'].config(text='Stop', command=lambda: stopGame(),background='red')

def menu():
    
    mn = Tk()
    mn.geometry('%dx%d+%d+%d' % (300, 100, mn.winfo_screenwidth() -300, mn.winfo_screenheight() -200))
    input_box = Entry(mn)
    input_box.pack(side=TOP, pady=5)
    button = Button(mn, text='Start', command=lambda: startGame(mn))
    button.pack(side=TOP, pady=5)
    mn.mainloop()

if __name__ == '__main__':
    menu()
    filename.close()

