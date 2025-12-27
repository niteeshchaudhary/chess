import keyboard

lst=["ctrl+c","ctrl+v","ctrl+shift+c","ctrl+shift+v","ctrl+f","ctrl+s","ctrl+h"]
def on_hotkey():
    keys_pressed = keyboard._pressed_events
    print(f"Keys {keys_pressed} pressed")

# Define your desired combination of keys as a hotkey
for i in lst:
    print(i)
    keyboard.add_hotkey(i,on_hotkey)

# Keep the program running
keyboard.wait('esc')  # Press 'esc' to exit the program
