from pynput.mouse import Listener as mouseListener
from pynput.keyboard import Key, Listener as keyboardListener

xy = []
sizes = []
isCtrl = False

size = 11


def on_scroll(x, y, dx, dy):
    global size, sizes
    global isCtrl
    print(isCtrl)
    if isCtrl:
        size += dy
        sizes.append(size)
        print(sizes[-1])


def on_press(key):
    global isCtrl
    if key == Key.ctrl:
        isCtrl = True
    print(isCtrl)


def on_release(key):
    global isCtrl
    if key == Key.ctrl:
        isCtrl = False
    print(isCtrl)

# Mouse listener
mouse_listener = mouseListener(on_scroll=on_scroll)
mouse_listener.start()

# Keyboard listener
with keyboardListener(on_press=on_press, on_release=on_release) as listener:
    listener.join()