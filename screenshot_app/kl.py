import keyboard

def on_key_event(event):
    print(f"Key {event.name} {'pressed' if event.event_type == 'down' else 'released'}")

keyboard.hook(on_key_event)

# Keep the program running
keyboard.wait('esc')  # Press 'esc' to exit the program
