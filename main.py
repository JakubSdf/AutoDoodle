import pyautogui
import time
import os
import keyboard
import mouse
import image_processor 
import colorama
from colorama import Fore, Style



# MAIN CONFIGURATION 
INPUT_IMAGE_PATH = "images/test_image2.png" # Change 'images/test_image2.png' to the path of your image 
PLUS_ICON_FILE = "plus_icon.png" # Change 'plus_icon.png' to the path of your plus icon if needed
THICKNESS_ADJUST_OFFSET_Y = 20 # Change '20' to the offset of your thickness slider handle if needed
DRAWING_SPEED = 0 # Change '0' to the speed of your drawing (0 = no pause, 1 = 1 second pause, etc.)

THICKNESS_SLIDER_HANDLE_FILE = "thickness_slider_handle.png"
THICKNESS_SLIDER_HANDLE_ALT_FILE = "thickness_slider_handle_alt.png" 
DRAW_BUTTON_Y_OFFSET = 75 
STOP_KEY = 'q'
colorama.init(autoreset=True)
is_paused = False

def toggle_pause(e):
    global is_paused
    if e.name == 'space':
        is_paused = not is_paused
        if is_paused:
            print(f"\n{Fore.YELLOW}{Style.BRIGHT}PAUSED. Press SPACE to resume...{Style.NORMAL}")
        else:
            print(f"\n{Fore.GREEN}{Style.BRIGHT}RESUMING...")


def calibrate_canvas():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 1: MANUAL CANVAS CALIBRATION ---")
    try:
        print(f"\n{Fore.YELLOW}Please {Style.BRIGHT}CLICK{Style.NORMAL} the top-left corner of the drawing area...")
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        x1, y1 = pyautogui.position()
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"{Fore.GREEN}Top-left corner set to: ({x1}, {y1})")
        time.sleep(0.5)
        
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
            return None
        center_x = x1 + w / 2.0
        center_y = y1 + h / 2.0
        return (x1, y1, w, h, center_x, center_y)
    except Exception as e:
        print(f"{Fore.RED}An error occurred during calibration: {e}")
        return None

def main():
    canvas_info = calibrate_canvas()
    if canvas_info is None: return
    canvas_x, canvas_y, canvas_w, canvas_h, canvas_center_x, canvas_center_y = canvas_info
    print(f"\n{Fore.GREEN}{Style.BRIGHT}Canvas calibrated successfully! Dimensions: {canvas_w}x{canvas_h}")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 2: UI AUTOMATION ---")
    print("Opening draw interface...")
    plus_coords = None
    try:
        plus_coords = pyautogui.locateCenterOnScreen(PLUS_ICON_FILE, confidence=0.8)
    except Exception as e:
        print(f"{Fore.RED}Error finding plus icon: {e}")
        return
        
    if plus_coords:
        pyautogui.click(plus_coords)
        time.sleep(0.5)
        pyautogui.click(plus_coords.x, plus_coords.y - DRAW_BUTTON_Y_OFFSET)
        print(f"{Fore.GREEN}Successfully opened drawing interface.")
        time.sleep(1)
    else:
        print(f"{Fore.RED}Could not find plus icon ('{PLUS_ICON_FILE}'). Exiting.")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 2.5: SETTING BRUSH THICKNESS ---")
    print("Setting brush thickness...")
    thickness_handle_coords = None
    try:
        thickness_handle_coords = pyautogui.locateCenterOnScreen(THICKNESS_SLIDER_HANDLE_FILE, confidence=0.8)
        if thickness_handle_coords:
            print(f"Found primary thickness slider: '{THICKNESS_SLIDER_HANDLE_FILE}'.")
    except Exception:
        pass 
        
    if not thickness_handle_coords:
        try:
            thickness_handle_coords = pyautogui.locateCenterOnScreen(THICKNESS_SLIDER_HANDLE_ALT_FILE, confidence=0.8)
            if thickness_handle_coords:
                print(f"Found alternate thickness slider: '{THICKNESS_SLIDER_HANDLE_ALT_FILE}'.")
        except Exception:
            pass

    if thickness_handle_coords:
        target_x = thickness_handle_coords.x
        target_y = thickness_handle_coords.y + THICKNESS_ADJUST_OFFSET_Y
        pyautogui.click(target_x, target_y)
        print(f"{Fore.GREEN}Brush thickness set by clicking at ({target_x}, {target_y}).")
        time.sleep(0.5)
    else:
        print(f"{Fore.YELLOW}Warning: Could not find any thickness slider icon. Using default thickness.")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}--- WAITING FOR USER ---")
    print(f"{Fore.YELLOW}Please select your desired color in the app.")
    print(f"{Fore.YELLOW}{Style.BRIGHT}CLICK THE MOUSE (Left Button){Style.NORMAL}{Fore.YELLOW} anywhere to continue...")
    try:
        mouse.wait(mouse.LEFT, target_types=mouse.DOWN)
        mouse.wait(mouse.LEFT, target_types=mouse.UP)
        print(f"{Fore.GREEN}User ready. Continuing...")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while waiting: {e}")
        return

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 3: IMAGE PROCESSING ---")
    print("Processing image...")
    contours_list, img_info, _ = image_processor.generate_sketch_contours(
        INPUT_IMAGE_PATH
    )
    if contours_list is None:
        print(f"{Fore.RED}Image processing failed. Exiting.")
        return
        
    img_width, img_height = img_info["width"], img_info["height"]
    img_center_x, img_center_y = img_info["center_x"], img_info["center_y"]
    print(f"Image loaded (Dimensions: {img_width}x{img_height})")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 4: CALCULATING SCALE ---")
    print("Calculating scale...")
    scale_x = canvas_w / img_width
    scale_y = canvas_h / img_height
    SCALE_FACTOR = min(scale_x, scale_y) * 0.9 # Change '0.9' to the margin of your drawing area if needed
    print(f"Calculated scale factor: {SCALE_FACTOR:.2f}")

    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- STEP 5: DRAWING ---")
    print(f"Drawing {len(contours_list)} contours...")
    print(f"{Fore.YELLOW}{Style.BRIGHT}Attention: Drawing will begin in 3 seconds.")
    print(f"{Fore.RED}{Style.BRIGHT}To stop immediately: Press and hold the '{STOP_KEY}' key.")
    print(f"{Fore.CYAN}{Style.BRIGHT}To PAUSE/RESUME: Press the 'SPACE' key.")
    
    time.sleep(3)
    pyautogui.PAUSE = DRAWING_SPEED

    keyboard.on_press_key('space', toggle_pause)

    try:
        for contour in contours_list:
            while is_paused:
                if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
                time.sleep(0.1)
                
            if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
            
            if len(contour) < 4:
                continue

            first_point = contour[0][0]
            scaled_x = int(canvas_center_x + (first_point[0] - img_center_x) * SCALE_FACTOR)
            scaled_y = int(canvas_center_y + (first_point[1] - img_center_y) * SCALE_FACTOR)
            
            pyautogui.moveTo(scaled_x, scaled_y)
            pyautogui.mouseDown()

            for point in contour[1:]:
                while is_paused:
                    if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
                    time.sleep(0.1)

                if keyboard.is_pressed(STOP_KEY): raise KeyboardInterrupt
                
                scaled_x = int(canvas_center_x + (point[0][0] - img_center_x) * SCALE_FACTOR)
                scaled_y = int(canvas_center_y + (point[0][1] - img_center_y) * SCALE_FACTOR)
                pyautogui.dragTo(scaled_x, scaled_y)

            pyautogui.mouseUp()
        
        print(f"\n{Fore.GREEN}{Style.BRIGHT}Done! Drawing complete.")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}{Style.BRIGHT}STOP: '{STOP_KEY}' key detected. Stopping script.")
    except pyautogui.FailSafeException:
        print(f"\n{Fore.RED}{Style.BRIGHT}STOP: Failsafe triggered (mouse moved to corner). Stopping script.")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred during drawing: {e}")
    finally:
        pyautogui.mouseUp()
        keyboard.unhook_all() 
        print(f"{Fore.YELLOW}Mouse button released. Script terminating.")

if __name__ == "__main__":
    main()