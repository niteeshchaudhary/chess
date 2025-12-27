import cv2
import numpy as np
import pyautogui
import threading
import time
from pynput import mouse, keyboard
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os

class OverlayWindow:
    """Transparent overlay window for real-time drawing and pointer tracer"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Overlay")
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.root.overrideredirect(True)
        
        # Try to make window click-through on Linux (requires compositor support)
        try:
            # For X11/Wayland compositors that support it
            self.root.attributes('-type', 'dock')
        except:
            pass
        
        # Canvas for drawing - black background (will be made transparent)
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Make window ignore mouse events (click-through)
        # This is a workaround - the window will still be visible but won't block clicks
        def ignore_event(event):
            return "break"
        
        self.canvas.bind('<Button-1>', ignore_event)
        self.canvas.bind('<Button-2>', ignore_event)
        self.canvas.bind('<Button-3>', ignore_event)
        self.canvas.bind('<Motion>', ignore_event)
        self.canvas.bind('<Key>', ignore_event)
        
        # Drawing data
        self.drawing_points = []
        self.current_drawing = []
        self.drawing_color = (0, 255, 0)
        self.drawing_thickness = 3
        
        # Pointer tracer data
        self.mouse_positions = []
        self.max_trail_length = 50
        self.pointer_radius = 10
        
        # State
        self.show_pointer = True
        self.is_drawing = False
        self.ctrl_pressed = False
        
        # Update loop
        self.update_interval = 16  # ~60 FPS
        self.root.after(self.update_interval, self.update_overlay)
        
        # Try to make black transparent (may not work on all systems)
        # This makes the black background transparent, leaving only drawings visible
        try:
            self.root.attributes('-transparentcolor', 'black')
            # Also try setting alpha for systems that support it
            self.root.attributes('-alpha', 0.99)
        except:
            try:
                # Fallback: use very high alpha but still visible
                self.root.attributes('-alpha', 0.99)
            except:
                pass
    
    def update_overlay(self):
        """Update the overlay display"""
        self.canvas.delete("all")
        
        # Draw pointer trail
        if self.show_pointer and self.mouse_positions:
            for i, pos in enumerate(self.mouse_positions):
                alpha = i / len(self.mouse_positions) if len(self.mouse_positions) > 1 else 1
                radius = max(2, int(self.pointer_radius * alpha))
                # Yellow trail
                self.canvas.create_oval(
                    pos[0] - radius, pos[1] - radius,
                    pos[0] + radius, pos[1] + radius,
                    fill='yellow', outline='', tags="pointer"
                )
            
            # Draw current pointer position
            if self.mouse_positions:
                current_pos = self.mouse_positions[-1]
                self.canvas.create_oval(
                    current_pos[0] - self.pointer_radius, current_pos[1] - self.pointer_radius,
                    current_pos[0] + self.pointer_radius, current_pos[1] + self.pointer_radius,
                    outline='red', width=2, tags="pointer"
                )
                self.canvas.create_oval(
                    current_pos[0] - 2, current_pos[1] - 2,
                    current_pos[0] + 2, current_pos[1] + 2,
                    fill='red', outline='', tags="pointer"
                )
        
        # Draw all saved drawings
        for points, color, thickness in self.drawing_points:
            if len(points) > 1:
                color_hex = self.rgb_to_hex(color)
                for i in range(len(points) - 1):
                    self.canvas.create_line(
                        points[i][0], points[i][1],
                        points[i+1][0], points[i+1][1],
                        fill=color_hex, width=thickness, tags="drawing"
                    )
        
        # Draw current drawing
        if self.current_drawing and len(self.current_drawing) > 1:
            color_hex = self.rgb_to_hex(self.drawing_color)
            for i in range(len(self.current_drawing) - 1):
                self.canvas.create_line(
                    self.current_drawing[i][0], self.current_drawing[i][1],
                    self.current_drawing[i+1][0], self.current_drawing[i+1][1],
                    fill=color_hex, width=self.drawing_thickness, tags="drawing"
                )
        
        self.root.after(self.update_interval, self.update_overlay)
    
    def rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex color"""
        return '#%02x%02x%02x' % (rgb[2], rgb[1], rgb[0])  # BGR to RGB
    
    def add_mouse_position(self, x, y):
        """Add mouse position to trail"""
        if self.show_pointer:
            self.mouse_positions.append((x, y))
            if len(self.mouse_positions) > self.max_trail_length:
                self.mouse_positions.pop(0)
    
    def start_drawing(self, x, y):
        """Start a new drawing"""
        if self.is_drawing and self.ctrl_pressed:
            self.current_drawing = [(x, y)]
    
    def add_drawing_point(self, x, y):
        """Add point to current drawing"""
        if self.is_drawing and self.ctrl_pressed and self.current_drawing:
            self.current_drawing.append((x, y))
            if len(self.current_drawing) > 1000:
                self.current_drawing = self.current_drawing[-500:]
    
    def finish_drawing(self):
        """Finish current drawing"""
        if self.current_drawing:
            self.drawing_points.append((
                list(self.current_drawing),
                self.drawing_color,
                self.drawing_thickness
            ))
            self.current_drawing = []
    
    def clear_drawings(self):
        """Clear all drawings"""
        self.drawing_points.clear()
        self.current_drawing = []
    
    def set_drawing_color(self, color):
        """Set drawing color"""
        self.drawing_color = color
    
    def set_drawing_thickness(self, thickness):
        """Set drawing thickness"""
        self.drawing_thickness = thickness
    
    def set_trail_length(self, length):
        """Set pointer trail length"""
        self.max_trail_length = length
    
    def show(self):
        """Show the overlay window"""
        self.root.deiconify()
    
    def hide(self):
        """Hide the overlay window"""
        self.root.withdraw()
    
    def destroy(self):
        """Destroy the overlay window"""
        self.root.destroy()


class ScreenRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Recorder & Streamer")
        self.root.geometry("600x550")
        
        # State variables
        self.is_recording = False
        self.is_streaming = False
        self.is_drawing = False
        self.show_pointer = True
        self.record_thread = None
        self.stream_thread = None
        self.mouse_listener = None
        self.keyboard_listener = None
        
        # Drawing variables
        self.drawing_color = (0, 255, 0)  # Green (BGR for OpenCV)
        self.drawing_thickness = 3
        
        # Pointer tracer variables
        self.pointer_radius = 10
        self.trail_length = 50
        
        # Video writer
        self.video_writer = None
        self.fps = 30
        self.output_file = None
        
        # Screen dimensions
        self.screen_width = pyautogui.size().width
        self.screen_height = pyautogui.size().height
        
        # Overlay window
        self.overlay = OverlayWindow()
        self.overlay.hide()  # Start hidden
        
        # Create GUI
        self.create_gui()
        
        # Start mouse and keyboard tracking
        self.start_mouse_tracking()
        self.start_keyboard_tracking()
    
    def create_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Screen Recorder & Streamer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Recording section
        record_frame = ttk.LabelFrame(main_frame, text="Recording", padding="10")
        record_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.record_btn = ttk.Button(record_frame, text="Start Recording", 
                                     command=self.toggle_recording)
        self.record_btn.grid(row=0, column=0, padx=5)
        
        self.save_path_btn = ttk.Button(record_frame, text="Choose Save Location", 
                                        command=self.choose_save_path)
        self.save_path_btn.grid(row=0, column=1, padx=5)
        
        self.save_path_label = ttk.Label(record_frame, text="No file selected")
        self.save_path_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Streaming section
        stream_frame = ttk.LabelFrame(main_frame, text="Streaming", padding="10")
        stream_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.stream_btn = ttk.Button(stream_frame, text="Start Streaming", 
                                     command=self.toggle_streaming)
        self.stream_btn.grid(row=0, column=0, padx=5)
        
        self.stream_status_label = ttk.Label(stream_frame, text="Stream: Off")
        self.stream_status_label.grid(row=0, column=1, padx=5)
        
        # Drawing section
        draw_frame = ttk.LabelFrame(main_frame, text="Drawing Overlay", padding="10")
        draw_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.draw_btn = ttk.Button(draw_frame, text="Enable Drawing", 
                                   command=self.toggle_drawing)
        self.draw_btn.grid(row=0, column=0, padx=5)
        
        self.clear_draw_btn = ttk.Button(draw_frame, text="Clear Drawings", 
                                         command=self.clear_drawings)
        self.clear_draw_btn.grid(row=0, column=1, padx=5)
        
        # Drawing options
        color_frame = ttk.Frame(draw_frame)
        color_frame.grid(row=1, column=0, columnspan=2, pady=5)
        
        ttk.Label(color_frame, text="Color:").grid(row=0, column=0, padx=5)
        self.color_var = tk.StringVar(value="Green")
        color_combo = ttk.Combobox(color_frame, textvariable=self.color_var, 
                                   values=["Red", "Green", "Blue", "Yellow", "White", "Black"],
                                   state="readonly", width=10)
        color_combo.grid(row=0, column=1, padx=5)
        color_combo.bind("<<ComboboxSelected>>", self.on_color_change)
        
        ttk.Label(color_frame, text="Thickness:").grid(row=0, column=2, padx=5)
        self.thickness_var = tk.IntVar(value=3)
        thickness_scale = ttk.Scale(color_frame, from_=1, to=10, 
                                    variable=self.thickness_var, orient=tk.HORIZONTAL, length=100)
        thickness_scale.grid(row=0, column=3, padx=5)
        thickness_scale.configure(command=self.on_thickness_change)
        
        # Pointer tracer section
        pointer_frame = ttk.LabelFrame(main_frame, text="Pointer Tracer", padding="10")
        pointer_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.pointer_btn = ttk.Button(pointer_frame, text="Toggle Pointer Tracer", 
                                      command=self.toggle_pointer)
        self.pointer_btn.grid(row=0, column=0, padx=5)
        
        ttk.Label(pointer_frame, text="Trail Length:").grid(row=0, column=1, padx=5)
        self.trail_var = tk.IntVar(value=50)
        trail_scale = ttk.Scale(pointer_frame, from_=10, to=200, 
                                variable=self.trail_var, orient=tk.HORIZONTAL, length=100)
        trail_scale.grid(row=0, column=2, padx=5)
        trail_scale.configure(command=self.on_trail_change)
        
        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(status_frame, text="Ready", font=("Arial", 10))
        self.status_label.grid(row=0, column=0)
        
        # Instructions
        instructions = """
Controls:
- Recording: Saves video to file
- Streaming: Shows live preview window
- Drawing: Hold Ctrl and drag to draw (visible in real-time!)
- Pointer Tracer: Shows mouse trail (visible in real-time!)
        """
        info_label = ttk.Label(main_frame, text=instructions, justify=tk.LEFT)
        info_label.grid(row=6, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
    
    def on_color_change(self, event=None):
        colors = {
            "Red": (0, 0, 255),
            "Green": (0, 255, 0),
            "Blue": (255, 0, 0),
            "Yellow": (0, 255, 255),
            "White": (255, 255, 255),
            "Black": (0, 0, 0)
        }
        self.drawing_color = colors.get(self.color_var.get(), (0, 255, 0))
        self.overlay.set_drawing_color(self.drawing_color)
    
    def on_thickness_change(self, value):
        self.drawing_thickness = int(float(value))
        self.overlay.set_drawing_thickness(self.drawing_thickness)
    
    def on_trail_change(self, value):
        self.trail_length = int(float(value))
        self.overlay.set_trail_length(self.trail_length)
    
    def choose_save_path(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("AVI files", "*.avi"), ("All files", "*.*")]
        )
        if filename:
            self.output_file = filename
            self.save_path_label.config(text=os.path.basename(filename))
    
    def toggle_recording(self):
        if not self.is_recording:
            if not self.output_file:
                messagebox.showwarning("Warning", "Please choose a save location first!")
                return
            self.start_recording()
        else:
            self.stop_recording()
    
    def toggle_streaming(self):
        if not self.is_streaming:
            self.start_streaming()
        else:
            self.stop_streaming()
    
    def toggle_drawing(self):
        self.is_drawing = not self.is_drawing
        self.overlay.is_drawing = self.is_drawing
        if self.is_drawing:
            self.draw_btn.config(text="Disable Drawing")
            self.status_label.config(text="Drawing enabled - Hold Ctrl and drag to draw")
            if not self.overlay.root.winfo_viewable():
                self.overlay.show()
        else:
            self.draw_btn.config(text="Enable Drawing")
            self.status_label.config(text="Drawing disabled")
            if not self.show_pointer:
                self.overlay.hide()
    
    def toggle_pointer(self):
        self.show_pointer = not self.show_pointer
        self.overlay.show_pointer = self.show_pointer
        if self.show_pointer:
            self.pointer_btn.config(text="Disable Pointer Tracer")
            if not self.overlay.root.winfo_viewable():
                self.overlay.show()
        else:
            self.pointer_btn.config(text="Enable Pointer Tracer")
            self.overlay.mouse_positions.clear()
            if not self.is_drawing:
                self.overlay.hide()
    
    def clear_drawings(self):
        self.overlay.clear_drawings()
    
    def start_keyboard_tracking(self):
        def on_key_press(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.overlay.ctrl_pressed = True
                    if self.is_drawing:
                        # Get current mouse position
                        x, y = pyautogui.position()
                        self.overlay.start_drawing(x, y)
            except:
                pass
        
        def on_key_release(key):
            try:
                if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                    self.overlay.ctrl_pressed = False
                    self.overlay.finish_drawing()
            except:
                pass
        
        self.keyboard_listener = KeyboardListener(
            on_press=on_key_press,
            on_release=on_key_release
        )
        self.keyboard_listener.start()
    
    def start_mouse_tracking(self):
        def on_move(x, y):
            # Update overlay with mouse position
            self.overlay.add_mouse_position(x, y)
            
            # Continue drawing if Ctrl is held
            if self.is_drawing and self.overlay.ctrl_pressed:
                self.overlay.add_drawing_point(x, y)
        
        def on_click(x, y, button, pressed):
            if self.is_drawing and pressed and button == mouse.Button.left and self.overlay.ctrl_pressed:
                self.overlay.start_drawing(x, y)
            elif self.is_drawing and not pressed and button == mouse.Button.left:
                self.overlay.finish_drawing()
        
        self.mouse_listener = MouseListener(
            on_move=on_move,
            on_click=on_click
        )
        self.mouse_listener.start()
    
    def capture_screen_with_overlay(self):
        """Capture screen and add drawing overlay and pointer tracer"""
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Draw pointer trail from overlay
        if self.overlay.show_pointer and self.overlay.mouse_positions:
            for i, pos in enumerate(self.overlay.mouse_positions):
                alpha = i / len(self.overlay.mouse_positions) if len(self.overlay.mouse_positions) > 1 else 1
                radius = max(2, int(self.pointer_radius * alpha))
                color = (0, 255, 255)  # Yellow trail
                cv2.circle(frame, pos, radius, color, -1)
            
            # Draw current pointer position
            if self.overlay.mouse_positions:
                current_pos = self.overlay.mouse_positions[-1]
                cv2.circle(frame, current_pos, self.pointer_radius, (0, 0, 255), 2)
                cv2.circle(frame, current_pos, 2, (0, 0, 255), -1)
        
        # Draw all saved drawings from overlay
        for points, color, thickness in self.overlay.drawing_points:
            if len(points) > 1:
                pts = np.array(points, np.int32)
                cv2.polylines(frame, [pts], False, color, thickness)
        
        # Draw current drawing from overlay
        if self.overlay.current_drawing and len(self.overlay.current_drawing) > 1:
            pts = np.array(self.overlay.current_drawing, np.int32)
            cv2.polylines(frame, [pts], False, self.overlay.drawing_color, self.overlay.drawing_thickness)
        
        return frame
    
    def start_recording(self):
        self.is_recording = True
        self.record_btn.config(text="Stop Recording", state="normal")
        
        # Initialize video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.video_writer = cv2.VideoWriter(
            self.output_file,
            fourcc,
            self.fps,
            (self.screen_width, self.screen_height)
        )
        
        self.record_thread = threading.Thread(target=self._record_loop, daemon=True)
        self.record_thread.start()
        self.status_label.config(text=f"Recording to {os.path.basename(self.output_file)}")
    
    def _record_loop(self):
        while self.is_recording:
            frame = self.capture_screen_with_overlay()
            self.video_writer.write(frame)
            time.sleep(1.0 / self.fps)
    
    def stop_recording(self):
        self.is_recording = False
        if self.video_writer:
            self.video_writer.release()
            self.video_writer = None
        self.record_btn.config(text="Start Recording")
        self.status_label.config(text=f"Recording saved to {os.path.basename(self.output_file)}")
        messagebox.showinfo("Success", f"Recording saved to {self.output_file}")
    
    def start_streaming(self):
        self.is_streaming = True
        self.stream_btn.config(text="Stop Streaming")
        self.stream_status_label.config(text="Stream: On")
        
        self.stream_thread = threading.Thread(target=self._stream_loop, daemon=True)
        self.stream_thread.start()
        self.status_label.config(text="Streaming...")
    
    def _stream_loop(self):
        cv2.namedWindow("Screen Stream", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Screen Stream", 1280, 720)
        
        while self.is_streaming:
            frame = self.capture_screen_with_overlay()
            cv2.imshow("Screen Stream", frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.stop_streaming()
                break
        
        cv2.destroyWindow("Screen Stream")
    
    def stop_streaming(self):
        self.is_streaming = False
        self.stream_btn.config(text="Start Streaming")
        self.stream_status_label.config(text="Stream: Off")
        self.status_label.config(text="Streaming stopped")
    
    def cleanup(self):
        """Clean up resources"""
        self.is_recording = False
        self.is_streaming = False
        if self.mouse_listener:
            self.mouse_listener.stop()
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        if self.video_writer:
            self.video_writer.release()
        if self.overlay:
            self.overlay.destroy()
        cv2.destroyAllWindows()

def main():
    root = tk.Tk()
    app = ScreenRecorder(root)
    
    def on_closing():
        app.cleanup()
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
