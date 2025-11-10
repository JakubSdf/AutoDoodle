import pyautogui
import time
import os
import keyboard
import mouse
import image_processor 
import colorama
from colorama import Fore, Style
import json
import threading

import sys
import queue
import re

import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledText

colorama.init(autoreset=True)

config = {}
canvas_info = None
selected_image_path = ""
is_paused = False
console_queue = queue.Queue()

class QueueRedirector:
    """A class to redirect stdout/stderr to a queue."""
    def __init__(self, queue):
        self.queue = queue
        self.ansi_escape = re.compile(r'\033\[[0-9;]*m')

    def write(self, text):
        text = self.ansi_escape.sub('', text)
        self.queue.put(text)

    def flush(self):
        pass
def load_config():
    global config, selected_image_path
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        selected_image_path = config.get('default_image_path', 'images/test_image2.png')
    except FileNotFoundError:
        messagebox.showerror("Error", "config.json not found! Please create it.")
        exit()
    except Exception as e:
        messagebox.showerror("Error", f"Error loading config.json: {e}")
        exit()

def check_stop():
    if keyboard.is_pressed(config.get('stop_key', 'q')):
        raise KeyboardInterrupt

def toggle_pause(e):
    global is_paused
    if e.name == config.get('pause_key', 'space'):
        is_paused = not is_paused
        if is_paused:
            update_status(f"PAUSED. Press {config.get('pause_key', 'space').upper()} to resume...")
        else:
            update_status("RESUMING...")

def locate_robust(image_list):
    """Tries to find any image from a list."""
    for image_file in image_list:
        if not os.path.exists(image_file):
            print(f"{Fore.YELLOW}Warning: UI image '{image_file}' not found. Skipping.")
            continue
        try:
            coords = pyautogui.locateCenterOnScreen(image_file, confidence=config.get('ui_confidence', 0.8))
            if coords:
                update_status(f"Found UI element: {image_file}")
                return coords
        except Exception as e:
            print(f"{Fore.RED}Error locating {image_file}: {e}")
    return None

def run_calibration():
    global canvas_info
    
    root.withdraw()
    time.sleep(0.5)
    
    original_stdout = sys.stdout
    sys.stdout = sys.__stdout__
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 1: MANUAL CANVAS CALIBRATION (Check this console) ---")
    try:
        print(f"\n{Fore.YELLOW}Please {Style.BRIGHT}CLICK{Style.NORMAL} the top-left corner of the drawing area...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        x1, y1 = pyautogui.position()
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"{Fore.GREEN}Top-left corner set to: ({x1}, {y1})")
        time.sleep(0.5)
        
        check_stop()

        print(f"\n{Fore.YELLOW}Great. Now {Style.BRIGHT}CLICK{Style.NORMAL} the bottom-right corner of the drawing area...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        x2, y2 = pyautogui.position()
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"{Fore.GREEN}Bottom-right corner set to: ({x2}, {y2})")
        time.sleep(0.5)
        
        w = x2 - x1
        h = y2 - y1
        if w <= 0 or h <= 0:
            print(f"{Fore.RED}Error: Invalid dimensions.")
            canvas_info = None
        else:
            center_x = x1 + w / 2.0
            center_y = y1 + h / 2.0
            canvas_info = (x1, y1, w, h, center_x, center_y)
            print(f"\n{Fore.GREEN}{Style.BRIGHT}Canvas calibrated successfully! Dimensions: {w}x{h}")
            update_status(f"Calibration successful! ({w}x{h})")
            
    except Exception as e:
        print(f"{Fore.RED}An error occurred during calibration: {e}")
        canvas_info = None
        update_status(f"Calibration failed: {e}")
    finally:
        sys.stdout = original_stdout
        root.deiconify()
        btn_draw.config(state=NORMAL)

def drawing_logic():
    global is_paused
    try:
        if not canvas_info:
            update_status("Error: Canvas is not calibrated.")
            return

        if not selected_image_path or not os.path.exists(selected_image_path):
            update_status(f"Error: Image file not found: {selected_image_path}")
            return

        canvas_x, canvas_y, canvas_w, canvas_h, canvas_center_x, canvas_center_y = canvas_info
        
        update_status("Finding 'plus' icon...")
        plus_coords = locate_robust(config.get('plus_icons', []))
        
        if plus_coords:
            pyautogui.click(plus_coords)
            time.sleep(0.5)
            pyautogui.click(plus_coords.x, plus_coords.y - config.get('draw_button_y_offset', 75))
            update_status("Drawing interface opened.")
            time.sleep(1)
        else:
            update_status("Error: Could not find 'plus' icon. Exiting.")
            return

        update_status("Setting brush thickness...")
        thickness_handle_coords = locate_robust(config.get('slider_handles', []))
        
        if thickness_handle_coords:
            target_x = thickness_handle_coords.x
            target_y = thickness_handle_coords.y + config.get('thickness_adjust_y_offset', 20)
            pyautogui.click(target_x, target_y)
            update_status("Brush thickness set.")
            time.sleep(0.5)
        else:
            update_status("Warning: Could not find thickness slider. Using default.")

        update_status("Select your color. Click mouse to continue...")
        print(f"\n--- WAITING FOR USER ---")
        print(f"Please select your desired color in the app.")
        print(f"CLICK THE MOUSE (Left Button) anywhere to continue...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        update_status("User ready. Continuing...")

        contours_list, img_info, _ = image_processor.generate_sketch_contours(
            selected_image_path,
            status_callback=update_status 
        )
        if contours_list is None:
            update_status("Error: Image processing failed. Exiting.")
            return
            
        img_width, img_height = img_info["width"], img_info["height"]
        img_center_x, img_center_y = img_info["center_x"], img_info["center_y"]
        update_status(f"Image loaded ({img_width}x{img_height})")
        
        update_status("Calculating scale...")
        scale_x = canvas_w / img_width
        scale_y = canvas_h / img_height
        SCALE_FACTOR = min(scale_x, scale_y) * config.get('scale_margin', 0.9)
        
        update_status(f"Starting draw in 3s. Press '{config.get('stop_key', 'q')}' to stop.")
        print(f"\n--- STEP 5: DRAWING ---")
        print(f"Drawing {len(contours_list)} contours...")
        print(f"Attention: Drawing will begin in 3 seconds.")
        print(f"To stop immediately: Press and hold the '{config.get('stop_key', 'q')}' key.")
        print(f"To PAUSE/RESUME: Press the '{config.get('pause_key', 'space')}' key.")
        
        time.sleep(3)
        pyautogui.PAUSE = config.get('drawing_speed', 0.0)

        keyboard.on_press_key(config.get('pause_key', 'space'), toggle_pause)

        for i, contour in enumerate(contours_list):
            while is_paused:
                check_stop()
                time.sleep(0.1)
                
            check_stop()
            
            if len(contour) < 4:
                continue
            
            update_status(f"Drawing contour {i+1} / {len(contours_list)}")

            first_point = contour[0][0]
            scaled_x = int(canvas_center_x + (first_point[0] - img_center_x) * SCALE_FACTOR)
            scaled_y = int(canvas_center_y + (first_point[1] - img_center_y) * SCALE_FACTOR)
            
            pyautogui.moveTo(scaled_x, scaled_y)
            pyautogui.mouseDown()

            for point in contour[1:]:
                while is_paused:
                    check_stop()
                    time.sleep(0.1)

                check_stop()
                
                scaled_x = int(canvas_center_x + (point[0][0] - img_center_x) * SCALE_FACTOR)
                scaled_y = int(canvas_center_y + (point[0][1] - img_center_y) * SCALE_FACTOR)
                pyautogui.dragTo(scaled_x, scaled_y)

            pyautogui.mouseUp()
        
        update_status("Done! Drawing complete.")
        print(f"\nDone! Drawing complete.")

    except KeyboardInterrupt:
        update_status(f"STOP: '{config.get('stop_key', 'q')}' key detected. Stopping.")
        print(f"\nSTOP: '{config.get('stop_key', 'q')}' key detected. Stopping script.")
    except pyautogui.FailSafeException:
        update_status("STOP: Failsafe triggered (mouse moved to corner).")
        print(f"\nSTOP: Failsafe triggered (mouse moved to corner). Stopping script.")
    except Exception as e:
        update_status(f"An error occurred: {e}")
        print(f"\nAn error occurred during drawing: {e}")
    finally:
        pyautogui.mouseUp()
        keyboard.unhook_all()
        print(f"\nMouse button released. Script terminating.")
        btn_draw.config(state=NORMAL)
        btn_calibrate.config(state=NORMAL)
        btn_select.config(state=NORMAL)

def update_status(message):
    """Updates the status label in the GUI (thread-safe)"""
    status_var.set(message)

def gui_select_image():
    global selected_image_path
    path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")],
        initialdir=os.path.dirname(os.path.abspath(selected_image_path))
    )
    if path:
        selected_image_path = path
        update_status(f"Image: {os.path.basename(path)}")
        lbl_image_path.config(text=os.path.basename(path))

def gui_start_calibration():
    update_status("Starting calibration... Check your terminal.")
    btn_draw.config(state=DISABLED) 
    threading.Thread(target=run_calibration, daemon=True).start()

def gui_start_drawing():
    if not canvas_info:
        messagebox.showwarning("Warning", "Please calibrate the canvas first!")
        return
        
    if not selected_image_path:
        messagebox.showwarning("Warning", "Please select an image first!")
        return

    btn_draw.config(state=DISABLED)
    btn_calibrate.config(state=DISABLED)
    btn_select.config(state=DISABLED)
    update_status("Starting draw... See console for details.")
    
    threading.Thread(target=drawing_logic, daemon=True).start()

def toggle_console():
    if console_check_var.get():
        console_frame.pack(fill=BOTH, expand=True, pady=(10, 0))
    else:
        console_frame.pack_forget()

def check_console_queue():
    """Polls the queue and updates the console text widget."""
    while not console_queue.empty():
        try:
            text = console_queue.get_nowait()
            console_text.insert(END, text)
            console_text.see(END)
        except queue.Empty:
            pass
    root.after(100, check_console_queue)

if __name__ == "__main__":
    load_config()

    root = ttk.Window(themename="vapor") 
    root.title("AutoDoodle Control Panel")
    root.geometry("450x500")

    try:
        root.iconbitmap("icon.ico")
    except Exception as e:
        print(f"Warning: Could not load icon.ico. {e}")
    
    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=BOTH, expand=True)

    img_frame = ttk.Labelframe(main_frame, text="Image Selection", padding=10)
    img_frame.pack(fill=X, expand=False)
    
    btn_select = ttk.Button(img_frame, text="Select Image", command=gui_select_image, bootstyle=INFO)
    btn_select.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
    
    lbl_image_path = ttk.Label(img_frame, text=os.path.basename(selected_image_path), relief=SUNKEN, padding=5, width=30)
    lbl_image_path.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)

    ctrl_frame = ttk.Labelframe(main_frame, text="Controls", padding=10)
    ctrl_frame.pack(fill=X, expand=False, pady=10)

    btn_calibrate = ttk.Button(ctrl_frame, text="1. Calibrate Canvas", command=gui_start_calibration, bootstyle=SECONDARY)
    btn_calibrate.pack(fill=BOTH, expand=True, padx=5, pady=5)

    btn_draw = ttk.Button(ctrl_frame, text="2. Start Drawing", command=gui_start_drawing, bootstyle=SUCCESS)
    btn_draw.pack(fill=BOTH, expand=True, padx=5, pady=5)
    btn_draw.config(state=DISABLED) 

    status_frame = ttk.Frame(main_frame)
    status_frame.pack(side=BOTTOM, fill=X, pady=(10,0))
    
    status_var = tk.StringVar()
    status_var.set("Welcome! Select an image and calibrate.")
    lbl_status = ttk.Label(status_frame, textvariable=status_var, relief=SUNKEN, padding=5)
    lbl_status.pack(side=LEFT, fill=X, expand=True)

    console_check_var = tk.BooleanVar()
    console_check = ttk.Checkbutton(status_frame, text="Show Console", variable=console_check_var, command=toggle_console, bootstyle="info-square-toggle")
    console_check.pack(side=LEFT, padx=(10, 0))

    console_frame = ttk.Labelframe(main_frame, text="Console Output", padding=5)
    
    console_text = ScrolledText(console_frame, height=10, wrap=WORD, bootstyle=DARK)
    console_text.pack(fill=BOTH, expand=True)
    
    redirector = QueueRedirector(console_queue)
    sys.stdout = redirector
    sys.stderr = redirector
    
    check_console_queue()

    root.mainloop()