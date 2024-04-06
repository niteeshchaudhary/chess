import tkinter as tk
from tkinter import messagebox
from game import Game

def p2Game(gmw):
    gmw.destroy()
    root.withdraw()
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.protocol("WM_DELETE_WINDOW", exit_game)

    # Set window to fullscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    # game_window.attributes('-fullscreen', True)
    button_frame = tk.Frame(game_window)
    button_frame.pack(pady=(30, root.winfo_width() /8))

    # Create a frame for the buttons
    game = Game(button_frame)
    # root.mainloop()

def start_game():
    # Close the main window
    root.withdraw()
    
    # Create a new window for the game
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.protocol("WM_DELETE_WINDOW", exit_game)

 
    # Set window to fullscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    # game_window.attributes('-fullscreen', True)

    # Create a frame for the buttons
    button_frame = tk.Frame(game_window)
    button_frame.pack(pady=(root.winfo_height() / 3, 0))

    # Create five buttons
    buttons = ["Exit","P2 Game","2","3","4","5"]
    button = tk.Button(button_frame, text=buttons[1], command=lambda:p2Game(game_window), width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[2], width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[3], width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[4], width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[5], width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[0], command=exit_game, width=20, height=2)
    button.pack(pady=10)

def exit_game():
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.quit()


def toggle_fullscreen(event=None):
    # Toggle fullscreen mode
    root.attributes("-fullscreen", not root.attributes("-fullscreen"))

# Create the main window
root = tk.Tk()
root.title("Game Front Page")

root.protocol("WM_DELETE_WINDOW", exit_game)
# Set window to fullscreen
# root.attributes('-fullscreen', True)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")


root.bind("<F11>", toggle_fullscreen)

# Bind Escape key to exit fullscreen
root.bind("<Escape>", toggle_fullscreen)

# Create a frame for the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=(root.winfo_screenheight()*2//5, 0))

# Create a start button
start_button = tk.Button(button_frame, text="Start Game", command=start_game, width=20, height=2)
start_button.pack(pady=10)

# Create an exit button
exit_button = tk.Button(button_frame, text="Exit", command=exit_game, width=20, height=2)
exit_button.pack(pady=10)

root.mainloop()
