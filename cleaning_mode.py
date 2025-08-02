import tkinter as tk
from keyboard import block_key, unhook_all, is_pressed
from pynput import mouse
from threading import Timer
from PIL import Image, ImageTk
import sys
import os

# ==== CONFIG ====
EXIT_KEY = 'esc'  # Hold ESC to exit
HOLD_DURATION = 3  # seconds

# Determine the path to the image based on whether it's a bundled executable
if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    base_path = sys._MEIPASS
else:
    # Running in development
    base_path = os.path.dirname(__file__)
IMAGE_PATH = os.path.join(base_path, "character.png")  # Path to your static image

# ==== LOCK STATE ====
is_held = False
hold_timer = None

# ==== Exit Function ====
def exit_app():
    print("Exiting cleaning mode...")
    unhook_all()  # Stop blocking inputs
    root.destroy()

# ==== ESC Hold Detection ====
def check_esc_hold():
    global is_held, hold_timer
    if is_pressed('esc'):
        if not is_held:
            is_held = True
            hold_timer = Timer(HOLD_DURATION, exit_app)
            hold_timer.start()
    else:
        is_held = False
        if hold_timer:
            hold_timer.cancel()
    root.after(100, check_esc_hold)  # Check every 100ms

# ==== Mouse Block ====
def on_mouse_event(*args, **kwargs):
    return False  # Block all mouse input

# ==== GUI SETUP ====
root = tk.Tk()
root.attributes("-fullscreen", True)
root.configure(bg='black')
root.title("Cleaning Mode")

# Center content vertically and horizontally
frame = tk.Frame(root, bg="black")
frame.pack(expand=True)

# Tagline
label = tk.Label(
    frame,
    text="Clean My Keys",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="black"
)
label.pack(pady=14)

# Static Image
try:
    img = Image.open(IMAGE_PATH)
    img = img.resize((300, 300), Image.Resampling.LANCZOS)  # Updated for PIL 10+
    tk_img = ImageTk.PhotoImage(img)
    img_label = tk.Label(frame, image=tk_img, bg="black")
    img_label.pack(pady=20)
except Exception as e:
    print("Image not loaded:", e)

# Hint
hint = tk.Label(
    frame,
    text=f"Hold Esc for {HOLD_DURATION} seconds to exit",
    font=("Arial", 16),
    fg="gray",
    bg="black"
)
hint.pack(pady=20)

# Hide mouse cursor
root.config(cursor="none")

# Block all keyboard inputs except ESC
def block_all_keys():
    block_key('left windows')
    block_key('right windows')
    for key in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                'space', 'enter', 'tab', 'backspace', 'delete', 'shift', 'ctrl', 'alt',
                'left', 'right', 'up', 'down', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6',
                'f7', 'f8', 'f9', 'f10', 'f11', 'f12']:
        block_key(key)

# Start blocking inputs
block_all_keys()

# Start mouse listener
mouse_listener = mouse.Listener(on_click=on_mouse_event, on_move=on_mouse_event, on_scroll=on_mouse_event)
mouse_listener.start()

# Start checking for ESC hold
root.after(100, check_esc_hold)

# Run the app
root.mainloop()