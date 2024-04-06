import tkinter as tk

def create_left_pane(root):
    left_frame = tk.Frame(root, bg="lightblue", width=200, height=400)
    left_frame.pack(side="left", fill="y")
    label = tk.Label(left_frame, text="Left Pane", bg="lightblue")
    label.pack(pady=20)

def create_top_pane(root):
    top_frame = tk.Frame(root, bg="lightgreen", height=100)
    top_frame.pack(side="top", fill="x")
    label = tk.Label(top_frame, text="Top Pane", bg="lightgreen")
    label.pack(pady=20)

def create_center_pane(root):
    center_frame = tk.Frame(root, bg="lightyellow")
    center_frame.pack(expand=True, fill="both")
    label = tk.Label(center_frame, text="Center Pane", bg="lightyellow")
    label.pack(pady=20)

def main():
    root = tk.Tk()
    root.title("Tkinter Layout")

    create_left_pane(root)
    create_top_pane(root)
    create_center_pane(root)

    root.mainloop()

if __name__ == "__main__":
    main()
