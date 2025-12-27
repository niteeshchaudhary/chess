# Screen Recorder & Streamer

A Python application for screen recording, streaming, drawing overlays, and pointer tracking with **real-time visibility**.

## Features

- **Screen Recording**: Record your screen to video files (MP4, AVI)
- **Screen Streaming**: Live preview of your screen in a window
- **Drawing Overlay**: Draw on your screen in **real-time** while recording/streaming
- **Pointer Tracer**: Visual trail showing mouse movement in **real-time**

## Installation

All required dependencies are already in `requirements.txt`. Install them with:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python screen_recorder.py
```

### Controls

1. **Recording**:
   - Click "Choose Save Location" to select where to save the video
   - Click "Start Recording" to begin recording
   - Click "Stop Recording" to save and stop

2. **Streaming**:
   - Click "Start Streaming" to open a live preview window
   - Press 'q' in the preview window to stop streaming
   - Or click "Stop Streaming" in the main window

3. **Drawing** (Real-time visible!):
   - Click "Enable Drawing" to activate drawing mode
   - Hold **Ctrl** and drag with your mouse to draw
   - Drawings appear **instantly** on your screen as you draw
   - Choose color and thickness from the options
   - Click "Clear Drawings" to remove all drawings

4. **Pointer Tracer** (Real-time visible!):
   - Click "Toggle Pointer Tracer" to show/hide mouse trail
   - Adjust trail length with the slider
   - The trail shows your mouse movement **in real-time** on your screen

## How It Works

The application uses a transparent overlay window that sits on top of your screen. This overlay:
- Shows drawings and pointer trail in real-time as you interact
- Is transparent (black background is made transparent)
- Doesn't block mouse clicks (click-through behavior)
- Updates at ~60 FPS for smooth real-time display

## Linux Notes

On Linux, the overlay window requires:
- A compositor that supports transparent windows (most modern desktop environments have this)
- X11 or Wayland with proper window manager support

If the overlay doesn't appear transparent or blocks clicks:
- Make sure you're using a compositor (e.g., Compiz, KWin, Mutter, etc.)
- Some window managers may need additional configuration
- The overlay will still work, but may have a slight black tint

## Notes

- Recording and streaming can run simultaneously
- Drawings and pointer tracer appear in both recordings and streams
- The drawing feature requires holding Ctrl while dragging
- All features work together - you can record with drawings and pointer tracer enabled
- The overlay window is always on top and shows drawings/pointer in real-time
