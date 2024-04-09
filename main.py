import tkinter as tk
from tkinter import messagebox
from two_player_game import Two_Player_Game
from ai_game import AI_Game

rotation_button=None
undo_button=None
game_=None


def restart_game(win_obj):
    global game_
    win_obj.destroy()
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.protocol("WM_DELETE_WINDOW", exit_game)

    option_pane=create_top_pane(game_window)
    history_pane=create_left_pane(game_window)

    # Set window to fullscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    
    board_frame=create_center_pane(game_window)

    # board_frame.pack()

    
    game_= Game(board_frame,history_pane,option_pane)

def resign():
    global game_
    game_.resign()
    pass

def undo():
    global undo_button
    if game_.undo>4:
        undo_button.config(text="")
        return
    
    black="♜♞♝♛♚♟"
    last_stat=game_.state[-1]
    del game_.state[-1]
    print("o ",game_.move_labels_text)
    game_.board,game_.current_player,game_.en_passant_target,game_.is_check,game_.is_checkmate,game_.move_labels_text=last_stat
    print("rv ",game_.move_labels_text)
    game_.undo+=1
    for i in range(8):
        for j in range(8):
            if game_.board[i][j]:
                game_.board_squares[i][j].config(text=game_.board[i][j].get_symbol())
            else:
                game_.board_squares[i][j].config(text="")

    game_.history.write(f"undo preformed\n")


    for i in game_.move_labels:
        i.destroy()
        del i

    for i in game_.move_labels_text:
        move_label = tk.Label(game_.move_history_frame, text=i, height=1, relief="sunken", font=("Arial", 20))
        if i[0] in black:
            move_label.pack(anchor="w",padx=5)
        else:
             move_label.pack(anchor="e",padx=5)
        game_.move_labels.append(move_label)



    pass

# def toggle_rotation():
#     global rotation_button
#     if not Game.is_rotation_enabled:
#         rotation_button.config(text="Disable Board Rotation")
#         Game.is_rotation_enabled=True
#     else:
#         rotation_button.config(text="Enable Board Rotation")
#         Game.is_rotation_enabled=False
#     print("hell")

def create_top_pane(win_obj):
    global rotation_button,undo_button
    
    top_frame = tk.Frame(win_obj, bg="lightgreen", height=100)
    top_frame.pack(side="top", fill="x")

    new_game_button = tk.Button(top_frame, text="New Game", command=lambda: restart_game(win_obj))
    new_game_button.pack(side="left", padx=10, pady=10)

    resign_button = tk.Button(top_frame, text="Resign", command=resign)
    resign_button.pack(side="left", padx=10, pady=10)

    undo_button = tk.Button(top_frame, text="Undo", command=undo)
    undo_button.pack(side="left", padx=10, pady=10)

    # rotation_button = tk.Button(top_frame, text="Enable Board Rotation", command=toggle_rotation)
    # rotation_button.pack(side="left", padx=10, pady=10)

    return top_frame

def create_left_pane(win_obj):
    left_frame = tk.Frame(win_obj, bg="lightblue", width=200, height=400)
    left_frame.pack(side="left", fill="y")
    left_frame.pack_propagate(0)
    return left_frame

def create_inner_frame(parent):
    inner_frame = tk.Frame(parent, bg="red", padx=0, pady=0)
    inner_frame.grid(row=1, column=1,columnspan=8,rowspan=8, sticky="ns")
    return inner_frame

def create_center_pane(win_obj):
    center_frame = tk.Frame(win_obj, bg="lightyellow")
    center_frame.pack(expand=True, fill="both")

    text=" abcdefgh"
    for ind,i in enumerate(text):
        top_label = tk.Label(center_frame, text=i,bg=["brown","lightyellow"][ind%2], padx=10, pady=10)
        top_label.grid(row=0, column=ind,sticky="ew")
    
    text=" 87654321"
    for ind,i in enumerate(text):
        left_label = tk.Label(center_frame,  text=i,bg=["brown","lightyellow"][ind%2], padx=0, pady=10)
        left_label.grid(row=ind, column=0, sticky="nsew")

    return create_inner_frame(center_frame)

def p2Game(gmw):
    global game_
    gmw.destroy()
    root.withdraw()
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.protocol("WM_DELETE_WINDOW", exit_game)

    option_pane=create_top_pane(game_window)
    history_pane=create_left_pane(game_window)

    # Set window to fullscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    
    board_frame=create_center_pane(game_window)

    # board_frame.pack()

    
    game_ = Two_Player_Game(board_frame,history_pane,option_pane)

def ai_Game(gmw):
    global game_
    gmw.destroy()
    root.withdraw()
    game_window = tk.Toplevel()
    game_window.title("Game Window")
    game_window.protocol("WM_DELETE_WINDOW", exit_game)

    option_pane=create_top_pane(game_window)
    history_pane=create_left_pane(game_window)

    # Set window to fullscreen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    game_window.geometry(f"{screen_width}x{screen_height}")
    
    board_frame=create_center_pane(game_window)

    # board_frame.pack()

    
    game_ = AI_Game(board_frame,history_pane,option_pane)


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
    buttons = ["Exit","P2 Game","AI","3","4","5"]
    button = tk.Button(button_frame, text=buttons[1], command=lambda:p2Game(game_window), width=20, height=2)
    button.pack(pady=10)

    button = tk.Button(button_frame, text=buttons[2],command=lambda:p2Game(game_window), width=20, height=2)
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
