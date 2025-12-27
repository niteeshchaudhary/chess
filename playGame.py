import os
import selector
import pyautogui as pg
import numpy as np
import cv2
from tkinter import *
from tkinter import messagebox
import time
from tokens_2 import Rook, Knight, Bishop, Queen, King, Pawn

# Try to use mss for better Linux/Wayland support
try:
    import mss
    USE_MSS = True
except ImportError:
    USE_MSS = False
    print("Warning: mss not installed. Using pyautogui for screenshots (may not work on Wayland).")
    print("Install with: pip install mss")


def take_screenshot():
    """Take a screenshot using the best available method."""
    if USE_MSS:
        with mss.mss() as sct:
            # Use monitors[0] to capture ALL monitors (virtual screen)
            # This ensures coordinates from tkinter selector match the screenshot
            monitor = sct.monitors[0]  # All monitors combined
            screenshot = sct.grab(monitor)
            # Convert to numpy array in BGR format for OpenCV
            img = np.array(screenshot)
            # mss returns BGRA, convert to BGR
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
    else:
        # Fallback to pyautogui
        screenshot = pg.screenshot()
        return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def get_match_confidence(main_image, template_path):
    """
    Get the best match confidence score for a template against the main image.
    Returns the confidence score (0.0 to 1.0) and location.
    Uses multi-scale matching to handle different piece sizes.
    """
    template = cv2.imread(template_path)
    
    if template is None:
        return 0.0, None, None, None
    
    # Convert to grayscale
    if len(main_image.shape) == 3:
        main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    else:
        main_gray = main_image
        
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    best_confidence = 0.0
    best_loc = None
    best_w, best_h = template_gray.shape[::-1]
    
    # Try multiple scales
    scales = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2]
    
    for scale in scales:
        # Resize template
        new_w = int(template_gray.shape[1] * scale)
        new_h = int(template_gray.shape[0] * scale)
        
        if new_w < 10 or new_h < 10:
            continue
        if new_w > main_gray.shape[1] or new_h > main_gray.shape[0]:
            continue
            
        resized_template = cv2.resize(template_gray, (new_w, new_h))
        
        try:
            # Use TM_CCOEFF_NORMED - most reliable for chess pieces
            result = cv2.matchTemplate(main_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val > best_confidence:
                best_confidence = max_val
                best_loc = max_loc
                best_w, best_h = new_w, new_h
        except:
            continue
    
    return best_confidence, best_loc, best_w, best_h


def detect_piece_in_square(sub_image, token_folder_path):
    """
    Detect which piece (if any) is in the given square.
    Returns the best matching piece type and color, or None if no piece detected.
    Uses "best match wins" approach - compares all pieces and picks highest confidence.
    """
    best_confidence = 0.0
    best_piece_type = None
    best_piece_color = None
    best_loc = None
    best_w, best_h = None, None
    
    # Minimum confidence threshold - must be high enough to avoid false positives
    MIN_CONFIDENCE = 0.75
    
    # Get all piece folders
    try:
        token_folders = os.listdir(token_folder_path)
    except:
        return None, None, 0.0, None, None, None
    
    for folder_name in token_folders:
        folder_path = os.path.join(token_folder_path, folder_name)
        
        # Skip if not a directory
        if not os.path.isdir(folder_path):
            continue
        
        # Parse piece type and color from folder name (e.g., "Bishop_black")
        parts = folder_name.split("_")
        if len(parts) < 2:
            continue
        piece_type = parts[0]
        piece_color = parts[1]
        
        # Try each template image in the folder
        try:
            template_files = os.listdir(folder_path)
        except:
            continue
            
        for template_file in template_files:
            if not template_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                continue
                
            template_path = os.path.join(folder_path, template_file)
            confidence, loc, w, h = get_match_confidence(sub_image, template_path)
            
            if confidence > best_confidence:
                best_confidence = confidence
                best_piece_type = piece_type
                best_piece_color = piece_color
                best_loc = loc
                best_w, best_h = w, h
    
    # Only return a piece if confidence is above threshold
    if best_confidence >= MIN_CONFIDENCE:
        return best_piece_type, best_piece_color, best_confidence, best_loc, best_w, best_h
    
    return None, None, best_confidence, None, None, None


def locate_image(main_image_path, template_image_path):
    """
    Legacy function for board detection. Returns match location.
    """
    main_image = main_image_path
    template_image = cv2.imread(template_image_path)
    
    if template_image is None:
        return None, None, None

    # Convert images to grayscale
    main_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY)
    template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    # Get the dimensions of the template image
    w, h = template_gray.shape[::-1]
    
    # Check if template is larger than main image
    if h > main_gray.shape[0] or w > main_gray.shape[1]:
        return None, None, None

    # Perform template matching
    res = cv2.matchTemplate(main_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(res >= threshold)

    if loc[0].size == 0:
        return None, None, None
    
    return loc, w, h


def print_board_state(board, title="Board State"):
    """Print the detected board state for debugging."""
    import sys
    sys.stdout.flush()  # Ensure output is flushed immediately
    print("\n" + "="*50, flush=True)
    print(f"  {title}", flush=True)
    print("="*50, flush=True)
    print("     0    1    2    3    4    5    6    7")
    print("   +----+----+----+----+----+----+----+----+")
    
    piece_symbols = {
        'Rook': 'R', 'Knight': 'N', 'Bishop': 'B', 
        'Queen': 'Q', 'King': 'K', 'Pawn': 'P'
    }
    
    for row in range(8):
        row_str = f" {row} |"
        for col in range(8):
            piece = board[row][col]
            if piece:
                piece_name = piece.__class__.__name__
                color = piece.color[0].upper()  # 'W' or 'B'
                symbol = piece_symbols.get(piece_name, '?')
                row_str += f" {symbol}{color} |"
            else:
                row_str += "    |"
        print(row_str, flush=True)
        print("   +----+----+----+----+----+----+----+----+", flush=True)
    
    # Count pieces
    piece_count = {'white': {}, 'black': {}}
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece:
                color = piece.color
                piece_name = piece.__class__.__name__
                piece_count[color][piece_name] = piece_count[color].get(piece_name, 0) + 1
    
    print("\nPiece Count:", flush=True)
    for color in ['white', 'black']:
        pieces = piece_count[color]
        if pieces:
            piece_str = ", ".join([f"{v} {k}{'s' if v > 1 else ''}" for k, v in pieces.items()])
            print(f"  {color.capitalize()}: {piece_str}", flush=True)
        else:
            print(f"  {color.capitalize()}: No pieces detected", flush=True)
    print("="*50 + "\n", flush=True)
    sys.stdout.flush()


class Game:
    def __init__(self):
        self.cur_locations=[[None for i in range(8)] for j in range(8)]
        self.board_data=[[None for i in range(8)] for j in range(8)]
        self.bl=0
        self.bt=0
        self.blkw=0
        self.blkh=0
        self.token_folder_path = "tokens_images"
        self.screenshot = None

    def play(self):
            self.screenshot = take_screenshot()
            board=""
            folder_path = "boardimages"
            
            num_files = len(os.listdir(folder_path))

            for regi in range(1, num_files+1):
                try:
                    board,w,h = locate_image(self.screenshot,f'./{folder_path}/{regi}.png')
                    if board:
                        board = Obj2(board,w,h)
                        break
                except:
                    pass

            exe = ''
            roi = ""
            if not board:
                print("please choose the correct region")
                b_inf = list(map(int, selector.getSelection()))
                print(b_inf)
                if (b_inf[3]-b_inf[1])<100 or (b_inf[2]-b_inf[0])<120:
                    menu()
                sc = take_screenshot()
                # Crop using numpy array slicing: [y1:y2, x1:x2]
                roi = sc[b_inf[1]:b_inf[3], b_inf[0]:b_inf[2]]
                cv2.imwrite(f"./{folder_path}/{num_files + 1}.png", roi)
                board = Obj(b_inf)

            prev = ""
            if board:
                print(board)
                cntgc=0
                errv = 4
                errw = 1
                bh = board.height
                bw = board.width
                self.bl = board.left
                self.bt = board.top
                self.blkh = (bh - errv) // 8
                self.blkw = (bw - errw) // 8
                cv2.rectangle(
                    self.screenshot,
                    (self.bl, self.bt),
                    (self.bl + bw, self.bt + bh),
                    (255, 255, 0),
                    3)
                
                i = 0
                # num_token_files = len(os.listdir(token_folder_path))
                self.board_data=[[None for i in range(8)] for j in range(8)]
                lst=[]
                nslst=[]
                cnt=0
                detected_pieces = 0
                while i < 8:
                    for ind in range(8):
                        if i == 0:
                            pg.click(self.bl, self.bt)

                        # Calculate square boundaries with validation
                        y1 = self.bt + self.blkh * i
                        y2 = y1 + self.blkh
                        x1 = self.bl + self.blkw * ind
                        x2 = x1 + self.blkw
                        
                        # Validate bounds
                        if y2 > self.screenshot.shape[0] or x2 > self.screenshot.shape[1]:
                            continue
                        if y1 < 0 or x1 < 0:
                            continue
                            
                        sub_image = self.screenshot[y1:y2, x1:x2]
                        
                        # Skip if sub_image is too small
                        if sub_image.shape[0] < 10 or sub_image.shape[1] < 10:
                            continue
                            
                        self.cur_locations[i][ind]=((x1 + x2)//2, (y1 + y2)//2)
                        cv2.circle(
                            self.screenshot,
                            self.cur_locations[i][ind],
                            2,
                            (255, 0, 0),3)
                        
                        
                        cv2.rectangle(
                            self.screenshot,
                            (x1, y1),
                            (x2, y2),
                            (255, 0, 255),3)
                        
                        # Use best-match detection to find piece in this square
                        piece_type, piece_color, confidence, loc, w, h = detect_piece_in_square(
                            sub_image, self.token_folder_path
                        )
                        
                        if piece_type and piece_color:
                            detected_pieces += 1
                            self.board_data[i][ind] = eval(f"{piece_type}('{piece_color}')")
                            # print(f"Detected {piece_type}_{piece_color} at ({i},{ind}) conf={confidence:.2f}")

                        
                    # lst.append(nslst)
                    i += 1

                import sys
                print(f"\n[Detection] Found {detected_pieces} pieces on the board", flush=True)
                print("[Detection] Printing board state...", flush=True)
                sys.stdout.flush()  # Ensure output is flushed
                # Print board state for debugging using the formatted function
                try:
                    print_board_state(self.board_data, "Detected Board State")
                except Exception as e:
                    print(f"[ERROR] Failed to print board state: {e}", flush=True)
                    import traceback
                    traceback.print_exc()
                    sys.stdout.flush()
                sys.stdout.flush()

                # cv2.imshow("scrn",self.screenshot)
                #     # #smelt
                # cv2.waitKey(0)
                return self.board_data,self.cur_locations
                

                
                # for i in range(8):
                #     print(self.board_data[i])
            else:
                return None,None

    def read_board(self):
        self.screenshot = take_screenshot()
        i = 0
        self.board_data=[[None for i in range(8)] for j in range(8)]
        detected_pieces = 0
        while i < 8:
            for ind in range(8):
                # Calculate square boundaries with validation
                y1 = self.bt + self.blkh * i
                y2 = y1 + self.blkh
                x1 = self.bl + self.blkw * ind
                x2 = x1 + self.blkw
                
                # Validate bounds
                if y2 > self.screenshot.shape[0] or x2 > self.screenshot.shape[1]:
                    continue
                if y1 < 0 or x1 < 0:
                    continue
                    
                sub_image = self.screenshot[y1:y2, x1:x2]
                
                # Skip if sub_image is too small
                if sub_image.shape[0] < 10 or sub_image.shape[1] < 10:
                    continue
                
                # Use best-match detection to find piece in this square
                piece_type, piece_color, confidence, loc, w, h = detect_piece_in_square(
                    sub_image, self.token_folder_path
                )
                
                if piece_type and piece_color:
                    detected_pieces += 1
                    self.board_data[i][ind] = eval(f"{piece_type}('{piece_color}')")
                
            i += 1

        # Print the detected board state before returning (for debugging)
        import sys
        print(f"\n[read_board] Detected {detected_pieces} pieces on the board", flush=True)
        try:
            print_board_state(self.board_data, "Current Board State (before move)")
        except Exception as e:
            print(f"[ERROR] Failed to print board state in read_board: {e}", flush=True)
            import traceback
            traceback.print_exc()
        sys.stdout.flush()

        return self.board_data

class Obj:
    def __init__(self,b_inf):
        self.top=b_inf[1]
        self.left=b_inf[0]
        self.width=b_inf[2]-b_inf[0]
        self.height=b_inf[3]-b_inf[1]

class Obj2:
    def __init__(self,board,w,h):
        lst=list(zip(*board[::-1]))
        self.top=lst[0][1]
        self.left=lst[0][0]
        self.width=w
        self.height=h



def flip_board(board, move_positions):
    """
    Flip the board 180 degrees (for when black is at bottom on screen).
    After flipping: pieces maintain their colors, just coordinates are flipped.
    """
    # Flip board array
    flipped_board = [[None for _ in range(8)] for _ in range(8)]
    flipped_positions = [[None for _ in range(8)] for _ in range(8)]
    
    for row in range(8):
        for col in range(8):
            # Flip coordinates: (row, col) -> (7-row, 7-col)
            flipped_row = 7 - row
            flipped_col = 7 - col
            flipped_board[flipped_row][flipped_col] = board[row][col]
            flipped_positions[flipped_row][flipped_col] = move_positions[row][col]
    
    return flipped_board, flipped_positions


def startGame(ref, selected_algo, selected_side, board_flipped):
    """Start the game with the selected algorithm, side, and board orientation."""
    algorithm_name = selected_algo.get()
    player_side = selected_side.get()
    is_flipped = board_flipped.get() == "Flipped"
    
    print(f"\n[Game] Starting with algorithm: {algorithm_name}")
    print(f"[Game] Playing as: {player_side}")
    print(f"[Game] Board orientation: {'Flipped (black at bottom)' if is_flipped else 'Normal (white at bottom)'}")
    ref.destroy()
    
    gm = Game()
    board, move_positions = gm.play()
    
    if not board:
        error()
        return
    
    # Flip board if needed
    if is_flipped:
        print("[Game] Flipping board orientation...")
        board, move_positions = flip_board(board, move_positions)
        print_board_state(board, "Board State After Flipping")
    else:
        # Print the detected board state for debugging
        print_board_state(board, "Detected Board State")
    
    # Use the selected player side
    player_color = player_side.lower()
    print(f"[Game] Playing as: {player_color}")
    
    from BotPlay import BotPlay
    game_ = BotPlay(player_color, board, move_positions, gm, algorithm_name)


def error():
    mn = Tk()
    messagebox.showerror("Error", "We faced issue in detecting grid region selected by you! Please try to select exact grid next time.")
    exit()


# Import shared algorithm list
from algorithm_list import ALGORITHMS


def menu():
    mn = Tk()
    mn.title("Chess Bot - Configuration")
    mn.geometry('%dx%d+%d+%d' % (400, 280, mn.winfo_screenwidth() // 2 - 200, mn.winfo_screenheight() // 2 - 140))
    mn.configure(bg='#2c3e50')
    
    # Title label
    title_label = Label(mn, text="Chess Bot Configuration", font=("Helvetica", 16, "bold"), 
                        bg='#2c3e50', fg='white')
    title_label.pack(pady=(15, 10))
    
    # Algorithm selection frame
    algo_frame = Frame(mn, bg='#2c3e50')
    algo_frame.pack(pady=8)
    
    algo_label = Label(algo_frame, text="Algorithm:", font=("Helvetica", 10),
                       bg='#2c3e50', fg='white', width=12, anchor='w')
    algo_label.pack(side=LEFT, padx=5)
    
    selected_algo = StringVar(mn)
    selected_algo.set("QuiescenceEngine")  # Default: Best overall algorithm
    
    algo_dropdown = OptionMenu(algo_frame, selected_algo, *ALGORITHMS)
    algo_dropdown.config(width=18, font=("Helvetica", 10))
    algo_dropdown.pack(side=LEFT, padx=5)
    
    # Side selection frame
    side_frame = Frame(mn, bg='#2c3e50')
    side_frame.pack(pady=8)
    
    side_label = Label(side_frame, text="Play As:", font=("Helvetica", 10),
                       bg='#2c3e50', fg='white', width=12, anchor='w')
    side_label.pack(side=LEFT, padx=5)
    
    selected_side = StringVar(mn)
    selected_side.set("White")  # Default side
    
    side_dropdown = OptionMenu(side_frame, selected_side, "White", "Black")
    side_dropdown.config(width=18, font=("Helvetica", 10))
    side_dropdown.pack(side=LEFT, padx=5)
    
    # Board orientation frame
    board_frame = Frame(mn, bg='#2c3e50')
    board_frame.pack(pady=8)
    
    board_label = Label(board_frame, text="Board Layout:", font=("Helvetica", 10),
                        bg='#2c3e50', fg='white', width=12, anchor='w')
    board_label.pack(side=LEFT, padx=5)
    
    board_flipped = StringVar(mn)
    board_flipped.set("Normal")  # Default: white at bottom
    
    board_dropdown = OptionMenu(board_frame, board_flipped, "Normal", "Flipped")
    board_dropdown.config(width=18, font=("Helvetica", 10))
    board_dropdown.pack(side=LEFT, padx=5)
    
    # Help text for board orientation
    help_text = Label(mn, text="Normal: White at bottom | Flipped: Black at bottom", 
                      font=("Helvetica", 8, "italic"),
                      bg='#2c3e50', fg='#95a5a6')
    help_text.pack(pady=(5, 5))
    
    # Algorithm recommendation text
    algo_help = Label(mn, text="🏆 StockfishEngine: Install python-chess (pip install python-chess) + Stockfish binary", 
                      font=("Helvetica", 8, "italic"),
                      bg='#2c3e50', fg='#e74c3c', wraplength=380)
    algo_help.pack(pady=(0, 5))
    algo_help2 = Label(mn, text="⭐ Recommended: QuiescenceEngine (strongest) or PhaseBasedEngine (fast+strong)", 
                      font=("Helvetica", 8, "italic"),
                      bg='#2c3e50', fg='#f39c12')
    algo_help2.pack(pady=(0, 10))
    
    # Play button
    button = Button(mn, text='Start Game', command=lambda: startGame(mn, selected_algo, selected_side, board_flipped),
                    font=("Helvetica", 12, "bold"), bg='#27ae60', fg='white',
                    width=18, height=1, cursor='hand2')
    button.pack(pady=15)
    
    mn.mainloop()


if __name__ == '__main__':
    menu()

